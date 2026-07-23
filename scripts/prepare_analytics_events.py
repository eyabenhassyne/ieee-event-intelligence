from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = BASE_DIR / "data" / "processed" / "events_clean.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "events_analytics.csv"
REPORT_PATH = BASE_DIR / "reports" / "events_analytics_preparation.md"

DATE_COLUMNS = [
    "start_time",
    "end_time",
    "registration_start_time",
    "registration_end_time",
    "created_at",
    "updated_at",
]


def safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    try:
        return pd.read_csv(path)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Unable to read CSV '{path}': {exc}") from exc


def parse_date_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    parsed_counts: dict[str, int] = {}
    for col in DATE_COLUMNS:
        if col not in df.columns:
            continue
        parsed = pd.to_datetime(df[col], errors="coerce", utc=True, format="mixed")
        parsed_counts[col] = int(parsed.notna().sum())
        df[col] = parsed
    return df, parsed_counts


def main() -> int:
    try:
        df = safe_read_csv(INPUT_PATH)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    input_rows = len(df)
    input_columns = list(df.columns)
    source_columns = set(df.columns)
    df = df.copy()

    df, parsed_counts = parse_date_columns(df)

    added_columns: list[str] = []
    removed_columns: list[str] = []
    validation_messages: list[str] = []
    limitations: list[str] = []

    if {"ieee_attending", "guests_attending"}.issubset(df.columns):
        df["total_attendance"] = df[["ieee_attending", "guests_attending"]].sum(axis=1, min_count=1)
        added_columns.append("total_attendance")
    else:
        limitations.append("total_attendance was not created because one or both attendance source columns are missing.")

    if "start_time" in df.columns:
        df["event_year"] = df["start_time"].dt.year
        df["event_month"] = df["start_time"].dt.month
        df["event_date"] = df["start_time"].dt.date
        added_columns.extend(["event_year", "event_month", "event_date"])
    else:
        limitations.append("event_year, event_month, and event_date were not created because start_time is unavailable.")

    if {"ieee_attending", "guests_attending"}.issubset(df.columns):
        df["attendance_available"] = df[["ieee_attending", "guests_attending"]].notna().any(axis=1)
        added_columns.append("attendance_available")

    registration_cols = {"registration_start_time", "registration_end_time", "registration_url"}
    if registration_cols.intersection(df.columns):
        df["registration_available"] = (
            df.get("registration_url", pd.Series(index=df.index, dtype="object")).notna()
            | df.get("registration_start_time", pd.Series(index=df.index, dtype="datetime64[ns, UTC]")).notna()
            | df.get("registration_end_time", pd.Series(index=df.index, dtype="datetime64[ns, UTC]")).notna()
        )
        added_columns.append("registration_available")
    else:
        limitations.append("registration_available was not created because registration fields are unavailable.")

    if "max_registrations" in df.columns:
        df["has_capacity"] = df["max_registrations"].notna()
        added_columns.append("has_capacity")
    else:
        limitations.append("has_capacity was not created because max_registrations is unavailable.")

    location_cols = {"city", "building", "address1", "latitude", "longitude"}
    if location_cols.intersection(df.columns):
        df["has_location"] = (
            df.get("city", pd.Series(index=df.index, dtype="object")).notna()
            | df.get("building", pd.Series(index=df.index, dtype="object")).notna()
            | df.get("address1", pd.Series(index=df.index, dtype="object")).notna()
            | df.get("latitude", pd.Series(index=df.index, dtype="float64")).notna()
            | df.get("longitude", pd.Series(index=df.index, dtype="float64")).notna()
        )
        added_columns.append("has_location")

    if "subcategory_id" in df.columns:
        df["has_subcategory"] = df["subcategory_id"].notna()
        added_columns.append("has_subcategory")
    else:
        limitations.append("has_subcategory was not created because subcategory_id is unavailable.")

    if {"start_time", "end_time"}.issubset(df.columns):
        invalid_order = df["start_time"].notna() & df["end_time"].notna() & (df["end_time"] < df["start_time"])
        invalid_order_count = int(invalid_order.sum())
        validation_messages.append(
            f"end_time before start_time: {invalid_order_count} rows"
        )
    else:
        validation_messages.append("end_time before start_time: unable to validate because one or both date columns are missing")

    if "latitude" in df.columns:
        lat_invalid = df["latitude"].notna() & ~df["latitude"].between(-90, 90)
        validation_messages.append(f"latitude outside -90..90: {int(lat_invalid.sum())} rows")
    else:
        validation_messages.append("latitude outside -90..90: latitude column missing")

    if "longitude" in df.columns:
        lon_invalid = df["longitude"].notna() & ~df["longitude"].between(-180, 180)
        validation_messages.append(f"longitude outside -180..180: {int(lon_invalid.sum())} rows")
    else:
        validation_messages.append("longitude outside -180..180: longitude column missing")

    if "speakers" in df.columns:
        df = df.drop(columns=["speakers"])
        removed_columns.append("speakers")

    output_columns = list(df.columns)
    output_rows = len(df)

    df.to_csv(OUTPUT_PATH, index=False)

    report_lines: list[str] = []
    report_lines.append("# IEEE Event Analytics Preparation Report")
    report_lines.append("")
    report_lines.append("## Input and Output")
    report_lines.append(f"- Input file: `{INPUT_PATH}`")
    report_lines.append(f"- Output file: `{OUTPUT_PATH}`")
    report_lines.append(f"- Input rows: {input_rows}")
    report_lines.append(f"- Output rows: {output_rows}")
    report_lines.append(f"- Input columns: {len(input_columns)}")
    report_lines.append(f"- Output columns: {len(output_columns)}")
    report_lines.append("")
    report_lines.append("## Added Columns")
    if added_columns:
        for col in added_columns:
            report_lines.append(f"- {col}")
    else:
        report_lines.append("- None")
    report_lines.append("")
    report_lines.append("## Removed Columns")
    if removed_columns:
        for col in removed_columns:
            report_lines.append(f"- {col}")
    else:
        report_lines.append("- None")
    report_lines.append("")
    report_lines.append("## Validation Results")
    for message in validation_messages:
        report_lines.append(f"- {message}")
    report_lines.append("")
    report_lines.append("## Unresolved Data Limitations")
    if limitations:
        for item in limitations:
            report_lines.append(f"- {item}")
    else:
        report_lines.append("- No unresolved structural limitations were detected during preparation.")
    report_lines.append("")
    report_lines.append("## Power BI Recommendations")
    report_lines.append("- Use `event_date`, `event_year`, and `event_month` as the primary time hierarchy.")
    report_lines.append("- Prefer `total_attendance` and `has_capacity` for event engagement and sizing visuals.")
    report_lines.append("- Keep `registration_available` and `has_location` as slicers or quality indicators.")
    report_lines.append("- Exclude `speakers` from the model because it is fully empty in the source extract.")
    report_lines.append("- Treat missing attendance and capacity fields as a reporting reality, not as zero.")
    report_lines.append("")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")

    print("Preparation complete")
    print(f"Input rows: {input_rows}")
    print(f"Output rows: {output_rows}")
    print(f"Added columns: {', '.join(added_columns) if added_columns else 'none'}")
    print(f"Removed columns: {', '.join(removed_columns) if removed_columns else 'none'}")
    print(f"Output written to: {OUTPUT_PATH}")
    print(f"Report written to: {REPORT_PATH}")
    print(f"Parsed date columns: {', '.join(sorted(parsed_counts)) if parsed_counts else 'none'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
