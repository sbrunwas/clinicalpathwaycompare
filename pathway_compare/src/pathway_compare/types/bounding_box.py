"""Bounding box type for spatial coordinates in pathway images."""

from dataclasses import dataclass


@dataclass
class BoundingBox:
    """Axis-aligned bounding box in image pixel coordinates."""

    x: float
    y: float
    width: float
    height: float
