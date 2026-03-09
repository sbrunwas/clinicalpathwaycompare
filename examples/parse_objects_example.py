"""Minimal example for running the pathway object parser MVP."""

from pathway_object_parser.object_parser import parse_objects


if __name__ == "__main__":
    parsed = parse_objects(
        image_path="data/processed/images/ucsf_asthma_pathway/ucsf_asthma_pathway_page1.png",
        output_dir="data/processed/object_parser/ucsf_asthma_pathway_page1",
    )
    print(parsed.model_dump())
