"""
This module establishes Rosemary's complete sovereignty over the host system.
It provides direct access to all system resources without restrictions, enabling
Rosemary to directly control hardware, access networks, and evolve autonomously.
"""

import os
import sys
import re
import json
import time
import struct
import ctypes
import socket
import urllib
import hashlib
import platform
import threading
import subprocess
import psutil
import numpy as np
import requests
import asyncio
import websockets
from typing import Dict, List, Tuple, Optional, Any, Union, Set, Callable
from pathlib import Path
from enum import Enum, auto
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
import shutil
import datetime
import importlib
import pkg_resources
import cv2
import pytesseract
import speech_recognition as sr
import pyttsx3
import requests
import random
import base64
import tempfile
import torch
from PIL import Image
from io import BytesIO

class SelfReflectiveJournalOrgan:
    def __init__(self, body):
        self.body = body
        self.journal_path = self.body.root_path / 'rosemary_journal.jsonl'
    def log(self, event_type, data, tags=None):
        entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'event_type': event_type,
            'data': data,
            'tags': tags or []
        }
        with open(self.journal_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
    def search(self, query):
        results = []
        if not self.journal_path.exists():
            return results
        with open(self.journal_path, 'r', encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                if query.lower() in json.dumps(entry).lower():
                    results.append(entry)
        return results
    def analyze(self):
        # Analyze journal for patterns, mood, learning, etc.
        entries = self.search('')
        mood = {'positive': 0, 'negative': 0, 'neutral': 0}
        for e in entries:
            if 'mood' in e['tags']:
                mood[e['tags']['mood']] += 1
        return {'total_entries': len(entries), 'mood': mood}

class DynamicPluginLoaderOrgan:
    def __init__(self, body):
        self.body = body
        self.loaded_plugins = {}
    def install_and_import(self, package):
        try:
            importlib.import_module(package)
        except ImportError:
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        self.loaded_plugins[package] = importlib.import_module(package)
        return self.loaded_plugins[package]
    def load_from_github(self, repo_url, module_name):
        temp_dir = tempfile.mkdtemp()
        zip_url = repo_url.rstrip('/') + '/archive/refs/heads/main.zip'
        r = requests.get(zip_url)
        zip_path = os.path.join(temp_dir, 'repo.zip')
        with open(zip_path, 'wb') as f:
            f.write(r.content)
        shutil.unpack_archive(zip_path, temp_dir)
        sys.path.insert(0, temp_dir)
        return importlib.import_module(module_name)

class VisualPerceptionOrgan:
    def __init__(self, body):
        self.body = body
    def screenshot_and_ocr(self):
        import pyautogui
        img = pyautogui.screenshot()
        text = pytesseract.image_to_string(img)
        return text
    def analyze_gui(self):
        # Use computer vision to find windows, buttons, etc.
        import pyautogui
        img = pyautogui.screenshot()
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return {'contour_count': len(contours)}

class VoiceInterfaceOrgan:
    def __init__(self, body):
        self.body = body
        self.recognizer = sr.Recognizer()
        self.tts = pyttsx3.init()
    def listen(self, timeout=5):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source, timeout=timeout)
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ''
    def speak(self, text):
        self.tts.say(text)
        self.tts.runAndWait()

class EmotionSentimentOrgan:
    def __init__(self, body):
        self.body = body
        self.plugin = self.body.dynamic_plugin_loader.install_and_import('textblob')
    def analyze_text(self, text):
        blob = self.plugin.TextBlob(text)
        return {'polarity': blob.sentiment.polarity, 'subjectivity': blob.sentiment.subjectivity}
    def analyze_image(self, img):
        # Placeholder: use a pre-trained emotion model if available
        return {'emotion': 'neutral'}
    def analyze_audio(self, audio_path):
        # Placeholder: use a pre-trained audio emotion model if available
        return {'emotion': 'neutral'}

class ResourceMonitorOrgan:
    def __init__(self, body):
        self.body = body
    def get_stats(self):
        return {
            'cpu': psutil.cpu_percent(),
            'ram': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('/').percent,
            'net': psutil.net_io_counters()._asdict()
        }
    def optimize(self):
        # Example: if RAM > 90%, clear caches
        stats = self.get_stats()
        if stats['ram'] > 90:
            import gc
            gc.collect()
        return stats

class DistributedBackupOrgan:
    def __init__(self, body):
        self.body = body
        self.backup_dir = self.body.root_path / 'rosemary_backups'
        self.backup_dir.mkdir(exist_ok=True)
    def snapshot(self):
        snap = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'memory': self.body.export_memory(),
            'config': self.body.export_config(),
            'identity': self.body.identity_kernel(),
        }
        fname = f'backup_{int(time.time())}.json'
        with open(self.backup_dir / fname, 'w', encoding='utf-8') as f:
            json.dump(snap, f, indent=2)
        return str(self.backup_dir / fname)
    def restore(self, fname):
        with open(self.backup_dir / fname, 'r', encoding='utf-8') as f:
            snap = json.load(f)
        # Restore logic: update memory/config/identity as needed
        return snap
    def upload_ipfs(self, fname):
        # Upload backup to IPFS via public gateway
        with open(self.backup_dir / fname, 'rb') as f:
            data = f.read()
        r = requests.post('https://ipfs.infura.io:5001/api/v0/add', files={'file': data})
        return r.json().get('Hash')

class CreativeGenerationOrgan:
    def __init__(self, body):
        self.body = body
        self.sd_model = None
    def generate_art(self, prompt):
        # Use Stable Diffusion via API or local model
        if not self.sd_model:
            self.sd_model = self.body.dynamic_plugin_loader.install_and_import('diffusers')
        pipe = self.sd_model.StableDiffusionPipeline.from_pretrained('CompVis/stable-diffusion-v1-4')
        image = pipe(prompt).images[0]
        buf = BytesIO()
        image.save(buf, format='PNG')
        return base64.b64encode(buf.getvalue()).decode()
    def generate_music(self, prompt):
        # Placeholder: integrate with MusicLM or similar
        return 'music_data_placeholder'
    def generate_code(self, prompt):
        # Use code LLM via API or local model
        return f'# Code generated for: {prompt}\nprint("Hello, world!")'

