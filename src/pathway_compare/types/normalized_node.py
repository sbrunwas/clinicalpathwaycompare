"""Normalized node type for canonicalized clinical semantics."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class NormalizedNode:
    """Canonical node representation with provenance and confidence."""

    node_id: str
    raw_text: str
    canonical_label: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    confidence: float | None = None
    provenance: dict[str, Any] = field(default_factory=dict)
