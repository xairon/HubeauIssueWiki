#!/usr/bin/env python3
"""
Static site generator for Hub'Eau knowledge base.
Converts wiki/*.md into a polished static website in site/.
"""

import argparse
import json
import os
import re
import glob

import markdown
from markdown.extensions.toc import TocExtension

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
WIKI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wiki")
SITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

# ---------------------------------------------------------------------------
# Parse the index.md to get ordered API list with issue counts
# ---------------------------------------------------------------------------

def parse_index_for_apis(wiki_dir: str):
    """Return list of dicts: {name, slug, filename, issues}."""
    index_path = os.path.join(wiki_dir, "index.md")
    apis = []
    with open(index_path, encoding="utf-8") as f:
        for line in f:
            # Match lines like: - [Hydrométrie](hydrometrie.md) (87 issues)
            m = re.match(
                r"^-\s+\[(.+?)\]\((.+?\.md)\)\s+\((\d+)\s+issues?\)",
                line.strip(),
            )
            if m:
                name = m.group(1)
                filename = m.group(2)
                issues = int(m.group(3))
                slug = filename.replace(".md", "")
                apis.append(
                    {
                        "name": name,
                        "slug": slug,
                        "filename": filename,
                        "issues": issues,
                    }
                )
    return apis


# ---------------------------------------------------------------------------
# Build search index from markdown source files
# ---------------------------------------------------------------------------

def build_search_index(wiki_dir: str, apis):
    """Extract text from each section of each API page.

    Returns a list of dicts:
      {title, section, text, url, api}
    """
    index_entries = []

    for api in apis:
        filepath = os.path.join(wiki_dir, api["filename"])
        if not os.path.isfile(filepath):
            continue

        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()

        current_section = ""
        in_details = False
        api_name = api["name"]
        slug = api["slug"]

        for line in lines:
            stripped = line.strip()

            # Track <details> block (archive)
            if stripped.startswith("<details"):
                in_details = True
                continue
            if stripped.startswith("</details>"):
                in_details = False
                continue
            if stripped.startswith("<summary") or stripped.startswith("</summary"):
                continue

            # Detect h2/h3 sections
            h2 = re.match(r"^##\s+(.+)", line)
            if h2:
                current_section = h2.group(1).strip()
                continue
            h3 = re.match(r"^###\s+(.+)", line)
            if h3:
                current_section = h3.group(1).strip()
                continue

            if not current_section:
                continue
            # Skip "Issues sources" section
            if current_section == "Issues sources":
                continue

            section_anchor = _section_to_anchor(current_section)

            # Detect bullet points
            bullet = re.match(r"^-\s+(.+)", line)
            if bullet:
                text = bullet.group(1).strip()
                index_entries.append(
                    {
                        "title": api_name,
                        "section": current_section,
                        "text": text,
                        "url": f"{slug}.html#{section_anchor}",
                        "api": api_name,
                    }
                )
                continue

            # Detect prose paragraphs (non-empty, not a heading, not in archive)
            if stripped and not in_details and not stripped.startswith(("#", ">", "---", "-")):
                index_entries.append(
                    {
                        "title": api_name,
                        "section": current_section,
                        "text": stripped,
                        "url": f"{slug}.html#{section_anchor}",
                        "api": api_name,
                    }
                )

    return index_entries


def _section_to_anchor(section: str) -> str:
    """Replicate python-markdown toc anchor generation."""
    anchor = section.lower()
    anchor = re.sub(r"[^\w\s-]", "", anchor)
    anchor = re.sub(r"[\s]+", "-", anchor)
    anchor = anchor.strip("-")
    return anchor


# ---------------------------------------------------------------------------
# Markdown -> HTML conversion
# ---------------------------------------------------------------------------

