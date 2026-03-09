"""Detected object type for parsed visual elements in diagrams."""

from dataclasses import dataclass

from pathway_compare.types.bounding_box import BoundingBox


@dataclass
class DetectedObject:
    """Single detected element such as text, shape, or arrow."""

    object_id: str
    object_type: str
    bbox: BoundingBox
    label: str | None = None
    confidence: float | None = None
