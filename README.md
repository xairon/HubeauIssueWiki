# HubEau KB

Un outil d'extraction structurée des issues GitHub du projet [Hub'Eau](https://hubeau.eaufrance.fr/) (BRGM) pour générer une base de connaissances technique et métier sur les APIs de données hydrologiques françaises.

## Vue d'ensemble

**HubEau KB** est un pipeline de recherche qui transforme les issues GitHub du projet [BRGM/hubeau](https://github.com/BRGM/hubeau) en une base de connaissances structurée. Le projet extrait automatiquement des faits techniques et du domaine des issues à l'aide du modèle Gemini 2.5 Flash, puis génère une wiki markdown organisée par API et un site web statique.

## Deux modes de déploiement

| Mode | Contenu | Déploiement |
|------|---------|-------------|
| **Wiki statique** (GitLab Pages) | Wiki + recherche, sans chatbot | Automatique via CI sur `master` |
| **Site complet** (Docker local) | Wiki + recherche + chatbot RAG (Ollama) | `docker compose --profile serve up -d site` sur port **49506** |

## Comment ça fonctionne

Le pipeline se compose de quatre étapes séquentielles :

1. **Fetch Issues** (`fetch_issues.py`) — Récupère toutes les issues depuis l'API GitHub BRGM/hubeau
2. **Extract Facts** (`extract_facts.py`) — Extrait des faits structurés via Gemini 2.5 Flash LLM
3. **Generate Wiki** (`generate_wiki.py`) — Génère une wiki markdown organisée par catégorie d'API
4. **Build Site** (`build_site.py`) — Construit un site web statique
5. **Build Embeddings** (`build_embeddings.py`) — Génère les embeddings pour le chatbot RAG (optionnel)

```
GitHub Issues → Facts Extraction → Markdown Wiki → Static Website
                                                  → Embeddings (RAG)
```

## Statistiques clés

- **255 issues** scrappées depuis le dépôt BRGM/hubeau
- **14 catégories d'API** (Hydrométrie, Piézométrie, Qualité des nappes, etc.)
- **Faits catégorisés** en : particularités techniques, connaissances du domaine, problèmes connus, astuces d'utilisation

## Prérequis

- Python 3.10 ou supérieur
- `GITHUB_TOKEN` — Token d'authentification GitHub
- `GEMINI_API_KEY` — Clé API Google Gemini (pour l'extraction de faits)
- Docker + Docker Compose (pour le déploiement local avec chatbot)
- GPU NVIDIA recommandé (pour Ollama)

## Installation

1. Clonez le dépôt
```bash
git clone https://scm.univ-tours.fr/ringuet/hubeauissuewiki.git
cd hubeauissuewiki
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

### Pipeline complet

```bash
python fetch_issues.py        # Récupérer les issues
python extract_facts.py       # Extraire les faits
python generate_wiki.py       # Générer la wiki
python build_site.py          # Construire le site (complet, avec chatbot)
python build_embeddings.py    # Générer les embeddings RAG
```

### Build wiki-only (pour GitLab Pages)

```bash
python build_site.py --wiki-only
```

Ce mode exclut le chatbot (HTML, JS, embeddings) pour un déploiement statique léger.

### Déploiement local avec chatbot RAG

```bash
# Lancer Ollama + le site web
docker compose --profile serve up -d site

# Le site est accessible sur http://localhost:49506
# Le chatbot utilise Ollama sur http://localhost:11434
```

### Pipeline de données (dans Docker)

```bash
docker compose --profile pipeline run pipeline
```

## Structure du projet

```
hubeauissuewiki/
├── fetch_issues.py          # Récupère les issues via l'API GitHub
├── extract_facts.py         # Extrait les faits via Gemini LLM
├── generate_wiki.py         # Génère la wiki markdown
├── build_site.py            # Construit le site statique (--wiki-only disponible)
├── build_embeddings.py      # Génère les embeddings pour le chatbot RAG
├── chatbot.js               # Chatbot RAG côté client (streaming, Ollama)
├── config.py                # Configuration partagée
├── requirements.txt         # Dépendances Python
├── docker-compose.yml       # Ollama + Nginx (site) + Pipeline
├── Dockerfile               # Image du pipeline
├── .gitlab-ci.yml           # CI/CD : build wiki-only → GitLab Pages
├── raw_data/
│   └── issues/              # Fichiers JSON des issues (cache)
├── extracted/               # Faits extraits (JSON)
├── wiki/                    # Wiki markdown générée
├── site/                    # Site web statique généré
└── README.md                # Ce fichier
```

## GitLab Pages

Le CI/CD (`.gitlab-ci.yml`) déploie automatiquement le wiki statique (sans chatbot) sur GitLab Pages à chaque push sur `master`. Le build utilise `--wiki-only` pour exclure les composants chatbot et les embeddings volumineux (~14 Mo).

## Crédits

**Projet de recherche** — Université de Tours, LIFAT
*Laboratoire d'Informatique Fondamentale et Appliquée de Tours*

## Licence

MIT License — Voir le fichier `LICENSE` pour plus de détails.

---

Pour plus d'informations sur Hub'Eau (BRGM), consultez : https://github.com/BRGM/hubeau