def convert_md_to_html(filepath: str):
    """Convert a markdown file to HTML body. Returns (html, toc_html, title)."""
    with open(filepath, encoding="utf-8") as f:
        text = f.read()

    # Add markdown="block" to <details> so md_in_html processes inner markdown
    text = text.replace("<details>", '<details markdown="block">')

    md = markdown.Markdown(
        extensions=[
            TocExtension(permalink=False, slugify=_toc_slugify),
            "fenced_code",
            "tables",
            "md_in_html",
        ]
    )
    html = md.convert(text)
    toc = md.toc  # noqa: the toc extension sets this attribute

    # Extract title from first h1
    title_match = re.search(r"<h1[^>]*>(.+?)</h1>", html)
    title = title_match.group(1) if title_match else "Hub'Eau"

    # Post-process: turn issue references (#NNN) into GitHub links
    html = re.sub(
        r"\(#(\d+)\)",
        r'(<a href="https://github.com/BRGM/hubeau/issues/\1">#\1</a>)',
        html,
    )

    # Post-process: rewrite .md links to .html for the static site
    html = re.sub(r'href="([^"]+)\.md"', r'href="\1.html"', html)
    html = re.sub(r'href="([^"]+)\.md#', r'href="\1.html#', html)

    return html, toc, title


def _toc_slugify(value, separator):
    """Custom slugify that matches our _section_to_anchor."""
    value = value.lower()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s]+", separator, value)
    value = value.strip(separator)
    return value


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

def render_page(body_html: str, title: str, apis: list, active_slug: str, wiki_only: bool = False) -> str:
    """Wrap HTML body in the full page template."""
    sidebar_items = []
    for api in apis:
        active_class = ' class="active"' if api["slug"] == active_slug else ""
        sidebar_items.append(
            f'<a href="{api["slug"]}.html"{active_class}>'
            f'<span class="api-name">{api["name"]}</span>'
            f'<span class="issue-count">{api["issues"]}</span>'
            f"</a>"
        )
    sidebar_html = "\n".join(sidebar_items)

    is_index = active_slug == "index"
    index_active = ' class="active"' if is_index else ""

    chatbot_html = "" if wiki_only else """    <!-- Chatbot toggle button -->
    <button class="chatbot-toggle" id="chatbotToggle" aria-label="Ouvrir le chatbot">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
    </button>

    <!-- Chatbot panel -->
    <div class="chatbot-panel" id="chatbotPanel">
        <div class="chatbot-header">
            <div class="chatbot-header-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                Hub'Eau Assistant
            </div>
            <div class="chatbot-header-actions">
                <button class="chatbot-clear" id="chatbotClear" title="Effacer la conversation">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                </button>
                <button class="chatbot-close" id="chatbotClose">&times;</button>
            </div>
        </div>
        <div class="chatbot-messages" id="chatbotMessages">
            <div class="chat-msg chat-msg-bot">
                <div class="chat-bubble">Bonjour ! Posez-moi une question sur les APIs Hub'Eau. Je cherche dans la base de connaissances pour vous r&eacute;pondre.</div>
            </div>
        </div>
        <div class="chatbot-status" id="chatbotStatus" style="display:none;"></div>
        <div class="chatbot-input-area">
            <input type="text" id="chatbotInput" placeholder="Posez votre question..." autocomplete="off">
            <button class="chatbot-send" id="chatbotSend">Envoyer</button>
        </div>
    </div>"""

    chatbot_script = "" if wiki_only else '\n    <script src="chatbot.js"></script>'

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Hub'Eau Knowledge Base</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Mobile hamburger -->
    <button class="hamburger" id="hamburger" aria-label="Ouvrir le menu">
        <span></span><span></span><span></span>
    </button>

    <!-- Sidebar overlay for mobile -->
    <div class="sidebar-overlay" id="sidebarOverlay"></div>

    <!-- Sidebar -->
    <nav class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <a href="index.html" class="sidebar-logo">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
                    <path d="M8 12c0-2 1-4 4-4s4 2 4 4-1 4-4 4-4-2-4-4z" fill="currentColor" opacity="0.3"/>
                </svg>
                <span>Hub'Eau KB</span>
            </a>
        </div>
        <div class="sidebar-section-title">APIs</div>
        <div class="sidebar-links">
            <a href="index.html"{index_active}>
                <span class="api-name">Accueil</span>
                <span class="issue-count home-icon">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
                </span>
            </a>
            {sidebar_html}
        </div>
        <div class="sidebar-footer-text">
            Base de connaissances
        </div>
    </nav>

    <!-- Main content -->
    <main class="main">
        <div class="topbar">
            <div class="search-container">
                <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
                </svg>
                <input type="text" id="searchInput" placeholder="Rechercher dans la base de connaissances..." autocomplete="off">
                <div class="search-results" id="searchResults"></div>
            </div>
        </div>

        <article class="content">
            {body_html}
        </article>

        <footer class="footer">
            <p>Projet de recherche &mdash; Universit&eacute; de Tours, LIFAT</p>
            <p class="footer-sub">Donn&eacute;es extraites automatiquement des issues GitHub <a href="https://github.com/BRGM/hubeau">BRGM/hubeau</a></p>
        </footer>
    </main>

