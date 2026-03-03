(function () {
  "use strict";

  // --- Config ---
  var EMBEDDINGS_URL = "embeddings.json";
  var TOP_K = 5;
  var OLLAMA_HOST = window.OLLAMA_HOST || "http://localhost:11434";
  var OLLAMA_CHAT_MODEL = "qwen3.5:4b";
  var OLLAMA_EMBED_MODEL = "nomic-embed-text";

  // --- State ---
  var embeddings = [];
  var isReady = false;
  var isProcessing = false;

  // --- DOM refs ---
  var toggle = document.getElementById("chatbotToggle");
  var panel = document.getElementById("chatbotPanel");
  var closeBtn = document.getElementById("chatbotClose");
  var messagesEl = document.getElementById("chatbotMessages");
  var inputEl = document.getElementById("chatbotInput");
  var sendBtn = document.getElementById("chatbotSend");
  var statusBar = document.getElementById("chatbotStatus");

  // --- Toggle panel ---
  toggle.addEventListener("click", function () {
    panel.classList.toggle("open");
    if (panel.classList.contains("open") && !isReady && embeddings.length === 0) {
      initChatbot();
    }
    if (panel.classList.contains("open")) {
      inputEl.focus();
    }
  });
  closeBtn.addEventListener("click", function () {
    panel.classList.remove("open");
  });

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

  // --- Query processing ---
  function processQuery(query) {
    isProcessing = true;
    sendBtn.disabled = true;
    showTyping();

    embedQuery(query)
      .then(function (queryVec) {
        var results = findSimilar(queryVec, TOP_K);
        return generateAnswer(query, results);
      })
      .then(function (result) {
        removeTyping();
        appendMsg("bot", result.answer, result.sources);
        isProcessing = false;
        sendBtn.disabled = false;
      })
      .catch(function (err) {
        removeTyping();
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

  // --- Vector search ---
  function findSimilar(queryVec, topK) {
    var scored = embeddings.map(function (entry) {
      return {
        score: cosineSim(queryVec, entry.embedding),
        text: entry.text,
        api: entry.api,
        section: entry.section,
        url: entry.url,
      };
    });
    scored.sort(function (a, b) { return b.score - a.score; });
    return scored.slice(0, topK);
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

  // --- LLM generation via Ollama (OpenAI-compatible) ---
  function generateAnswer(query, results) {
    var contextParts = results.map(function (r) {
      return "[" + r.api + " - " + r.section + "] " + r.text;
    });

    var systemPrompt =
      "Tu es un assistant expert sur les APIs Hub'Eau " +
      "(plateforme de donnees ouvertes sur l'eau en France, par le BRGM).\n\n" +
      "Regles :\n" +
      "- Reponds en francais, de maniere concise et structuree.\n" +
      "- Base ta reponse UNIQUEMENT sur le contexte fourni.\n" +
      "- Utilise le formatage markdown : **gras** pour les points cles, `code` pour les parametres/endpoints, des listes a puces pour les enumerations.\n" +
      "- Cite les numeros d'issues quand c'est pertinent, ex: (#123).\n" +
      "- Structure ta reponse : d'abord une reponse directe et courte, puis les details si necessaire.\n" +
      "- Si le contexte ne contient pas l'information, dis-le clairement et suggere ou chercher.\n" +
      "- Si la question n'est pas liee aux APIs Hub'Eau ou a l'hydrologie, indique poliment que tu ne peux aider que sur ces sujets.";

    var userMsg =
      "Contexte:\n" + contextParts.join("\n\n") +
      "\n\nQuestion: " + query;

    var url = OLLAMA_HOST + "/v1/chat/completions";

    return fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: OLLAMA_CHAT_MODEL,
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userMsg },
        ],
        max_tokens: 1000,
        temperature: 0.3,
        keep_alive: 0
      }),
    })
      .then(function (resp) {
        if (!resp.ok) {
          return resp.text().then(function (t) {
            throw new Error("Ollama API error " + resp.status + ": " + t);
          });
        }
        return resp.json();
      })
      .then(function (data) {
        var answer = "";
        if (data.choices && data.choices[0] && data.choices[0].message) {
          answer = data.choices[0].message.content.trim();
        } else {
          answer = "Pas de reponse generee.";
        }

        var sources = results
          .filter(function (r) { return r.score > 0.3; })
          .slice(0, 3)
          .map(function (r) {
            return { api: r.api, section: r.section, url: r.url };
          });

        return { answer: answer, sources: sources };
      });
  }

  // --- Safe DOM UI helpers ---
  function appendMsg(role, text, sources) {
    var msgDiv = document.createElement("div");
    msgDiv.className = "chat-msg chat-msg-" + role;

    var bubble = document.createElement("div");
    bubble.className = "chat-bubble";

    var paragraphs = text.split("\n");
    var currentList = null;
    paragraphs.forEach(function (para) {
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
      } else {
        currentList = null;
        if (para.trim()) {
          var p = document.createElement("p");
          p.style.margin = "4px 0";
          renderFormattedText(p, para);
          bubble.appendChild(p);
        }
      }
    });

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
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function renderFormattedText(parent, text) {
    var pattern = /(\*\*(.+?)\*\*|`(.+?)`)/g;
    var lastIdx = 0;
    var m;
    while ((m = pattern.exec(text)) !== null) {
      if (m.index > lastIdx) {
        parent.appendChild(document.createTextNode(text.slice(lastIdx, m.index)));
      }
      if (m[2]) {
        var b = document.createElement("strong");
        b.textContent = m[2];
        parent.appendChild(b);
      } else if (m[3]) {
        var c = document.createElement("code");
        c.textContent = m[3];
        parent.appendChild(c);
      }
      lastIdx = pattern.lastIndex;
    }
    if (lastIdx < text.length) {
      parent.appendChild(document.createTextNode(text.slice(lastIdx)));
    }
  }

  function showTyping() {
    var div = document.createElement("div");
    div.className = "chat-msg chat-msg-bot";
    div.id = "chatTyping";
    var bubble = document.createElement("div");
    bubble.className = "chat-bubble";
    var typing = document.createElement("div");
    typing.className = "chat-typing";
    for (var i = 0; i < 3; i++) typing.appendChild(document.createElement("span"));
    bubble.appendChild(typing);
    div.appendChild(bubble);
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function removeTyping() {
    var el = document.getElementById("chatTyping");
    if (el) el.remove();
  }

  function showStatus(text) {
    statusBar.textContent = text;
    statusBar.style.display = "block";
  }

  function hideStatus() {
    statusBar.style.display = "none";
  }
})();
