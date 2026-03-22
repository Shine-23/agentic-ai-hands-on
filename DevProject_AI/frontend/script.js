const API_BASE = "http://localhost:8000";
let allExpanded = false;
let lastPlan = null;

const SECTIONS = [
  { key: "clarifying_questions",   label: "Clarifying Questions", emoji: "❓" },
  { key: "assumptions",            label: "Assumptions",          emoji: "💡" },
  { key: "suggested_mvp_scope",    label: "MVP Scope",            emoji: "🎯" },
  { key: "proposed_architecture",  label: "Architecture",         emoji: "🏗️" },
  { key: "data_model_entities",    label: "Data Model",           emoji: "🗄️" },
  { key: "api_draft",              label: "API Draft",            emoji: "🔌" },
  { key: "implementation_plan",    label: "Implementation Plan",  emoji: "📋" },
  { key: "risks_and_dependencies", label: "Risks & Dependencies", emoji: "⚠️" },
  { key: "recommended_next_steps", label: "Next Steps",           emoji: "➡️" },
];

// ── API STATUS CHECK ──
async function checkApiStatus() {
  try {
    const res = await fetch(`${API_BASE}/`, { signal: AbortSignal.timeout(3000) });
    if (res.ok) {
      document.getElementById("statusDot").className = "status-dot online";
      document.getElementById("statusText").textContent = "API online";
    } else { throw new Error(); }
  } catch {
    document.getElementById("statusDot").className = "status-dot offline";
    document.getElementById("statusText").textContent = "API offline";
  }
}

// ── ACTIVE PILLS ──
function updateActivePills() {
  const pills = document.getElementById("activePills");
  pills.innerHTML = "";
  if (document.getElementById("directory").value.trim()) addPill(pills, "Repo");
  if (document.getElementById("sources").value.trim())   addPill(pills, "Docs");
  if (document.getElementById("commands").value.trim())  addPill(pills, "Shell");
}

function addPill(container, label) {
  const p = document.createElement("span");
  p.className = "tool-pill";
  p.textContent = label;
  container.appendChild(p);
}

// ── GENERATE PLAN ──
async function generatePlan() {
  const requirement  = document.getElementById("requirement").value.trim();
  const directory    = document.getElementById("directory").value.trim() || null;
  const sourcesRaw   = document.getElementById("sources").value.trim();
  const commandsRaw  = document.getElementById("commands").value.trim();
  const sources  = sourcesRaw  ? sourcesRaw.split(",").map(s => s.trim()).filter(Boolean)  : null;
  const commands = commandsRaw ? commandsRaw.split(",").map(s => s.trim()).filter(Boolean) : null;

  setLoading(true);
  clearOutput();

  const hints = ["Analysing requirement...", "Gathering context...", "Consulting Claude...", "Structuring plan..."];
  let hintIdx = 0;
  const hintTimer = setInterval(() => {
    document.getElementById("spinnerSub").textContent = hints[hintIdx % hints.length];
    hintIdx++;
  }, 2500);

  try {
    const body = { requirement };
    if (directory) body.directory = directory;
    if (sources  && sources.length)  body.sources  = sources;
    if (commands && commands.length) body.commands = commands;

    const res = await fetch(`${API_BASE}/plan/generate-with-context`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }

    lastPlan = await res.json();
    renderPlan(lastPlan);
  } catch (err) {
    showError(err.message);
  } finally {
    clearInterval(hintTimer);
    setLoading(false);
  }
}

// ── RENDER PLAN ──
function renderPlan(plan) {
  document.getElementById("summaryBox").textContent = plan.requirement_summary || "";

  const container = document.getElementById("planSections");
  container.innerHTML = "";

  SECTIONS.forEach(({ key, label, emoji }) => {
    const items = plan[key];
    if (!items || !items.length) return;

    const section = document.createElement("div");
    section.className = "plan-section";
    section.dataset.key = key;

    const header = document.createElement("div");
    header.className = "plan-section-header";
    header.innerHTML = `
      <div class="plan-section-title">
        <span class="section-emoji">${emoji}</span>
        <span class="section-label">${label}</span>
        <span class="section-count">${items.length}</span>
      </div>
      <span class="plan-section-arrow">▶</span>
    `;

    const body = document.createElement("div");
    body.className = "plan-section-body";
    body.innerHTML = `<ul>${items.map(item => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;

    header.addEventListener("click", () => {
      header.classList.toggle("open");
      body.classList.toggle("open");
    });

    if (key === "suggested_mvp_scope" || key === "implementation_plan") {
      header.classList.add("open");
      body.classList.add("open");
    }

    section.appendChild(header);
    section.appendChild(body);
    container.appendChild(section);
  });

  document.getElementById("planOutput").classList.add("visible");
  document.getElementById("planOutput").scrollIntoView({ behavior: "smooth", block: "start" });
}

// ── EXPAND / COLLAPSE ALL ──
function toggleAll() {
  allExpanded = !allExpanded;
  document.querySelectorAll(".plan-section-header").forEach(h => h.classList.toggle("open", allExpanded));
  document.querySelectorAll(".plan-section-body").forEach(b => b.classList.toggle("open", allExpanded));
  const btn = document.getElementById("expandAllBtn");
  btn.textContent = allExpanded ? "⊟ Collapse All" : "⊞ Expand All";
  btn.classList.toggle("active", allExpanded);
}

// ── COPY PLAN ──
function copyPlan() {
  if (!lastPlan) return;
  const lines = [`# Engineering Plan\n\n${lastPlan.requirement_summary}\n`];
  SECTIONS.forEach(({ key, label }) => {
    const items = lastPlan[key];
    if (items && items.length) {
      lines.push(`\n## ${label}`);
      items.forEach(item => lines.push(`- ${item}`));
    }
  });
  navigator.clipboard.writeText(lines.join("\n")).then(() => showToast("Copied to clipboard"));
}

// ── NEW PLAN ──
function resetForm() {
  document.getElementById("planOutput").classList.remove("visible");
  document.getElementById("requirement").value = "";
  document.getElementById("charCount").textContent = "0 chars";
  window.scrollTo({ top: 0, behavior: "smooth" });
  lastPlan = null;
  allExpanded = false;
}

// ── HELPERS ──
function setLoading(on) {
  document.getElementById("spinner").classList.toggle("visible", on);
  document.getElementById("submitBtn").disabled = on;
  document.getElementById("submitBtn").textContent = on ? "Generating…" : "Generate Engineering Plan";
}

function clearOutput() {
  document.getElementById("errorBox").style.display = "none";
  document.getElementById("planOutput").classList.remove("visible");
  document.getElementById("planSections").innerHTML = "";
  document.getElementById("summaryBox").textContent = "";
}

function showError(msg) {
  const box = document.getElementById("errorBox");
  document.getElementById("errorText").textContent = msg;
  box.style.display = "flex";
}

function showToast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2200);
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// ── INIT ──
checkApiStatus();

document.getElementById("requirement").addEventListener("input", function () {
  document.getElementById("charCount").textContent = this.value.length + " chars";
  updateActivePills();
});

["directory", "sources", "commands"].forEach(id => {
  document.getElementById(id).addEventListener("input", updateActivePills);
});

document.getElementById("contextToggle").addEventListener("click", () => {
  document.getElementById("contextToggle").classList.toggle("open");
  document.getElementById("contextPanel").classList.toggle("open");
});

document.getElementById("planForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  await generatePlan();
});
