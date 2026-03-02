# IssueRAG

Un outil d'extraction structurée des issues GitHub du projet [Hub'Eau](https://hubeau.eaufrance.fr/) (BRGM) pour générer une base de connaissances technique et métier sur les APIs de données hydrologiques françaises.

## Vue d'ensemble

**IssueRAG** est un pipeline de recherche qui transforme les issues GitHub du projet [BRGM/hubeau](https://github.com/BRGM/hubeau) en une base de connaissances structurée. Le projet extrait automatiquement des faits techniques et du domaine des issues à l'aide du modèle Gemini 2.5 Flash, puis génère une wiki markdown organisée par API et un site web statique accessible via GitHub Pages.

## Comment ça fonctionne

Le pipeline se compose de quatre étapes séquentielles :

1. **Fetch Issues** (`fetch_issues.py`) — Récupère toutes les issues depuis l'API GitHub BRGM/hubeau
2. **Extract Facts** (`extract_facts.py`) — Extrait des faits structurés via Gemini 2.5 Flash LLM
3. **Generate Wiki** (`generate_wiki.py`) — Génère une wiki markdown organisée par catégorie d'API
4. **Build Site** (`build_site.py`) — Construit un site web statique pour GitHub Pages

```
GitHub Issues → Facts Extraction → Markdown Wiki → Static Website
```

## Statistiques clés

- **255 issues** scrappées depuis le dépôt BRGM/hubeau
- **14 catégories d'API** (Hydrométrie, Piézométrie, Qualité des nappes, etc.)
- **Faits catégorisés** en : particularités techniques, connaissances du domaine, problèmes connus, astuces d'utilisation

## Prérequis

- Python 3.10 ou supérieur
- `GITHUB_TOKEN` — Token d'authentification GitHub (générés sur https://github.com/settings/tokens)
- `GEMINI_API_KEY` — Clé API Google Gemini (obtenue sur https://ai.google.dev/)

## Installation

1. Clonez le dépôt
```bash
git clone <url-du-repo>
cd IssueRAG
```

2. Installez les dépendances
```bash
pip install -r requirements.txt
```

3. Configurez les variables d'environnement
```bash
export GITHUB_TOKEN="votre_token_github"
export GEMINI_API_KEY="votre_clé_gemini"
```

## Utilisation

Exécutez le pipeline complet :

```bash
# Étape 1 : Récupérer les issues
python fetch_issues.py

# Étape 2 : Extraire les faits
python extract_facts.py

# Étape 3 : Générer la wiki
python generate_wiki.py

# Étape 4 : Construire le site
python build_site.py
```

Ou exécutez chaque étape individuellement selon vos besoins.

## Structure du projet

```
IssueRAG/
├── fetch_issues.py          # Récupère les issues via l'API GitHub
├── extract_facts.py         # Extrait les faits via Gemini LLM
├── generate_wiki.py         # Génère la wiki markdown
├── build_site.py            # Construit le site statique
├── config.py                # Configuration partagée
├── requirements.txt         # Dépendances (httpx, markdown)
├── raw_data/
│   └── issues/              # Fichiers JSON des issues (cache)
├── extracted/               # Faits extraits (JSON)
├── wiki/                    # Wiki markdown générée
├── site/                    # Site web statique généré
└── README.md                # Ce fichier
```

## Dépendances

- `httpx` — Client HTTP pour l'API GitHub et l'API Gemini
- `markdown` — Conversion Markdown → HTML pour le site statique

## Crédits

**Projet de recherche** — Université de Tours, LIFAT
*Laboratoire d'Informatique Fondamentale et Appliquée de Tours*

## Licence

MIT License — Voir le fichier `LICENSE` pour plus de détails.

---

Pour plus d'informations sur Hub'Eau (BRGM), consultez : https://github.com/BRGM/hubeau
