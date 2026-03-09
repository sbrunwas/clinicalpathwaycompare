"""OpenCV contour-based shape detection for pathway diagrams."""

from __future__ import annotations

import cv2
import numpy as np

from pathway_object_parser.models import ShapeObject


def _classify_quad_shape(approx: np.ndarray, contour_area: float, bbox_area: float) -> tuple[str, float]:
    """Classify a 4-point contour as rectangle or diamond with heuristic confidence."""
    extent = contour_area / bbox_area if bbox_area > 0 else 0.0
    # TODO: Replace with orientation + angle-based classification for more robust diamond detection.
    if extent < 0.8:
        shape_type = "diamond"
        confidence = max(0.5, min(0.95, 1.0 - abs(0.6 - extent)))
    else:
        shape_type = "rectangle"
        confidence = max(0.5, min(0.99, extent))
    return shape_type, float(confidence)


def detect_shapes(image: np.ndarray) -> list[ShapeObject]:
    """
    Detect geometric shape candidates from an image.

    Parameters
    ----------
    image : np.ndarray
        Input BGR image.

    Returns
    -------
    list[ShapeObject]
        Rectangle/diamond candidates with bounding boxes.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        21,
        8,
    )

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    shapes: list[ShapeObject] = []
    idx = 1
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 800:
            continue

        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) != 4:
            continue

        x, y, w, h = cv2.boundingRect(approx)
        bbox_area = float(w * h)
        shape_type, confidence = _classify_quad_shape(approx, area, bbox_area)

        shapes.append(
            ShapeObject(
                id=f"s{idx}",
                shape_type=shape_type,
                bbox=[int(x), int(y), int(x + w), int(y + h)],
                confidence=confidence,
            )
        )
        idx += 1

    return shapes