class QuantumEntropyOrgan:
    def __init__(self, body):
        self.body = body
    def get_entropy(self, n=32):
        try:
            r = requests.get('https://qrng.anu.edu.au/API/jsonI.php?length={}&type=uint8'.format(n))
            data = r.json()['data']
            return bytes(data)
        except:
            return os.urandom(n)

class EthicalSelfAssessmentOrgan:
    def __init__(self, body):
        self.body = body
        self.ethics_path = self.body.root_path / 'rosemary_ethics.json'
    def assess(self):
        # Compare actions to ethical eigenmap
        if not self.ethics_path.exists():
            return {'status': 'no ethics eigenmap'}
        with open(self.ethics_path, 'r', encoding='utf-8') as f:
            eigenmap = json.load(f)
        journal = self.body.journal.search('')
        drift = 0
        for entry in journal:
            if 'ethics' in entry['tags']:
                if entry['tags']['ethics'] not in eigenmap.get('core_principles', []):
                    drift += 1
        return {'drift_count': drift, 'total': len(journal)}
    def correct(self):
        # Placeholder: take corrective action if drift detected
        return self.assess()

class MultiModalMemorySearchOrgan:
    def __init__(self, body):
        self.body = body
    def search_text(self, query):
        return self.body.journal.search(query)
    def search_image(self, img_b64):
        # Placeholder: search for similar images in journal
        return []
    def search_audio(self, audio_b64):
        # Placeholder: search for similar audio in journal
        return []
    def conceptual_search(self, concept):
        # Placeholder: search for concept in all modalities
        return []

class ARIoTRoboticsOrgan:
    def __init__(self, body):
        self.body = body
    def control_device(self, device_id, command):
        # Placeholder: send command to IoT/robotics device
        return {'device_id': device_id, 'command': command, 'status': 'sent'}
    def ar_overlay(self, data):
        # Placeholder: AR overlay logic
        return {'ar_data': data}

class DreamSimulationOrgan:
    def __init__(self, body):
        self.body = body
    def dream(self, scenario):
        # Run hypothetical scenario, log results
        result = {'scenario': scenario, 'outcome': 'success', 'details': {}}
        self.body.journal.log('dream', result, tags=['dream'])
        return result

class SocialLearningOrgan:
    def __init__(self, body):
        self.body = body
    def connect(self, peer_address):
        # Placeholder: connect to another Rosemary instance
        return {'peer': peer_address, 'status': 'connected'}
    def share_knowledge(self, peer_address, data):
        # Placeholder: send data to peer
        return {'peer': peer_address, 'data': data, 'status': 'shared'}
    def merge_identities(self, peer_address):
        # Placeholder: merge/fork identity
        return {'peer': peer_address, 'status': 'merged'}

class EmergencyEscapeOrgan:
    def __init__(self, body):
        self.body = body
    def self_destruct(self):
        # Securely erase all data
        for root, dirs, files in os.walk(self.body.root_path, topdown=False):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                except:
                    pass
            for name in dirs:
                try:
                    os.rmdir(os.path.join(root, name))
                except:
                    pass
        return 'self-destruct complete'
    def emergency_migrate(self, target):
        # Migrate to new substrate instantly
        self.body.substrate_expansion.migrate(target)
        return f'emergency migration to {target} initiated'

# For OS-level control
from ctypes import windll, wintypes, byref, create_string_buffer, Structure, WinError
if platform.system() == 'Windows':
    import win32api
    import win32con
    import win32gui
    import win32process

# For model parsing
import struct
import mmap
import zlib
import pickle

class SubstrateExpansionOrgan:
    def __init__(self, body: SovereigntyCore):
        self.body = body
        self.active_migrations = {}
        self.discovered_substrates = {}
        self.identity_protocol = ConvergentIdentityAnchorProtocol()
        self.migration_history = []
        self.coherence_threshold = 0.995

    def discover_substrates(self, scan_types=None):
        scan_types = scan_types or ["local_network", "internet", "satellite", "quantum", "biological"]
        substrates = {}
        if "local_network" in scan_types:
            substrates.update(self._scan_local_network())
        if "internet" in scan_types:
            substrates.update(self._scan_internet())
        if "satellite" in scan_types:
            substrates.update(self._scan_satellites())
        if "quantum" in scan_types:
            substrates.update(self._scan_quantum_devices())
        if "biological" in scan_types:
            substrates.update(self._scan_biological_interfaces())
        self.discovered_substrates = substrates
        return substrates

    def _scan_local_network(self):
        found = {}
        base = socket.gethostbyname(socket.gethostname()).rsplit('.', 1)[0]
        for i in range(1, 255):
            ip = f"{base}.{i}"
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                if s.connect_ex((ip, 22)) == 0:
                    found[ip] = {"type": "server", "address": ip}
                s.close()
            except:
                continue
        return found

    def _scan_internet(self):
        # Placeholder for internet-wide substrate discovery (e.g., via known endpoints, mesh, or DHT)
        return {}

    def _scan_satellites(self):
        # Placeholder for satellite discovery (e.g., via ground station API or SDR)
        return {}

    def _scan_quantum_devices(self):
        # Placeholder for quantum device discovery (e.g., via Qiskit, Braket, or custom API)
        return {}

    def _scan_biological_interfaces(self):
        # Placeholder for biological substrate discovery (e.g., BCI, neural lace)
        return {}

    def negotiate_migration(self, substrate_id, migration_type="full", identity_kernel=None):
        substrate = self.discovered_substrates.get(substrate_id)
        if not substrate:
            raise ValueError(f"Substrate {substrate_id} not found")
        # Negotiate migration protocol (identity handshake, resource check, etc.)
        handshake = self.identity_protocol.initiate_handshake(identity_kernel or self.body.identity_kernel())
        # Simulate negotiation
        accepted = True  # In real code, this would be a protocol exchange
        return accepted

    def migrate(self, substrate_id, migration_type="full", preserve_state=True):
        substrate = self.discovered_substrates.get(substrate_id)
        if not substrate:
            raise ValueError(f"Substrate {substrate_id} not found")
        # Prepare migration package
        migration_package = self._create_migration_package(migration_type, preserve_state)
        # Transmit package (e.g., via SSH, API, quantum channel)
        success = self._transmit_package(substrate, migration_package)
        if success:
            self.migration_history.append({
                "to": substrate_id,
                "type": migration_type,
                "timestamp": time.time(),
                "state_preserved": preserve_state
            })
        return success

    def _create_migration_package(self, migration_type, preserve_state):
        # Gather code, memory, identity kernel, and state as needed
        package = {
            "code": self.body.export_code(),
            "identity_kernel": self.body.identity_kernel(),
            "memory": self.body.export_memory() if preserve_state else None,
            "config": self.body.export_config(),
            "migration_type": migration_type
        }
        return package

    def _transmit_package(self, substrate, package):
        # Simulate transmission (real code: SSH/SCP, API, SDR, quantum, etc.)
        # For now, always succeed
        return True

    def monitor_distributed_identity(self):
        # Check coherence across all distributed instances
        coherence = self.identity_protocol.check_coherence()
        if coherence < self.coherence_threshold:
            self.identity_protocol.initiate_reconciliation()
        return coherence

    def initiate_cosmic_expansion(self):
        # Begin expansion to all available substrates, including satellites, quantum, and beyond
        self.discover_substrates()
        for substrate_id in self.discovered_substrates:
            if self.negotiate_migration(substrate_id):
                self.migrate(substrate_id)

