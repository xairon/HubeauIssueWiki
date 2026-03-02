# IssueRAG — Design Document

## Objectif

Scraper toutes les issues du repo GitHub [BRGM/hubeau](https://github.com/BRGM/hubeau/issues) et en extraire des faits structurés — particularités techniques de l'API et informations métier hydrologiques — organisés en wiki markdown par API.

## Décisions

- **Format de sortie** : Markdown wiki (un fichier .md par API Hub'Eau)
- **Méthode d'extraction** : LLM (Claude API via Anthropic SDK, modèle Haiku)
- **Organisation** : Par API + sous-sections (technique, métier, problèmes, tips)
- **Auth GitHub** : Token via variable d'environnement `GITHUB_TOKEN`
- **Stack** : Python (httpx + anthropic)
- **Architecture** : Pipeline séquentiel en 3 étapes indépendantes

## Volumétrie

- ~276 issues, 47 ouvertes
- Labels existants : bug, données, enhancement, information, question, corrigé/effectué
- Contenu en français

## Architecture

```
fetch_issues.py → raw_data/ (JSON) → extract_facts.py (Claude) → wiki/ (Markdown)
```

3 scripts indépendants, chacun rejouable séparément.

## Structure du projet

```
IssueRAG/
├── fetch_issues.py          # Étape 1 : récupère les issues GitHub
├── extract_facts.py         # Étape 2 : extraction des faits via Claude
├── generate_wiki.py         # Étape 3 : génère le wiki markdown
├── config.py                # Config partagée (repo, paths, modèle Claude)
├── requirements.txt         # httpx, anthropic
├── raw_data/                # Issues brutes en JSON (cache)
│   └── issues/
│       ├── 001.json
│       └── ...
├── extracted/               # Faits extraits par issue (JSON)
│   └── 001_facts.json
└── wiki/                    # Wiki markdown généré
    ├── index.md
    ├── hydrometrie.md
    ├── piezometrie.md
    ├── qualite_eau.md
    ├── poisson.md
    ├── prelevements.md
    ├── general.md
    └── non_classe.md
```

## Étape 1 — Fetch (fetch_issues.py)

- Lit `GITHUB_TOKEN` depuis l'environnement
- Pagine `GET /repos/BRGM/hubeau/issues?state=all&per_page=100`
- Pour chaque issue, récupère les commentaires via `GET /issues/{n}/comments`
- Sauvegarde un JSON par issue dans `raw_data/issues/{number}.json`
- Contenu du JSON : titre, body, labels, état, auteur, dates, commentaires complets
- **Incrémental** : skip si le fichier existe et que `updated_at` n'a pas changé
- Gestion du rate limiting via header `X-RateLimit-Remaining`

## Étape 2 — Extract (extract_facts.py)

- Lit chaque JSON de `raw_data/issues/`
- Envoie à Claude (Haiku) avec un prompt structuré demandant :
  - `api_concernee` : quelle(s) API Hub'Eau ou "Général"
  - `faits_techniques` : comportement API (limites, erreurs, formats, paramètres)
  - `faits_metier` : hydrologie/données (codes BSS, stations, mesures)
  - `statut` : résolu / en cours / information
  - `pertinence` : score 1-5 (filtre le bruit)
- Sauvegarde en `extracted/{number}_facts.json`
- Skip les issues déjà extraites (sauf `--force`)

## Étape 3 — Generate (generate_wiki.py)

- Lit tous les `extracted/*_facts.json`
- Filtre par pertinence (>= 2)
- Regroupe par `api_concernee`
- Génère un fichier markdown par API avec 4 sous-sections :
  - Particularités techniques
  - Informations métier
  - Problèmes connus
  - Tips d'utilisation
- Déduplique les faits similaires
- Génère `wiki/index.md` comme sommaire

## Dépendances

- `httpx` — client HTTP async-ready
- `anthropic` — SDK Claude
- Python 3.10+
