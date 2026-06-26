# Methods Plan

## Biological Aim

Identify rice genes and alternative-splicing events associated with heat stress, recovery, and possible temperature memory.

## Data Design

Potential sample groups:

- Control plants under normal temperature.
- Acute heat-stress plants.
- Recovery plants after heat exposure.
- Primed plants exposed to an earlier mild heat event and later challenged.
- Heat-tolerant and heat-sensitive rice cultivars, if available.

## Computational Workflow

1. Quality control of RNA-seq reads.
2. Read alignment or quasi-mapping to the rice reference transcriptome.
3. Gene-level differential expression analysis.
4. Isoform and alternative-splicing analysis.
5. Functional annotation of heat-responsive candidates.
6. Candidate ranking with transparent feature scores.
7. Biological interpretation and validation planning.

## Candidate Features

- Heat-response expression strength.
- Alternative-splicing delta between control and heat.
- Persistence during recovery or primed response.
- Known stress pathway relevance.
- Breeding or crop-improvement relevance.
- Feasibility for validation.

## Possible Tools

- FastQC or MultiQC for quality control.
- STAR, HISAT2, Salmon, or kallisto for alignment or quantification.
- DESeq2 or edgeR for differential expression.
- rMATS, SUPPA2, or MAJIQ for splicing analysis.
- R, Python, and Bioconductor for analysis and visualization.

## Expected Outputs

- Ranked list of candidate genes.
- Heat-response expression plots.
- Alternative-splicing event summary.
- Candidate validation plan.
- A short biological interpretation for each candidate.

## Validation Ideas

- qRT-PCR for selected heat-responsive genes.
- RT-PCR for selected isoform changes.
- Compare tolerant and sensitive cultivars.
- Review CRISPR or overexpression feasibility for top candidates.
