// When opened as a local file (file://) talk directly to the dev server.
// When served from the same origin (Docker / Railway) use relative URLs.
const API_BASE = window.location.protocol === "file:" ? "http://localhost:8000" : "";
let allExpanded = false;
let lastPlan = null;
let lastTickets = [];

const SECTIONS = [
  { key: "clarifying_questions",   label: "Clarifying Questions" },
  { key: "assumptions",            label: "Assumptions"          },
  { key: "suggested_mvp_scope",    label: "MVP Scope"            },
  { key: "proposed_architecture",  label: "Architecture"         },
  { key: "data_model_entities",    label: "Data Model"           },
  { key: "api_draft",              label: "API Draft"            },
  { key: "implementation_plan",    label: "Implementation Plan"  },
  { key: "risks_and_dependencies", label: "Risks & Dependencies" },
  { key: "recommended_next_steps", label: "Next Steps"           },
];

// ── API STATUS CHECK ──
async function checkApiStatus() {
  try {
    const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(3000) });
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

  SECTIONS.forEach(({ key, label }) => {
    const items = plan[key];
    if (!items || !items.length) return;

    const section = document.createElement("div");
    section.className = "plan-section";
    section.dataset.key = key;

    const header = document.createElement("div");
    header.className = "plan-section-header";
    header.innerHTML = `
      <div class="plan-section-title">
        <span class="section-label">${label}</span>
        <span class="section-count">${items.length}</span>
      </div>
      <span class="plan-section-arrow">▶</span>
    `;

    const body = document.createElement("div");
    body.className = "plan-section-body";
    body.innerHTML = `<ul>${items.map(item => `<li>${renderText(item)}</li>`).join("")}</ul>`;

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

// ── GENERATE TASKS ──
async function generateTasks() {
  if (!lastPlan) return;

  const btn = document.getElementById("generateTasksBtn");
  btn.disabled = true;
  btn.textContent = "Generating tickets…";

  document.getElementById("taskSpinner").classList.add("visible");
  document.getElementById("taskOutput").classList.remove("visible");

  try {
    const res = await fetch(`${API_BASE}/plan/generate-tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lastPlan),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }

    const data = await res.json();
    lastTickets = data.tickets || [];
    renderTickets(lastTickets);
  } catch (err) {
    showError(err.message);
  } finally {
    document.getElementById("taskSpinner").classList.remove("visible");
    btn.disabled = false;
    btn.textContent = "Generate Tasks from this Plan";
  }
}

function renderTickets(tickets) {
  const container = document.getElementById("ticketList");
  container.innerHTML = "";

  document.getElementById("ticketCount").textContent = `${tickets.length} tickets`;

  // Group by phase
  const phases = {};
  tickets.forEach(t => {
    if (!phases[t.phase]) phases[t.phase] = [];
    phases[t.phase].push(t);
  });

  Object.entries(phases).forEach(([phase, phaseTickets]) => {
    const phaseEl = document.createElement("div");
    phaseEl.className = "phase-header";
    phaseEl.textContent = phase;
    container.appendChild(phaseEl);

    phaseTickets.forEach(ticket => {
      const card = document.createElement("div");
      card.className = "ticket-card";

      const header = document.createElement("div");
      header.className = "ticket-header";
      header.innerHTML = `
        <div class="ticket-header-left">
          <span class="ticket-id">${escapeHtml(ticket.id)}</span>
          <span class="ticket-title">${escapeHtml(ticket.title)}</span>
        </div>
        <div class="ticket-meta">
          <span class="priority-badge priority-${ticket.priority}">${ticket.priority}</span>
          ${ticket.estimate ? `<span class="estimate-badge">${ticket.estimate} SP</span>` : ""}
          <span class="ticket-arrow">▶</span>
        </div>
      `;

      const depsHtml = ticket.dependencies && ticket.dependencies.length
        ? `<div class="ticket-section-label">Dependencies</div>
           <div class="ticket-deps">Requires: ${ticket.dependencies.map(d => escapeHtml(d)).join(", ")}</div>`
        : "";

      const labelsHtml = ticket.labels && ticket.labels.length
        ? `<div class="ticket-section-label">Labels</div>
           <div class="ticket-labels">${ticket.labels.map(l => `<span class="ticket-label">${escapeHtml(l)}</span>`).join("")}</div>`
        : "";

      const body = document.createElement("div");
      body.className = "ticket-body";
      body.innerHTML = `
        <div class="ticket-description">${renderText(ticket.description)}</div>
        <div class="ticket-section-label">Acceptance Criteria</div>
        <ul class="ticket-criteria">
          ${ticket.acceptance_criteria.map(c => `<li>${renderText(c)}</li>`).join("")}
        </ul>
        ${depsHtml}
        ${labelsHtml}
      `;

      header.addEventListener("click", () => {
        header.classList.toggle("open");
        body.classList.toggle("open");
      });

      card.appendChild(header);
      card.appendChild(body);
      container.appendChild(card);
    });
  });

  document.getElementById("taskOutput").classList.add("visible");
  document.getElementById("taskOutput").scrollIntoView({ behavior: "smooth", block: "start" });
}

// ── COPY TICKETS ──
function copyTickets() {
  if (!lastTickets || !lastTickets.length) return;
  const lines = ["# Development Tickets\n"];
  let currentPhase = "";
  lastTickets.forEach(t => {
    if (t.phase !== currentPhase) {
      currentPhase = t.phase;
      lines.push(`\n## ${t.phase}`);
    }
    lines.push(`\n### ${t.id} — ${t.title}`);
    lines.push(`**Priority:** ${t.priority}${t.estimate ? ` | **Estimate:** ${t.estimate} SP` : ""}`);
    lines.push(`\n${t.description}`);
    lines.push(`\n**Acceptance Criteria:**`);
    t.acceptance_criteria.forEach(c => lines.push(`- [ ] ${c}`));
    if (t.labels && t.labels.length) lines.push(`\n**Labels:** ${t.labels.join(", ")}`);
    if (t.dependencies && t.dependencies.length) lines.push(`**Depends on:** ${t.dependencies.join(", ")}`);
  });
  navigator.clipboard.writeText(lines.join("\n")).then(() => showToast("Tickets copied to clipboard"));
}

// ── SAVE TICKETS ──
async function saveTickets() {
  if (!lastPlan || !lastTickets.length) return;
  const btn = document.getElementById("saveTicketsBtn");
  btn.disabled = true;
  btn.textContent = "Saving…";
  try {
    const res = await fetch(`${API_BASE}/history/save`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ plan: lastPlan, tickets: lastTickets }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }
    btn.textContent = "✓ Saved";
    showToast("Saved to history");
    loadHistory();
  } catch (err) {
    btn.disabled = false;
    btn.textContent = "Save";
    showToast("Save failed: " + err.message);
  }
}