{chatbot_html}

    <script src="search.js"></script>{chatbot_script}
    <script>
        // Hamburger menu toggle
        const hamburger = document.getElementById('hamburger');
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebarOverlay');
        hamburger.addEventListener('click', () => {{
            sidebar.classList.toggle('open');
            overlay.classList.toggle('open');
            hamburger.classList.toggle('open');
        }});
        overlay.addEventListener('click', () => {{
            sidebar.classList.remove('open');
            overlay.classList.remove('open');
            hamburger.classList.remove('open');
        }});
    </script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

STYLE_CSS = """\
/* ============================================================
   Hub'Eau Knowledge Base - Style Sheet
   ============================================================ */

/* --- Reset & Base --- */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --primary: #2563eb;
    --primary-light: #3b82f6;
    --dark: #1a365d;
    --dark-hover: #1e3f6e;
    --light-bg: #f8fafc;
    --text: #1e293b;
    --text-light: #64748b;
    --accent: #0ea5e9;
    --border: #e2e8f0;
    --sidebar-width: 280px;
    --topbar-height: 64px;
    --radius: 8px;
    --shadow: 0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.06);
    --shadow-lg: 0 10px 30px rgba(0,0,0,.12);
}

html { scroll-behavior: smooth; }

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 16px;
    line-height: 1.7;
    color: var(--text);
    background: var(--light-bg);
}

/* --- Sidebar --- */
.sidebar {
    position: fixed;
    top: 0; left: 0;
    width: var(--sidebar-width);
    height: 100vh;
    background: var(--dark);
    color: #fff;
    overflow-y: auto;
    z-index: 100;
    display: flex;
    flex-direction: column;
    transition: transform .3s ease;
}

.sidebar-header {
    padding: 24px 20px 16px;
    border-bottom: 1px solid rgba(255,255,255,.08);
}

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #fff;
    text-decoration: none;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: -.3px;
}

.sidebar-section-title {
    padding: 16px 20px 8px;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: rgba(255,255,255,.4);
    font-weight: 600;
}

.sidebar-links {
    flex: 1;
    overflow-y: auto;
    padding-bottom: 16px;
}

.sidebar-links a {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 9px 20px;
    color: rgba(255,255,255,.75);
    text-decoration: none;
    font-size: 14px;
    transition: background .15s, color .15s;
    border-left: 3px solid transparent;
}

.sidebar-links a:hover {
    background: var(--dark-hover);
    color: #fff;
}

.sidebar-links a.active {
    background: rgba(37, 99, 235, .25);
    color: #fff;
    border-left-color: var(--accent);
    font-weight: 600;
}

.api-name {
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-right: 8px;
}

.issue-count {
    font-size: 11px;
    background: rgba(255,255,255,.12);
    color: rgba(255,255,255,.7);
    padding: 2px 8px;
    border-radius: 10px;
    font-weight: 600;
    flex-shrink: 0;
}

.home-icon {
    background: none;
    padding: 0;
    display: flex;
    align-items: center;
}

.sidebar-footer-text {
    padding: 16px 20px;
    font-size: 11px;
    color: rgba(255,255,255,.3);
    border-top: 1px solid rgba(255,255,255,.06);
    text-align: center;
}

/* --- Main content --- */
.main {
    margin-left: var(--sidebar-width);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* --- Topbar / Search --- */
.topbar {
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(248, 250, 252, .85);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
    padding: 12px 32px;
    display: flex;
    align-items: center;
    height: var(--topbar-height);
}

.search-container {
    position: relative;
    width: 100%;
    max-width: 560px;
}

.search-icon {
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-light);
    pointer-events: none;
}

#searchInput {
    width: 100%;
    padding: 10px 16px 10px 42px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    font-size: 14px;
    font-family: inherit;
    background: #fff;
    color: var(--text);
    transition: border-color .2s, box-shadow .2s;
    outline: none;
}

#searchInput:focus {
    border-color: var(--primary-light);
    box-shadow: 0 0 0 3px rgba(37,99,235,.12);
}

#searchInput::placeholder { color: var(--text-light); }

.search-results {
    display: none;
    position: absolute;
    top: calc(100% + 6px);
    left: 0; right: 0;
    background: #fff;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow-lg);
    max-height: 420px;
    overflow-y: auto;
    z-index: 200;
}

.search-results.visible { display: block; }

.search-result-item {
    display: block;
    padding: 10px 16px;
    text-decoration: none;
    color: var(--text);
    border-bottom: 1px solid var(--border);
    transition: background .1s;
}

.search-result-item:last-child { border-bottom: none; }
.search-result-item:hover { background: #f1f5f9; }

.search-result-tags {
    display: flex;
    gap: 6px;
    margin-bottom: 4px;
    flex-wrap: wrap;
}

.search-tag {
    font-size: 11px;
    font-weight: 600;
    padding: 1px 7px;
    border-radius: 4px;
}

.search-tag-api {
    background: #dbeafe;
    color: #1d4ed8;
}

.search-tag-section {
    background: #e0f2fe;
    color: #0369a1;
}

.search-result-text {
    font-size: 13px;
    color: var(--text-light);
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.search-no-results {
    padding: 20px 16px;
    text-align: center;
    color: var(--text-light);
    font-size: 14px;
}

/* --- Article content --- */
.content {
    flex: 1;
    max-width: 900px;
    width: 100%;
    margin: 0 auto;
    padding: 40px 32px;
}

.content h1 {
    font-size: 2em;
    font-weight: 800;
    color: var(--dark);
    margin-bottom: 8px;
    letter-spacing: -.5px;
    line-height: 1.2;
}

.content h2 {
    font-size: 1.4em;
    font-weight: 700;
    color: var(--dark);
    margin-top: 2em;
    margin-bottom: 0.6em;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--border);
}

.content h3 {
    font-size: 1.15em;
    font-weight: 600;
    color: var(--text);
    margin-top: 1.5em;
    margin-bottom: 0.4em;
}

.content p {
    margin-bottom: 1em;
}

.content a {
    color: var(--accent);
    text-decoration: none;
    font-weight: 500;
    transition: color .15s;
}

.content a:hover {
    color: var(--primary);
    text-decoration: underline;
}

.content ul, .content ol {
    margin: 0.5em 0 1.2em 1.5em;
}

.content li {
    margin-bottom: 0.5em;
    line-height: 1.65;
}

.content li::marker {
    color: var(--primary-light);
}

.content code {
    font-family: "SF Mono", "Fira Code", "Fira Mono", "Roboto Mono", Menlo, Consolas, monospace;
    font-size: 0.88em;
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 4px;
    color: #be185d;
}

.content pre {
    background: #1e293b;
    color: #e2e8f0;
    padding: 16px 20px;
    border-radius: var(--radius);
    overflow-x: auto;
    margin: 1em 0 1.5em;
    font-size: 14px;
    line-height: 1.6;
}

.content pre code {
    background: none;
    padding: 0;
    color: inherit;
    font-size: inherit;
}

.content table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0 1.5em;
    font-size: 14px;
}

.content th, .content td {
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid var(--border);
}

.content th {
    background: #f1f5f9;
    font-weight: 600;
    color: var(--dark);
}

.content tr:hover td { background: #f8fafc; }

.content hr {
    border: none;
    border-top: 2px solid var(--border);
    margin: 2.5em 0;
}

.content strong { color: var(--dark); }

/* Index page cards */
.content li a {
    font-weight: 600;
}

/* --- Footer --- */
.footer {
    padding: 24px 32px;
    text-align: center;
    border-top: 1px solid var(--border);
    background: #fff;
    font-size: 13px;
    color: var(--text-light);
    margin-top: auto;
}

.footer p { margin: 2px 0; }

.footer a {
    color: var(--accent);
    text-decoration: none;
    font-weight: 600;
}

.footer-sub { font-size: 12px; }

/* --- Hamburger --- */
.hamburger {
    display: none;
    position: fixed;
    top: 14px; left: 14px;
    z-index: 200;
    width: 40px; height: 40px;
    background: var(--dark);
    border: none;
    border-radius: var(--radius);
    cursor: pointer;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 5px;
    box-shadow: var(--shadow);
}

.hamburger span {
    display: block;
    width: 20px; height: 2px;
    background: #fff;
    border-radius: 2px;
    transition: transform .3s, opacity .3s;
}

.hamburger.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.hamburger.open span:nth-child(2) { opacity: 0; }
.hamburger.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }

.sidebar-overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,.4);
    z-index: 90;
}

/* --- Responsive --- */
@media (max-width: 768px) {
    .hamburger { display: flex; }

    .sidebar {
        transform: translateX(-100%);
    }

    .sidebar.open {
        transform: translateX(0);
    }

    .sidebar-overlay.open { display: block; }

    .main {
        margin-left: 0;
    }

    .topbar {
        padding: 12px 16px 12px 60px;
    }

    .content {
        padding: 24px 16px;
    }
}

@media (max-width: 480px) {
    .content h1 { font-size: 1.6em; }
    .content h2 { font-size: 1.2em; }
}

/* --- Details/Archive section --- */
details {
    margin: 1.5em 0;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: #fff;
}

details summary {
    padding: 14px 20px;
    cursor: pointer;
    font-size: 15px;
    color: var(--dark);
    background: #f8fafc;
    border-radius: var(--radius);
    transition: background .15s;
    list-style: none;
}

details summary::-webkit-details-marker { display: none; }

details summary::before {
    content: "\\25B6";
    display: inline-block;
    margin-right: 10px;
    font-size: 11px;
    transition: transform .2s;
    color: var(--text-light);
}

details[open] summary::before {
    transform: rotate(90deg);
}

details summary:hover {
    background: #f1f5f9;
}

details[open] summary {
    border-bottom: 1px solid var(--border);
    border-radius: var(--radius) var(--radius) 0 0;
}

details > *:not(summary) {
    padding: 0 20px;
}

details > h3, details > h4 {
    padding: 0 20px;
}

/* Strikethrough for resolved facts */
.content li del {
    color: var(--text-light);
    text-decoration: line-through;
}

/* --- Chatbot --- */
.chatbot-toggle {
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: var(--primary);
    color: #fff;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(37, 99, 235, .35);
    z-index: 300;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform .2s, box-shadow .2s;
}

.chatbot-toggle:hover {
    transform: scale(1.08);
    box-shadow: 0 6px 24px rgba(37, 99, 235, .45);
}

.chatbot-toggle svg { pointer-events: none; }

.chatbot-panel {
    display: none;
    position: fixed;
    bottom: 92px;
    right: 24px;
    width: 420px;
    max-height: 540px;
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 16px;
    box-shadow: 0 12px 40px rgba(0,0,0,.15);
    z-index: 300;
    flex-direction: column;
    overflow: hidden;
}

.chatbot-panel.open { display: flex; }

.chatbot-header {
    padding: 16px 20px;
    background: var(--dark);
    color: #fff;
    font-weight: 600;
    font-size: 15px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.chatbot-header-title {
    display: flex;
    align-items: center;
    gap: 8px;
}

.chatbot-header-actions {
    display: flex;
    align-items: center;
    gap: 8px;
}

.chatbot-clear {
    background: none;
    border: none;
    color: rgba(255,255,255,.5);
    cursor: pointer;
    padding: 4px;
    display: flex;
    align-items: center;
    transition: color .15s;
    border-radius: 4px;
}

.chatbot-clear:hover { color: #fff; background: rgba(255,255,255,.1); }

.chatbot-close {
    background: none;
    border: none;
    color: rgba(255,255,255,.7);
    cursor: pointer;
    font-size: 20px;
    padding: 0 4px;
    transition: color .15s;
}

.chatbot-close:hover { color: #fff; }

.chatbot-messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    min-height: 200px;
    max-height: 360px;
}

.chat-msg {
    margin-bottom: 12px;
    display: flex;
    gap: 8px;
}

.chat-msg-user { justify-content: flex-end; }

.chat-bubble {
    max-width: 85%;
    padding: 10px 14px;
    border-radius: 12px;
    font-size: 14px;
    line-height: 1.55;
}

.chat-msg-user .chat-bubble {
    background: var(--primary);
    color: #fff;
    border-bottom-right-radius: 4px;
}

.chat-msg-bot .chat-bubble {
    background: #f1f5f9;
    color: var(--text);
    border-bottom-left-radius: 4px;
}

.chat-bubble a {
    color: var(--accent);
    text-decoration: underline;
}

.chat-msg-user .chat-bubble a { color: #bfdbfe; }

.chat-sources {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid rgba(0,0,0,.08);
    font-size: 12px;
    color: var(--text-light);
}

.chat-sources a { font-weight: 500; }

.chat-typing {
    display: flex;
    gap: 4px;
    padding: 8px 12px;
}

.chat-typing span {
    width: 6px; height: 6px;
    background: var(--text-light);
    border-radius: 50%;
    animation: chatTyping .6s infinite alternate;
}

.chat-typing span:nth-child(2) { animation-delay: .2s; }
.chat-typing span:nth-child(3) { animation-delay: .4s; }

@keyframes chatTyping {
    from { opacity: .3; transform: translateY(0); }
    to { opacity: 1; transform: translateY(-3px); }
}

.chatbot-input-area {
    padding: 12px 16px;
    border-top: 1px solid var(--border);
    display: flex;
    gap: 8px;
}

.chatbot-input-area input {
    flex: 1;
    padding: 10px 14px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    font-size: 14px;
    font-family: inherit;
    outline: none;
    transition: border-color .2s;
}

.chatbot-input-area input:focus { border-color: var(--primary-light); }

.chatbot-send {
    padding: 8px 16px;
    background: var(--primary);
    color: #fff;
    border: none;
    border-radius: var(--radius);
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: background .15s;
}

.chatbot-send:hover { background: var(--primary-light); }
.chatbot-send:disabled { opacity: .5; cursor: not-allowed; }

.chatbot-status {
    padding: 8px 16px;
    font-size: 12px;
    color: var(--text-light);
    text-align: center;
    background: #fefce8;
    border-top: 1px solid #fef08a;
}

@media (max-width: 768px) {
    .chatbot-panel {
        bottom: 0; right: 0; left: 0;
        width: 100%;
        max-height: 80vh;
        border-radius: 16px 16px 0 0;
    }
    .chatbot-toggle { bottom: 16px; right: 16px; }
}

/* --- Search highlight --- */
mark {
    background: #fef08a;
    color: inherit;
    padding: 0 1px;
    border-radius: 2px;
}
"""

