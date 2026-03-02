"""Shared configuration for IssueRAG pipeline."""

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

# Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"

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

# Minimum relevance score to include a fact in the wiki
MIN_RELEVANCE = 2
