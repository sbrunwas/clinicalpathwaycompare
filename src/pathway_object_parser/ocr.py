"""OCR helpers for extracting text blocks from pathway images."""

from __future__ import annotations

from pathlib import Path

from paddleocr import PaddleOCR

from pathway_object_parser.models import TextBlock


_OCR_ENGINE: PaddleOCR | None = None


def get_ocr_engine() -> PaddleOCR:
    """Create or return a shared PaddleOCR engine instance."""
    global _OCR_ENGINE
    if _OCR_ENGINE is None:
        _OCR_ENGINE = PaddleOCR(
            lang="en",
            ocr_version="PP-OCRv5",
            text_detection_model_name="PP-OCRv5_mobile_det",
            text_recognition_model_name="en_PP-OCRv5_mobile_rec",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            text_det_limit_side_len=2000,
        )
    return _OCR_ENGINE


def _quad_to_bbox(points: list[list[float]]) -> list[int]:
    """Convert a quadrilateral point list into [x_min, y_min, x_max, y_max]."""
    xs = [int(round(p[0])) for p in points]
    ys = [int(round(p[1])) for p in points]
    return [min(xs), min(ys), max(xs), max(ys)]


def extract_text_blocks(image_path: str) -> list[TextBlock]:
    """
    Run OCR on an image and return text detections.

    Parameters
    ----------
    image_path : str
        Path to a PNG/JPG pathway image.

    Returns
    -------
    list[TextBlock]
        OCR detections with normalized bounding boxes.
    """
    image_file = Path(image_path)
    engine = get_ocr_engine()
    results = engine.ocr(str(image_file))

    text_blocks: list[TextBlock] = []
    if not results:
        return text_blocks

    result = results[0]
    polygons = result.get("dt_polys", [])
    texts = result.get("rec_texts", [])
    scores = result.get("rec_scores", [])

    for block_id, (points, text, confidence) in enumerate(
        zip(polygons, texts, scores), start=1
    ):
        text_value = str(text).strip()
        if not text_value:
            continue

        point_list = points.tolist() if hasattr(points, "tolist") else points
        text_blocks.append(
            TextBlock(
                id=f"t{block_id}",
                text=text_value,
                bbox=_quad_to_bbox(point_list),
                confidence=float(confidence),
            )
        )

    return text_blocks
