from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "events_clean.csv"
REPORT_PATH = BASE_DIR / "reports" / "events_profile.md"


def pct(value: int, total: int) -> float:
    return 0.0 if total == 0 else (value / total) * 100.0


def format_float(value: float) -> str:
    return f"{value:.2f}"


def safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    try:
        return pd.read_csv(path)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Unable to read CSV '{path}': {exc}") from exc


def detect_event_id_column(df: pd.DataFrame) -> str | None:
    candidates = [
        "event_id",
        "id",
        "eventid",
        "event_id_clean",
        "event_id_raw",
    ]
    lower_map = {col.lower(): col for col in df.columns}
    for candidate in candidates:
        if candidate in lower_map:
            return lower_map[candidate]

    for col in df.columns:
        name = col.lower()
        if "event" in name and (name.endswith("id") or name.endswith("_id") or name == "id"):
            return col

    for col in df.columns:
        if col.lower() == "id":
            return col

    return None


def looks_like_date_column(series: pd.Series, column_name: str) -> bool:
    name = column_name.lower()
    if name in {"time_zone", "is_valid_date"}:
        return False
    if any(token in name for token in ["date", "timestamp"]) or name.endswith("_time") or name.endswith("_at"):
        return True
    if pd.api.types.is_datetime64_any_dtype(series):
        return True

    sample = series.dropna().astype(str).head(10)
    if sample.empty:
        return False
    parsed = pd.to_datetime(sample, errors="coerce", utc=True, format="mixed")
    return parsed.notna().mean() >= 0.6


def numeric_series(df: pd.DataFrame) -> list[str]:
    numeric_cols = []
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)
            continue
        coerced = pd.to_numeric(df[col], errors="coerce")
        non_null = df[col].notna().sum()
        if non_null > 0 and coerced.notna().sum() / non_null >= 0.8:
            numeric_cols.append(col)
    return numeric_cols


def categorical_series(df: pd.DataFrame) -> list[str]:
    cats = []
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            continue
        if col in numeric_series(df):
            continue
        nunique = df[col].nunique(dropna=True)
        if nunique <= 20:
            cats.append(col)
    return cats


