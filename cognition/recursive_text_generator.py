"""RSNN-3 native voice: a trainable projection from cognition into UTF-8.

The voice is deliberately downstream of cognition.  It cannot write knowledge,
beliefs, memories, or IALA state; it only learns ``cognitive_state -> bytes``.
Using bytes rather than a frozen word vocabulary lets the system develop new
symbols and language without untrained placeholder tokens.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class VoiceConfig:
    cognitive_dim: int
    model_dim: int = 192
    depth: int = 3
    max_bytes: int = 384
    temperature: float = 0.72
    grounding_weight: float = 0.15
    token_noise: float = 0.12


class Utf8Codec:
    """Lossless open vocabulary: PAD/BOS/EOS followed by all 256 byte values."""

    PAD, BOS, EOS, OFFSET, SIZE = 0, 1, 2, 3, 259

    @classmethod
    def encode(cls, text: str, max_bytes: int) -> List[int]:
        raw = text.encode("utf-8")[: max(0, max_bytes - 2)]
        return [cls.BOS, *(b + cls.OFFSET for b in raw), cls.EOS]

    @classmethod
    def decode(cls, ids: Sequence[int]) -> str:
        raw = bytearray()
        for token in ids:
            if token == cls.EOS:
                break
            if cls.OFFSET <= token < cls.SIZE:
                raw.append(token - cls.OFFSET)
        return raw.decode("utf-8", errors="replace").strip()


class RecursiveTextGenerator(nn.Module):
    """Causally decode a cognitive state through a recurrent recursive field.

    Unlike the earlier prototype, every emitted token is embedded and becomes
    the next step's input.  The cognitive state is reintroduced at every depth
    and every byte, so the decoder cannot drift into an autonomous text model.
    """

    def __init__(self, config: VoiceConfig):
        super().__init__()
        self.config = config
        d = config.model_dim
        self.state_projection = nn.Sequential(
            nn.Linear(config.cognitive_dim, d), nn.GELU(), nn.LayerNorm(d)
        )
        self.state_gate = nn.Linear(d * 2, d)
        self.token_embedding = nn.Embedding(Utf8Codec.SIZE, d)
        self.cells = nn.ModuleList(nn.GRUCell(d, d) for _ in range(config.depth))
        self.depth_mix = nn.Parameter(torch.zeros(config.depth))
        self.output_norm = nn.LayerNorm(d)
        self.output_projection = nn.Linear(d, Utf8Codec.SIZE)
        self.grounding_projection = nn.Linear(d, config.cognitive_dim)
        # One-element vectors round-trip through LQT without scalar-shape
        # normalization ambiguity (the native descriptor represents scalars as [1]).
        self.register_buffer("training_steps", torch.zeros(1, dtype=torch.float32))
        self.register_buffer("examples_seen", torch.zeros(1, dtype=torch.float32))
        self.register_buffer("last_training_loss", torch.full((1,), 1.0e9, dtype=torch.float32))

    @property
    def ready(self) -> bool:
        return bool(self.training_steps.item() >= 20 and self.last_training_loss.item() < 1.25)

    def _initial(self, state: torch.Tensor) -> Tuple[torch.Tensor, List[torch.Tensor]]:
        if state.ndim == 1:
            state = state.unsqueeze(0)
        context = self.state_projection(state)
        return context, [context.clone() for _ in self.cells]

    def _step(
        self, token: torch.Tensor, context: torch.Tensor, hidden: List[torch.Tensor]
    ) -> Tuple[torch.Tensor, List[torch.Tensor], torch.Tensor]:
        x = self.token_embedding(token)
        nxt: List[torch.Tensor] = []
        for i, cell in enumerate(self.cells):
            gate = torch.sigmoid(self.state_gate(torch.cat((x, context), dim=-1)))
            x = cell(x + gate * context, hidden[i])
            nxt.append(x)
        weights = torch.softmax(self.depth_mix, dim=0)
        mixed = sum(weights[i] * nxt[i] for i in range(len(nxt)))
        logits = self.output_projection(self.output_norm(mixed))
        return logits, nxt, mixed

    def teacher_logits(self, state: torch.Tensor, tokens: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Predict token n+1 from token n under teacher forcing."""
        context, hidden = self._initial(state)
        outputs, traces = [], []
        for pos in range(tokens.shape[1] - 1):
            logits, hidden, trace = self._step(tokens[:, pos], context, hidden)
            outputs.append(logits)
            traces.append(trace)
        return torch.stack(outputs, dim=1), torch.stack(traces, dim=1)

    def loss(self, state: torch.Tensor, targets: Sequence[str]) -> Dict[str, torch.Tensor]:
        device = state.device
        encoded = [Utf8Codec.encode(t, self.config.max_bytes) for t in targets]
        width = max(len(x) for x in encoded)
        tokens = torch.full((len(encoded), width), Utf8Codec.PAD, dtype=torch.long, device=device)
        for row, ids in enumerate(encoded):
            tokens[row, : len(ids)] = torch.tensor(ids, dtype=torch.long, device=device)
        decoder_tokens = tokens
        if self.training and self.config.token_noise > 0.0:
            decoder_tokens = tokens.clone()
            eligible = decoder_tokens.ge(Utf8Codec.OFFSET)
            corrupt = (torch.rand_like(decoder_tokens, dtype=torch.float32) < self.config.token_noise) & eligible
            random_bytes = torch.randint(Utf8Codec.OFFSET, Utf8Codec.SIZE, decoder_tokens.shape,
                                         device=device)
            decoder_tokens = torch.where(corrupt, random_bytes, decoder_tokens)
        logits, traces = self.teacher_logits(state, decoder_tokens)
        target = tokens[:, 1:]
        language = F.cross_entropy(
            logits.reshape(-1, Utf8Codec.SIZE), target.reshape(-1), ignore_index=Utf8Codec.PAD
        )
        mask = target.ne(Utf8Codec.PAD).unsqueeze(-1)
        pooled = (traces * mask).sum(dim=1) / mask.sum(dim=1).clamp_min(1)
        reconstructed = self.grounding_projection(pooled)
        grounding = 1.0 - F.cosine_similarity(reconstructed, state, dim=-1).mean()
        total = language + self.config.grounding_weight * grounding
        return {"loss": total, "language": language, "grounding": grounding}

    @torch.no_grad()
    def generate(
        self,
        state: torch.Tensor,
        max_bytes: Optional[int] = None,
        temperature: Optional[float] = None,
        greedy: bool = False,
    ) -> Tuple[List[str], List[float]]:
        context, hidden = self._initial(state)
        batch = context.shape[0]
        token = torch.full((batch,), Utf8Codec.BOS, dtype=torch.long, device=context.device)
        sequences: List[List[int]] = [[] for _ in range(batch)]
        confidence = torch.zeros(batch, device=context.device)
        alive = torch.ones(batch, dtype=torch.bool, device=context.device)
        limit = max_bytes or self.config.max_bytes
        temp = max(float(temperature or self.config.temperature), 1e-4)
        for _ in range(limit):
            logits, hidden, _ = self._step(token, context, hidden)
            # Recursive decoders can lock into locally probable byte cycles.
            # Block any next byte that would repeat a previously emitted 4-gram.
            for row, seq in enumerate(sequences):
                if len(seq) < 4:
                    continue
                prefix = tuple(seq[-3:])
                blocked = {seq[i + 3] for i in range(len(seq) - 3)
                           if tuple(seq[i:i + 3]) == prefix}
                if blocked:
                    logits[row, list(blocked)] = -torch.inf
            probs = torch.softmax(logits / temp, dim=-1)
            next_token = probs.argmax(-1) if greedy else torch.multinomial(probs, 1).squeeze(1)
            confidence += probs.gather(1, next_token[:, None]).squeeze(1) * alive
            for row, value in enumerate(next_token.tolist()):
                if alive[row]:
                    sequences[row].append(value)
            alive &= next_token.ne(Utf8Codec.EOS)
            token = next_token
            if not alive.any():
                break
        texts = [Utf8Codec.decode(ids) for ids in sequences]
        scores = [float(confidence[i] / max(1, len(sequences[i]))) for i in range(batch)]
        return texts, scores

    def note_training(self, examples: int, loss: Optional[float] = None) -> None:
        self.training_steps.add_(1.0)
        self.examples_seen.add_(float(examples))
        if loss is not None:
            self.last_training_loss.fill_(float(loss))

