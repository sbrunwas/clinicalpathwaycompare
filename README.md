# Clinical Pathway Parsing Project

A research-oriented toolkit for converting clinical decision pathways (flowcharts, algorithms, and guideline diagrams) into structured, comparable representations.

## Motivation

Clinical pathways are often published as static PDFs, images, or webpage diagrams, which makes systematic cross-institution comparison difficult. This project aims to transform those artifacts into machine-readable graph data so pathway variation can be analyzed programmatically.

## Pipeline Overview

1. Capture pathway diagrams from webpages or PDFs.
2. Parse visual objects (text blocks, shapes, arrows).
3. Extract a decision-tree/graph structure.
4. Normalize language into structured clinical concepts.
5. Compare pathways across institutions.

## Core Representation

The central intermediate format is a structured JSON graph that preserves provenance and confidence where uncertainty exists.

## Initial Research Test Case

The first target domain is **pediatric emergency asthma pathways** to evaluate variation in escalation logic, timing, thresholds, and disposition criteria.
