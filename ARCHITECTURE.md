# Architecture

This repository is organized as a modular, research-first pipeline for pathway parsing and comparison. The focus is on inspectable intermediate outputs, reproducible analysis, and support for human-in-the-loop review.

## End-to-End Flow

```text
Webpage / PDF
      ↓
Screenshots
      ↓
Detected Objects
      ↓
Spatial Graph
      ↓
Normalized Graph
      ↓
Cross-Institution Comparison
```

Intermediate outputs should be saved at each stage to support debugging, adjudication, and incremental method improvement.

## 1) Capture

### Inputs
- Webpage URLs, PDF files, or local diagram assets.

### Outputs
- Screenshot/image assets.
- Capture manifest with source metadata and provenance.

### Core Challenges
- Variable rendering quality and layout.
- Multi-page PDF handling.
- Preserving source traceability.

### Expected JSON Structure
```json
{
  "source_id": "example_asthma_pathway",
  "source_type": "pdf",
  "pages": [
    {
      "page_index": 0,
      "image_path": "data/raw/example/page_0.png",
      "width": 2480,
      "height": 3508
    }
  ],
  "captured_at": "2026-03-08T00:00:00Z"
}
```

## 2) Object Parser

### Inputs
- Captured pathway images.
- Capture manifest metadata.

### Outputs
- Detected objects: text blocks, shapes, arrows, connectors.
- Object-level confidence and spatial coordinates.

### Core Challenges
- Dense diagrams and overlapping elements.
- Arrow direction ambiguity.
- OCR noise and fragmented text boxes.

### Expected JSON Structure
```json
{
  "image_id": "page_0",
  "objects": [
    {
      "object_id": "obj_001",
      "object_type": "shape",
      "label": "Decision",
      "bbox": {"x": 100, "y": 120, "width": 240, "height": 90},
      "confidence": 0.81
    }
  ]
}
```

## 3) Tree Extractor

### Inputs
- Detected objects with geometry and labels.

### Outputs
- Spatial/structural pathway graph (nodes + directed edges).
- Inferred node types and edge semantics.

### Core Challenges
- Reconstructing directionality from visual cues.
- Distinguishing flow edges from decorative lines.
- Handling loops, cross-links, and split/merge ambiguity.

### Expected JSON Structure
```json
{
  "graph_id": "pathway_graph_page_0",
  "nodes": [
    {"node_id": "n1", "node_type": "decision", "text": "Severe distress?"}
  ],
  "edges": [
    {"source": "n1", "target": "n2", "condition": "yes", "confidence": 0.74}
  ]
}
```

## 4) Language Normalizer

### Inputs
- Spatial pathway graph with raw node text.

### Outputs
- Normalized nodes (canonical concepts, thresholds, actions).
- Mapping metadata and uncertainty/provenance details.

### Core Challenges
- Institution-specific terminology.
- Implicit thresholds and temporal language.
- Clinical synonym resolution.

### Expected JSON Structure
```json
{
  "graph_id": "pathway_graph_page_0",
  "normalized_nodes": [
    {
      "node_id": "n1",
      "raw_text": "Give albuterol q20min x3",
      "canonical_action": "short_acting_beta_agonist",
      "attributes": {"frequency": "q20min", "repeat": 3},
      "confidence": 0.67,
      "provenance": {"method": "rule_plus_llm"}
    }
  ]
}
```

## 5) Pathway Comparison

### Inputs
- Two or more normalized pathway graphs from distinct institutions.

### Outputs
- Structured diffs for node concepts, thresholds, branch criteria, and flow patterns.
- Research summary suitable for manuscript tables/figures.

### Core Challenges
- Alignment of semantically similar but differently structured graphs.
- Quantifying meaningful variation vs extraction artifacts.
- Presenting uncertainty transparently.

### Expected JSON Structure
```json
{
  "comparison_id": "inst_a_vs_inst_b",
  "graph_pair": ["inst_a_graph", "inst_b_graph"],
  "differences": {
    "concept_diffs": [],
    "threshold_diffs": [],
    "topology_diffs": []
  },
  "summary": "Placeholder comparison summary",
  "confidence_notes": []
}
```

## Design Philosophy

- Modular pipeline design: each stage is independently testable and replaceable.
- Inspectable intermediate outputs: each transformation should emit JSON artifacts for review.
- Human-in-the-loop review: uncertain extractions should be preserved for manual adjudication.
- Research-first focus: prioritize transparent methodology and reproducibility over UI complexity.
