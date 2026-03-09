"""Debug overlay rendering for OCR, shape, and line detections."""

from __future__ import annotations

import cv2
import numpy as np

from pathway_object_parser.models import ParsedObjects


def draw_overlay(image: np.ndarray, parsed: ParsedObjects) -> np.ndarray:
    """
    Draw a debug overlay for detected text blocks, shapes, and lines.

    Parameters
    ----------
    image : np.ndarray
        Input BGR image copy.
    parsed : ParsedObjects
        Parsed detection results.

    Returns
    -------
    np.ndarray
        Overlay image with detections drawn.
    """
    overlay = image.copy()

    for block in parsed.text_blocks:
        x1, y1, x2, y2 = block.bbox
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 180, 255), 2)
        cv2.putText(
            overlay,
            block.id,
            (x1, max(20, y1 - 6)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 180, 255),
            1,
            cv2.LINE_AA,
        )

    for shape in parsed.shapes:
        x1, y1, x2, y2 = shape.bbox
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (60, 220, 60), 2)
        cv2.putText(
            overlay,
            f"{shape.id}:{shape.shape_type}",
            (x1, max(20, y2 - 4)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (60, 220, 60),
            1,
            cv2.LINE_AA,
        )

    for line in parsed.lines:
        (x1, y1), (x2, y2) = line.points
        cv2.line(overlay, (x1, y1), (x2, y2), (255, 120, 50), 2)
        mx = (x1 + x2) // 2
        my = (y1 + y2) // 2
        cv2.putText(
            overlay,
            line.id,
            (mx, my),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 120, 50),
            1,
            cv2.LINE_AA,
        )

    return overlay
