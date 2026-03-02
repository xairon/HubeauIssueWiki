"""Fetch all issues and comments from BRGM/hubeau GitHub repo."""

import json
import time

import httpx

from config import GITHUB_API_BASE, GITHUB_REPO, GITHUB_TOKEN, RAW_DATA_DIR


def get_headers() -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def handle_rate_limit(response: httpx.Response) -> None:
    remaining = int(response.headers.get("X-RateLimit-Remaining", 1))
    if remaining == 0:
        reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
        wait = max(reset_time - int(time.time()), 1)
        print(f"  Rate limited. Waiting {wait}s...")
        time.sleep(wait)


def fetch_all_issues(client: httpx.Client) -> list[dict]:
    """Fetch all issues (open + closed), paginated."""
    all_issues = []
    page = 1
    while True:
        url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/issues"
        params = {"state": "all", "per_page": 100, "page": page}
        resp = client.get(url, params=params)
        resp.raise_for_status()
        handle_rate_limit(resp)

        issues = resp.json()
        if not issues:
            break

        # Filter out pull requests (GitHub API returns PRs as issues too)
        issues = [i for i in issues if "pull_request" not in i]
        all_issues.extend(issues)
        print(f"  Page {page}: fetched {len(issues)} issues (total: {len(all_issues)})")
        page += 1

    return all_issues


def fetch_comments(client: httpx.Client, issue_number: int) -> list[dict]:
    """Fetch all comments for a given issue."""
    comments = []
    page = 1
    while True:
        url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/issues/{issue_number}/comments"
        params = {"per_page": 100, "page": page}
        resp = client.get(url, params=params)
        resp.raise_for_status()
        handle_rate_limit(resp)

        page_comments = resp.json()
        if not page_comments:
            break

        comments.extend(page_comments)
        page += 1

    return comments


def save_issue(issue: dict, comments: list[dict]) -> None:
    """Save issue + comments as a single JSON file."""
    data = {
        "number": issue["number"],
        "title": issue["title"],
        "body": issue.get("body", ""),
        "state": issue["state"],
        "labels": [label["name"] for label in issue.get("labels", [])],
        "author": issue["user"]["login"],
        "created_at": issue["created_at"],
        "updated_at": issue["updated_at"],
        "closed_at": issue.get("closed_at"),
        "comments_count": issue["comments"],
        "comments": [
            {
                "author": c["user"]["login"],
                "body": c["body"],
                "created_at": c["created_at"],
            }
            for c in comments
        ],
    }

    filepath = RAW_DATA_DIR / f"{issue['number']:04d}.json"
    filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def should_skip(issue: dict) -> bool:
    """Check if issue was already fetched and hasn't been updated."""
    filepath = RAW_DATA_DIR / f"{issue['number']:04d}.json"
    if not filepath.exists():
        return False
    existing = json.loads(filepath.read_text(encoding="utf-8"))
    return existing.get("updated_at") == issue["updated_at"]


def main() -> None:
    if not GITHUB_TOKEN:
        print("WARNING: No GITHUB_TOKEN set. Rate limit will be 60 req/h.")

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    with httpx.Client(headers=get_headers(), timeout=30) as client:
        print("Fetching issues...")
        issues = fetch_all_issues(client)
        print(f"Found {len(issues)} issues total.\n")

        skipped = 0
        fetched = 0
        for i, issue in enumerate(issues, 1):
            num = issue["number"]
            if should_skip(issue):
                skipped += 1
                continue

            comments = []
            if issue["comments"] > 0:
                comments = fetch_comments(client, num)

            save_issue(issue, comments)
            fetched += 1
            print(f"  [{i}/{len(issues)}] #{num}: {issue['title'][:60]}... ({len(comments)} comments)")

        print(f"\nDone. Fetched: {fetched}, Skipped (unchanged): {skipped}")


if __name__ == "__main__":
    main()