# ---------------------------------------------------------------------------
# JavaScript: search
# ---------------------------------------------------------------------------

SEARCH_JS = r"""(function() {
    'use strict';

    var searchIndex = [];
    var debounceTimer = null;
    var input = document.getElementById('searchInput');
    var resultsContainer = document.getElementById('searchResults');

    // Load search index
    fetch('search-index.json')
        .then(function(r) { return r.json(); })
        .then(function(data) { searchIndex = data; })
        .catch(function() { console.warn('Could not load search index.'); });

    // Debounced search
    input.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        var val = this.value.trim();
        debounceTimer = setTimeout(function() { performSearch(val); }, 200);
    });

    // Close results on click outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-container')) {
            resultsContainer.classList.remove('visible');
        }
    });

    // Re-open on focus if there is a query
    input.addEventListener('focus', function() {
        if (this.value.trim().length > 0 && resultsContainer.children.length > 0) {
            resultsContainer.classList.add('visible');
        }
    });

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.textContent;
    }

    function performSearch(query) {
        // Clear previous results
        while (resultsContainer.firstChild) {
            resultsContainer.removeChild(resultsContainer.firstChild);
        }

        if (query.length < 2) {
            resultsContainer.classList.remove('visible');
            return;
        }

        var lowerQ = query.toLowerCase();
        var matches = searchIndex.filter(function(entry) {
            return entry.text.toLowerCase().indexOf(lowerQ) !== -1 ||
                   entry.title.toLowerCase().indexOf(lowerQ) !== -1 ||
                   entry.section.toLowerCase().indexOf(lowerQ) !== -1;
        }).slice(0, 20);

        if (matches.length === 0) {
            var noRes = document.createElement('div');
            noRes.className = 'search-no-results';
            noRes.textContent = 'Aucun r\u00e9sultat trouv\u00e9';
            resultsContainer.appendChild(noRes);
            resultsContainer.classList.add('visible');
            return;
        }

        matches.forEach(function(entry) {
            var item = document.createElement('a');
            item.className = 'search-result-item';
            item.href = entry.url;

            // Tags row
            var tagsDiv = document.createElement('div');
            tagsDiv.className = 'search-result-tags';

            var apiTag = document.createElement('span');
            apiTag.className = 'search-tag search-tag-api';
            apiTag.textContent = entry.api;
            tagsDiv.appendChild(apiTag);

            var secTag = document.createElement('span');
            secTag.className = 'search-tag search-tag-section';
            secTag.textContent = entry.section;
            tagsDiv.appendChild(secTag);

            item.appendChild(tagsDiv);

            // Text with highlighting via DOM
            var displayText = entry.text;
            if (displayText.length > 160) {
                var idx = displayText.toLowerCase().indexOf(lowerQ);
                if (idx > 60) {
                    displayText = '...' + displayText.substring(idx - 40);
                }
                if (displayText.length > 160) {
                    displayText = displayText.substring(0, 157) + '...';
                }
            }

            var textDiv = document.createElement('div');
            textDiv.className = 'search-result-text';

            // Split on query matches and build text nodes + mark elements
            var escapedQ = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            var regex = new RegExp('(' + escapedQ + ')', 'gi');
            var parts = displayText.split(regex);
            parts.forEach(function(part) {
                if (part.toLowerCase() === query.toLowerCase()) {
                    var mark = document.createElement('mark');
                    mark.textContent = part;
                    textDiv.appendChild(mark);
                } else {
                    textDiv.appendChild(document.createTextNode(part));
                }
            });

            item.appendChild(textDiv);
            resultsContainer.appendChild(item);
        });

        resultsContainer.classList.add('visible');
    }
})();
"""


