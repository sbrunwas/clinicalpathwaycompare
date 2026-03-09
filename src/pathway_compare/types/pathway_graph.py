"""Graph type representing extracted pathway structure."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PathwayGraph:
    """Minimal graph container for nodes, edges, and metadata."""

    graph_id: str
    nodes: list[dict[str, Any]] = field(default_factory=list)
    edges: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