// ── HISTORY ──

async function loadHistory() {
  const list = document.getElementById("historyList");
  list.innerHTML = '<div class="history-empty">Loading...</div>';
  try {
    const res = await fetch(`${API_BASE}/history`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const plans = await res.json();
    if (!plans.length) {
      list.innerHTML = '<div class="history-empty">No saved plans yet.</div>';
      return;
    }
    list.innerHTML = "";
    plans.forEach(p => {
      const row = document.createElement("div");
      row.className = "history-row";
      row.innerHTML = `
        <div class="history-row-info">
          <div class="history-row-title">${escapeHtml(p.title)}</div>
          <div class="history-row-date">${new Date(p.created_at).toLocaleString()}</div>
        </div>
        <div class="history-row-actions">
          <button class="btn-sm" data-id="${p.id}" data-action="load">Load</button>
          <button class="btn-sm btn-danger" data-id="${p.id}" data-action="delete">Delete</button>
        </div>
      `;
      row.querySelectorAll("button[data-action]").forEach(btn => {
        btn.addEventListener("click", () => {
          const id = Number(btn.dataset.id);
          if (btn.dataset.action === "load") loadPlan(id);
          else deletePlan(id);
        });
      });
      list.appendChild(row);
    });
  } catch {
    list.innerHTML = '<div class="history-empty">Could not load history.</div>';
  }
}

async function loadPlan(id) {
  try {
    const res = await fetch(`${API_BASE}/history/${id}`);
    if (!res.ok) throw new Error("Not found");
    const data = await res.json();

    lastPlan = data.plan;
    renderPlan(lastPlan);

    if (data.tickets && data.tickets.length) {
      lastTickets = data.tickets;
      renderTickets(lastTickets);
    } else {
      lastTickets = [];
      document.getElementById("taskOutput").classList.remove("visible");
    }

    document.querySelector(".welcome").style.display = "none";
    document.querySelector(".card").style.display = "none";

    showToast("Plan loaded");
  } catch {
    showToast("Failed to load plan");
  }
}

async function deletePlan(id) {
  if (!confirm("Delete this plan? This cannot be undone.")) return;
  try {
    const res = await fetch(`${API_BASE}/history/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Failed");
    showToast("Deleted");
    loadHistory();
  } catch {
    showToast("Delete failed");
  }
}

// ── NEW PLAN ──
function resetForm() {
  document.getElementById("planOutput").classList.remove("visible");
  document.getElementById("taskOutput").classList.remove("visible");
  document.getElementById("requirement").value = "";
  document.getElementById("charCount").textContent = "0 / 4000";
  document.getElementById("directory").value = "";
  document.getElementById("sources").value = "";
  document.getElementById("commands").value = "";
  updateActivePills();
  document.querySelector(".welcome").style.display = "";
  document.querySelector(".card").style.display = "";
  window.scrollTo({ top: 0, behavior: "smooth" });
  lastPlan = null;
  lastTickets = [];
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

function renderText(str) {
  return escapeHtml(str)
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/`(.+?)`/g, "<code>$1</code>");
}

// ── INIT ──
checkApiStatus();
loadHistory();

document.getElementById("requirement").addEventListener("input", function () {
  document.getElementById("charCount").textContent = `${this.value.length} / 4000`;
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
