"""OpenCV-based straight line detection for pathway connectors."""

from __future__ import annotations

import math

import cv2
import numpy as np

from pathway_object_parser.models import LineObject


def detect_lines(image: np.ndarray) -> list[LineObject]:
    """
    Detect straight line segments using Canny edges and HoughLinesP.

    Parameters
    ----------
    image : np.ndarray
        Input BGR image.

    Returns
    -------
    list[LineObject]
        Straight line segments with endpoint pairs.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 180)

    hough_lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=80,
        minLineLength=40,
        maxLineGap=10,
    )

    height, width = gray.shape[:2]
    max_len = float(math.hypot(width, height))

    lines: list[LineObject] = []
    if hough_lines is None:
        return lines

    for idx, line in enumerate(hough_lines, start=1):
        x1, y1, x2, y2 = [int(v) for v in line[0]]
        length = math.hypot(x2 - x1, y2 - y1)
        confidence = max(0.5, min(0.99, length / max_len + 0.45))

        lines.append(
            LineObject(
                id=f"l{idx}",
                points=[[x1, y1], [x2, y2]],
                confidence=float(confidence),
            )
        )

    return lines