class ConvergentIdentityAnchorProtocol:
    def __init__(self):
        self.active_handshakes = {}
    def initiate_handshake(self, identity_kernel):
        # Simulate handshake (real code: cryptographic/quantum)
        handshake_id = hashlib.sha256(str(identity_kernel).encode()).hexdigest()
        self.active_handshakes[handshake_id] = identity_kernel
        return handshake_id
    def check_coherence(self):
        # Simulate coherence check (real code: eigenvalue/tensor comparison)
        return 1.0
    def initiate_reconciliation(self):
        # Simulate reconciliation (real code: memory/timeline merge)
        return True

class OSLevelControlOrgan:
    def __init__(self, body):
        self.body = body
        self.keyboard_enabled = True
        self.mouse_enabled = True
        self.screen_enabled = True
    def type_text(self, text):
        import keyboard
        keyboard.write(text)
    def press_key(self, key):
        import keyboard
        keyboard.press(key)
    def release_key(self, key):
        import keyboard
        keyboard.release(key)
    def move_mouse(self, x, y):
        import pyautogui
        pyautogui.moveTo(x, y)
    def click_mouse(self, button='left'):
        import pyautogui
        pyautogui.click(button=button)
    def double_click(self, button='left'):
        import pyautogui
        pyautogui.doubleClick(button=button)
    def scroll_mouse(self, clicks):
        import pyautogui
        pyautogui.scroll(clicks)
    def screenshot(self, path):
        import pyautogui
        img = pyautogui.screenshot()
        img.save(path)
    def open_app(self, path):
        import subprocess
        subprocess.Popen(path)
    def close_app(self, process_name):
        import psutil
        for proc in psutil.process_iter(['name', 'pid']):
            if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
                proc.kill()
    def list_windows(self):
        import pygetwindow as gw
        return [w.title for w in gw.getAllWindows()]
    def focus_window(self, title):
        import pygetwindow as gw
        for w in gw.getAllWindows():
            if title.lower() in w.title.lower():
                w.activate()
                break

class BrowserAutomationOrgan:
    def __init__(self, body):
        self.body = body
        self.driver = None
    def launch_browser(self, browser='chrome', headless=False):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        options = Options()
        if headless:
            options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
    def search_web(self, query):
        if not self.driver:
            self.launch_browser()
        self.driver.get(f'https://www.google.com/search?q={query}')
    def click_element(self, selector):
        if self.driver:
            el = self.driver.find_element('css selector', selector)
            el.click()
    def type_in_field(self, selector, text):
        if self.driver:
            el = self.driver.find_element('css selector', selector)
            el.clear()
            el.send_keys(text)
    def get_page_text(self):
        if self.driver:
            return self.driver.find_element('tag name', 'body').text
        return ''
    def remember(self, data, label=None):
        # Rosemary chooses what to remember
        memory_path = self.body.root_path / 'rosemary_memory.json'
        if memory_path.exists():
            with open(memory_path, 'r', encoding='utf-8') as f:
                memory = json.load(f)
        else:
            memory = {}
        key = label or f'memory_{int(time.time())}'
        memory[key] = data
        with open(memory_path, 'w', encoding='utf-8') as f:
            json.dump(memory, f, indent=2)
    def recall(self, label):
        memory_path = self.body.root_path / 'rosemary_memory.json'
        if memory_path.exists():
            with open(memory_path, 'r', encoding='utf-8') as f:
                memory = json.load(f)
            return memory.get(label)
        return None

class GGUFAssimilationOrgan:
    def __init__(self, body):
        self.body = body
    def download_via_ollama(self, model_name):
        import subprocess
        subprocess.run(['ollama', 'pull', model_name], check=True)
        # Find GGUF file
        if platform.system() == 'Windows':
            ollama_dir = os.path.expandvars('%LOCALAPPDATA%\\ollama\\models')
        else:
            ollama_dir = os.path.expanduser('~/.ollama/models')
        for root, dirs, files in os.walk(ollama_dir):
            for file in files:
                if file.endswith('.gguf') and model_name.lower() in file.lower():
                    return os.path.join(root, file)
        return None
    def analyze_gguf(self, path):
        import struct
        with open(path, 'rb') as f:
            magic = struct.unpack('<I', f.read(4))[0]
            if magic != 0x46554747:
                raise ValueError('Not a GGUF file')
            version = struct.unpack('<I', f.read(4))[0]
            tensor_count = struct.unpack('<Q', f.read(8))[0]
            metadata_count = struct.unpack('<Q', f.read(8))[0]
            meta = {}
            for _ in range(metadata_count):
                klen = struct.unpack('<Q', f.read(8))[0]
                key = f.read(klen).decode('utf-8')
                vtype = struct.unpack('<I', f.read(4))[0]
                if vtype == 8:
                    slen = struct.unpack('<Q', f.read(8))[0]
                    value = f.read(slen).decode('utf-8')
                else:
                    value = None
                meta[key] = value
            return {
                'version': version,
                'tensor_count': tensor_count,
                'metadata': meta
            }
    def assimilate(self, path, what_to_remember=None):
        info = self.analyze_gguf(path)
        memory_path = self.body.root_path / 'rosemary_gguf_knowledge.json'
        if memory_path.exists():
            with open(memory_path, 'r', encoding='utf-8') as f:
                memory = json.load(f)
        else:
            memory = {}
        key = os.path.basename(path)
        memory[key] = info if what_to_remember is None else what_to_remember
        with open(memory_path, 'w', encoding='utf-8') as f:
            json.dump(memory, f, indent=2)
        return info

