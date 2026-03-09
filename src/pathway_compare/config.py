"""Configuration models for pipeline paths and runtime settings."""

from dataclasses import dataclass


@dataclass
class PipelineConfig:
    """Placeholder configuration for pipeline execution."""

    raw_data_dir: str = "data/raw"
    processed_data_dir: str = "data/processed"
    enable_human_review: bool = True
