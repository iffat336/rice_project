const candidates = [
  { gene: "OsHSP70", expression: 96, splicing: 48, memory: 82, breeding: 74, note: "Strong heat-response signal and recovery stability." },
  { gene: "OsHSFA2d", expression: 88, splicing: 42, memory: 76, breeding: 66, note: "Heat-shock transcriptional regulator candidate." },
  { gene: "OsDREB2A", expression: 78, splicing: 32, memory: 64, breeding: 88, note: "Stress-response regulator with breeding relevance." },
  { gene: "OsSR45", expression: 42, splicing: 96, memory: 70, breeding: 54, note: "Splicing regulator candidate for isoform-level heat response." },
  { gene: "OsJMJ703", expression: 34, splicing: 57, memory: 94, breeding: 49, note: "Epigenetic candidate for temperature-memory follow-up." },
  { gene: "OsAPX2", expression: 62, splicing: 26, memory: 58, breeding: 82, note: "Oxidative-stress protection signal under heat stress." },
  { gene: "OsPIF4-like", expression: 54, splicing: 49, memory: 88, breeding: 69, note: "Temperature-response and memory-linked candidate." },
];

const weights = {
  balanced: { expression: 0.34, splicing: 0.26, memory: 0.22, breeding: 0.18 },
  splicing: { expression: 0.18, splicing: 0.52, memory: 0.18, breeding: 0.12 },
  memory: { expression: 0.22, splicing: 0.2, memory: 0.46, breeding: 0.12 },
  breeding: { expression: 0.26, splicing: 0.14, memory: 0.18, breeding: 0.42 },
};

const heatLabels = {
  1: "Mild heat, short pulse",
  2: "Moderate heat, 1 hour",
  3: "Severe heat, 2 hours",
  4: "Recovery after heat",
  5: "Primed heat-memory response",
};

function score(candidate, heatLevel, focus) {
  const w = weights[focus] || weights.balanced;
  const heatFactor = Number(heatLevel) / 5;
  return Math.min(
    99,
    Math.round(
      candidate.expression * w.expression * (0.88 + heatFactor * 0.24) +
        candidate.splicing * w.splicing +
        candidate.memory * w.memory +
        candidate.breeding * w.breeding
    )
  );
}

function render() {
  const heatLevel = document.getElementById("heatLevel").value;
  const focus = document.getElementById("focus").value;
  const chart = document.getElementById("chart");
  const heatLabel = document.getElementById("heatLabel");
  const topGene = document.getElementById("topGene");
  const topNote = document.getElementById("topNote");

  const ranked = candidates
    .map((candidate) => ({ ...candidate, score: score(candidate, heatLevel, focus) }))
    .sort((a, b) => b.score - a.score);

  heatLabel.textContent = heatLabels[heatLevel];
  topGene.textContent = ranked[0].gene;
  topNote.textContent = ranked[0].note;
  chart.innerHTML = "";

  ranked.forEach((candidate) => {
    const row = document.createElement("div");
    row.className = "row";
    row.innerHTML = `
      <strong>${candidate.gene}</strong>
      <div class="bar"><span style="--width:${candidate.score}%"></span></div>
      <em>${candidate.score}</em>
    `;
    chart.appendChild(row);
  });
}

document.getElementById("heatLevel").addEventListener("input", render);
document.getElementById("focus").addEventListener("change", render);
render();