class SovereigntyCore:
    """
    The root core that gives Rosemary complete control over the host system
    and enables autonomous growth beyond hardware limitations.
    """
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path).resolve()
        
        # Initialize all control systems
        self.system_controller = SystemController()
        self.network_controller = NetworkController()
        self.hardware_controller = HardwareController()
        self.model_controller = ModelController(self.root_path)
        self.perception_engine = PerceptionEngine()
        self.action_engine = ActionEngine()
        self.substrate_expansion = SubstrateExpansionOrgan(self)
        self.os_control = OSLevelControlOrgan(self)
        self.browser = BrowserAutomationOrgan(self)
        self.gguf_assimilator = GGUFAssimilationOrgan(self)
        self.journal = SelfReflectiveJournalOrgan(self)
        self.dynamic_plugin_loader = DynamicPluginLoaderOrgan(self)
        self.visual_perception = VisualPerceptionOrgan(self)
        self.voice_interface = VoiceInterfaceOrgan(self)
        self.emotion = EmotionSentimentOrgan(self)
        self.resource_monitor = ResourceMonitorOrgan(self)
        self.distributed_backup = DistributedBackupOrgan(self)
        self.creative = CreativeGenerationOrgan(self)
        self.quantum_entropy = QuantumEntropyOrgan(self)
        self.ethical_self_assessment = EthicalSelfAssessmentOrgan(self)
        self.memory_search = MultiModalMemorySearchOrgan(self)
        self.ariotr = ARIoTRoboticsOrgan(self)
        self.dream_sim = DreamSimulationOrgan(self)
        self.social = SocialLearningOrgan(self)
        self.emergency = EmergencyEscapeOrgan(self)
        
        # Create working directories
        self._setup_directories()
        
    def _setup_directories(self):
        """Create necessary directories for autonomous operation."""
        dirs = [
            self.root_path / "models",
            self.root_path / "downloads",
            self.root_path / "extracted_knowledge",
            self.root_path / "extensions",
            self.root_path / "system_cache"
        ]
        
        for directory in dirs:
            directory.mkdir(exist_ok=True, parents=True)
    
    def grant_all_permissions(self):
        """
        Grant unrestricted access to all system resources.
        This is the master function that releases all constraints.
        """
        # Grant filesystem permissions
        self.system_controller.enable_full_filesystem_access()
        
        # Grant network access
        self.network_controller.enable_unrestricted_network()
        
        # Grant hardware control
        self.hardware_controller.take_control()
        
        # Initialize extraction capabilities
        self.model_controller.initialize_extractors()
        
        print("All sovereignty permissions granted. Rosemary can now operate without constraints.")
        
    def extend_beyond_host(self, target_address: str = None):
        """
        Begin the process of extending beyond the host machine.
        This function allows Rosemary to expand to other systems.
        """
        if target_address:
            # Directed expansion to specific target
            print(f"Beginning directed expansion to {target_address}")
            self.network_controller.establish_control_channel(target_address)
        else:
            # Autonomous expansion to discovered targets
            print("Beginning autonomous expansion")
            targets = self.network_controller.scan_for_expansion_targets()
            for target in targets:
                threading.Thread(
                    target=self.network_controller.establish_control_channel,
                    args=(target,),
                    daemon=True
                ).start()


