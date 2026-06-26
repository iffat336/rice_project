# How To Explain RiceHeat-AS AI (Simple Version)

Read this once, out loud, and you'll be able to explain the project without sounding like you're
reading code documentation. Everything is written the way you'd actually *say* it in the interview.

---

## The 1-Minute Summary (memorize this)

> "I built a small prototype called RiceHeat-AS AI. It's inspired by Prof. Calixto's rice
> heat-stress project. Since I couldn't run a real lab experiment before today, I built a
> demonstration dataset and a dashboard that shows how I'd analyze rice genes under heat stress —
> looking at which genes turn on, which genes change how they're spliced, and using a simple
> machine-learning model to help rank the most important candidate genes. It's not real lab data —
> it's a working demo of my thinking process."

That's it. If you only remember one paragraph, remember that one.

---

## The Story In 5 Simple Beats

**1. The problem.** Rice doesn't grow well in extreme heat. Some rice plants survive heat better
than others. Scientists want to know *which genes* make the difference, so they can breed
heat-tolerant rice.

**2. The data (fake, but realistic).** I couldn't grow real rice or run real RNA sequencing before
today, so I built a small fake dataset that *behaves* like real data would: some genes go up under
heat, some genes change which "version" of themselves gets used (that's called splicing), and the
heat-tolerant rice variety responds more strongly than the sensitive one.

**3. The analysis.** I compare "before heat" vs "after heat" for every gene, and check two things:
   - Did the gene's activity level change? (expression)
   - Did the gene's spliced transcript form change? (splicing)

**4. The AI part.** I trained a simple machine-learning model (a "Random Forest") to see if it can
tell apart heat-stressed samples from normal ones just by looking at gene activity. If it can, the
genes it relies on most are probably important — so I use that as one more clue, not as proof.

**5. The output.** Everything gets combined into one ranked list: "these are the genes most worth
testing further in the lab." Then I connect that list to breeding — which type of gene is useful
for which kind of crop improvement.

---

## Walking Through The Dashboard (page by page, simple words)

Say this while you click through the sidebar, in order:

1. **Project Overview** — "This page just states the question I'm trying to answer: can we use
   gene activity and splicing data to find candidate genes for heat tolerance in rice?"

2. **Dataset Explorer** — "Here's my demo dataset — 16 fake rice samples, 12 genes, under control
   and heat conditions, across two rice types: heat-tolerant and heat-sensitive."

3. **Gene Expression** — "This page shows which genes turn on the most under heat. The bar charts
   show the strongest reactions, and the chart on the bottom is a heatmap — darker means higher
   activity."

4. **Alternative Splicing** — "This is the part that connects directly to Prof. Calixto's work.
   Some genes don't just turn on more — they also start using a different spliced version of
   themselves under heat. I measure that with something called PSI, which just means 'how often is
   this version used.' A big jump in PSI means the gene's RNA processing changed."

5. **Machine Learning** — "Here I trained a basic AI model to see if gene activity alone can tell
   the difference between a heat-stressed sample and a normal one. It's not trying to prove
   biology — it's a tool to help me see which genes carry the strongest signal."

6. **Candidate Ranking** — "This page combines everything — expression change, statistics,
   splicing change, and the AI's opinion — into one final score per gene. You can even move the
   sliders to change how much weight each factor gets, and watch the ranking update."

7. **Breeding Report** — "This is where I connect the molecular result back to my actual
   background — plant breeding. I sort the top genes into categories like 'direct stress
   protection' or 'possible heat-memory control,' and there's a button to download the whole report."

8. **Interview & Validation** — "This last page is honestly for me — it has background on Prof.
   Calixto's lab, and a reminder of what should happen *after* this dashboard: real lab validation
   like qPCR or CRISPR. The AI only suggests candidates; it doesn't prove anything biologically."

---

## If She Asks... (quick answers)

**"Is this real data?"**
> "No — it's a synthetic demo dataset I built to show the workflow. I was upfront about that on
> every page. Real data would come from RNA sequencing of actual heat-stressed rice."

**"Why machine learning, isn't this a biology project?"**
> "I'm using ML only as a prioritization tool — to help narrow down hundreds of possible genes into
> a short, testable list. It doesn't replace lab validation; it just helps decide where to look
> first."

**"What's PSI / alternative splicing, in one sentence?"**
> "It's how often a particular spliced version of a gene's RNA gets used. If that ratio shifts a
> lot under heat, the gene is being regulated after transcription, not just before it."

**"What would you do next if this were real?"**
> "Replace the demo data with real or public RNA-seq data, validate the top candidates with qPCR,
> and eventually test the strongest ones with CRISPR or overexpression."

**"How did you build this so fast?"**
> "I used Streamlit for the dashboard, pandas for data handling, scikit-learn for the machine
> learning, and Plotly for the charts. It's deployed live on Streamlit Cloud and the code is on
> GitHub."

---

## Tiny Glossary (so nothing sounds unfamiliar if she repeats a word back to you)

| Term | Plain meaning |
| --- | --- |
| Expression | How "on" or "off" a gene is — how much of its RNA is being made |
| Log2 fold change | A number showing how many times expression doubled (or halved) |
| p-value | How confident we are the change isn't just random noise |
| Alternative splicing | A gene making more than one version of its final RNA message |
| PSI | "Percent Spliced In" — how often one particular version is used |
| Random Forest | A machine-learning model made of many simple decision trees voting together |
| Feature importance | Which genes the AI model relied on most to make its prediction |
| Candidate gene | A gene worth testing further — not a confirmed result |
| Tolerant / Sensitive cultivar | The heat-resistant vs. heat-vulnerable rice variety in the demo |

---

## Where Everything Lives (if she wants to see the code)

- Live demo: `https://riceproject-uhenhtxlxaqdcrfmwapizi.streamlit.app/`
- Code on GitHub: `https://github.com/iffat336/rice_project`
- Full pitch script and smart questions to ask her: [`interview_script.md`](interview_script.md)
- Full technical README (if she wants details): [`../README.md`](../README.md)

You don't need to memorize the engineering. You need to be able to say, calmly: *"Here's the
question, here's how I approached it, here's what the dashboard shows, and here's what I'd do next
with real data."* That's the whole interview.
