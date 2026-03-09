"""Main object parsing orchestration for pathway diagram images."""

from __future__ import annotations

from pathlib import Path

import cv2

from pathway_object_parser.detect_lines import detect_lines
from pathway_object_parser.detect_shapes import detect_shapes
from pathway_object_parser.models import ParsedObjects
from pathway_object_parser.ocr import extract_text_blocks
from pathway_object_parser.visualize import draw_overlay


def parse_objects(image_path: str, output_dir: str | None = None) -> ParsedObjects:
    """
    Parse visual objects from a pathway PNG/JPG image.

    Parameters
    ----------
    image_path : str
        Path to pathway image file.
    output_dir : str | None, default=None
        Optional output directory for parsed JSON and overlay image.

    Returns
    -------
    ParsedObjects
        OCR blocks, shape detections, and line detections.
    """
    image_file = Path(image_path)
    if not image_file.exists() or not image_file.is_file():
        raise FileNotFoundError(f"Image file not found: '{image_path}'")

    image = cv2.imread(str(image_file))
    if image is None:
        raise ValueError(f"Unable to read image file: '{image_path}'")

    height, width = image.shape[:2]

    text_blocks = extract_text_blocks(str(image_file))
    shapes = detect_shapes(image)
    lines = detect_lines(image)

    parsed = ParsedObjects(
        image_path=str(image_file),
        image_width=int(width),
        image_height=int(height),
        text_blocks=text_blocks,
        shapes=shapes,
        lines=lines,
    )

    if output_dir is not None:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        json_path = out_dir / "parsed_objects.json"
        json_path.write_text(parsed.model_dump_json(indent=2), encoding="utf-8")

        overlay = draw_overlay(image=image, parsed=parsed)
        overlay_path = out_dir / "overlay.png"
        cv2.imwrite(str(overlay_path), overlay)

    return parsed
