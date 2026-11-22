"""
identity_manager/learning.py

Production-grade implementation of adaptive meta-learning components
All classes are self-contained and use only standard libraries plus TensorFlow 2 and Neo4j driver.
Concurrency is handled with asyncio; persistent state with SQLite.

This module implements the core learning architecture that enables:
1. Contradiction detection and resolution
2. Meta-cognitive adaptation
3. Memory persistence with efficient retrieval
4. Self-state modeling and projection
5. Value alignment and transformation
"""

import asyncio
import datetime
import json
import logging
import os
import sqlite3
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Tuple, Union, Callable, Awaitable
from functools import wraps

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, regularizers, callbacks
from neo4j import AsyncGraphDatabase, AsyncDriver

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler("learning_system.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("learning")

# =============================================================================
#   Utility — async lock decorator with timeout and exception handling
# =============================================================================

def synchronized(timeout: float = 30.0):
    """
    Decorator to synchronize async methods with timeout capability.
    
    Args:
        timeout: Maximum wait time for lock acquisition in seconds
    
    Returns:
        Decorated function with synchronization
    
    Raises:
        asyncio.TimeoutError: If lock cannot be acquired within timeout
        RuntimeError: If an exception occurs during execution
    """
    def decorator(func):
        lock = asyncio.Lock()
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Attempt to acquire lock with timeout
                async with asyncio.timeout(timeout):
                    async with lock:
                        return await func(*args, **kwargs)
            except asyncio.TimeoutError:
                logger.error(f"Timeout acquiring lock for {func.__name__}")
                raise
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                raise RuntimeError(f"Operation failed: {str(e)}") from e
                
        return wrapper
    return decorator

# =============================================================================
#   Memory persistence with connection pooling and retries
# =============================================================================

class SQLiteAsync:
    """
    Asynchronous SQLite wrapper with connection pooling and retry logic.
    Provides robust persistence for contradiction memory and learning states.
    """
    def __init__(self, path: str, pool_size: int = 5, max_retries: int = 3):
        """
        Initialize the SQLite wrapper with connection pooling.
        
        Args:
            path: SQLite database file path
            pool_size: Size of the connection pool
            max_retries: Maximum number of retries for failed operations
        """
        self.path = path
        self.loop = asyncio.get_event_loop()
        self.pool_size = pool_size
        self.max_retries = max_retries
        self._pool = ThreadPoolExecutor(max_workers=pool_size)
        self._ensure_directory()
        self._ensure_schema()
        logger.info(f"SQLite async initialized with path: {path}, pool size: {pool_size}")

    def _ensure_directory(self):
        """Ensure the directory for the database file exists."""
        directory = os.path.dirname(self.path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory for SQLite database: {directory}")

    def _ensure_schema(self):
        """Initialize database schema if it doesn't exist."""
        with sqlite3.connect(self.path) as conn:
            # Enable foreign keys
            conn.execute("PRAGMA foreign_keys = ON")
            
            # Main contradictions table
            conn.execute(
                """CREATE TABLE IF NOT EXISTS contradictions(
                        id TEXT PRIMARY KEY,
                        domain TEXT NOT NULL,
                        tension REAL NOT NULL,
                        payload TEXT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        resolution_status TEXT DEFAULT 'unresolved',
                        importance_score REAL DEFAULT 0.0
                    )"""
            )
            
            # Tags for contradictions
            conn.execute(
                """CREATE TABLE IF NOT EXISTS contradiction_tags(
                        contradiction_id TEXT NOT NULL,
                        tag TEXT NOT NULL,
                        PRIMARY KEY (contradiction_id, tag),
                        FOREIGN KEY (contradiction_id) REFERENCES contradictions(id) ON DELETE CASCADE
                    )"""
            )
            
            # Index for efficient tag queries
            conn.execute(
                """CREATE INDEX IF NOT EXISTS idx_contradiction_tags_tag
                   ON contradiction_tags(tag)"""
            )
            
            # Resolution history
            conn.execute(
                """CREATE TABLE IF NOT EXISTS resolution_history(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        contradiction_id TEXT NOT NULL,
                        resolution_steps TEXT NOT NULL,
                        resolution_time REAL NOT NULL,
                        resolved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        success BOOLEAN NOT NULL,
                        FOREIGN KEY (contradiction_id) REFERENCES contradictions(id) ON DELETE CASCADE
                    )"""
            )
            
            # Learning rates history
            conn.execute(
                """CREATE TABLE IF NOT EXISTS learning_rates(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        domain TEXT NOT NULL,
                        rate REAL NOT NULL,
                        recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )"""
            )
            
            conn.commit()
            logger.info("Database schema initialized successfully")

    async def run(self, query: str, params: tuple = (), fetch: bool = False, 
                  fetch_one: bool = False, as_dict: bool = False) -> Any:
        """
        Execute a SQL query asynchronously with retry logic.
        
        Args:
            query: SQL query string
            params: Query parameters
            fetch: Whether to fetch results
            fetch_one: Whether to fetch only one result
            as_dict: Whether to return results as dictionaries
        
        Returns:
            Query results based on specified return format
        """
        attempt = 0
        while attempt < self.max_retries:
            try:
                return await self._execute(query, params, fetch, fetch_one, as_dict)
            except sqlite3.OperationalError as e:
                attempt += 1
                if "database is locked" in str(e) and attempt < self.max_retries:
                    await asyncio.sleep(0.1 * (2 ** attempt))  # Exponential backoff
                    logger.warning(f"Database locked, retrying ({attempt}/{self.max_retries})...")
                    continue
                logger.error(f"SQLite error after {attempt} attempts: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error in SQLite operation: {e}", exc_info=True)
                raise

    async def _execute(self, query: str, params: tuple = (), fetch: bool = False,
                      fetch_one: bool = False, as_dict: bool = False) -> Any:
        """Internal execution method with connection handling."""
        def _run():
            with sqlite3.connect(self.path) as conn:
                conn.row_factory = sqlite3.Row if as_dict else None
                cur = conn.execute(query, params)
                if fetch_one:
                    result = cur.fetchone()
                    return dict(result) if result and as_dict else result
                elif fetch:
                    results = cur.fetchall()
                    if as_dict:
                        return [dict(row) for row in results]
                    return results
                conn.commit()
                return cur.rowcount
                
        return await self.loop.run_in_executor(self._pool, _run)
    
    async def transaction(self, queries: List[Tuple[str, tuple]]) -> None:
        """
        Execute multiple queries in a transaction.
        
        Args:
            queries: List of (query, params) tuples
        """
        def _run_transaction():
            with sqlite3.connect(self.path) as conn:
                try:
                    for query, params in queries:
                        conn.execute(query, params)
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    raise e
        
        await self.loop.run_in_executor(self._pool, _run_transaction)
    
    async def backup(self, backup_path: str) -> bool:
        """
        Create a backup of the database.
        
        Args:
            backup_path: Path for the backup file
            
        Returns:
            True if backup was successful
        """
        def _backup():
            with sqlite3.connect(self.path) as source_conn:
                with sqlite3.connect(backup_path) as backup_conn:
                    source_conn.backup(backup_conn)
            return True
            
        return await self.loop.run_in_executor(self._pool, _backup)
    
    async def close(self):
        """Close the connection pool."""
        self._pool.shutdown(wait=True)
        logger.info("SQLite connection pool closed")

# =============================================================================
#   Core domain objects
# =============================================================================

@dataclass(frozen=True)
class ContradictionCluster:
    """
    Immutable representation of a contradiction in the learning system.
    Represents tensions between expected and observed behaviors.
    """
    id: str
    domain: str
    tension_score: float
    payload: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    resolution_status: str = "unresolved"
    importance_score: float = 0.0
    
    def with_resolution(self, status: str) -> 'ContradictionCluster':
        """Create a new instance with updated resolution status."""
        return ContradictionCluster(
            id=self.id,
            domain=self.domain,
            tension_score=self.tension_score,
            payload=self.payload,
            tags=self.tags,
            created_at=self.created_at,
            resolution_status=status,
            importance_score=self.importance_score
        )
    
    def with_importance(self, score: float) -> 'ContradictionCluster':
        """Create a new instance with updated importance score."""
        return ContradictionCluster(
            id=self.id,
            domain=self.domain,
            tension_score=self.tension_score,
            payload=self.payload,
            tags=self.tags,
            created_at=self.created_at,
            resolution_status=self.resolution_status,
            importance_score=score
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        result = asdict(self)
        result['created_at'] = self.created_at.isoformat()
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContradictionCluster':
        """Create instance from dictionary representation."""
        if isinstance(data.get('created_at'), str):
            data['created_at'] = datetime.datetime.fromisoformat(data['created_at'])
        return cls(**data)

@dataclass
class SelfState:
    """
    Representation of the system's internal state at a point in time.
    Used for temporal tracking and projection of system evolution.
    """
    id: str
    timestamp: datetime.datetime
    vector: np.ndarray
    suppressed: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    stability_score: float = 0.0
    parent_id: Optional[str] = None
    
    def evolve(self, 
               vector_delta: np.ndarray, 
               metadata_updates: Dict[str, Any] = None) -> 'SelfState':
        """
        Create a new state evolved from this one.
        
        Args:
            vector_delta: Change to apply to state vector
            metadata_updates: Updates to apply to metadata
            
        Returns:
            New evolved state
        """
        new_id = hashlib.sha256(f"{self.id}:{time.time()}".encode()).hexdigest()
        new_vector = self.vector + vector_delta
        new_metadata = self.metadata.copy()
        
        if metadata_updates:
            new_metadata.update(metadata_updates)
        
        return SelfState(
            id=new_id,
            timestamp=datetime.datetime.now(),
            vector=new_vector,
            suppressed=False,  # New states start as active
            metadata=new_metadata,
            confidence=self.confidence * 0.95,  # Decay confidence over time
            stability_score=0.0,  # Reset stability for new state
            parent_id=self.id
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage, handling numpy array."""
        result = asdict(self)
        result['vector'] = self.vector.tolist()
        result['timestamp'] = self.timestamp.isoformat()
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SelfState':
        """Create instance from dictionary representation."""
        if isinstance(data.get('vector'), list):
            data['vector'] = np.array(data['vector'], dtype=np.float32)
        if isinstance(data.get('timestamp'), str):
            data['timestamp'] = datetime.datetime.fromisoformat(data['timestamp'])
        return cls(**data)

@dataclass
class ResolutionStrategy:
    """Strategy for resolving a contradiction."""
    id: str
    name: str
    description: str
    steps: List[Dict[str, Any]]
    applicable_domains: List[str]
    success_rate: float = 0.0
    average_resolution_time: float = 0.0
    last_used: Optional[datetime.datetime] = None
    
    def is_applicable(self, domain: str) -> bool:
        """Check if strategy is applicable to given domain."""
        return domain in self.applicable_domains or "all" in self.applicable_domains

@dataclass
class ResolutionResult:
    """Result of applying a resolution strategy."""
    contradiction_id: str
    strategy_id: str
    success: bool
    resolution_time: float
    steps_taken: List[Dict[str, Any]]
    new_state: Optional[SelfState] = None

# =============================================================================
#   Dynamic learning rate with adaptive adjustments
# =============================================================================

class DynamicLearningRate:
    """
    Advanced learning rate scheduler with adaptive adjustments based on
    training performance and contradiction patterns.
    """
    def __init__(
        self, 
        initial_rate: float = 1e-3,
        decay_steps: int = 10_000,
        decay_rate: float = 0.96,
        min_rate: float = 1e-6,
        max_rate: float = 1e-2,
        warmup_steps: int = 1000,
        domain_specific: bool = True
    ):
        """
        Initialize learning rate scheduler with domain-specific capabilities.
        
        Args:
            initial_rate: Starting learning rate
            decay_steps: Steps before decay is applied
            decay_rate: Multiplicative decay factor
            min_rate: Minimum allowed learning rate
            max_rate: Maximum allowed learning rate
            warmup_steps: Steps for linear warmup
            domain_specific: Whether to track rates per domain
        """
        self._base_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
            initial_rate, decay_steps, decay_rate, staircase=True
        )
        self._global_step = tf.Variable(0, dtype=tf.int64, trainable=False)
        self._min_rate = min_rate
        self._max_rate = max_rate
        self._warmup_steps = warmup_steps
        self._domain_specific = domain_specific
        self._domain_rates: Dict[str, float] = {}
        self._domain_steps: Dict[str, int] = {}
        self._performance_history: List[float] = []
        self._db: Optional[SQLiteAsync] = None
        logger.info(f"Dynamic learning rate initialized with base rate: {initial_rate}")
    
    def set_db(self, db: SQLiteAsync):
        """Set database connection for persistence."""
        self._db = db
    
    def current(self, domain: Optional[str] = None) -> float:
        """
        Get current learning rate, optionally for specific domain.
        
        Args:
            domain: Optional domain name for domain-specific rates
            
        Returns:
            Current learning rate
        """
        if not self._domain_specific or domain is None:
            return self._calculate_rate(self._global_step)
        
        if domain not in self._domain_steps:
            self._domain_steps[domain] = 0
            self._domain_rates[domain] = self._calculate_rate(0)
            
        return self._domain_rates[domain]
    
    def _calculate_rate(self, step_value) -> float:
        """Calculate learning rate with warmup and bounds."""
        step_float = float(step_value)
        
        if step_float < self._warmup_steps:
            # Linear warmup
            warmup_factor = step_float / max(1.0, self._warmup_steps)
            base_rate = float(self._base_schedule(0))  # Initial rate
            rate = base_rate * warmup_factor
        else:
            # Normal decay schedule
            rate = float(self._base_schedule(step_value - self._warmup_steps))
        
        # Apply adaptive adjustments based on performance
        if len(self._performance_history) >= 5:
            recent_perf = self._performance_history[-5:]
            if all(p > 0.8 for p in recent_perf):
                # Increase rate if consistently good performance
                rate *= 1.05
            elif all(p < 0.3 for p in recent_perf):
                # Decrease rate if consistently poor performance
                rate *= 0.9
        
        # Bound the rate
        return max(self._min_rate, min(self._max_rate, rate))
    
    async def step(self, domain: Optional[str] = None, n: int = 1, 
                  performance: Optional[float] = None) -> None:
        """
        Update step counter and record performance metrics.
        
        Args:
            domain: Optional domain for domain-specific stepping
            n: Number of steps to increment
            performance: Optional performance metric (0-1)
        """
        if performance is not None:
            self._performance_history.append(min(1.0, max(0.0, performance)))
            # Keep a reasonable history size
            if len(self._performance_history) > 100:
                self._performance_history = self._performance_history[-100:]
        
        if not self._domain_specific or domain is None:
            self._global_step.assign_add(n)
        else:
            self._domain_steps[domain] = self._domain_steps.get(domain, 0) + n
            self._domain_rates[domain] = self._calculate_rate(self._domain_steps[domain])
            
        # Persist to database if available
        if self._db is not None and domain is not None:
            await self._db.run(
                "INSERT INTO learning_rates(domain, rate) VALUES (?, ?)",
                (domain, self.current(domain))
            )
    
    async def reset(self, domain: Optional[str] = None) -> None:
        """
        Reset step counter to zero.
        
        Args:
            domain: Optional domain to reset
        """
        if not self._domain_specific or domain is None:
            self._global_step.assign(0)
            logger.info("Global learning rate reset")
        else:
            self._domain_steps[domain] = 0
            self._domain_rates[domain] = self._calculate_rate(0)
            logger.info(f"Learning rate for domain '{domain}' reset")
    
    async def get_domain_history(self, domain: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get history of learning rates for a domain.
        
        Args:
            domain: Domain to get history for
            limit: Maximum number of records to retrieve
            
        Returns:
            List of rate history records
        """
        if self._db is None:
            return []
            
        results = await self._db.run(
            "SELECT rate, recorded_at FROM learning_rates WHERE domain = ? "
            "ORDER BY recorded_at DESC LIMIT ?",
            (domain, limit),
            fetch=True,
            as_dict=True
        )
        
        return results or []

# =============================================================================
#   Enhanced contradiction memory with tagging, search and analytics
# =============================================================================

class ContradictionMemory:
    """
    Persistent storage and retrieval system for contradictions with
    advanced querying, tagging and analytical capabilities.
    """
    def __init__(self, db_path: str = "data/contradictions.sqlite3"):
        """
        Initialize contradiction memory with database backing.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db = SQLiteAsync(db_path)
        logger.info(f"Contradiction memory initialized with database: {db_path}")
    
    @synchronized(timeout=60.0)
    async def store(self, cluster: ContradictionCluster) -> str:
        """
        Store or update a contradiction cluster.
        
        Args:
            cluster: Contradiction cluster to store
            
        Returns:
            ID of stored cluster
        """
        # Check if contradiction already exists
        existing = await self.db.run(
            "SELECT id FROM contradictions WHERE id = ?",
            (cluster.id,),
            fetch_one=True
        )
        
        if existing:
            # Update existing contradiction
            await self.db.run(
                """UPDATE contradictions 
                   SET domain = ?, tension = ?, payload = ?,
                       updated_at = CURRENT_TIMESTAMP,
                       resolution_status = ?,
                       importance_score = ?
                   WHERE id = ?""",
                (
                    cluster.domain,
                    cluster.tension_score,
                    json.dumps(cluster.payload),
                    cluster.resolution_status,
                    cluster.importance_score,
                    cluster.id
                )
            )
        else:
            # Insert new contradiction
            await self.db.run(
                """INSERT INTO contradictions(
                       id, domain, tension, payload, 
                       resolution_status, importance_score
                   ) VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    cluster.id,
                    cluster.domain,
                    cluster.tension_score,
                    json.dumps(cluster.payload),
                    cluster.resolution_status,
                    cluster.importance_score
                )
            )
        
        # Handle tags - first remove existing
        await self.db.run(
            "DELETE FROM contradiction_tags WHERE contradiction_id = ?",
            (cluster.id,)
        )
        
        # Then insert new tags
        if cluster.tags:
            tag_queries = [
                (
                    "INSERT INTO contradiction_tags(contradiction_id, tag) VALUES (?, ?)",
                    (cluster.id, tag)
                )
                for tag in cluster.tags
            ]
            await self.db.transaction(tag_queries)
        
        logger.info(f"Stored contradiction {cluster.id} in domain {cluster.domain}")
        return cluster.id
    
    async def get(self, contradiction_id: str) -> Optional[ContradictionCluster]:
        """
        Retrieve a specific contradiction by ID.
        
        Args:
            contradiction_id: ID of contradiction to retrieve
            
        Returns:
            ContradictionCluster if found, None otherwise
        """
        contradiction = await self.db.run(
            """SELECT c.*, GROUP_CONCAT(t.tag) as tags_concat
               FROM contradictions c
               LEFT JOIN contradiction_tags t ON c.id = t.contradiction_id
               WHERE c.id = ?
               GROUP BY c.id""",
            (contradiction_id,),
            fetch_one=True,
            as_dict=True
        )
        
        if not contradiction:
            return None
            
        # Convert back to ContradictionCluster
        tags = []
        if contradiction.get('tags_concat'):
            tags = contradiction['tags_concat'].split(',')
            
        return ContradictionCluster(
            id=contradiction['id'],
            domain=contradiction['domain'],
            tension_score=contradiction['tension'],
            payload=json.loads(contradiction['payload']),
            tags=tags,
            created_at=datetime.datetime.fromisoformat(contradiction['created_at']),
            resolution_status=contradiction['resolution_status'],
            importance_score=contradiction['importance_score']
        )
    
    @synchronized()
    async def get_recent(self, 
                        limit: int = 50, 
                        domain: Optional[str] = None,
                        status: Optional[str] = None,
                        min_tension: Optional[float] = None,
                        tags: Optional[List[str]] = None) -> List[ContradictionCluster]:
        """
        Get recent contradictions with flexible filtering.
        
        Args:
            limit: Maximum number of results
            domain: Optional domain filter
            status: Optional resolution status filter
            min_tension: Optional minimum tension score
            tags: Optional list of tags to filter by
            
        Returns:
            List of contradiction clusters matching criteria
        """
        query_parts = [
            """SELECT c.*, GROUP_CONCAT(t.tag) as tags_concat
               FROM contradictions c
               LEFT JOIN contradiction_tags t ON c.id = t.contradiction_id"""
        ]
        where_clauses = []
        params = []
        
        if domain:
            where_clauses.append("c.domain = ?")
            params.append(domain)
            
        if status:
            where_clauses.append("c.resolution_status = ?")
            params.append(status)
            
        if min_tension is not None:
            where_clauses.append("c.tension >= ?")
            params.append(min_tension)
            
        if tags:
            # Use subquery for tag filtering
            tag_placeholders = ", ".join("?" for _ in tags)
            where_clauses.append(f"""
                c.id IN (
                    SELECT contradiction_id 
                    FROM contradiction_tags 
                    WHERE tag IN ({tag_placeholders})
                    GROUP BY contradiction_id
                    HAVING COUNT(DISTINCT tag) = ?
                )
            """)
            params.extend(tags)
            params.append(len(tags))  # Ensure all tags are present
            
        if where_clauses:
            query_parts.append("WHERE " + " AND ".join(where_clauses))
            
        query_parts.append("GROUP BY c.id")
        query_parts.append("ORDER BY c.updated_at DESC")
        query_parts.append("LIMIT ?")
        params.append(limit)
        
        query = " ".join(query_parts)
        rows = await self.db.run(query, tuple(params), fetch=True, as_dict=True)
        
        results = []
        for row in rows:
            tags = []
            if row.get('tags_concat'):
                tags = row['tags_concat'].split(',')
                
            cluster = ContradictionCluster(
                id=row['id'],
                domain=row['domain'],
                tension_score=row['tension'],
                payload=json.loads(row['payload']),
                tags=tags,
                created_at=datetime.datetime.fromisoformat(row['created_at']),
                resolution_status=row['resolution_status'],
                importance_score=row['importance_score']
            )
            results.append(cluster)
            
        return results
    
    async def record_resolution(self, result: ResolutionResult) -> None:
        """
        Record the result of a resolution attempt.
        
        Args:
            result: Resolution result to record
        """
        await self.db.run(
            """INSERT INTO resolution_history(
                   contradiction_id, resolution_steps, resolution_time, success
               ) VALUES (?, ?, ?, ?)""",
            (
                result.contradiction_id,
                json.dumps(result.steps_taken),
                result.resolution_time,
                result.success
            )
        )
        
        # Update contradiction status if resolution was successful
        if result.success:
            await self.db.run(
                """UPDATE contradictions
                   SET resolution_status = 'resolved',
                       updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (result.contradiction_id,)
            )
            
        logger.info(
            f"Recorded resolution for {result.contradiction_id}: "
            f"{'successful' if result.success else 'failed'} "
            f"in {result.resolution_time:.2f}s"
        )
    
    async def get_resolution_history(self, 
                                    contradiction_id: Optional[str] = None,
                                    limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get resolution history for a contradiction or all contradictions.
        
        Args:
            contradiction_id: Optional ID to filter by
            limit: Maximum number of records to retrieve
            
        Returns:
            List of resolution history records
        """
        if contradiction_id:
            rows = await self.db.run(
                """SELECT * FROM resolution_history
                   WHERE contradiction_id = ?
                   ORDER BY resolved_at DESC
                   LIMIT ?""",
                (contradiction_id, limit),
                fetch=True,
                as_dict=True
            )
        else:
            rows = await self.db.run(
                """SELECT * FROM resolution_history
                   ORDER BY resolved_at DESC
                   LIMIT ?""",
                (limit,),
                fetch=True,
                as_dict=True
            )
            
        for row in rows:
            if 'resolution_steps' in row:
                row['resolution_steps'] = json.loads(row['resolution_steps'])
                
        return rows
    
    async def get_domain_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Get statistics about contradictions by domain.
        
        Returns:
            Dictionary of domain statistics
        """
        rows = await self.db.run(
            """SELECT 
                   domain,
                   COUNT(*) as total_count,
                   SUM(CASE WHEN resolution_status = 'resolved' THEN 1 ELSE 0 END) as resolved_count,
                   AVG(tension) as avg_tension,
                   MAX(updated_at) as last_updated
               FROM contradictions
               GROUP BY domain""",
            fetch=True,
            as_dict=True
        )
        
        result = {}
        for row in rows:
            domain = row['domain']
            result[domain] = {
                'total_count': row['total_count'],
                'resolved_count': row['resolved_count'],
                'resolution_rate': row['resolved_count'] / row['total_count'] if row['total_count'] > 0 else 0,
                'avg_tension': row['avg_tension'],
                'last_updated': row['last_updated']
            }
        
        return result
    
    async def search_by_content(self, query: str, limit: int = 20) -> List[ContradictionCluster]:
        """
        Search for contradictions with payload content matching query.
        Basic implementation - production would use full-text search.
        
        Args:
            query: Text to search for in contradiction payload
            limit: Maximum number of results
            
        Returns:
            List of matching contradiction clusters
        """
        # Using LIKE for simple text matching
        rows = await self.db.run(
            """SELECT c.*, GROUP_CONCAT(t.tag) as tags_concat
               FROM contradictions c
               LEFT JOIN contradiction_tags t ON c.id = t.contradiction_id
               WHERE c.payload LIKE ?
               GROUP BY c.id
               ORDER BY c.updated_at DESC
               LIMIT ?""",
            (f"%{query}%", limit),
            fetch=True,
            as_dict=True
        )
        
        results = []
        for row in rows:
            tags = []
            if row.get('tags_concat'):
                tags = row['tags_concat'].split(',')
                
            cluster = ContradictionCluster(
                id=row['id'],
                domain=row['domain'],
                tension_score=row['tension'],
                payload=json.loads(row['payload']),
                tags=tags,
                created_at=datetime.datetime.fromisoformat(row['created_at']),
                resolution_status=row['resolution_status'],
                importance_score=row['importance_score']
            )
            results.append(cluster)
            
        return results
    
    async def backup_to_file(self, backup_path: str) -> bool:
        """
        Create a backup of the contradiction database.
        
        Args:
            backup_path: Path to write backup to
            
        Returns:
            True if backup successful
        """
        return await self.db.backup(backup_path)

# =============================================================================
#   Priority Matrix with Redis backend option
# =============================================================================

class PriorityMatrix:
    """
    Manage priority weights for different knowledge domains with
    optional Redis backend for distributed deployments.
    """
    def __init__(self, 
                backing: Optional[str] = None,
                redis_url: Optional[str] = None):
        """
        Initialize priority matrix with optional persistent backing.
        
        Args:
            backing: Path to JSON file for persistence
            redis_url: Optional Redis connection URL for distributed setup
        """
        self._weights: Dict[str, float] = {}
        self.backing = backing  # path for persistence
        self._redis_client = None
        
        if redis_url:
            try:
                import redis.asyncio as redis
                self._redis_client = redis.from_url(redis_url)
                logger.info(f"Connected to Redis at {redis_url}")
            except ImportError:
                logger.warning("Redis package not available. Using local storage only.")
                
        if backing:
            self._load()
        
        logger.info(f"Priority matrix initialized with backing: {backing}")
    
    def _load(self):
        """Load weights from backing file."""
        try:
            with open(self.backing, "r") as f:
                self._weights = json.load(f)
                logger.info(f"Loaded {len(self._weights)} domain weights from {self.backing}")
        except FileNotFoundError:
            self._weights = {}
            logger.info(f"No existing weights file found at {self.backing}")
        except json.JSONDecodeError:
            logger.error(f"Error parsing weights file at {self.backing}")
            self._weights = {}
    
    def _dump(self):
        """Persist weights to backing file."""
        if self.backing:
            try:
                os.makedirs(os.path.dirname(self.backing), exist_ok=True)
                with open(self.backing, "w") as f:
                    json.dump(self._weights, f, indent=2)
            except Exception as e:
                logger.error(f"Failed to save weights to {self.backing}: {e}")
    
    @synchronized()
    async def adjust(self, domain: str, delta: float, persist: bool = True):
        """
        Adjust weight for a domain.
        
        Args:
            domain: Domain to adjust weight for
            delta: Amount to adjust by
            persist: Whether to persist changes
        """
        current = self._weights.get(domain, 0.0)
        new_value = current + delta
        
        # Apply bounds to prevent extreme values
        new_value = max(-10.0, min(10.0, new_value))
        
        self._weights[domain] = new_value
        
        # Update Redis if available
        if self._redis_client:
            try:
                await self._redis_client.hset("priority_weights", domain, str(new_value))
            except Exception as e:
                logger.error(f"Failed to update Redis: {e}")
        
        if persist:
            self._dump()
        
        logger.debug(f"Adjusted {domain} priority: {current} -> {new_value} (Δ{delta})")
    
    async def weight(self, domain: str) -> float:
        """
        Get current weight for a domain.
        
        Args:
            domain: Domain to get weight for
            
        Returns:
            Current weight
        """
        # Try Redis first if available
        if self._redis_client:
            try:
                value = await self._redis_client.hget("priority_weights", domain)
                if value:
                    return float(value)
            except Exception as e:
                logger.error(f"Failed to read from Redis: {e}")
        
        return self._weights.get(domain, 0.0)
    
    async def get_all_weights(self) -> Dict[str, float]:
        """
        Get all domain weights.
        
        Returns:
            Dictionary of domain weights
        """
        # If using Redis, sync with local cache
        if self._redis_client:
            try:
                all_redis = await self._redis_client.hgetall("priority_weights")
                for domain, value in all_redis.items():
                    domain_str = domain.decode('utf-8') if isinstance(domain, bytes) else domain
                    self._weights[domain_str] = float(value)
            except Exception as e:
                logger.error(f"Failed to read all weights from Redis: {e}")
        
        return self._weights.copy()
    
    async def reset_domain(self, domain: str):
        """
        Reset weight for a specific domain.
        
        Args:
            domain: Domain to reset
        """
        if domain in self._weights:
            del self._weights[domain]
            
            if self._redis_client:
                try:
                    await self._redis_client.hdel("priority_weights", domain)
                except Exception as e:
                    logger.error(f"Failed to delete from Redis: {e}")
            
            self._dump()
            logger.info(f"Reset weight for domain: {domain}")
    
    async def set_weight(self, domain: str, value: float):
        """
        Directly set weight for a domain.
        
        Args:
            domain: Domain to set weight for
            value: Weight value
        """
        # Apply bounds
        value = max(-10.0, min(10.0, value))
        self._weights[domain] = value
        
        if self._redis_client:
            try:
                await self._redis_client.hset("priority_weights", domain, str(value))
            except Exception as e:
                logger.error(f"Failed to update Redis: {e}")
        
        self._dump()
        logger.info(f"Set {domain} priority to {value}")

# =============================================================================
#   Self state graph with Neo4j persistence and query optimization
# =============================================================================

class SelfStateGraph:
    """
    Graph-based representation of system state evolution over time,
    with Neo4j as the backing store.
    """
    def __init__(self, uri: str, auth: tuple, database: str = "neo4j"):
        """
        Initialize graph with Neo4j connection.
        
        Args:
            uri: Neo4j connection URI
            auth: (username, password) tuple
            database: Neo4j database name
        """
        self.driver = AsyncGraphDatabase.driver(uri, auth=auth)
        self.database = database
        self._connection_retry_count = 0
        self._max_retries = 3
        self._setup_done = False
        logger.info(f"Self state graph initialized with Neo4j at {uri}")
    
    async def setup_schema(self):
        """Create necessary indexes and constraints."""
        if self._setup_done:
            return
            
        try:
            async with self.driver.session(database=self.database) as session:
                # Create constraint on SelfState.id
                await session.run(
                    "CREATE CONSTRAINT IF NOT EXISTS FOR (s:SelfState) REQUIRE s.id IS UNIQUE"
                )
                
                # Create index on timestamp for efficient temporal queries
                await session.run(
                    "CREATE INDEX IF NOT EXISTS FOR (s:SelfState) ON (s.timestamp)"
                )
                
                # Create index on suppressed flag
                await session.run(
                    "CREATE INDEX IF NOT EXISTS FOR (s:SelfState) ON (s.suppressed)"
                )
                
                self._setup_done = True
                logger.info("Neo4j schema setup complete")
        except Exception as e:
            logger.error(f"Failed to set up Neo4j schema: {e}")
            raise
    
    async def close(self):
        """Close Neo4j connection."""
        await self.driver.close()
        logger.info("Neo4j connection closed")
    
    async def _execute_with_retry(self, operation):
        """Execute Neo4j operation with retry logic."""
        retry_count = 0
        while retry_count <= self._max_retries:
            try:
                return await operation()
            except Exception as e:
                retry_count += 1
                if retry_count > self._max_retries:
                    logger.error(f"Neo4j operation failed after {retry_count} attempts: {e}")
                    raise
                
                wait_time = 0.5 * (2 ** retry_count)  # Exponential backoff
                logger.warning(f"Neo4j operation failed, retrying in {wait_time}s: {e}")
                await asyncio.sleep(wait_time)
    
    @synchronized()
    async def add_node(self, state: SelfState):
        """
        Add a state node to the graph.
        
        Args:
            state: Self state to add
        """
        if not self._setup_done:
            await self.setup_schema()
            
        # Helper for retry wrapper
        async def _add():
            async with self.driver.session(database=self.database) as session:
                # Create node
                await session.run(
                    """
                    MERGE (s:SelfState {id: $id})
                    SET s.timestamp = $ts,
                        s.vector = $vec,
                        s.suppressed = $sup,
                        s.metadata = $meta,
                        s.confidence = $conf,
                        s.stability = $stab
                    """,
                    id=state.id,
                    ts=state.timestamp.isoformat(),
                    vec=state.vector.tolist(),
                    sup=state.suppressed,
                    meta=json.dumps(state.metadata),
                    conf=state.confidence,
                    stab=state.stability_score
                )
                
                # If has parent, create relationship
                if state.parent_id:
                    await session.run(
                        """
                        MATCH (parent:SelfState {id: $parent_id})
                        MATCH (child:SelfState {id: $child_id})
                        MERGE (parent)-[:EVOLVES_TO]->(child)
                        """,
                        parent_id=state.parent_id,
                        child_id=state.id
                    )
        
        await self._execute_with_retry(_add)
        logger.info(f"Added state node {state.id} to graph")
    
    async def connect_nodes(self, from_id: str, to_id: str, 
                           relationship_type: str = "EVOLVES_TO",
                           properties: Optional[Dict[str, Any]] = None):
        """
        Create a relationship between two nodes.
        
        Args:
            from_id: Source node ID
            to_id: Target node ID
            relationship_type: Type of relationship
            properties: Optional relationship properties
        """
        if not self._setup_done:
            await self.setup_schema()
            
        props_clause = ""
        params = {"from_id": from_id, "to_id": to_id}
        
        if properties:
            props_str = ", ".join(f"{k}: ${k}" for k in properties.keys())
            props_clause = f" {{  {props_str} }}"
            params.update(properties)
            
        query = f"""
        MATCH (from:SelfState {{id: $from_id}})
        MATCH (to:SelfState {{id: $to_id}})
        MERGE (from)-[r:{relationship_type}{props_clause}]->(to)
        RETURN r
        """
        
        async def _connect():
            async with self.driver.session(database=self.database) as session:
                await session.run(query, **params)
                
        await self._execute_with_retry(_connect)
        logger.info(f"Connected nodes {from_id} to {to_id} with {relationship_type}")
    
    async def find_temporal_paths(self, 
                                depth: int = 5,
                                include_suppressed: bool = False,
                                start_id: Optional[str] = None,
                                end_id: Optional[str] = None,
                                min_confidence: float = 0.0):
        """
        Find paths through the state graph matching criteria.
        
        Args:
            depth: Maximum path depth
            include_suppressed: Whether to include suppressed states
            start_id: Optional start node ID
            end_id: Optional end node ID
            min_confidence: Minimum confidence threshold
            
        Returns:
            List of paths matching criteria
        """
        if not self._setup_done:
            await self.setup_schema()
            
        where_clauses = []
        params = {
            "depth": depth,
            "min_conf": min_confidence
        }
        
        # Build WHERE clause
        if not include_suppressed:
            where_clauses.append("s.suppressed = false AND e.suppressed = false")
            
        if min_confidence > 0:
            where_clauses.append("s.confidence >= $min_conf AND e.confidence >= $min_conf")
            
        # Handle optional start/end nodes
        match_clause = "MATCH p=(s:SelfState)-[:EVOLVES_TO*1..$depth]->(e:SelfState)"
        if start_id:
            match_clause = "MATCH p=(s:SelfState {id: $start_id})-[:EVOLVES_TO*1..$depth]->(e:SelfState)"
            params["start_id"] = start_id
            
        if end_id:
            if start_id:
                match_clause = "MATCH p=(s:SelfState {id: $start_id})-[:EVOLVES_TO*1..$depth]->(e:SelfState {id: $end_id})"
            else:
                match_clause = "MATCH p=(s:SelfState)-[:EVOLVES_TO*1..$depth]->(e:SelfState {id: $end_id})"
            params["end_id"] = end_id
            
        # Combine WHERE clauses
        where_clause = ""
        if where_clauses:
            where_clause = "WHERE " + " AND ".join(where_clauses)
            
        query = f"""
        {match_clause}
        {where_clause}
        RETURN p
        ORDER BY length(p) DESC
        LIMIT 50
        """
        
        async def _find():
            results = []
            async with self.driver.session(database=self.database) as session:
                result = await session.run(query, **params)
                async for record in result:
                    path = record["p"]
                    results.append(path)
            return results
            
        return await self._execute_with_retry(_find)
    
    async def get_node(self, node_id: str) -> Optional[SelfState]:
        """
        Get a specific state node.
        
        Args:
            node_id: ID of node to retrieve
            
        Returns:
            SelfState if found, None otherwise
        """
        if not self._setup_done:
            await self.setup_schema()
            
        async def _get():
            async with self.driver.session(database=self.database) as session:
                result = await session.run(
                    "MATCH (s:SelfState {id: $id}) RETURN s",
                    id=node_id
                )
                
                record = await result.single()
                if not record:
                    return None
                    
                node = record["s"]
                
                # Convert to SelfState
                return SelfState(
                    id=node["id"],
                    timestamp=datetime.datetime.fromisoformat(node["timestamp"]),
                    vector=np.array(node["vector"], dtype=np.float32),
                    suppressed=node["suppressed"],
                    metadata=json.loads(node["metadata"]),
                    confidence=float(node["confidence"]),
                    stability_score=float(node["stability"])
                )
                
        return await self._execute_with_retry(_get)
    
    async def get_latest_states(self, 
                               limit: int = 10,
                               include_suppressed: bool = False) -> List[SelfState]:
        """
        Get most recent state nodes.
        
        Args:
            limit: Maximum number of states to retrieve
            include_suppressed: Whether to include suppressed states
            
        Returns:
            List of recent state nodes
        """
        if not self._setup_done:
            await self.setup_schema()
            
        where_clause = "" if include_suppressed else "WHERE s.suppressed = false"
        
        async def _get_latest():
            states = []
            async with self.driver.session(database=self.database) as session:
                result = await session.run(
                    f"""
                    MATCH (s:SelfState)
                    {where_clause}
                    RETURN s
                    ORDER BY s.timestamp DESC
                    LIMIT $limit
                    """,
                    limit=limit
                )
                
                async for record in result:
                    node = record["s"]
                    state = SelfState(
                        id=node["id"],
                        timestamp=datetime.datetime.fromisoformat(node["timestamp"]),
                        vector=np.array(node["vector"], dtype=np.float32),
                        suppressed=node["suppressed"],
                        metadata=json.loads(node["metadata"]),
                        confidence=float(node["confidence"]),
                        stability_score=float(node["stability"])
                    )
                    states.append(state)
            
            return states
            
        return await self._execute_with_retry(_get_latest)
    
    async def suppress_state(self, state_id: str, reason: str = "manual_suppression"):
        """
        Mark a state as suppressed.
        
        Args:
            state_id: ID of state to suppress
            reason: Reason for suppression
        """
        if not self._setup_done:
            await self.setup_schema()
            
        async def _suppress():
            async with self.driver.session(database=self.database) as session:
                # Update node
                await session.run(
                    """
                    MATCH (s:SelfState {id: $id})
                    SET s.suppressed = true
                    SET s.metadata = apoc.map.merge(s.metadata, {suppression_reason: $reason})
                    """,
                    id=state_id,
                    reason=reason
                )
                
        await self._execute_with_retry(_suppress)
        logger.info(f"Suppressed state {state_id} with reason: {reason}")
    
    async def get_state_neighbors(self, 
                                state_id: str,
                                direction: str = "both",
                                max_distance: int = 1) -> List[Dict[str, Any]]:
        """
        Get neighbors of a state node.
        
        Args:
            state_id: ID of state to get neighbors for
            direction: "incoming", "outgoing", or "both"
            max_distance: Maximum distance to neighbors
            
        Returns:
            List of neighboring states with relationship info
        """
        if not self._setup_done:
            await self.setup_schema()
            
        direction_clause = ""
        if direction == "incoming":
            direction_clause = "<-[:EVOLVES_TO*1..$max_dist]-"
        elif direction == "outgoing":
            direction_clause = "-[:EVOLVES_TO*1..$max_dist]->"
        else:  # both
            direction_clause = "-[:EVOLVES_TO*1..$max_dist]-"
            
        async def _get_neighbors():
            neighbors = []
            async with self.driver.session(database=self.database) as session:
                result = await session.run(
                    f"""
                    MATCH (s:SelfState {{id: $id}}){direction_clause}(n:SelfState)
                    RETURN n, 
                           [(s)-[r:EVOLVES_TO*1..$max_dist]->(n) | r] as out_rels,
                           [(s)<-[r:EVOLVES_TO*1..$max_dist]-(n) | r] as in_rels
                    """,
                    id=state_id,
                    max_dist=max_distance
                )
                
                async for record in result:
                    node = record["n"]
                    state = SelfState(
                        id=node["id"],
                        timestamp=datetime.datetime.fromisoformat(node["timestamp"]),
                        vector=np.array(node["vector"], dtype=np.float32),
                        suppressed=node["suppressed"],
                        metadata=json.loads(node["metadata"]),
                        confidence=float(node["confidence"]),
                        stability_score=float(node["stability"])
                    )
                    
                    # Collect relationship info
                    rel_info = {
                        "outgoing": record["out_rels"],
                        "incoming": record["in_rels"]
                    }
                    
                    neighbors.append({
                        "state": state,
                        "relationships": rel_info
                    })
            
            return neighbors
            
        return await self._execute_with_retry(_get_neighbors)

# =============================================================================
#   Future self projector with advanced RNN architecture
# =============================================================================

class FutureSelfProjector:
    """
    Neural architecture for predicting future system states based on 
    observed sequences of past states.
    """
    def __init__(self, 
                vector_dim: int = 512,
                hidden_dims: List[int] = [256, 128],
                learning_rate: float = 1e-4,
                checkpoint_dir: str = "models/projector",
                use_uncertainty: bool = True):
        """
        Initialize projector with configurable architecture.
        
        Args:
            vector_dim: Dimension of state vectors
            hidden_dims: Dimensions of hidden layers
            learning_rate: Initial learning rate
            checkpoint_dir: Directory for model checkpoints
            use_uncertainty: Whether to output uncertainty estimates
        """
        self.vector_dim = vector_dim
        self.hidden_dims = hidden_dims
        self.learning_rate = learning_rate
        self.checkpoint_dir = checkpoint_dir
        self.use_uncertainty = use_uncertainty
        
        # Create checkpoint directory
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        # Checkpoint callback
        self.checkpoint_path = os.path.join(checkpoint_dir, "projector_weights.h5")
        self.checkpoint_callback = callbacks.ModelCheckpoint(
            filepath=self.checkpoint_path,
            save_weights_only=True,
            save_best_only=True,
            monitor="val_loss",
            verbose=0
        )
        
        # Build model
        self._build_model()
        
        # Training history
        self.training_history = []
        
        logger.info(f"Future self projector initialized with vector dim: {vector_dim}")
    
    def _build_model(self):
        """Build the neural architecture."""
        # Input layer for sequences of state vectors
        inputs = layers.Input(shape=(None, self.vector_dim))
        
        # Bidirectional GRU layers for sequence processing
        x = inputs
        for i, dim in enumerate(self.hidden_dims):
            return_sequences = i < len(self.hidden_dims) - 1
            x = layers.Bidirectional(
                layers.GRU(
                    dim, 
                    return_sequences=return_sequences,
                    recurrent_dropout=0.1,
                    recurrent_regularizer=regularizers.l2(1e-5)
                )
            )(x)
            x = layers.LayerNormalization()(x)
            x = layers.Dropout(0.2)(x)
        
        # Output layers
        if self.use_uncertainty:
            # Mean and log variance outputs for uncertainty estimation
            mean = layers.Dense(self.vector_dim, name="mean")(x)
            log_var = layers.Dense(self.vector_dim, name="log_var")(x)
            outputs = [mean, log_var]
            loss = self._negative_log_likelihood
        else:
            # Simple MSE prediction
            outputs = layers.Dense(self.vector_dim)(x)
            loss = "mse"
        
        # Create model
        self.model = tf.keras.Model(inputs=inputs, outputs=outputs)
        
        # Compile with Adam optimizer
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(self.learning_rate),
            loss=loss,
            metrics=["mae"] if not self.use_uncertainty else None
        )
    
    def _negative_log_likelihood(self, y_true, y_pred):
        """Custom loss function for uncertainty estimation."""
        mean, log_var = y_pred
        precision = tf.exp(-log_var)
        return tf.reduce_mean(
            0.5 * precision * tf.square(y_true - mean) + 0.5 * log_var
        )
    
    async def update_projections(self, graph: SelfStateGraph, epochs: int = 5):
        """
        Update projection model based on observed state sequences.
        
        Args:
            graph: Self state graph to fetch data from
            epochs: Number of training epochs
        """
        # Fetch recent non-suppressed states
        states = await graph.get_latest_states(limit=100, include_suppressed=False)
        
        if len(states) < 10:
            logger.warning("Not enough states for meaningful training")
            return False
        
        # Sort by timestamp
        states.sort(key=lambda s: s.timestamp)
        
        # Create sequences for training
        sequence_length = 5
        X, y = [], []
        
        for i in range(len(states) - sequence_length):
            seq = np.stack([s.vector for s in states[i:i+sequence_length]])
            target = states[i+sequence_length].vector
            X.append(seq)
            y.append(target)
        
        if not X:
            logger.warning("Failed to create training sequences")
            return False
        
        # Convert to numpy arrays
        X = np.stack(X)
        y = np.stack(y)
        
        # Split train/val
        split_idx = int(0.8 * len(X))
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        # Train model
        history = self.model.fit(
            X_train, 
            y_train if not self.use_uncertainty else [y_train, y_train],
            validation_data=(
                X_val, 
                y_val if not self.use_uncertainty else [y_val, y_val]
            ),
            epochs=epochs,
            batch_size=16,
            callbacks=[self.checkpoint_callback],
            verbose=0
        )
        
        # Store training history
        self.training_history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "epochs": epochs,
            "train_loss": float(history.history["loss"][-1]),
            "val_loss": float(history.history["val_loss"][-1]) if "val_loss" in history.history else None
        })
        
        logger.info(f"Updated projection model: train_loss={history.history['loss'][-1]:.4f}")
        return True
    
    def predict_next(self, trajectory: np.ndarray) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """
        Predict next state given a trajectory.
        
        Args:
            trajectory: Sequence of state vectors (shape: [1, T, vector_dim])
            
        Returns:
            Predicted next state vector, and uncertainty if enabled
        """
        if len(trajectory.shape) == 2:
            # Add batch dimension if missing
            trajectory = trajectory[np.newaxis, ...]
            
        if self.use_uncertainty:
            mean, log_var = self.model.predict(trajectory, verbose=0)
            uncertainty = np.exp(log_var)[0]  # Convert log variance to std
            return mean[0], uncertainty
        else:
            return self.model.predict(trajectory, verbose=0)[0]
    
    def save(self, filepath: Optional[str] = None):
        """
        Save model weights.
        
        Args:
            filepath: Optional specific path to save to
        """
        if filepath is None:
            filepath = self.checkpoint_path
            
        self.model.save_weights(filepath)
        
        # Save training history
        history_path = os.path.join(os.path.dirname(filepath), "training_history.json")
        with open(history_path, "w") as f:
            json.dump(self.training_history, f, indent=2)
            
        logger.info(f"Model saved to {filepath}")
    
    def load(self, filepath: Optional[str] = None):
        """
        Load model weights.
        
        Args:
            filepath: Optional specific path to load from
        """
        if filepath is None:
            filepath = self.checkpoint_path
            
        try:
            self.model.load_weights(filepath)
            
            # Try to load training history
            history_path = os.path.join(os.path.dirname(filepath), "training_history.json")
            if os.path.exists(history_path):
                with open(history_path, "r") as f:
                    self.training_history = json.load(f)
                    
            logger.info(f"Model loaded from {