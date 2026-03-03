(function () {
  "use strict";

  // --- Config ---
  var EMBEDDINGS_URL = "embeddings.json";
  var BASE_TOP_K = 5;
  var MAX_TOP_K = 12;
  var MIN_SCORE = 0.35;
  var DEDUP_THRESHOLD = 0.6;
  var MAX_HISTORY_TURNS = 4; // 4 exchanges = 8 messages
  var OLLAMA_HOST = window.OLLAMA_HOST || "http://localhost:11434";
  var OLLAMA_CHAT_MODEL = "qwen3.5:4b";
  var OLLAMA_EMBED_MODEL = "nomic-embed-text";
  var SESSION_KEY = "hubeau_chat_history";
  var SESSION_PANEL_KEY = "hubeau_chat_open";

  // --- State ---
  var embeddings = [];
  var isReady = false;
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
    if (isOpen && !isReady && embeddings.length === 0) {
      initChatbot();
    }
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

  // --- Initialize: load embeddings ---
  function initChatbot() {
    showStatus("Chargement de l'index...");

    fetch(EMBEDDINGS_URL)
      .then(function (r) { return r.json(); })
      .then(function (data) {
        embeddings = data;
        isReady = true;
        hideStatus();
      })
      .catch(function (err) {
        console.error("Init error:", err);
        showStatus("Erreur: " + err.message);
      });
  }

  // --- Auto-open if was open + auto-init ---
  if (loadPanelState()) {
    panel.classList.add("open");
    initChatbot();
  }
  restoreSession();

  // --- Query processing ---
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

    embedQuery(query)
      .then(function (queryVec) {
        var results = findSimilarDynamic(queryVec);
        return streamAnswer(query, results, streamBubble);
      })
      .then(function (result) {
        // Remove streaming div
        var el = document.getElementById("chatStreaming");
        if (el) el.remove();
        // Add final message
        appendMsg("bot", result.answer, result.sources);
        isProcessing = false;
        sendBtn.disabled = false;
      })
      .catch(function (err) {
        var el = document.getElementById("chatStreaming");
        if (el) el.remove();
        console.error("Query error:", err);
        var msg = err.message || "Erreur inconnue";
        msg += "\nVerifiez qu'Ollama est bien lance (ollama serve).";
        appendMsg("bot", "Erreur: " + msg);
        isProcessing = false;
        sendBtn.disabled = false;
      });
  }

  // --- Embed query via Ollama ---
  function embedQuery(text) {
    return fetch(OLLAMA_HOST + "/api/embed", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: OLLAMA_EMBED_MODEL,
        input: ["search_query: " + text],
        keep_alive: 0
      })
    })
      .then(function (r) {
        if (!r.ok) {
          return r.text().then(function (t) {
            throw new Error("Ollama embed error " + r.status + ": " + t);
          });
        }
        return r.json();
      })
      .then(function (data) { return data.embeddings[0]; });
  }

  // --- Dynamic vector search with deduplication ---
  function findSimilarDynamic(queryVec) {
    var scored = embeddings.map(function (entry) {
      return {
        score: cosineSim(queryVec, entry.embedding),
        text: entry.text,
        api: entry.api,
        section: entry.section,
        url: entry.url,
        source: entry.source || "wiki",
      };
    });
    scored.sort(function (a, b) { return b.score - a.score; });

    var selected = [];
    var selectedTexts = [];

    for (var i = 0; i < scored.length && selected.length < MAX_TOP_K; i++) {
      var item = scored[i];

      // Stop if below minimum score (after getting BASE_TOP_K)
      if (selected.length >= BASE_TOP_K && item.score < MIN_SCORE) break;
      // Hard stop if score is very low
      if (item.score < 0.2) break;

      // Deduplication: skip fact chunks that overlap too much with already selected wiki chunks
      if (item.source === "fact" && selectedTexts.length > 0) {
        var itemWords = getWords(item.text);
        var dominated = false;
        for (var j = 0; j < selectedTexts.length; j++) {
          if (wordOverlap(itemWords, selectedTexts[j]) >= DEDUP_THRESHOLD) {
            dominated = true;
            break;
          }
        }
        if (dominated) continue;
      }

      selected.push(item);
      selectedTexts.push(getWords(item.text));
    }

    return selected;
  }

  function getWords(text) {
    return text.toLowerCase().replace(/[^\w\s\u00e0\u00e2\u00e4\u00e9\u00e8\u00ea\u00eb\u00ef\u00ee\u00f4\u00f9\u00fb\u00fc\u00ff\u00e7\u0153\u00e6]/g, " ").split(/\s+/).filter(function (w) { return w.length > 2; });
  }

  function wordOverlap(wordsA, wordsB) {
    if (wordsA.length === 0) return 0;
    var setB = {};
    for (var i = 0; i < wordsB.length; i++) setB[wordsB[i]] = true;
    var overlap = 0;
    for (var j = 0; j < wordsA.length; j++) {
      if (setB[wordsA[j]]) overlap++;
    }
    return overlap / wordsA.length;
  }

  function cosineSim(a, b) {
    var dot = 0, nA = 0, nB = 0;
    for (var i = 0; i < a.length; i++) {
      dot += a[i] * b[i];
      nA += a[i] * a[i];
      nB += b[i] * b[i];
    }
    return dot / (Math.sqrt(nA) * Math.sqrt(nB) + 1e-8);
  }

  // --- Build messages for multi-turn ---
  function buildMessages(query, results) {
    var contextParts = results.map(function (r) {
      var tag = r.source === "fact" ? "FAIT BRUT" : r.section;
      return "[" + r.api + " - " + tag + "] " + r.text;
    });

    var systemPrompt =
      "Tu es un assistant expert sur les APIs Hub'Eau " +
      "(plateforme de donnees ouvertes sur l'eau en France, par le BRGM).\n\n" +
      "Les 14 APIs Hub'Eau sont :\n" +
      "- Hydrometrie (debits, hauteurs d'eau)\n" +
      "- Piezometrie (niveaux des nappes)\n" +
      "- Qualite des cours d'eau (analyses physico-chimiques)\n" +
      "- Qualite des nappes (qualite eaux souterraines)\n" +
      "- Qualite de l'eau potable\n" +
      "- Poisson (donnees piscicoles)\n" +
      "- Prelevements en eau\n" +
      "- Hydrobiologie (IBGN, IBD, indices biologiques)\n" +
      "- Temperature des cours d'eau\n" +
      "- Ecoulement des cours d'eau (observations visuelles)\n" +
      "- Surveillance des eaux littorales\n" +
      "- Indicateurs des services (eau potable, assainissement)\n" +
      "- Phytopharmaceutiques (pesticides dans l'eau)\n" +
      "- General (transverse a toutes les APIs)\n\n" +
      "Regles :\n" +
      "- Reponds en francais, de maniere concise et structuree.\n" +
      "- Base ta reponse UNIQUEMENT sur le contexte fourni et l'historique de conversation.\n" +
      "- Utilise le formatage markdown : **gras** pour les points cles, `code` pour les parametres/endpoints, ### pour les sous-titres si la reponse est longue, des listes a puces.\n" +
      "- Cite les numeros d'issues quand c'est pertinent, ex: (#123).\n" +
      "- Structure ta reponse : d'abord une reponse directe et courte, puis les details si necessaire.\n" +
      "- Si le contexte ne contient pas l'information, dis-le clairement et suggere ou chercher.\n" +
      "- Si la question n'est pas liee aux APIs Hub'Eau ou a l'hydrologie, indique poliment que tu ne peux aider que sur ces sujets.\n" +
      "- Pour les questions de suivi (ex: 'et pour la piezometrie ?'), utilise l'historique de conversation pour comprendre le contexte.\n" +
      "- Distingue les problemes resolus (passes) des problemes encore en cours.\n" +
      "- Pour les liens, utilise le format [texte](url).";

    var messages = [{ role: "system", content: systemPrompt }];

    // Add last N turns of conversation history (plain, no RAG context)
    var historySlice = conversationHistory.slice(-(MAX_HISTORY_TURNS * 2));
    for (var i = 0; i < historySlice.length; i++) {
      var h = historySlice[i];
      messages.push({ role: h.role === "bot" ? "assistant" : h.role, content: h.content });
    }

    // Current question with RAG context
    var userMsg =
      "Contexte (extraits de la base de connaissances):\n" +
      contextParts.join("\n\n") +
      "\n\nQuestion: " + query;

    messages.push({ role: "user", content: userMsg });

    return messages;
  }

  // --- Streaming LLM generation via Ollama native /api/chat ---
  function streamAnswer(query, results, bubble) {
    var messages = buildMessages(query, results);

    return fetch(OLLAMA_HOST + "/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: OLLAMA_CHAT_MODEL,
        messages: messages,
        stream: true,
        options: {
          temperature: 0.3,
          num_predict: 2048,
        },
        keep_alive: 0,
      }),
    }).then(function (resp) {
      if (!resp.ok) {
        return resp.text().then(function (t) {
          throw new Error("Ollama API error " + resp.status + ": " + t);
        });
      }

      var reader = resp.body.getReader();
      var decoder = new TextDecoder();
      var fullText = "";
      var buffer = "";

      function processChunk() {
        return reader.read().then(function (result) {
          if (result.done) {
            // Process remaining buffer
            if (buffer.trim()) {
              try {
                var data = JSON.parse(buffer.trim());
                if (data.message && data.message.content) {
                  fullText += data.message.content;
                }
              } catch (e) { /* ignore */ }
            }
            return;
          }

          buffer += decoder.decode(result.value, { stream: true });
          var lines = buffer.split("\n");
          buffer = lines.pop() || ""; // Keep incomplete line in buffer

          for (var i = 0; i < lines.length; i++) {
            var line = lines[i].trim();
            if (!line) continue;
            try {
              var data = JSON.parse(line);
              if (data.message && data.message.content) {
                fullText += data.message.content;
                renderMarkdownIntoBubble(bubble, fullText);
                messagesEl.scrollTop = messagesEl.scrollHeight;
              }
            } catch (e) {
              // Malformed JSON line, skip
            }
          }

          return processChunk();
        });
      }

      return processChunk().then(function () {
        if (!fullText.trim()) fullText = "Pas de reponse generee.";

        var sources = results
          .filter(function (r) { return r.score > 0.3; })
          .slice(0, 3)
          .map(function (r) {
            return { api: r.api, section: r.section, url: r.url };
          });

        return { answer: fullText.trim(), sources: sources };
      });
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
        // Link [text](url)
        var a = document.createElement("a");
        a.href = m[5];
        a.textContent = m[4];
        a.target = "_blank";
        a.rel = "noopener";
        parent.appendChild(a);
      } else if (m[6]) {
        // Issue ref (#NNN)
        var issueLink = document.createElement("a");
        issueLink.href = "https://github.com/BRGM/hubeau/issues/" + m[6];
        issueLink.textContent = "#" + m[6];
        issueLink.target = "_blank";
        issueLink.rel = "noopener";
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
