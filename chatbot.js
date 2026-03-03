(function () {
  "use strict";

  // --- Config ---
  var EMBEDDINGS_URL = "embeddings.json";
  var TOP_K = 5;
  var HF_GEN_URL = "https://router.huggingface.co/cerebras/v1/chat/completions";
  var HF_GEN_MODEL = "llama3.1-8b";
  var HF_TOKEN_STORAGE = "hubeau_kb_hf_token";

  // --- State ---
  var embeddings = [];
  var embedder = null;
  var hfToken = localStorage.getItem(HF_TOKEN_STORAGE) || "";
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
    if (panel.classList.contains("open") && !isReady && !embedder) {
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

    if (!hfToken) {
      promptForToken();
      return;
    }

    if (!isReady) {
      showStatus("Chargement en cours, patientez...");
      return;
    }

    inputEl.value = "";
    appendMsg("user", query);
    processQuery(query);
  }

  // --- Initialize: load embeddings + Transformers.js ---
  function initChatbot() {
    if (!hfToken) {
      promptForToken();
      return;
    }

    showStatus("Chargement de l'index et du modele d'embeddings (~120 Mo)...");

    fetch(EMBEDDINGS_URL)
      .then(function (r) { return r.json(); })
      .then(function (data) {
        embeddings = data;
        showStatus("Index charge (" + embeddings.length + " passages). Chargement du modele...");
        return loadTransformers();
      })
      .then(function (pipe) {
        embedder = pipe;
        isReady = true;
        hideStatus();
      })
      .catch(function (err) {
        console.error("Init error:", err);
        showStatus("Erreur: " + err.message);
      });
  }

  function loadTransformers() {
    return import(
      "https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.4.1"
    ).then(function (mod) {
      return mod.pipeline("feature-extraction", "Xenova/multilingual-e5-small", {
        dtype: "fp32",
      });
    });
  }

  function promptForToken() {
    appendMsg(
      "bot",
      "Pour utiliser l'assistant, entrez votre token HuggingFace " +
      "(gratuit sur huggingface.co/settings/tokens). " +
      "Le token est stocke localement dans votre navigateur."
    );

    var keyDiv = document.createElement("div");
    keyDiv.className = "chat-msg chat-msg-bot";

    var bubble = document.createElement("div");
    bubble.className = "chat-bubble";

    var keyInput = document.createElement("input");
    keyInput.type = "password";
    keyInput.placeholder = "hf_...";
    keyInput.style.cssText = "width:100%;padding:6px 10px;border:1px solid #ddd;border-radius:6px;font-size:13px;margin-bottom:6px;";

    var saveBtn = document.createElement("button");
    saveBtn.textContent = "Enregistrer";
    saveBtn.style.cssText = "padding:6px 14px;background:#2563eb;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:13px;";

    saveBtn.addEventListener("click", function () {
      var key = keyInput.value.trim();
      if (key) {
        hfToken = key;
        localStorage.setItem(HF_TOKEN_STORAGE, key);
        keyDiv.remove();
        appendMsg("bot", "Token enregistre. Chargement...");
        initChatbot();
      }
    });

    keyInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") saveBtn.click();
    });

    bubble.appendChild(keyInput);
    bubble.appendChild(saveBtn);
    keyDiv.appendChild(bubble);
    messagesEl.appendChild(keyDiv);
    messagesEl.scrollTop = messagesEl.scrollHeight;
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
        if (msg.indexOf("401") !== -1 || msg.indexOf("403") !== -1) {
          hfToken = "";
          localStorage.removeItem(HF_TOKEN_STORAGE);
          msg = "Token invalide. Rechargez la page et reessayez.";
        }
        appendMsg("bot", "Erreur: " + msg);
        isProcessing = false;
        sendBtn.disabled = false;
      });
  }

  // --- Embed query via Transformers.js ---
  function embedQuery(text) {
    return embedder("query: " + text, { pooling: "mean", normalize: true }).then(
      function (output) {
        return Array.from(output.data);
      }
    );
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

  // --- LLM generation via HuggingFace Router (OpenAI-compatible) ---
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

    return fetch(HF_GEN_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + hfToken,
      },
      body: JSON.stringify({
        model: HF_GEN_MODEL,
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userMsg },
        ],
        max_tokens: 1000,
        temperature: 0.3,
      }),
    })
      .then(function (resp) {
        if (!resp.ok) {
          return resp.text().then(function (t) {
            throw new Error("API error " + resp.status + ": " + t);
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
