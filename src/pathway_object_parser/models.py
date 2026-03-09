"""Pydantic models for object parser outputs."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TextBlock(BaseModel):
    """OCR-detected text block with location and confidence."""

    id: str
    text: str
    bbox: list[int] = Field(description="[x_min, y_min, x_max, y_max]")
    confidence: float


class ShapeObject(BaseModel):
    """Detected geometric shape candidate from contour analysis."""

    id: str
    shape_type: str
    bbox: list[int] = Field(description="[x_min, y_min, x_max, y_max]")
    confidence: float


class LineObject(BaseModel):
    """Detected line segment from Hough transform."""

    id: str
    points: list[list[int]] = Field(description="[[x1, y1], [x2, y2]]")
    confidence: float


class ParsedObjects(BaseModel):
    """Combined object detections for a pathway image."""

    image_path: str
    image_width: int
    image_height: int
    text_blocks: list[TextBlock]
    shapes: list[ShapeObject]
    lines: list[LineObject]
