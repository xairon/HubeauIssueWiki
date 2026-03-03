"""Shared configuration for HubEau KB pipeline."""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
RAW_DATA_DIR = BASE_DIR / "raw_data" / "issues"
EXTRACTED_DIR = BASE_DIR / "extracted"
WIKI_DIR = BASE_DIR / "wiki"

# GitHub
GITHUB_REPO = "BRGM/hubeau"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_API_BASE = "https://api.github.com"

# Ollama
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_BIG_MODEL = os.environ.get("OLLAMA_BIG_MODEL", "qwen3:14b")
OLLAMA_SMALL_MODEL = os.environ.get("OLLAMA_SMALL_MODEL", "qwen3.5:4b")
OLLAMA_EMBED_MODEL = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")

# Hub'Eau APIs — used for classification and wiki file mapping
HUBEAU_APIS = {
    "Hydrométrie": "hydrometrie",
    "Piézométrie": "piezometrie",
    "Qualité des cours d'eau": "qualite_cours_eau",
    "Qualité des nappes": "qualite_nappes",
    "Qualité de l'eau potable": "qualite_eau_potable",
    "Poisson": "poisson",
    "Prélèvements en eau": "prelevements",
    "Hydrobiologie": "hydrobiologie",
    "Température des cours d'eau": "temperature",
    "Écoulement des cours d'eau": "ecoulement",
    "Surveillance des eaux littorales": "eaux_littorales",
    "Indicateurs des services": "indicateurs_services",
    "Phytopharmaceutiques": "phytopharmaceutiques",
    "Général": "general",
}

# Aliases for non-canonical API names (LLM sometimes generates these)
HUBEAU_API_ALIASES = {
    "Qualité des nappes d'eau souterraines": "Qualité des nappes",
    "Qualite des nappes d'eau souterraines": "Qualité des nappes",
    "Hydro": "Hydrométrie",
    "API Hydro": "Hydrométrie",
    "API Hydrométrie": "Hydrométrie",
    "API Piézométrie": "Piézométrie",
    "API Qualité des cours d'eau": "Qualité des cours d'eau",
    "API Poisson": "Poisson",
    "Poissons": "Poisson",
    "API Poissons": "Poisson",
    "API Température": "Température des cours d'eau",
    "Température": "Température des cours d'eau",
    "API Écoulement": "Écoulement des cours d'eau",
    "Écoulement": "Écoulement des cours d'eau",
    "API Hydrobiologie": "Hydrobiologie",
    "API Prélèvements": "Prélèvements en eau",
    "Prélèvements": "Prélèvements en eau",
    "Eaux littorales": "Surveillance des eaux littorales",
    "API Eaux littorales": "Surveillance des eaux littorales",
    "Indicateurs services": "Indicateurs des services",
    "API Indicateurs services": "Indicateurs des services",
    "API Phytopharmaceutiques": "Phytopharmaceutiques",
    "API Qualité de l'eau potable": "Qualité de l'eau potable",
    "Eau potable": "Qualité de l'eau potable",
    "Qualité eau potable": "Qualité de l'eau potable",
}

# Minimum relevance score to include a fact in the wiki
MIN_RELEVANCE = 2