# ---------------------------------------------------------------------------
# Main build logic
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Build Hub'Eau static site")
    parser.add_argument("--wiki-only", action="store_true",
                        help="Build wiki-only (no chatbot, no embeddings)")
    args = parser.parse_args()
    wiki_only = args.wiki_only

    if wiki_only:
        print("=== Wiki-only mode (no chatbot) ===")

    os.makedirs(SITE_DIR, exist_ok=True)

    # 1. Parse API list from index
    apis = parse_index_for_apis(WIKI_DIR)
    print(f"Found {len(apis)} APIs in index.md")

    # 2. Build search index
    search_index = build_search_index(WIKI_DIR, apis)
    search_index_path = os.path.join(SITE_DIR, "search-index.json")
    with open(search_index_path, "w", encoding="utf-8") as f:
        json.dump(search_index, f, ensure_ascii=False, indent=2)
    print(f"Search index: {len(search_index)} entries -> search-index.json")

    # 3. Write static assets
    css_path = os.path.join(SITE_DIR, "style.css")
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(STYLE_CSS)
    print("Wrote style.css")

    js_path = os.path.join(SITE_DIR, "search.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(SEARCH_JS)
    print("Wrote search.js")

    # Copy chatbot.js (skip in wiki-only mode)
    if not wiki_only:
        chatbot_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot.js")
        if os.path.isfile(chatbot_src):
            import shutil
            shutil.copy2(chatbot_src, os.path.join(SITE_DIR, "chatbot.js"))
            print("Copied chatbot.js")

    # 4. Convert each wiki page to HTML
    # Start with index.md
    md_files = [os.path.join(WIKI_DIR, "index.md")]
    for api in apis:
        fp = os.path.join(WIKI_DIR, api["filename"])
        if os.path.isfile(fp):
            md_files.append(fp)

    for md_path in md_files:
        basename = os.path.basename(md_path)
        slug = basename.replace(".md", "")

        body_html, toc_html, title = convert_md_to_html(md_path)

        page_html = render_page(
            body_html=body_html,
            title=title,
            apis=apis,
            active_slug=slug,
            wiki_only=wiki_only,
        )

        out_path = os.path.join(SITE_DIR, f"{slug}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"  {basename} -> {slug}.html")

    # In wiki-only mode, remove chatbot artifacts from site/ if present
    if wiki_only:
        for artifact in ("chatbot.js", "embeddings.json"):
            artifact_path = os.path.join(SITE_DIR, artifact)
            if os.path.isfile(artifact_path):
                os.remove(artifact_path)
                print(f"Removed {artifact} (wiki-only mode)")

    print(f"\nBuild complete! {len(md_files)} pages in {SITE_DIR}/")


if __name__ == "__main__":
    main()
