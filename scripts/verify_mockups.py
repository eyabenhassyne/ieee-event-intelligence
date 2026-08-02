from __future__ import annotations

import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
MOCKUPS_DIR = BASE_DIR / "mockups"
DOCS_DIR = BASE_DIR / "docs" / "mockups"
REPORTS_DIR = BASE_DIR / "reports"

REQUIRED_FILES = [
    DOCS_DIR / "dashboard-design-system.md",
    DOCS_DIR / "low-fidelity-wireframes.md",
    DOCS_DIR / "visual-to-data-mapping.md",
    DOCS_DIR / "mockup-review-checklist.md",
    MOCKUPS_DIR / "index.html",
    MOCKUPS_DIR / "styles.css",
    MOCKUPS_DIR / "app.js",
    MOCKUPS_DIR / "assets" / "README.md",
    MOCKUPS_DIR / "pages" / "executive-overview.html",
    MOCKUPS_DIR / "pages" / "event-inventory.html",
    MOCKUPS_DIR / "pages" / "attendance-analytics.html",
    MOCKUPS_DIR / "pages" / "organizational-units.html",
    MOCKUPS_DIR / "pages" / "category-analysis.html",
    MOCKUPS_DIR / "pages" / "geographic-analysis.html",
    MOCKUPS_DIR / "pages" / "data-quality-etl.html",
    MOCKUPS_DIR / "pages" / "monthly-export.html",
]

EXPECTED_PHRASES = {
    DOCS_DIR / "dashboard-design-system.md": ["Supported Metric Boundaries", "Unsupported"],
    DOCS_DIR / "low-fidelity-wireframes.md": ["Executive Overview", "Data Quality and ETL"],
    DOCS_DIR / "visual-to-data-mapping.md": ["analytics.v_event_overview", "audit.etl_run"],
    DOCS_DIR / "mockup-review-checklist.md": ["No datasets were added or modified", "No `.env` file was created or changed"],
    MOCKUPS_DIR / "index.html": ["Dashboard Mockups", "Executive Overview"],
    MOCKUPS_DIR / "pages" / "executive-overview.html": ["6,197", "232,940"],
    MOCKUPS_DIR / "pages" / "data-quality-etl.html": ["PARTIAL", "14,136"],
}


def main() -> int:
    missing = [str(path.relative_to(BASE_DIR)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        print("ERROR: Missing required mockup files:")
        for item in missing:
            print(f" - {item}")
        return 1

    problems: list[str] = []
    for path, phrases in EXPECTED_PHRASES.items():
        content = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in content:
                problems.append(f"{path.relative_to(BASE_DIR)} missing phrase: {phrase}")

    if problems:
        print("ERROR: Mockup content checks failed:")
        for problem in problems:
            print(f" - {problem}")
        return 2

    print("Mockup verification: PASS")
    print(f"Checked files: {len(REQUIRED_FILES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