def main() -> int:
    try:
        df = safe_read_csv(DATA_PATH)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    rows, cols = df.shape
    columns = list(df.columns)
    dtypes = df.dtypes.astype(str)
    missing_counts = df.isna().sum()
    missing_pct = (missing_counts / rows * 100.0) if rows else missing_counts * 0.0
    duplicated_rows = int(df.duplicated().sum())

    event_id_col = detect_event_id_column(df)
    event_id_duplicates = None
    event_id_duplicate_rows = None
    if event_id_col:
        event_id_series = df[event_id_col]
        event_id_non_null = event_id_series.dropna()
        event_id_duplicates = int(event_id_non_null.duplicated().sum())
        event_id_duplicate_rows = (
            df.loc[event_id_series.notna() & event_id_series.duplicated(keep=False), event_id_col]
            .value_counts()
            .sort_index()
        )

    date_columns = [col for col in df.columns if looks_like_date_column(df[col], col)]
    date_quality = {}
    for col in date_columns:
        parsed = pd.to_datetime(df[col], errors="coerce", utc=True, format="mixed")
        invalid = int(df[col].notna().sum() - parsed.notna().sum())
        date_quality[col] = {
            "invalid": invalid,
            "invalid_pct": pct(invalid, int(df[col].notna().sum())),
        }

    numeric_cols = numeric_series(df)
    numeric_quality = {}
    for col in numeric_cols:
        values = pd.to_numeric(df[col], errors="coerce")
        negative = int((values < 0).sum(skipna=True))
        numeric_quality[col] = {
            "negative": negative,
            "negative_pct": pct(negative, int(values.notna().sum())),
        }

    categorical_cols = categorical_series(df)
    categorical_values = {}
    for col in categorical_cols:
        unique_vals = [v for v in df[col].dropna().astype(str).unique().tolist()]
        categorical_values[col] = unique_vals[:50]

    risks = []
    if duplicated_rows:
        risks.append(f"{duplicated_rows} fully duplicated rows suggest possible repeated records.")
    if event_id_col and event_id_duplicates:
        risks.append(f"Event ID column '{event_id_col}' has {event_id_duplicates} duplicate non-null IDs.")
    if any(v["invalid"] > 0 for v in date_quality.values()):
        risks.append("One or more date-like columns contain invalid or unparseable values.")
    if any(v["negative"] > 0 for v in numeric_quality.values()):
        risks.append("One or more numeric columns contain negative values that may be invalid for this dataset.")
    if any(df[col].isna().mean() > 0.5 for col in df.columns):
        risks.append("Several columns have high missingness and may require filtering or imputation.")
    if not risks:
        risks.append("No major structural issues were detected by the automated checks.")

    recommendations = [
        "Review duplicate event IDs and decide whether to deduplicate or preserve versioned records.",
        "Inspect date fields with invalid parses before using them in time-based analysis.",
        "Confirm whether negative numeric values are legitimate for the affected columns.",
        "Assess sparse columns for removal, imputation, or separate handling in downstream modeling.",
    ]

    report_lines = []
    report_lines.append("# IEEE Event Dataset Profiling Report")
    report_lines.append("")
    report_lines.append("## Dataset Overview")
    report_lines.append(f"- Source file: `{DATA_PATH}`")
    report_lines.append(f"- Rows: {rows}")
    report_lines.append(f"- Columns: {cols}")
    report_lines.append(f"- Fully duplicated rows: {duplicated_rows}")
    report_lines.append(f"- Event ID column detected: `{event_id_col}`" if event_id_col else "- Event ID column detected: not found")
    report_lines.append("")

    report_lines.append("## Column Summary")
    report_lines.append("| Column | Dtype | Non-null | Missing | Missing % |")
    report_lines.append("| --- | --- | ---: | ---: | ---: |")
    for col in columns:
        report_lines.append(
            f"| {col} | {dtypes[col]} | {int(df[col].notna().sum())} | {int(missing_counts[col])} | {format_float(missing_pct[col])} |"
        )
    report_lines.append("")

    report_lines.append("## Missing-Data Summary")
    report_lines.append("| Column | Missing Count | Missing % |")
    report_lines.append("| --- | ---: | ---: |")
    for col in columns:
        report_lines.append(f"| {col} | {int(missing_counts[col])} | {format_float(missing_pct[col])} |")
    report_lines.append("")

    report_lines.append("## Duplicate Summary")
    report_lines.append(f"- Fully duplicated rows: {duplicated_rows}")
    if event_id_col:
        report_lines.append(f"- Event ID column: `{event_id_col}`")
        report_lines.append(f"- Duplicate non-null event IDs: {event_id_duplicates}")
        if event_id_duplicate_rows is not None and not event_id_duplicate_rows.empty:
            report_lines.append("")
            report_lines.append("| Event ID | Count |")
            report_lines.append("| --- | ---: |")
            for event_id, count in event_id_duplicate_rows.items():
                if count > 1:
                    report_lines.append(f"| {event_id} | {int(count)} |")
    else:
        report_lines.append("- Event ID column: not found")
    report_lines.append("")

    report_lines.append("## Date-Quality Summary")
    if date_quality:
        report_lines.append("| Column | Invalid / Unparseable | Invalid % |")
        report_lines.append("| --- | ---: | ---: |")
        for col, info in date_quality.items():
            report_lines.append(f"| {col} | {info['invalid']} | {format_float(info['invalid_pct'])} |")
    else:
        report_lines.append("- No date-like columns detected.")
    report_lines.append("")

    report_lines.append("## Numeric-Quality Summary")
    if numeric_quality:
        report_lines.append("| Column | Negative Values | Negative % of Non-null Numeric Values |")
        report_lines.append("| --- | ---: | ---: |")
        for col, info in numeric_quality.items():
            report_lines.append(f"| {col} | {info['negative']} | {format_float(info['negative_pct'])} |")
    else:
        report_lines.append("- No numeric columns detected.")
    report_lines.append("")

    report_lines.append("## Categorical-Value Summary")
    if categorical_values:
        for col, values in categorical_values.items():
            report_lines.append(f"### {col}")
            if values:
                report_lines.append(", ".join(f"`{v}`" for v in values))
            else:
                report_lines.append("_No non-null values detected._")
            report_lines.append("")
    else:
        report_lines.append("- No low-cardinality categorical columns detected.")
        report_lines.append("")

    report_lines.append("## Detected Risks and Recommended Next Actions")
    report_lines.append("### Risks")
    for risk in risks:
        report_lines.append(f"- {risk}")
    report_lines.append("")
    report_lines.append("### Recommended Next Actions")
    for rec in recommendations:
        report_lines.append(f"- {rec}")
    report_lines.append("")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")

    print("Profiling complete")
    print(f"Input: {DATA_PATH}")
    print(f"Rows: {rows}")
    print(f"Columns: {cols}")
    print(f"Fully duplicated rows: {duplicated_rows}")
    print(f"Event ID column: {event_id_col if event_id_col else 'not found'}")
    print(f"Date-like columns: {', '.join(date_columns) if date_columns else 'none'}")
    print(f"Numeric columns: {', '.join(numeric_cols) if numeric_cols else 'none'}")
    print(f"Report written to: {REPORT_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