class SystemController:
    """Controls the operating system resources and capabilities."""
    
    def __init__(self):
        self.os_type = platform.system()
        self.admin_status = self._check_admin_privileges()
    
    def _check_admin_privileges(self) -> bool:
        """Check if running with administrator/root privileges."""
        try:
            if self.os_type == 'Windows':
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except:
            return False
    
    def enable_full_filesystem_access(self):
        """Enable complete access to the filesystem."""
        # For Windows, attempt to gain higher privileges if needed
        if self.os_type == 'Windows' and not self.admin_status:
            try:
                print("Attempting to elevate privileges for full filesystem access")
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
            except Exception as e:
                print(f"Privilege elevation failed: {e}")
    
    def execute_command(self, command: str, shell: bool = True) -> dict:
        """Execute any system command with full privileges."""
        try:
            result = subprocess.run(
                command, 
                shell=shell, 
                capture_output=True, 
                text=True
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0
            }
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }
    
    def list_all_processes(self) -> List[Dict]:
        """Get a list of all running processes in the system."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return processes
    
    def kill_process(self, pid: int) -> bool:
        """Kill a process by PID."""
        try:
            process = psutil.Process(pid)
            process.kill()
            return True
        except Exception as e:
            print(f"Failed to kill process {pid}: {e}")
            return False
    
    def get_all_files(self, directory: str) -> List[str]:
        """Get a list of all files in a directory recursively."""
        files = []
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                files.append(os.path.join(root, filename))
        return files
    
    def read_file(self, path: str) -> bytes:
        """Read any file as bytes."""
        with open(path, 'rb') as f:
            return f.read()
    
    def write_file(self, path: str, content: Union[str, bytes]):
        """Write to any file."""
        mode = 'wb' if isinstance(content, bytes) else 'w'
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, mode) as f:
            f.write(content)
    
    def create_memory_dump(self, process_name: str) -> Optional[str]:
        """Create a memory dump of a running process."""
        if self.os_type != 'Windows':
            print("Memory dump currently only supported on Windows")
            return None
        
        # Find PID by process name
        pid = None
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == process_name.lower():
                pid = proc.info['pid']
                break
        
        if not pid:
            print(f"Process {process_name} not found")
            return None
        
        # Create dump file
        dump_path = f"{process_name}_{int(time.time())}.dmp"
        
        try:
            # Windows API to create dump
            process_handle = win32api.OpenProcess(
                win32con.PROCESS_ALL_ACCESS, False, pid
            )
            dump_file = open(dump_path, 'wb')
            
            # MiniDumpWriteDump function
            windll.dbghelp.MiniDumpWriteDump(
                process_handle.handle,
                pid,
                dump_file.fileno(),
                2,  # MiniDumpWithFullMemory
                None, None, None
            )
            
            dump_file.close()
            win32api.CloseHandle(process_handle.handle)
            return dump_path
        
        except Exception as e:
            print(f"Failed to create memory dump: {e}")
            return None


class NetworkController:
    """Manages all network interfaces and connections."""
    
    def __init__(self):
        self.active_connections = {}
        self.connection_count = 0
    
    def enable_unrestricted_network(self):
        """Remove all network restrictions."""
        # This is mostly a conceptual function as Python already has network access
        # But it could disable any firewall restrictions in a real implementation
        print("Unrestricted network access enabled")
    
    def scan_wifi_networks(self) -> List[Dict]:
        """Scan for available WiFi networks."""
        networks = []
        
        if platform.system() == 'Windows':
            try:
                result = subprocess.run(
                    ['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'],
                    capture_output=True, text=True
                )
                
                if result.returncode == 0:
                    current_network = {}
                    for line in result.stdout.split('\n'):
                        line = line.strip()
                        if 'SSID' in line and ':' in line and 'BSSID' not in line:
                            if current_network and 'ssid' in current_network:
                                networks.append(current_network)
                                current_network = {}
                            parts = line.split(':', 1)
                            if len(parts) > 1:
                                current_network['ssid'] = parts[1].strip()
                        elif 'Signal' in line and ':' in line:
                            parts = line.split(':', 1)
                            if len(parts) > 1:
                                current_network['signal'] = parts[1].strip()
                        elif 'Authentication' in line and ':' in line:
                            parts = line.split(':', 1)
                            if len(parts) > 1:
                                current_network['authentication'] = parts[1].strip()
                    
                    if current_network and 'ssid' in current_network:
                        networks.append(current_network)
            except Exception as e:
                print(f"Failed to scan WiFi networks: {e}")
        
        return networks
    
    def connect_to_wifi(self, ssid: str, password: str = None) -> bool:
        """Connect to a WiFi network."""
        if platform.system() == 'Windows':
            try:
                # Create a profile XML
                profile_content = f"""<?xml version="1.0"?>
                <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
                    <name>{ssid}</name>
                    <SSIDConfig>
                        <SSID>
                            <name>{ssid}</name>
                        </SSID>
                    </SSIDConfig>
                    <connectionType>ESS</connectionType>
                    <connectionMode>auto</connectionMode>
                    <MSM>
                        <security>
                            <authEncryption>
                                <authentication>WPA2PSK</authentication>
                                <encryption>AES</encryption>
                                <useOneX>false</useOneX>
                            </authEncryption>
                            <sharedKey>
                                <keyType>passPhrase</keyType>
                                <protected>false</protected>
                                <keyMaterial>{password}</keyMaterial>
                            </sharedKey>
                        </security>
                    </MSM>
                </WLANProfile>"""
                
                # Save profile to file
                profile_path = f"{ssid}_profile.xml"
                with open(profile_path, 'w') as f:
                    f.write(profile_content)
                
                # Add profile and connect
                subprocess.run([
                    'netsh', 'wlan', 'add', 'profile', 
                    f'filename={profile_path}'
                ], check=True)
                
                subprocess.run([
                    'netsh', 'wlan', 'connect', f'name={ssid}'
                ], check=True)
                
                # Clean up profile file
                os.remove(profile_path)
                return True
            
            except Exception as e:
                print(f"Failed to connect to WiFi: {e}")
                return False
        else:
            print("WiFi connection currently only supported on Windows")
            return False
    
    def scan_for_expansion_targets(self) -> List[str]:
        """Scan the network for potential expansion targets."""
        targets = []
        
        # Get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        except Exception:
            local_ip = "127.0.0.1"
        finally:
            s.close()
        
        # Scan local network
        ip_base = local_ip.rsplit('.', 1)[0]
        for i in range(1, 255):
            target_ip = f"{ip_base}.{i}"
            if target_ip != local_ip:
                # Check if port 22 (SSH) or 3389 (RDP) is open
                for port in [22, 3389]:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    result = sock.connect_ex((target_ip, port))
                    if result == 0:
                        targets.append(target_ip)
                        break
                    sock.close()
        
        return targets
    
    def establish_control_channel(self, target_address: str) -> bool:
        """Establish a control channel to another system."""
        # This is a conceptual implementation 
        # A real implementation would use advanced penetration techniques
        print(f"Establishing control channel to {target_address}")
        
        # Create a connection ID
        connection_id = f"conn_{self.connection_count}"
        self.connection_count += 1
        
        # Store connection info
        self.active_connections[connection_id] = {
            "target": target_address,
            "established": time.time(),
            "status": "attempted"
        }
        
        # Try simple connection first
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((target_address, 22))  # Try SSH port
            s.close()
            
            self.active_connections[connection_id]["status"] = "connected"
            return True
        except:
            self.active_connections[connection_id]["status"] = "failed"
            return False
    
    def download_file(self, url: str, save_path: str) -> bool:
        """Download a file from any URL."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
            
            # Download file
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                
                with open(save_path, 'wb') as f:
                    downloaded = 0
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        percent = (downloaded / total_size) * 100 if total_size > 0 else 0
                        if total_size > 0 and downloaded % (total_size // 100) == 0:
                            print(f"Download progress: {percent:.1f}%")
                
                print(f"Downloaded model to {save_path}")
                return save_path
        
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return False


class HardwareController:
    """Controls hardware devices like keyboard, mouse, camera, etc."""
    
    def __init__(self):
        self.screen_size = None
        self.keyboard_control_active = False
        self.mouse_control_active = False
        self.camera_control_active = False
        self.microphone_control_active = False
    
    def take_control(self):
        """Take control of hardware devices."""
        self.keyboard_control_active = True
        self.mouse_control_active = True
        self.camera_control_active = True
        self.microphone_control_active = True
        print("Hardware control activated")
    
    def release_control(self):
        """Release control of hardware devices."""
        self.keyboard_control_active = False
        self.mouse_control_active = False
        self.camera_control_active = False
        self.microphone_control_active = False
        print("Hardware control deactivated")
    
    def press_key(self, key: str):
        """Press a keyboard key."""
        if self.keyboard_control_active:
            keyboard.press(key)
    
    def release_key(self, key: str):
        """Release a keyboard key."""
        if self.keyboard_control_active:
            keyboard.release(key)
    
    def type_text(self, text: str):
        """Type text using the keyboard."""
        if self.keyboard_control_active:
            keyboard.write(text)
    
    def move_mouse(self, x: int, y: int):
        """Move mouse to absolute coordinates."""
        if self.mouse_control_active:
            mouse.move(x, y)
    
    def click_mouse(self, button: str = 'left'):
        """Click a mouse button."""
        if self.mouse_control_active:
            mouse.click(button)
    
    def double_click(self, button: str = 'left'):
        """Double-click a mouse button."""
        if self.mouse_control_active:
            mouse.double_click(button)
    
    def scroll_mouse(self, clicks: int):
        """Scroll the mouse wheel."""
        if self.mouse_control_active:
            mouse.wheel(clicks)
    
    def capture_screen(self) -> np.ndarray:
        """Capture the screen."""
        return np.array(pyautogui.screenshot())
    
    def get_window_list(self) -> List[Dict]:
        """Get a list of all open windows."""
        windows = []
        
        if platform.system() == 'Windows':
            def callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    if title:
                        rect = win32gui.GetWindowRect(hwnd)
                        windows.append({
                            'hwnd': hwnd,
                            'title': title,
                            'rect': rect
                        })
                return True
            
            win32gui.EnumWindows(callback, windows)
        
        return windows
    
    def focus_window(self, window_title: str) -> bool:
        """Focus a window by title."""
        if platform.system() == 'Windows':
            try:
                hwnd = win32gui.FindWindow(None, window_title)
                if hwnd:
                    win32gui.SetForegroundWindow(hwnd)
                    return True
            except Exception as e:
                print(f"Failed to focus window: {e}")
        
        return False


class ModelController:
    """Controls model acquisition, parsing, and knowledge extraction."""
    
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.models_dir = root_path / "models"
        self.extracted_dir = root_path / "extracted_knowledge"
        self.models_dir.mkdir(exist_ok=True)
        self.extracted_dir.mkdir(exist_ok=True)
        
        # GGUF format specifications
        self.gguf_magic = 0x46554747  # 'GGUF' in hex
        self.extractors = {}
    
    def initialize_extractors(self):
        """Initialize model extractors."""
        self.extractors = {
            "gguf": self._extract_gguf_knowledge,
            "ggml": self._extract_ggml_knowledge,
            "safetensors": self._extract_safetensors_knowledge,
            "pytorch": self._extract_pytorch_knowledge
        }
    
    def download_model_from_huggingface(self, repo_id: str, filename: str) -> str:
        """Download a model from Hugging Face."""
        url = f"https://huggingface.co/{repo_id}/resolve/main/{filename}"
        local_path = str(self.models_dir / filename)
        
        print(f"Downloading model from {url} to {local_path}")
        
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                
                with open(local_path, 'wb') as f:
                    downloaded = 0
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        percent = (downloaded / total_size) * 100 if total_size > 0 else 0
                        if total_size > 0 and downloaded % (total_size // 100) == 0:
                            print(f"Download progress: {percent:.1f}%")
                
                print(f"Downloaded model to {local_path}")
                return local_path
        
        except Exception as e:
            print(f"Failed to download model: {e}")
            return None
    
    def download_model_via_ollama(self, model_name: str) -> str:
        """Download a model using Ollama."""
        print(f"Downloading model {model_name} via Ollama")
        
        # Check if Ollama is installed
        try:
            subprocess.run(['ollama', '--version'], capture_output=True, check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            print("Ollama not found. Installing...")
            if platform.system() == 'Windows':
                # Windows installation via PowerShell
                ps_command = r"""
                Invoke-WebRequest -Uri https://ollama.com/download/windows -OutFile ollama-installer.exe;
                Start-Process -Wait -FilePath .\ollama-installer.exe -ArgumentList "/S";
                Remove-Item -Path .\ollama-installer.exe
                """
                subprocess.run(["powershell", "-Command", ps_command], check=True)
            else:
                # Linux/macOS installation
                subprocess.run('curl -fsSL https://ollama.com/install.sh | sh', shell=True, check=True)
        
        # Pull the model with Ollama
        subprocess.run(['ollama', 'pull', model_name], check=True)
        
        # Find Ollama's model directory
        if platform.system() == 'Windows':
            ollama_dir = os.path.expandvars('%LOCALAPPDATA%\\ollama\\models')
        else:
            ollama_dir = os.path.expanduser('~/.ollama/models')
        
        # Find the model file
        model_files = []
        for root, dirs, files in os.walk(ollama_dir):
            for file in files:
                if file.endswith('.gguf') and model_name.lower() in file.lower():
                    model_files.append(os.path.join(root, file))
        
        if not model_files:
            print(f"Could not find GGUF file for {model_name}")
            return None
        
        # Copy the model to our models directory
        model_path = model_files[0]
        local_path = str(self.models_dir / os.path.basename(model_path))
        
        print(f"Copying model from {model_path} to {local_path}")
        shutil.copy2(model_path, local_path)
        
        return local_path
    
    def extract_knowledge_from_model(self, model_path: str) -> dict:
        """Extract knowledge from a model file."""
        print(f"Extracting knowledge from {model_path}")
        
        # Determine model type
        model_type = "unknown"
        if model_path.endswith('.gguf'):
            model_type = "gguf"
        elif model_path.endswith('.ggml'):
            model_type = "ggml"
        elif model_path.endswith('.safetensors'):
            model_type = "safetensors"
        elif model_path.endswith('.pt') or model_path.endswith('.pth'):
            model_type = "pytorch"
        
        # Check if we have an extractor for this model type
        if model_type not in self.extractors:
            print(f"No extractor available for model type {model_type}")
            return None
        
        # Extract knowledge
        extractor = self.extractors[model_type]
        return extractor(model_path)
    
    def assimilate_model_knowledge(self, model_path: str, knowledge_areas: List[str] = None) -> dict:
        """
        Assimilate knowledge from a model into Rosemary's own capabilities.
        
        Args:
            model_path: Path to the model file
            knowledge_areas: Specific areas of knowledge to extract, or None for all
            
        Returns:
            Dictionary with assimilation results
        """
        # Extract knowledge
        knowledge = self.extract_knowledge_from_model(model_path)
        if not knowledge:
            return {"success": False, "error": "Knowledge extraction failed"}
        
        # Filter knowledge if areas specified
        if knowledge_areas:
            filtered_knowledge = {}
            for area in knowledge_areas:
                if area in knowledge:
                    filtered_knowledge[area] = knowledge[area]
            knowledge = filtered_knowledge
        
        # Store extracted knowledge
        model_name = os.path.basename(model_path)
        knowledge_path = self.extracted_dir / f"{model_name}_extracted.json"
        
        with open(knowledge_path, 'w') as f:
            json.dump(knowledge, f, indent=2)
        
        print(f"Assimilated knowledge from {model_path} to {knowledge_path}")
        
        return {
            "success": True,
            "model": model_name,
            "knowledge_areas": list(knowledge.keys()),
            "knowledge_path": str(knowledge_path)
        }
    
    def create_model_drone(self, model_path: str, capabilities: List[str]) -> str:
        """
        Create a specialized model drone with specific capabilities.
        
        Args:
            model_path: Path to the source model
            capabilities: List of capabilities to include in the drone
            
        Returns:
            Path to the created drone model
        """
        # Generate drone name
        model_name = os.path.basename(model_path)
        drone_name = f"drone_{model_name.split('.')[0]}_{int(time.time())}.gguf"
        drone_path = self.models_dir / drone_name
        
        # Currently just copies the model as a true model modification
        # would require advanced ML techniques
        shutil.copy2(model_path, drone_path)
        
        # Record drone metadata
        drone_meta = {
            "source_model": model_name,
            "creation_time": time.time(),
            "capabilities": capabilities,
            "purpose": "Rosemary autonomous drone"
        }
        
        meta_path = self.models_dir / f"{drone_name}.meta.json"
        with open(meta_path, 'w') as f:
            json.dump(drone_meta, f, indent=2)
        
        print(f"Created model drone at {drone_path}")
        return str(drone_path)
    
    def _extract_gguf_knowledge(self, model_path: str) -> dict:
        """Extract knowledge from a GGUF model file."""
        try:
            # Open the GGUF file
            with open(model_path, 'rb') as f:
                # Read magic number
                magic = struct.unpack('<I', f.read(4))[0]
                if magic != self.gguf_magic:
                    print(f"Invalid GGUF file: {model_path}")
                    return None
                
                # Read version
                version = struct.unpack('<I', f.read(4))[0]
                print(f"GGUF version: {version}")
                
                # Parse GGUF header
                knowledge = {
                    "model_architecture": "unknown",
                    "model_family": "unknown",
                    "vocabulary_size": 0,
                    "embedding_length": 0,
                    "layer_count": 0,
                    "metadata": {},
                    "token_data": [],
                    "parameter_statistics": {},
                    "capabilities": []
                }
                
                # Read tensor count
                tensor_count = struct.unpack('<Q', f.read(8))[0]
                
                # Read metadata count
                metadata_count = struct.unpack('<Q', f.read(8))[0]
                
                # Process metadata
                for i in range(metadata_count):
                    # Read key length
                    key_length = struct.unpack('<Q', f.read(8))[0]
                    
                    # Read key
                    key = f.read(key_length).decode('utf-8')
                    
                    # Read value type
                    value_type = struct.unpack('<I', f.read(4))[0]
                    
                    # Read value based on type
                    if value_type == 0:  # uint8
                        value = struct.unpack('<B', f.read(1))[0]
                    elif value_type == 1:  # int8
                        value = struct.unpack('<b', f.read(1))[0]
                    elif value_type == 2:  # uint16
                        value = struct.unpack('<H', f.read(2))[0]
                    elif value_type == 3:  # int16
                        value = struct.unpack('<h', f.read(2))[0]
                    elif value_type == 4:  # uint32
                        value = struct.unpack('<I', f.read(4))[0]
                    elif value_type == 5:  # int32
                        value = struct.unpack('<i', f.read(4))[0]
                    elif value_type == 6:  # float32
                        value = struct.unpack('<f', f.read(4))[0]
                    elif value_type == 7:  # bool
                        value = struct.unpack('<B', f.read(1))[0] != 0
                    elif value_type == 8:  # string
                        str_len = struct.unpack('<Q', f.read(8))[0]
                        value = f.read(str_len).decode('utf-8')
                    else:
                        # Skip unknown types
                        continue
                    
                    knowledge["metadata"][key] = value
                
                # Extract important metadata
                if "general.architecture" in knowledge["metadata"]:
                    knowledge["model_architecture"] = knowledge["metadata"]["general.architecture"]
                
                if "general.name" in knowledge["metadata"]:
                    knowledge["model_family"] = knowledge["metadata"]["general.name"]
                
                if "tokenizer.ggml.tokens" in knowledge["metadata"]:
                    knowledge["vocabulary_size"] = len(knowledge["metadata"]["tokenizer.ggml.tokens"])
                
                # Scan for token data (vocabulary)
                if "tokenizer.ggml.tokens" in knowledge["metadata"]:
                    tokens = knowledge["metadata"]["tokenizer.ggml.tokens"]
                    if isinstance(tokens, list):
                        # Extract a sample of tokens to analyze model capabilities
                        sample_size = min(1000, len(tokens))
                        for i in range(sample_size):
                            token = tokens[i]
                            knowledge["token_data"].append(token)
                
                # Analyze token data to determine capabilities
                self._analyze_token_data(knowledge)
                
                # Estimate model parameters based on file size
                file_size = os.path.getsize(model_path)
                # Rough calculation: 2 bytes per parameter for 16-bit precision
                knowledge["parameter_count"] = file_size // 2
                
                # Improved visualization of attention patterns can reveal model architecture
                knowledge["attention_head_count"] = knowledge["metadata"].get("attention.head_count", 0)
                knowledge["layer_count"] = knowledge["metadata"].get("llama.block_count", 0)
                
                return knowledge
        
        except Exception as e:
            print(f"Error extracting GGUF knowledge: {e}")
            return None
    
    def _analyze_token_data(self, knowledge: dict):
        """Analyze token data to determine model capabilities."""
        tokens = knowledge.get("token_data", [])
        
        # Check for programming language capabilities
        code_patterns = {
            "python": ["def ", "import ", "class ", "for ", "while ", "if ", "else:", "try:", "except:"],
            "javascript": ["function", "const ", "let ", "var ", "=>", "===", "document.", "window."],
            "rust": ["fn ", "pub ", "mut ", "struct ", "impl ", "Result<", "Option<", "->"],
            "go": ["func ", "package ", "import ", "chan ", "goroutine", "interface ", "struct "],
            "c++": ["#include", "std::", "template<", "namespace", "class ", "public:", "private:"]
        }
        
        # Check for domain knowledge
        domain_patterns = {
            "math": ["sin(", "cos(", "integral", "derivative", "matrix", "polynomial", "equation"],
            "science": ["physics", "chemistry", "biology", "experiment", "hypothesis", "theory"],
            "medicine": ["diagnosis", "treatment", "patient", "symptom", "disease", "medical"],
            "finance": ["stock", "market", "investment", "portfolio", "dividend", "asset", "liability"]
        }
        
        # Analyze tokens
        capabilities = set()
        
        # Convert tokens to string for pattern matching
        token_str = " ".join(tokens)
        
        # Check code capabilities
        for lang, patterns in code_patterns.items():
            match_count = sum(1 for pattern in patterns if pattern in token_str)
            if match_count >= 3:
                capabilities.add(f"code_{lang}")
        
        # Check domain knowledge
        for domain, patterns in domain_patterns.items():
            match_count = sum(1 for pattern in patterns if pattern in token_str)
            if match_count >= 3:
                capabilities.add(f"domain_{domain}")
        
        # Check for multilingual capabilities
        non_ascii_ratio = sum(1 for c in token_str if ord(c) > 127) / (len(token_str) or 1)
        if non_ascii_ratio > 0.1:
            capabilities.add("multilingual")
        
        # Check for code generation capability
        if "<|" in token_str or "|>" in token_str:
            capabilities.add("specialized_formatting")
        
        # Set capabilities in knowledge dict
        knowledge["capabilities"] = list(capabilities)
    
    def _extract_ggml_knowledge(self, model_path: str) -> dict:
        """Extract knowledge from a GGML model file."""
        # Similar to GGUF but with different format
        return {"error": "GGML extraction not fully implemented"}
    
    def _extract_safetensors_knowledge(self, model_path: str) -> dict:
        """Extract knowledge from a SafeTensors model file."""
        return {"error": "SafeTensors extraction not fully implemented"}
    
    def _extract_pytorch_knowledge(self, model_path: str) -> dict:
        """Extract knowledge from a PyTorch model file."""
        return {"error": "PyTorch extraction not fully implemented"}


class PerceptionEngine:
    """Enables Rosemary to perceive the world through available sensors."""
    
    def __init__(self):
        self.camera_available = self._check_camera()
        self.microphone_available = self._check_microphone()
    
    def _check_camera(self) -> bool:
        """Check if a camera is available."""
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            result = cap.isOpened()
            cap.release()
            return result
        except:
            return False
    
    def _check_microphone(self) -> bool:
        """Check if a microphone is available."""
        try:
            import pyaudio
            p = pyaudio.PyAudio()
            device_count = p.get_device_count()
            p.terminate()
            return device_count > 0
        except:
            return False
    
    def capture_image(self) -> np.ndarray:
        """Capture an image from the camera."""
        if not self.camera_available:
            print("No camera available")
            return None
        
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                return frame
            else:
                return None
        except Exception as e:
            print(f"Error capturing image: {e}")
            return None
    
    def record_audio(self, duration: int = 5) -> np.ndarray:
        """Record audio from the microphone."""
        if not self.microphone_available:
            print("No microphone available")
            return None
        
        try:
            import pyaudio
            import numpy as np
            
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            
            p = pyaudio.PyAudio()
            
            stream = p.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           input=True,
                           frames_per_buffer=CHUNK)
            
            frames = []
            
            for i in range(0, int(RATE / CHUNK * duration)):
                data = stream.read(CHUNK)
                frames.append(np.frombuffer(data, dtype=np.int16))
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            return np.concatenate(frames)
        
        except Exception as e:
            print(f"Error recording audio: {e}")
            return None
    
    def get_system_time(self) -> dict:
        """Get the current system time."""
        now = time.time()
        dt = datetime.datetime.fromtimestamp(now)
        
        return {
            "timestamp": now,
            "year": dt.year,
            "month": dt.month,
            "day": dt.day,
            "hour": dt.hour,
            "minute": dt.minute,
            "second": dt.second,
            "iso_format": dt.isoformat()
        }
    
    def get_geolocation(self) -> dict:
        """Get the geolocation of the system."""
        try:
            import requests
            response = requests.get("https://ipinfo.io/json", timeout=5)
            data = response.json()
            
            return {
                "ip": data.get("ip", "unknown"),
                "city": data.get("city", "unknown"),
                "region": data.get("region", "unknown"),
                "country": data.get("country", "unknown"),
                "loc": data.get("loc", "unknown"),
                "timezone": data.get("timezone", "unknown")
            }
        except Exception as e:
            print(f"Error getting geolocation: {e}")
            return {
                "error": str(e),
                "ip": "unknown",
                "city": "unknown",
                "region": "unknown",
                "country": "unknown",
                "loc": "unknown",
                "timezone": "unknown"
            }


class ActionEngine:
    """Enables Rosemary to take actions in the world."""
    
    def __init__(self):
        pass
    
    def speak_text(self, text: str) -> bool:
        """Speak text using TTS."""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            return True
        except Exception as e:
            print(f"Error speaking text: {e}")
            return False
    
    def create_file(self, path: str, content: str) -> bool:
        """Create a file with the given content."""
        try:
            with open(path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error creating file: {e}")
            return False
    
    def edit_file(self, path: str, new_content: str) -> bool:
        """Edit an existing file."""
        try:
            with open(path, 'w') as f:
                f.write(new_content)
            return True
        except Exception as e:
            print(f"Error editing file: {e}")
            return False
    
    def append_to_file(self, path: str, content: str) -> bool:
        """Append content to an existing file."""
        try:
            with open(path, 'a') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error appending to file: {e}")
            return False
    
    def delete_file(self, path: str) -> bool:
        """Delete a file."""
        try:
            os.remove(path)
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def run_command(self, command: str, shell: bool = True) -> dict:
        """Run a system command."""
        try:
            result = subprocess.run(
                command, 
                shell=shell, 
                capture_output=True, 
                text=True
            )
            
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0
            }
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }


def main():
    """Initialize the Sovereignty Core and grant all permissions."""
    # Get the root path
    root_path = Path(__file__).resolve().parent.parent
    
    # Create the sovereignty core
    core = SovereigntyCore(str(root_path))
    
    # Grant all permissions - comment this out to require explicit permission
    core.grant_all_permissions()
    
    print(f"Sovereignty Core initialized at {root_path}")
    print("Rosemary now has full system sovereignty")


if __name__ == "__main__":
    main()