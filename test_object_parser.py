from pathlib import Path

from pathway_object_parser.object_parser import parse_objects


def resolve_test_image() -> Path:
    """Return the preferred test image path for the object parser debug run."""
    preferred = Path("data/images/ucsf_asthma_pathway_page1.png")
    fallback = Path(
        "data/processed/images/ucsf_asthma_pathway/ucsf_asthma_pathway_page1.png"
    )

    if preferred.exists():
        return preferred
    if fallback.exists():
        return fallback

    raise FileNotFoundError(
        "No test image found. Expected either "
        "'data/images/ucsf_asthma_pathway_page1.png' or "
        "'data/processed/images/ucsf_asthma_pathway/ucsf_asthma_pathway_page1.png'."
    )


def main() -> None:
    image_path = resolve_test_image()
    output_dir = Path("data/outputs/ucsf_asthma")

    result = parse_objects(image_path=str(image_path), output_dir=str(output_dir))

    print("Image:", result.image_path)
    print("Size:", f"{result.image_width} x {result.image_height}")
    print("Text blocks:", len(result.text_blocks))
    print("Shapes:", len(result.shapes))
    print("Lines:", len(result.lines))

    if result.text_blocks:
        print("\nFirst 5 text blocks:")
        for block in result.text_blocks[:5]:
            print(block)

    if result.shapes:
        print("\nFirst 5 shapes:")
        for shape in result.shapes[:5]:
            print(shape)

    if result.lines:
        print("\nFirst 5 lines:")
        for line in result.lines[:5]:
            print(line)

    print("\nSaved outputs to:", output_dir)
    print("Parsed JSON:", output_dir / "parsed_objects.json")
    print("Overlay image:", output_dir / "overlay.png")


if __name__ == "__main__":
    main()
