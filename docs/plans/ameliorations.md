# Cahier des charges — Améliorations du projet HubEau Issue Wiki

> **Date :** 2026-03-03
> **Version :** 1.0
> **Statut :** Proposition

---

## Table des matières

1. [État des lieux](#1-état-des-lieux)
2. [Diagnostic par étape du pipeline](#2-diagnostic-par-étape-du-pipeline)
3. [Améliorations proposées](#3-améliorations-proposées)
4. [Priorisation](#4-priorisation)
5. [Dépendances entre chantiers](#5-dépendances-entre-chantiers)

---

## 1. État des lieux

### Architecture actuelle

```
GitHub Issues (276)
  → fetch_issues.py         # Récupère issues + commentaires
  → extract_facts.py        # LLM (qwen3:14b) → faits structurés JSON
  → synthesize_wiki.py      # LLM (qwen3:14b) → wiki markdown (Guide + Archive)
  → build_site.py           # Markdown → HTML statique + CSS + JS
  → build_embeddings.py     # Wiki chunks + fact chunks → nomic-embed-text (768d)

Navigateur → Nginx (:49506) → /api/* → FastAPI backend (:8000) → Ollama (interne)
                              → /*    → fichiers statiques (site/)
```

### Chiffres clés

| Métrique | Valeur |
|----------|--------|
| Issues GitHub | 276 |
| Issues avec commentaires | ~200 |
| Faits extraits (total) | ~1 029 chunks fact + 307 chunks wiki |
| Embeddings | 1 336 vecteurs (768 dim, ~14 MB) |
| Pages wiki | 14 APIs + index |
| Modèle extraction/synthèse | qwen3:14b |
| Modèle chatbot | qwen3.5:4b |
| Modèle embeddings | nomic-embed-text |

---

## 2. Diagnostic par étape du pipeline

### 2.1 Fetch (`fetch_issues.py`)

**Ce qui fonctionne bien :**
- Récupération complète des issues (ouvertes + fermées) + tous les commentaires
- Cache incrémental (`should_skip` basé sur `updated_at`)
- Gestion du rate limit GitHub

**Ce qui manque :**

| Problème | Impact | Détail |
|----------|--------|--------|
| Pas de réactions (👍 etc.) | Moyen | Signal gratuit de priorité communautaire. Une issue avec 20 thumbs-up est bien plus importante qu'une à 0. |
| Pas de `author_association` | Fort | L'API GitHub renvoie `OWNER`, `COLLABORATOR`, `MEMBER`, `CONTRIBUTOR`, `NONE`. Le compte `Supp-Hubeau` (équipe officielle) n'est pas distingué des utilisateurs lambda. |
| Pas de `html_url` stocké | Faible | Reconstruit à partir du numéro, mais un champ explicite serait plus propre. |
| Labels d'issue non exploités en aval | Moyen | `corrigé / effectué`, `enhancement`, `bug` etc. sont stockés mais jamais utilisés par l'extraction. |

### 2.2 Extraction (`extract_facts.py`)

**Ce qui fonctionne bien :**
- Structure JSON claire (faits techniques + métier + statut + pertinence)
- Normalisation des noms d'API robuste (aliases)
- Fallback si le LLM ne renvoie pas du JSON valide

**Problèmes identifiés :**

#### P1 — Score de pertinence inutile

Sur 255 issues extraites, **247 (96,9 %) ont un score de 3/5**. Le `MIN_RELEVANCE = 2` ne filtre rien. La distribution :

| Score | Nombre | % |
|-------|--------|---|
| 1 | 0 | 0 % |
| 2 | 0 | 0 % |
| 3 | 247 | 96,9 % |
| 4 | 7 | 2,7 % |
| 5 | 1 | 0,4 % |

**Cause :** Le prompt donne des exemples trop vagues (`1=bruit/merci/ça marche, 2=info mineure, 3=utile`). Le LLM met 3 par défaut sur tout ce qui est un peu technique.

#### P2 — Images perdues (15 % des issues)

39 issues contiennent des screenshots (JSON d'erreur, captures d'API, diagrammes). Le LLM reçoit `<img src=.../>` et ne peut rien en extraire.

#### P3 — Pas de champs structurés

Les faits sont du texte libre. Pas d'extraction de :
- Noms d'endpoints (`/v2/hydrometrie/obs_elab`)
- Paramètres (`code_entite`, `date_debut_obs`)
- Codes d'erreur HTTP (500, 404, 206)
- Méthodes HTTP (GET, POST)

Impossible de faire une recherche exacte "quels bugs sur tel endpoint ?".

#### P4 — Statut `résolu` mal inféré

Le prompt inclut `state` et `labels` dans le header mais n'instruit jamais le LLM à s'en servir pour le statut. Parmi les 53 issues labellées `corrigé / effectué`, 11 ont des faits avec des statuts incohérents. Le LLM tente de deviner la résolution à partir du texte des commentaires, ce qui est fragile.

#### P5 — Pas de poids des auteurs

Un commentaire de `Supp-Hubeau` (équipe officielle) a le même poids qu'une question d'utilisateur. Le LLM n'a aucun signal pour distinguer les deux.

### 2.3 Synthèse wiki (`synthesize_wiki.py`)

**Ce qui fonctionne bien :**
- Structure Guide + Archive claire et lisible
- 6 sections bien définies (Comportement actuel, Pièges, Bonnes pratiques, Contexte métier, Évolutions récentes, Historique)
- Archive avec faits bruts + issues sources

**Problèmes identifiés :**

#### P6 — Compression excessive pour les grosses APIs

Hydrométrie a 86 issues (~47K caractères de faits), compressées en sections de "3-10 lignes max". Des faits importants sont nécessairement perdus. Le wiki de l'API Hydrométrie devrait être plus long que celui de l'API Phytopharmaceutiques (2 issues).

#### P7 — Pas de synthèse transverse

Les faits qui touchent plusieurs APIs (CORS, Swagger, package R `hubeau`) sont dupliqués sur chaque page API sans être agrégés dans `general.md`.

#### P8 — Pas de validation du markdown généré

Aucune vérification que les numéros d'issues cités existent, que les faits résolus ne sont pas décrits comme actuels, ou que la structure de sections est respectée.

#### P9 — `generate_wiki.py` est orphelin

Deux générateurs de wiki coexistent. `generate_wiki.py` (bullet points) et `synthesize_wiki.py` (prose synthétisée). Exécuter le premier écraserait le travail du second sans avertissement.

### 2.4 Embeddings (`build_embeddings.py`)

**Ce qui fonctionne bien :**
- Double source (wiki + faits bruts) pour couvrir synthèse et détails
- Chunking sémantique avec limites à 1 000 caractères
- Préfixe `search_document:` / `search_query:` correct pour nomic-embed-text

**Problèmes identifiés :**

#### P10 — Redondance massive

307 chunks wiki + 1 029 chunks fact = ratio 3,35x. Un même fait apparaît au minimum 3 fois dans l'espace d'embeddings :
1. Comme fact chunk brut
2. Dans la section "Faits actuels" de l'archive wiki
3. Dans la prose de synthèse du Guide

Résultat : les top-k slots sont remplis de quasi-doublons sur toute requête pertinente.

#### P11 — Pas de déduplication sémantique

Le même bug (ex: limite de 20 000 résultats Qualité des cours d'eau) apparaît dans 3+ issues. Chaque occurrence produit un chunk embeddings séparé. Pas de clustering avant indexation.

#### P12 — Sections "Issues sources" embedées inutilement

84 chunks proviennent des sections "Issues sources" (listes `- **#NNN** titre — résumé`). Ce sont des listes de liens, pas de contenu sémantique utile. Déjà exclues du search index texte dans `build_site.py` mais pas des embeddings.

#### P13 — Pas d'incrémentalité

Modifier 1 issue → tout ré-extraire, tout re-synthétiser, tout ré-embedder. Le rebuild complet prend ~1h sur GPU.

### 2.5 RAG / Chatbot (`server.py` + `chatbot.js`)

**Ce qui fonctionne bien :**
- Streaming NDJSON propre
- Top-k dynamique (5-12) avec seuil de score
- Déduplication par overlap de mots (fact vs wiki)
- Multi-tour avec historique (4 échanges)
- Ollama non exposé publiquement

**Problèmes identifiés :**

#### P14 — Pas de routage par API

Une question sur "le filtrage dans l'API piézométrie" ramène aussi des chunks de l'API hydrométrie (qui parle aussi de filtrage). Pas de pré-filtre par nom d'API détecté dans la requête.

#### P15 — Déduplication partielle

La dédup par word-overlap ne s'applique qu'aux chunks `source == "fact"`. Les chunks wiki ne sont pas dédupliqués entre eux. Deux sections wiki différentes parlant du même sujet occupent les deux des slots top-k.

#### P16 — Pas de recherche hybride

100 % sémantique. Pas de recherche exacte par endpoint, paramètre ou code d'erreur. Une requête "`date_debut_obs` renvoie erreur 500" ne matchera que par similarité cosinus.

#### P17 — `sessionStorage` perd l'historique à la fermeture d'onglet

Pour une base de connaissances consultée régulièrement, `localStorage` avec bouton clear serait plus adapté.

---

## 3. Améliorations proposées

### A1 — Score de pertinence calibré

**Résout :** P1
**Effort :** Faible (modifier le prompt + re-extraire)

Remplacer la description vague du score par des critères concrets :

```
- pertinence 5 : perte de données, corruption, résultats faux silencieusement
- pertinence 4 : affecte tous les utilisateurs de l'API (erreur 500 systématique, endpoint cassé)
- pertinence 3 : affecte un cas d'usage courant (pagination, filtre spécifique)
- pertinence 2 : cosmétique, documentation, cas d'usage rare
- pertinence 1 : remerciement, question sans réponse, doublon, bruit
```

**Utilisation en aval :**
- `MIN_RELEVANCE = 2` aurait un vrai effet filtrant
- Pondération dans le RAG : `score * (pertinence / 5)`
- Ordre de priorité dans la synthèse wiki

### A2 — Extraction structurée (endpoints, paramètres)

**Résout :** P3, P16 (partiellement)
**Effort :** Moyen (modifier le prompt + le schéma JSON + adapter build_embeddings)

Ajouter au schéma d'extraction :

```json
{
  "endpoints_concernés": ["/v2/hydrometrie/obs_elab"],
  "parametres_concernés": ["code_entite", "date_debut_obs"],
  "codes_erreur": [500, 206],
  "faits_techniques": [...]
}
```

**Utilisation en aval :**
- Recherche exacte dans le RAG (pré-filtre par endpoint/paramètre avant cosinus)
- Index structuré dans le wiki (liste des endpoints connus par API)
- Meilleure chunking : chaque fait embedé avec ses métadonnées structurées

### A3 — Poids des auteurs officiels

**Résout :** P5
**Effort :** Faible (modifier `fetch_issues.py` + prompt d'extraction)

1. Dans `fetch_issues.py`, récupérer `author_association` depuis l'API GitHub pour chaque commentaire
2. Dans le prompt d'extraction, ajouter : *"Les commentaires de contributeurs officiels (`OWNER`, `COLLABORATOR`, `MEMBER`) font autorité sur le statut et la résolution des bugs."*
3. Formatter les commentaires avec un marqueur : `**Supp-Hubeau** [MEMBRE OFFICIEL] (2025-01-15): ...`

### A4 — Déduplication sémantique des faits

**Résout :** P10, P11
**Effort :** Moyen (nouveau script ou étape dans build_embeddings)

**Approche proposée :**

1. Après extraction, regrouper les faits par API
2. Calculer les embeddings de tous les faits d'une API
3. Clustering agglomératif (seuil cosinus ≥ 0.85) → fusionner les clusters en un seul fait représentatif avec la liste des issues sources
4. Embedder uniquement les faits dédupliqués

**Alternative plus simple :** dans `build_embeddings.py`, après calcul des embeddings, supprimer les chunks dont le cosinus avec un chunk déjà retenu dépasse 0.90.

**Gain attendu :** réduction de ~30-40 % du nombre de chunks, amélioration directe de la diversité des résultats RAG.

### A5 — Routage par API dans le RAG

**Résout :** P14
**Effort :** Faible (modifier `server.py`)

1. Détecter le nom d'API dans la requête utilisateur (matching flou contre `HUBEAU_APIS` + aliases)
2. Si une API est détectée : booster les chunks de cette API (multiplier le score cosinus par 1.3) ou filtrer exclusivement
3. Si aucune API détectée : comportement actuel

**Implémentation :** ~20 lignes dans `find_similar()`.

### A6 — Exploitation des labels GitHub

**Résout :** P4 (partiellement)
**Effort :** Faible (modifier le prompt d'extraction)

Ajouter au prompt :

```
- Si l'issue a le label "corrigé / effectué" et est fermée, tous les faits
  techniques décrivant un bug DOIVENT avoir le statut "résolu".
- Si l'issue a le label "enhancement", les faits sont des demandes
  d'évolution : utilise le statut "en_cours" si l'issue est ouverte,
  "résolu" si fermée.
```

### A7 — Pipeline incrémental

**Résout :** P13
**Effort :** Fort (refactoring du pipeline)

**Approche proposée :**

1. `fetch_issues.py` — Déjà incrémental (skip si `updated_at` inchangé). ✅
2. `extract_facts.py` — Ajouter un hash du contenu issue (body + comments) dans le fichier extrait. Ne re-extraire que si le hash change.
3. `synthesize_wiki.py` — Tracker par API quels `issue_number` ont changé. Ne re-synthétiser que les pages API affectées.
4. `build_embeddings.py` — Stocker un mapping `chunk_hash → embedding`. Ne recalculer que les chunks modifiés.

**Gain :** passer de ~1h de rebuild complet à ~5 min pour une mise à jour incrémentale.

### A8 — Synthèse wiki adaptative

**Résout :** P6
**Effort :** Faible (modifier le prompt de synthèse)

Remplacer la contrainte fixe "3-10 lignes max" par une contrainte proportionnelle :

```
- Chaque section fait entre 3 et {max_lines} lignes.
```

Où `max_lines = max(10, issue_count // 3)`. Hydrométrie (86 issues) → 28 lignes max. Phytopharmaceutiques (2 issues) → 10 lignes max.

### A9 — Description des images

**Résout :** P2
**Effort :** Fort (nécessite un modèle vision)

**Option A (recommandée) :** Pré-traitement dans `fetch_issues.py` ou `extract_facts.py` :
1. Détecter les URLs d'images dans le body/commentaires
2. Télécharger l'image
3. Appeler un modèle vision (Qwen2-VL via Ollama, ou llava) pour obtenir une description textuelle
4. Remplacer `<img src=...>` par `[Image: {description}]` dans le texte fourni au LLM d'extraction

**Option B (plus simple) :** Ignorer les images mais ajouter au prompt : *"Si tu vois des balises `<img>`, note qu'une image était présente mais que tu ne peux pas la voir. Utilise le contexte textuel environnant."*

### A10 — Recherche hybride (sémantique + exacte)

**Résout :** P16
**Effort :** Moyen (nécessite A2 comme prérequis)

Avec les champs structurés de A2 disponibles :

1. **Recherche exacte :** si la requête contient un endpoint (`/v2/...`), un paramètre connu, ou un code d'erreur → filtrer d'abord les chunks qui matchent exactement
2. **Recherche sémantique :** cosinus sur le reste
3. **Fusion :** résultats exacts en priorité, complétés par les résultats sémantiques

### A11 — Nettoyage des chunks embeddings

**Résout :** P12, P15
**Effort :** Faible (modifier `build_embeddings.py`)

1. Exclure les sections "Issues sources" des chunks wiki (comme c'est déjà fait pour le search index dans `build_site.py`)
2. Appliquer la déduplication par word-overlap aussi entre chunks wiki (pas seulement fact)

### A12 — Supprimer `generate_wiki.py`

**Résout :** P9
**Effort :** Trivial

`generate_wiki.py` est obsolète depuis l'introduction de `synthesize_wiki.py`. Le supprimer ou le renommer en `generate_wiki_legacy.py` pour éviter toute confusion.

### A13 — Historique persistant (`localStorage`)

**Résout :** P17
**Effort :** Trivial (modifier `chatbot.js`)

Remplacer `sessionStorage` par `localStorage` pour `SESSION_KEY`. Garder le bouton "Clear" pour purge manuelle.

---

## 4. Priorisation

### Tier 1 — Quick wins (effort faible, impact fort)

| # | Amélioration | Effort | Impact |
|---|-------------|--------|--------|
| A1 | Score de pertinence calibré | Faible | Fort — débouche le filtrage et la pondération |
| A6 | Exploitation des labels GitHub | Faible | Fort — corrige les statuts résolu/en_cours |
| A5 | Routage par API dans le RAG | Faible | Fort — précision du chatbot |
| A11 | Nettoyage des chunks embeddings | Faible | Moyen — réduit le bruit dans le RAG |
| A12 | Supprimer `generate_wiki.py` | Trivial | Faible — hygiène du projet |
| A13 | `localStorage` | Trivial | Faible — confort utilisateur |

### Tier 2 — Investissements moyens, impact structurant

| # | Amélioration | Effort | Impact |
|---|-------------|--------|--------|
| A3 | Poids des auteurs officiels | Faible | Moyen — qualité d'extraction |
| A4 | Déduplication sémantique | Moyen | Fort — diversité des résultats RAG |
| A2 | Extraction structurée | Moyen | Fort — ouvre la porte à la recherche hybride |
| A8 | Synthèse wiki adaptative | Faible | Moyen — meilleure couverture wiki |

### Tier 3 — Chantiers lourds

| # | Amélioration | Effort | Impact |
|---|-------------|--------|--------|
| A7 | Pipeline incrémental | Fort | Fort — mais pas bloquant tant qu'on a < 500 issues |
| A10 | Recherche hybride | Moyen | Fort — nécessite A2 |
| A9 | Description des images | Fort | Moyen — concerne 15 % des issues |

### Ordre d'implémentation recommandé

```
Phase 1 (quick wins) :  A1 → A6 → A12 → A13 → A11 → A5
Phase 2 (structurant) : A3 → A8 → A2 → A4
Phase 3 (avancé) :      A10 → A7 → A9
```

Chaque phase est autonome et apporte de la valeur indépendamment des suivantes.

---

## 5. Dépendances entre chantiers

```
A1 (pertinence) ─────────────┐
A6 (labels) ─────────────────┤
                              ├→ re-extraction nécessaire (extract_facts.py --force)
A3 (auteurs officiels) ──────┤
A9 (images) ─────────────────┘
                                    │
                                    ▼
                    A8 (synthèse adaptative) → re-synthèse wiki
                                    │
                                    ▼
A11 (nettoyage chunks) ──┐
A4 (déduplication) ───────┤→ rebuild embeddings
A2 (extraction struct.) ──┘
                              │
                              ▼
                    A5 (routage API) ──┐
                    A10 (hybride) ─────┤→ modifications server.py
                              │
                              ▼
                    A13 (localStorage) → modification chatbot.js
                    A12 (suppr. generate_wiki.py) → standalone
```

**Contrainte forte :** A1 + A6 + A3 nécessitent un `--force` re-extraction de toutes les issues (~1h GPU). Regrouper ces changements de prompt en une seule passe.

**Contrainte :** A10 (recherche hybride) dépend de A2 (extraction structurée). Ne pas commencer A10 avant que A2 soit validé.
