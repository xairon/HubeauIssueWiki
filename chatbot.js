(function () {
  "use strict";

  // --- Config ---
  var SESSION_KEY = "hubeau_chat_history";
  var SESSION_PANEL_KEY = "hubeau_chat_open";

  // --- State ---
  var isReady = true;
  var isProcessing = false;
  var conversationHistory = []; // {role, content, sources, timestamp}

  // --- DOM refs ---
  var toggle = document.getElementById("chatbotToggle");
  var panel = document.getElementById("chatbotPanel");
  var closeBtn = document.getElementById("chatbotClose");
  var clearBtn = document.getElementById("chatbotClear");
  var messagesEl = document.getElementById("chatbotMessages");
  var inputEl = document.getElementById("chatbotInput");
  var sendBtn = document.getElementById("chatbotSend");
  var statusBar = document.getElementById("chatbotStatus");

  // --- Session persistence ---
  function saveSession() {
    try {
      sessionStorage.setItem(SESSION_KEY, JSON.stringify(conversationHistory));
    } catch (e) { /* quota exceeded — ignore */ }
  }

  function loadSession() {
    try {
      var raw = sessionStorage.getItem(SESSION_KEY);
      if (raw) {
        conversationHistory = JSON.parse(raw);
        return true;
      }
    } catch (e) { /* corrupt — ignore */ }
    return false;
  }

  function savePanelState(open) {
    try { sessionStorage.setItem(SESSION_PANEL_KEY, open ? "1" : "0"); } catch (e) {}
  }

  function loadPanelState() {
    try { return sessionStorage.getItem(SESSION_PANEL_KEY) === "1"; } catch (e) { return false; }
  }

  // --- Restore session on load ---
  function restoreSession() {
    if (!loadSession() || conversationHistory.length === 0) return;
    conversationHistory.forEach(function (msg) {
      appendMsgToDOM(msg.role, msg.content, msg.sources, true);
    });
  }

  // --- Toggle panel ---
  toggle.addEventListener("click", function () {
    panel.classList.toggle("open");
    var isOpen = panel.classList.contains("open");
    savePanelState(isOpen);
    if (isOpen) {
      inputEl.focus();
    }
  });
  closeBtn.addEventListener("click", function () {
    panel.classList.remove("open");
    savePanelState(false);
  });

  // --- Clear conversation ---
  if (clearBtn) {
    clearBtn.addEventListener("click", function () {
      conversationHistory = [];
      saveSession();
      // Remove all messages except the welcome message
      while (messagesEl.children.length > 1) {
        messagesEl.removeChild(messagesEl.lastChild);
      }
      // If welcome message was removed too, re-add it
      if (messagesEl.children.length === 0) {
        var welcomeDiv = document.createElement("div");
        welcomeDiv.className = "chat-msg chat-msg-bot";
        var welcomeBubble = document.createElement("div");
        welcomeBubble.className = "chat-bubble";
        welcomeBubble.textContent = "Bonjour ! Posez-moi une question sur les APIs Hub\u2019Eau. Je cherche dans la base de connaissances pour vous r\u00e9pondre.";
        welcomeDiv.appendChild(welcomeBubble);
        messagesEl.appendChild(welcomeDiv);
      }
    });
  }

  // --- Send message ---
  sendBtn.addEventListener("click", sendMessage);
  inputEl.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  function sendMessage() {
    var query = inputEl.value.trim();
    if (!query || isProcessing) return;

    if (!isReady) {
      showStatus("Chargement en cours, patientez...");
      return;
    }

    inputEl.value = "";
    appendMsg("user", query);
    processQuery(query);
  }

  // --- Auto-open if was open ---
  if (loadPanelState()) {
    panel.classList.add("open");
  }
  restoreSession();

  // --- Query processing via backend ---
  function processQuery(query) {
    isProcessing = true;
    sendBtn.disabled = true;

    // Create empty bot bubble for streaming
    var streamDiv = document.createElement("div");
    streamDiv.className = "chat-msg chat-msg-bot";
    streamDiv.id = "chatStreaming";
    var streamBubble = document.createElement("div");
    streamBubble.className = "chat-bubble";
    // Show typing indicator initially
    var typing = document.createElement("div");
    typing.className = "chat-typing";
    for (var i = 0; i < 3; i++) typing.appendChild(document.createElement("span"));
    streamBubble.appendChild(typing);
    streamDiv.appendChild(streamBubble);
    messagesEl.appendChild(streamDiv);
    messagesEl.scrollTop = messagesEl.scrollHeight;

    // Build history for backend (last N turns, role + content only)
    var historyForBackend = conversationHistory.map(function (h) {
      return { role: h.role, content: h.content };
    });

    fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: query, history: historyForBackend }),
    })
      .then(function (resp) {
        if (!resp.ok) {
          return resp.text().then(function (t) {
            throw new Error("Erreur serveur " + resp.status + ": " + t);
          });
        }

        var reader = resp.body.getReader();
        var decoder = new TextDecoder();
        var fullText = "";
        var buffer = "";
        var sources = [];

        function processChunk() {
          return reader.read().then(function (result) {
            if (result.done) {
              // Process remaining buffer
              if (buffer.trim()) {
                try {
                  var data = JSON.parse(buffer.trim());
                  if (data.token) fullText += data.token;
                  if (data.done) sources = data.sources || [];
                } catch (e) { /* ignore */ }
              }
              return;
            }

            buffer += decoder.decode(result.value, { stream: true });
            var lines = buffer.split("\n");
            buffer = lines.pop() || "";

            for (var i = 0; i < lines.length; i++) {
              var line = lines[i].trim();
              if (!line) continue;
              try {
                var data = JSON.parse(line);
                if (data.error) {
                  throw new Error(data.error);
                }
                if (data.token) {
                  fullText += data.token;
                  renderMarkdownIntoBubble(streamBubble, fullText);
                  messagesEl.scrollTop = messagesEl.scrollHeight;
                }
                if (data.done) {
                  sources = data.sources || [];
                }
              } catch (e) { /* malformed line, skip */ }
            }

            return processChunk();
          });
        }

        return processChunk().then(function () {
          if (!fullText.trim()) fullText = "Pas de reponse generee.";

          // Remove streaming div
          var el = document.getElementById("chatStreaming");
          if (el) el.remove();
          // Add final message
          appendMsg("bot", fullText.trim(), sources);
          isProcessing = false;
          sendBtn.disabled = false;
        });
      })
      .catch(function (err) {
        var el = document.getElementById("chatStreaming");
        if (el) el.remove();
        console.error("Query error:", err);
        var msg = err.message || "Erreur inconnue";
        appendMsg("bot", "Erreur: " + msg);
        isProcessing = false;
        sendBtn.disabled = false;
      });
  }

  // --- Markdown rendering into a bubble ---
  function renderMarkdownIntoBubble(bubble, text) {
    // Clear bubble content
    while (bubble.firstChild) bubble.removeChild(bubble.firstChild);

    var paragraphs = text.split("\n");
    var currentList = null;

    paragraphs.forEach(function (para) {
      // Heading ###
      var headingMatch = para.match(/^(#{1,3})\s+(.+)/);
      if (headingMatch) {
        currentList = null;
        var level = headingMatch[1].length;
        var h = document.createElement("h" + Math.min(level + 2, 6)); // h3-h6 in bubble
        h.style.cssText = "margin:8px 0 4px;font-size:" + (level === 1 ? "1.1em" : level === 2 ? "1em" : "0.95em") + ";";
        renderFormattedText(h, headingMatch[2]);
        bubble.appendChild(h);
        return;
      }

      // List items
      var listMatch = para.match(/^\s*[-*]\s+(.*)/);
      if (listMatch) {
        if (!currentList) {
          currentList = document.createElement("ul");
          currentList.style.cssText = "margin:4px 0;padding-left:20px;";
          bubble.appendChild(currentList);
        }
        var li = document.createElement("li");
        renderFormattedText(li, listMatch[1]);
        currentList.appendChild(li);
        return;
      }

      // Numbered list
      var numMatch = para.match(/^\s*(\d+)\.\s+(.*)/);
      if (numMatch) {
        if (!currentList || currentList.tagName !== "OL") {
          currentList = document.createElement("ol");
          currentList.style.cssText = "margin:4px 0;padding-left:20px;";
          bubble.appendChild(currentList);
        }
        var oli = document.createElement("li");
        renderFormattedText(oli, numMatch[2]);
        currentList.appendChild(oli);
        return;
      }

      // Regular paragraph
      currentList = null;
      if (para.trim()) {
        var p = document.createElement("p");
        p.style.margin = "4px 0";
        renderFormattedText(p, para);
        bubble.appendChild(p);
      }
    });
  }

  function renderFormattedText(parent, text) {
    // Pattern: **bold**, `code`, [text](url), (#NNN) issue refs
    var pattern = /(\*\*(.+?)\*\*|`(.+?)`|\[([^\]]+)\]\(([^)]+)\)|\(#(\d+)\))/g;
    var lastIdx = 0;
    var m;
    while ((m = pattern.exec(text)) !== null) {
      if (m.index > lastIdx) {
        parent.appendChild(document.createTextNode(text.slice(lastIdx, m.index)));
      }
      if (m[2]) {
        // Bold
        var b = document.createElement("strong");
        b.textContent = m[2];
        parent.appendChild(b);
      } else if (m[3]) {
        // Code
        var c = document.createElement("code");
        c.textContent = m[3];
        parent.appendChild(c);
      } else if (m[4] && m[5]) {
        // Link [text](url) — only allow http(s) to prevent javascript: XSS
        if (/^https?:\/\//i.test(m[5])) {
          var a = document.createElement("a");
          a.href = m[5];
          a.textContent = m[4];
          a.target = "_blank";
          a.rel = "noopener noreferrer";
          parent.appendChild(a);
        } else {
          parent.appendChild(document.createTextNode("[" + m[4] + "](" + m[5] + ")"));
        }
      } else if (m[6]) {
        // Issue ref (#NNN)
        var issueLink = document.createElement("a");
        issueLink.href = "https://github.com/BRGM/hubeau/issues/" + m[6];
        issueLink.textContent = "#" + m[6];
        issueLink.target = "_blank";
        issueLink.rel = "noopener noreferrer";
        parent.appendChild(document.createTextNode("("));
        parent.appendChild(issueLink);
        parent.appendChild(document.createTextNode(")"));
      }
      lastIdx = pattern.lastIndex;
    }
    if (lastIdx < text.length) {
      parent.appendChild(document.createTextNode(text.slice(lastIdx)));
    }
  }

  // --- Safe DOM UI helpers ---
  function appendMsg(role, text, sources) {
    // Save to history
    conversationHistory.push({
      role: role,
      content: text,
      sources: sources || null,
      timestamp: Date.now(),
    });
    saveSession();

    appendMsgToDOM(role, text, sources, false);
  }

  function appendMsgToDOM(role, text, sources, skipScroll) {
    var msgDiv = document.createElement("div");
    msgDiv.className = "chat-msg chat-msg-" + role;

    var bubble = document.createElement("div");
    bubble.className = "chat-bubble";

    if (role === "bot") {
      renderMarkdownIntoBubble(bubble, text);
    } else {
      // User messages: simple text
      var p = document.createElement("p");
      p.style.margin = "0";
      p.textContent = text;
      bubble.appendChild(p);
    }

    if (sources && sources.length > 0) {
      var srcDiv = document.createElement("div");
      srcDiv.className = "chat-sources";
      srcDiv.appendChild(document.createTextNode("Sources: "));
      sources.forEach(function (s, i) {
        if (i > 0) srcDiv.appendChild(document.createTextNode(", "));
        var link = document.createElement("a");
        link.href = s.url;
        link.textContent = s.api + " - " + s.section;
        srcDiv.appendChild(link);
      });
      bubble.appendChild(srcDiv);
    }

    msgDiv.appendChild(bubble);
    messagesEl.appendChild(msgDiv);
    if (!skipScroll) {
      messagesEl.scrollTop = messagesEl.scrollHeight;
    }
  }

  function showStatus(text) {
    statusBar.textContent = text;
    statusBar.style.display = "block";
  }

  function hideStatus() {
    statusBar.style.display = "none";
  }
})();
