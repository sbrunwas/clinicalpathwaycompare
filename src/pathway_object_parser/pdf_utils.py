"""PDF preprocessing utilities for converting pathway PDFs into PNG pages."""

from __future__ import annotations

import argparse
from pathlib import Path

import fitz


def _prepare_paths(pdf_path: str, output_dir: str) -> tuple[Path, Path]:
    """
    Validate the input PDF and ensure output directory exists.

    Parameters
    ----------
    pdf_path : str
        Path to the input PDF file.
    output_dir : str
        Directory where PNG pages should be written.

    Returns
    -------
    tuple[Path, Path]
        Resolved PDF and output directory paths.

    Raises
    ------
    FileNotFoundError
        If the provided PDF path does not exist or is not a file.
    """
    pdf = Path(pdf_path)
    if not pdf.exists() or not pdf.is_file():
        raise FileNotFoundError(
            f"PDF file not found: '{pdf_path}'. Provide a valid path to an existing PDF."
        )

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    return pdf, out_dir


def pdf_to_png(pdf_path: str, output_dir: str, dpi: int = 300) -> list[str]:
    """
    Render each page of a PDF as a high-resolution PNG image.

    Parameters
    ----------
    pdf_path : str
        Path to an input PDF containing one or more pathway pages.
    output_dir : str
        Directory where rendered PNG files will be saved.
    dpi : int, default=300
        Rendering resolution in dots per inch.

    Returns
    -------
    list[str]
        List of generated PNG file paths, ordered by page number.
    """
    pdf, out_dir = _prepare_paths(pdf_path=pdf_path, output_dir=output_dir)
    scale = dpi / 72.0
    matrix = fitz.Matrix(scale, scale)
    generated_paths: list[str] = []

    with fitz.open(pdf) as doc:
        for page_index, page in enumerate(doc, start=1):
            output_path = out_dir / f"{pdf.stem}_page{page_index}.png"
            pixmap = page.get_pixmap(matrix=matrix, alpha=False)
            pixmap.save(output_path)
            generated_paths.append(str(output_path))

    return generated_paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF pages to PNG images.")
    parser.add_argument("pdf_path", help="Path to input PDF file.")
    parser.add_argument("output_dir", help="Directory for output PNG files.")
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Render DPI (default: 300).",
    )
    args = parser.parse_args()

    output_files = pdf_to_png(args.pdf_path, args.output_dir, dpi=args.dpi)
    print(output_files)
