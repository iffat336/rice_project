# Interview Script

## 45-Second Explanation

I prepared a small project concept called RiceHeat-AS AI. The idea is to study how rice responds to heat stress by integrating gene-expression data, alternative-splicing (PSI) changes, and machine-learning feature ranking. My goal would be to rank candidate genes or splicing events that may contribute to thermotolerance, then use those candidates for biological validation through qPCR, cultivar comparison, or further experimental design.

This connects with my background in plant breeding and genetics because I am interested in stress-resilient crop improvement. My AI and data skills can support the computational part: differential expression analysis, splicing-shift detection, candidate prioritization, and clear biological interpretation.

## Longer Explanation

The project starts from a practical climate-resilience problem: heat stress reduces rice productivity, and molecular mechanisms such as gene regulation and alternative splicing may help explain why some plants tolerate heat better than others.

The dashboard walks through this in stages: a Dataset Explorer for the demo samples and genes, a Gene Expression page comparing control and heat conditions with log2 fold change and a volcano plot, an Alternative Splicing page showing PSI shifts, a Machine Learning page that trains a Random Forest classifier and ranks feature importance, a Candidate Ranking page that combines all of those signals into one weight-adjustable score, and a Breeding Report page that translates the top candidates into breeding-relevant interpretation with a downloadable report.

I see this as a bridge between plant molecular biology and crop improvement. It respects the biological question first, and uses AI as a tool to organize complex transcriptomic evidence.

## Questions To Ask Prof. Calixto

1. Would your group prefer that a new PhD student begins with public RNA-seq reanalysis, lab-generated samples, or a combination of both?
2. In your current rice heat-stress work, which layer is most important: gene expression, alternative splicing, temperature memory, or validation of specific candidates?
3. Which computational skills should I strengthen first for your lab: R/Bioconductor, RNA-seq alignment and quantification, differential splicing analysis, or statistical modeling?
4. Are there rice cultivars or heat-stress contrasts already available in the lab that could be used for a first project?
5. Could machine learning be useful for ranking candidate genes before experimental validation?

## What To Avoid Saying

- Do not say the AI model proves gene function.
- Do not present the synthetic data as real results.
- Do not make the project sound only like software.
- Do not over-focus on general AI agents; keep the focus on transcriptomics and plant stress biology.
