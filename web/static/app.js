/**
 * Hiver AI Copilot - Frontend Application Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  // Application State
  let tickets = [];
  let currentTicketId = null;
  let currentTicketDetail = null;
  let selectedCategory = "all";
  let latestBenchmarkData = null;

  // DOM Elements
  const ticketListEl = document.getElementById("ticket-list");
  const ticketSearchInput = document.getElementById("ticket-search");
  const categoryChips = document.getElementById("category-chips");
  const replyEditor = document.getElementById("reply-editor");
  const replyWordCount = document.getElementById("reply-word-count");
  const providerSelect = document.getElementById("provider-select");
  const customInstructionInput = document.getElementById("custom-instruction");
  const btnGenerateReply = document.getElementById("btn-generate-reply");
  const btnEvaluateReply = document.getElementById("btn-evaluate-reply");

  // Thread DOM Elements
  const thTicketId = document.getElementById("th-ticket-id");
  const thCategory = document.getElementById("th-category");
  const thTier = document.getElementById("th-tier");
  const thSentiment = document.getElementById("th-sentiment");
  const thPriority = document.getElementById("th-priority");
  const thSubject = document.getElementById("th-subject");
  const thAccountId = document.getElementById("th-account-id");
  const thMrr = document.getElementById("th-mrr");
  const thCustomerName = document.getElementById("th-customer-name");
  const thCustomerEmail = document.getElementById("th-customer-email");
  const threadMessagesEl = document.getElementById("thread-messages");
  const ragDrawerContent = document.getElementById("rag-drawer-content");
  const gtText = document.getElementById("gt-text");

  // Accordion Toggles
  const ragDrawerToggle = document.getElementById("rag-drawer-toggle");
  const gtDrawerToggle = document.getElementById("gt-drawer-toggle");
  const ragDrawer = document.getElementById("rag-drawer");
  const gtDrawer = document.getElementById("ground-truth-drawer");

  // Scorecard Elements
  const gaugeHeqiVal = document.getElementById("gauge-heqi-val");
  const heqiGrade = document.getElementById("heqi-grade");
  const confidenceLabel = document.getElementById("confidence-label");
  const confidenceDesc = document.getElementById("confidence-desc");
  const scorePolicy = document.getElementById("score-policy");
  const barPolicy = document.getElementById("bar-policy");
  const scoreIntent = document.getElementById("score-intent");
  const barIntent = document.getElementById("bar-intent");
  const scoreTone = document.getElementById("score-tone");
  const barTone = document.getElementById("bar-tone");
  const scoreAction = document.getElementById("score-action");
  const barAction = document.getElementById("bar-action");
  const scoreSemantic = document.getElementById("score-semantic");
  const barSemantic = document.getElementById("bar-semantic");
  const lexRougel = document.getElementById("lex-rougel");
  const lexBleu = document.getElementById("lex-bleu");
  const feedbackStrengths = document.getElementById("feedback-strengths");
  const feedbackImprovements = document.getElementById("feedback-improvements");

  // Modals
  const benchmarkModal = document.getElementById("benchmark-modal");
  const btnOpenBenchmark = document.getElementById("btn-open-benchmark");
  const btnCloseBenchmark = document.getElementById("btn-close-benchmark");
  const btnStartBenchmark = document.getElementById("btn-start-benchmark");
  const benchProviderSelect = document.getElementById("bench-provider-select");
  const btnDownloadJson = document.getElementById("btn-download-json");
  const btnDownloadMd = document.getElementById("btn-download-md");

  const kbModal = document.getElementById("kb-modal");
  const btnOpenKb = document.getElementById("btn-open-kb");
  const btnCloseKb = document.getElementById("btn-close-kb");
  const kbModalContent = document.getElementById("kb-modal-content");

  // Fetch and Load Initial Tickets
  async function init() {
    try {
      const res = await fetch("/api/tickets");
      tickets = await res.json();
      document.getElementById("nav-ticket-count").textContent = `${tickets.length} Tickets`;
      document.getElementById("inbox-badge-count").textContent = tickets.length;
      renderTicketList();

      if (tickets.length > 0) {
        selectTicket(tickets[0].ticket_id);
      }
    } catch (err) {
      console.error("Failed to load tickets:", err);
      ticketListEl.innerHTML = `<div class="loading-state">Failed to connect to backend server.</div>`;
    }
  }

  // Render Left Column Tickets
  function renderTicketList() {
    const query = ticketSearchInput.value.toLowerCase().trim();
    const filtered = tickets.filter(t => {
      const matchCat = selectedCategory === "all" || t.category === selectedCategory;
      const matchQuery = !query || 
        t.ticket_id.toLowerCase().includes(query) ||
        t.subject.toLowerCase().includes(query) ||
        t.customer_name.toLowerCase().includes(query) ||
        t.category.toLowerCase().includes(query);
      return matchCat && matchQuery;
    });

    if (filtered.length === 0) {
      ticketListEl.innerHTML = `<div class="loading-state">No matching tickets found.</div>`;
      return;
    }

    ticketListEl.innerHTML = filtered.map(t => {
      const isSelected = t.ticket_id === currentTicketId;
      const initials = t.customer_name.split(" ").map(w => w[0]).join("").slice(0, 2).toUpperCase();
      return `
        <div class="ticket-card ${isSelected ? 'selected' : ''}" data-id="${t.ticket_id}">
          <div class="ticket-card-top">
            <div class="ticket-sender-group">
              <div class="sender-avatar">${initials}</div>
              <span class="sender-name">${escapeHtml(t.customer_name)}</span>
            </div>
            <div class="ticket-pill-row">
              <span class="pill-sm tier-${t.plan_tier.toLowerCase()}">${t.plan_tier}</span>
              <span class="pill-sm sentiment-${t.sentiment.toLowerCase()}">${t.sentiment}</span>
            </div>
          </div>
          <div class="ticket-card-subject">${escapeHtml(t.subject)}</div>
          <div class="ticket-card-footer">
            <span>#${t.ticket_id}</span>
            <span>$${t.mrr}/mo</span>
          </div>
        </div>
      `;
    }).join("");

    // Attach click listeners
    ticketListEl.querySelectorAll(".ticket-card").forEach(el => {
      el.addEventListener("click", () => {
        selectTicket(el.dataset.id);
      });
    });
  }

  // Select Ticket and Fetch Details
  async function selectTicket(ticketId) {
    currentTicketId = ticketId;
    renderTicketList(); // update active card highlight

    try {
      const res = await fetch(`/api/tickets/${ticketId}`);
      currentTicketDetail = await res.json();
      renderTicketView(currentTicketDetail);
      
      // Auto-generate reply for the selected ticket
      triggerGenerateReply();
    } catch (err) {
      console.error("Failed to load ticket details:", err);
    }
  }

  // Render Middle Column Thread & RAG Info
  function renderTicketView(data) {
    const t = data.ticket;
    thTicketId.textContent = t.ticket_id;
    thCategory.textContent = t.category.replace("_", " ");
    thTier.textContent = t.customer_context.plan_tier;
    thSentiment.textContent = t.sentiment;
    thPriority.textContent = t.priority;
    thSubject.textContent = t.subject;
    thAccountId.textContent = t.customer_context.account_id;
    thMrr.textContent = `$${t.customer_context.mrr}/mo`;
    
    const firstMsg = t.thread[0] || {};
    thCustomerName.textContent = firstMsg.sender_name || "Customer";
    thCustomerEmail.textContent = firstMsg.sender_email || "";

    // Render RAG Policy Articles
    const kbDocs = data.relevant_kb || [];
    ragDrawerContent.innerHTML = kbDocs.map(doc => `
      <div class="kb-pill-card">
        <div class="kb-pill-title">${escapeHtml(doc.title)} (ID: ${doc.id})</div>
        <p>${escapeHtml(doc.content)}</p>
      </div>
    `).join("");

    // Render Ground Truth
    gtText.textContent = t.ground_truth_reply;

    // Render Thread Messages
    threadMessagesEl.innerHTML = t.thread.map(m => {
      const isCustomer = m.sender === "customer";
      return `
        <div class="message-bubble ${isCustomer ? 'customer' : 'agent'}">
          <div class="msg-header">
            <span class="msg-author">${escapeHtml(m.sender_name)} (${isCustomer ? 'Customer' : 'Hiver Support'})</span>
            <span class="msg-time">${new Date(m.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
          </div>
          <div class="msg-body">${escapeHtml(m.body)}</div>
        </div>
      `;
    }).join("");
  }

  // Generate AI Reply
  async function triggerGenerateReply() {
    if (!currentTicketId) return;

    btnGenerateReply.disabled = true;
    btnGenerateReply.innerHTML = `<span class="spinner"></span> Generating reply...`;

    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticket_id: currentTicketId,
          provider: providerSelect.value,
          custom_instruction: customInstructionInput.value.trim() || null
        })
      });

      const data = await res.json();
      replyEditor.value = data.reply;
      updateWordCount();
      updateScorecard(data.evaluation);
    } catch (err) {
      console.error("Generation failed:", err);
      replyEditor.value = "Error generating reply. Please check console.";
    } finally {
      btnGenerateReply.disabled = false;
      btnGenerateReply.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
        <span>Generate AI Reply</span>
      `;
    }
  }

  // Re-evaluate Edited Draft
  async function triggerEvaluateReply() {
    if (!currentTicketId) return;

    btnEvaluateReply.disabled = true;
    btnEvaluateReply.textContent = "Evaluating...";

    try {
      const res = await fetch("/api/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticket_id: currentTicketId,
          reply: replyEditor.value
        })
      });

      const evalData = await res.json();
      updateScorecard(evalData);
    } catch (err) {
      console.error("Evaluation failed:", err);
    } finally {
      btnEvaluateReply.disabled = false;
      btnEvaluateReply.textContent = "Evaluate";
    }
  }

  // Update Scorecard DOM
  function updateScorecard(evalData) {
    const s = evalData.scores;
    gaugeHeqiVal.textContent = s.composite_heqi;

    // Conic gradient gauge fill
    const gaugeEl = document.querySelector(".gauge-circle");
    if (gaugeEl) {
      gaugeEl.style.background = `conic-gradient(var(--accent-emerald) 0% ${s.composite_heqi}%, rgba(255, 255, 255, 0.1) ${s.composite_heqi}% 100%)`;
    }

    // Badge and Confidence
    if (s.composite_heqi >= 85) {
      heqiGrade.textContent = "Exceptional";
      heqiGrade.style.background = "rgba(16, 185, 129, 0.2)";
      heqiGrade.style.color = "#34D399";
      confidenceLabel.textContent = "High Confidence - Ready to Send";
      confidenceDesc.textContent = "Adheres strictly to all company policies, resolves customer queries, and maintains ideal tone.";
    } else if (s.composite_heqi >= 70) {
      heqiGrade.textContent = "Good Draft";
      heqiGrade.style.background = "rgba(59, 130, 246, 0.2)";
      heqiGrade.style.color = "#60A5FA";
      confidenceLabel.textContent = "Suggested Draft - Review Recommended";
      confidenceDesc.textContent = "Solid foundation with minor refinement opportunities.";
    } else {
      heqiGrade.textContent = "Flagged / Needs Review";
      heqiGrade.style.background = "rgba(239, 68, 68, 0.2)";
      heqiGrade.style.color = "#F87171";
      confidenceLabel.textContent = "Attention Needed";
      confidenceDesc.textContent = "Missing key policy facts, resolution points, or requires tone de-escalation.";
    }

    // Dimensions
    scorePolicy.textContent = `${s.policy_adherence_score}%`;
    barPolicy.style.width = `${s.policy_adherence_score}%`;

    scoreIntent.textContent = `${s.intent_resolution_score}%`;
    barIntent.style.width = `${s.intent_resolution_score}%`;

    scoreTone.textContent = `${s.tone_empathy_score}%`;
    barTone.style.width = `${s.tone_empathy_score}%`;

    scoreAction.textContent = `${s.actionability_score}%`;
    barAction.style.width = `${s.actionability_score}%`;

    scoreSemantic.textContent = `${s.semantic_similarity}%`;
    barSemantic.style.width = `${s.semantic_similarity}%`;

    lexRougel.textContent = s.rougeL_f1.toFixed(2);
    lexBleu.textContent = s.bleu_score.toFixed(1);

    // Feedback
    feedbackStrengths.innerHTML = (evalData.strengths || ["Covers core customer inquiry"]).map(st => `<li>${escapeHtml(st)}</li>`).join("");
    feedbackImprovements.innerHTML = (evalData.areas_for_improvement && evalData.areas_for_improvement.length > 0)
      ? evalData.areas_for_improvement.map(imp => `<li>${escapeHtml(imp)}</li>`).join("")
      : `<li>No critical issues detected.</li>`;
  }

  // Word Count Helper
  function updateWordCount() {
    const text = replyEditor.value.trim();
    const count = text ? text.split(/\s+/).length : 0;
    replyWordCount.textContent = `${count} words`;
  }

  // Benchmark Execution
  async function runBenchmark() {
    btnStartBenchmark.disabled = true;
    btnStartBenchmark.innerHTML = `<span class="spinner"></span> Benchmarking 20 tickets...`;

    try {
      const res = await fetch("/api/benchmark", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ provider: benchProviderSelect.value })
      });

      latestBenchmarkData = await res.json();
      renderBenchmarkResults(latestBenchmarkData);
    } catch (err) {
      console.error("Benchmark failed:", err);
    } finally {
      btnStartBenchmark.disabled = false;
      btnStartBenchmark.innerHTML = `
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
        Execute Benchmark Across Dataset
      `;
    }
  }

  function renderBenchmarkResults(data) {
    const sum = data.summary;
    document.getElementById("kpi-mean-heqi").textContent = sum.mean_heqi;
    document.getElementById("kpi-policy").textContent = `${sum.mean_policy_adherence}%`;
    document.getElementById("kpi-intent").textContent = `${sum.mean_intent_resolution}%`;
    document.getElementById("kpi-high-perf").textContent = `${sum.high_performers_count} / ${sum.total_tickets}`;
    document.getElementById("nav-mean-heqi").textContent = `${sum.mean_heqi} / 100`;

    // Category Table
    const catTbody = document.querySelector("#table-bench-categories tbody");
    catTbody.innerHTML = Object.entries(sum.category_breakdown).map(([cat, d]) => `
      <tr>
        <td><code>${cat}</code></td>
        <td>${d.count}</td>
        <td><strong>${d.mean_heqi}</strong></td>
      </tr>
    `).join("");

    // Sentiment Table
    const sentTbody = document.querySelector("#table-bench-sentiments tbody");
    sentTbody.innerHTML = Object.entries(sum.sentiment_breakdown).map(([sent, d]) => `
      <tr>
        <td><code>${sent}</code></td>
        <td>${d.count}</td>
        <td><strong>${d.mean_heqi}</strong></td>
      </tr>
    `).join("");
  }

  // Knowledge Base Modal
  async function openKbModal() {
    kbModal.classList.add("active");
    try {
      const res = await fetch("/api/kb");
      const docs = await res.json();
      kbModalContent.innerHTML = docs.map(doc => `
        <div class="kb-article-card">
          <div class="kb-article-header">
            <h4>${escapeHtml(doc.title)}</h4>
            <span class="tag-badge">${doc.id}</span>
          </div>
          <p class="kb-article-content">${escapeHtml(doc.content)}</p>
          <div class="kb-keywords-row">
            ${doc.keywords.map(kw => `<span class="kw-badge">${escapeHtml(kw)}</span>`).join("")}
          </div>
        </div>
      `).join("");
    } catch (err) {
      kbModalContent.innerHTML = `<p>Failed to load knowledge base articles.</p>`;
    }
  }

  // Download Reports Helper
  function downloadFile(filename, content, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  // Event Listeners
  ticketSearchInput.addEventListener("input", renderTicketList);

  categoryChips.querySelectorAll(".chip").forEach(chip => {
    chip.addEventListener("click", () => {
      categoryChips.querySelectorAll(".chip").forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      selectedCategory = chip.dataset.category;
      renderTicketList();
    });
  });

  replyEditor.addEventListener("input", updateWordCount);
  btnGenerateReply.addEventListener("click", triggerGenerateReply);
  btnEvaluateReply.addEventListener("click", triggerEvaluateReply);

  // Accordion clicks
  ragDrawerToggle.addEventListener("click", () => {
    ragDrawer.classList.toggle("collapsed");
    ragDrawerContent.style.display = ragDrawer.classList.contains("collapsed") ? "none" : "flex";
  });

  gtDrawerToggle.addEventListener("click", () => {
    gtDrawer.classList.toggle("collapsed");
    document.getElementById("gt-drawer-content").style.display = gtDrawer.classList.contains("collapsed") ? "none" : "block";
  });

  // Modals
  btnOpenBenchmark.addEventListener("click", () => {
    benchmarkModal.classList.add("active");
    if (!latestBenchmarkData) {
      runBenchmark();
    }
  });
  btnCloseBenchmark.addEventListener("click", () => benchmarkModal.classList.remove("active"));

  btnStartBenchmark.addEventListener("click", runBenchmark);

  btnOpenKb.addEventListener("click", openKbModal);
  btnCloseKb.addEventListener("click", () => kbModal.classList.remove("active"));

  // Download buttons
  btnDownloadJson.addEventListener("click", () => {
    if (!latestBenchmarkData) return;
    downloadFile("evaluation_report.json", JSON.stringify(latestBenchmarkData, null, 2), "application/json");
  });

  btnDownloadMd.addEventListener("click", async () => {
    // Generate human-readable Markdown summary
    if (!latestBenchmarkData) return;
    const sum = latestBenchmarkData.summary;
    let md = `# Hiver AI Email Evaluation & Benchmark Report\n\n`;
    md += `## Executive Summary\n`;
    md += `- **Mean HEQI Score**: ${sum.mean_heqi} / 100\n`;
    md += `- **Policy Adherence**: ${sum.mean_policy_adherence}%\n`;
    md += `- **Intent Resolution**: ${sum.mean_intent_resolution}%\n`;
    md += `- **Tone & Empathy**: ${sum.mean_tone_empathy}%\n`;
    md += `- **Actionability**: ${sum.mean_actionability}%\n`;
    md += `- **Semantic Similarity**: ${sum.mean_semantic_similarity}%\n`;
    md += `- **High Confidence Drafts**: ${sum.high_performers_count} / ${sum.total_tickets}\n\n`;
    downloadFile("evaluation_report.md", md, "text/markdown");
  });

  function escapeHtml(str) {
    if (!str) return "";
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  // Start app
  init();
});
