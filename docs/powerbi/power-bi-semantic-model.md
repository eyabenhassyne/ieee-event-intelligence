# Power BI Semantic Model

## Connection
- PostgreSQL server: `localhost`
- Database: `ieee_event_intelligence`
- User: `postgres`
- Password: managed locally in `.env`, never committed

## Load Mode
- Recommended mode: Import
- Use the direct star schema for flexible filtering
- Use aggregated views for validation pages and lightweight executive summaries

## Recommended Tables
- `analytics.fact_events`
- `analytics.dim_date`
- `analytics.dim_category`
- `analytics.dim_subcategory`
- `analytics.dim_country`
- `analytics.dim_state`
- `analytics.dim_location`
- `analytics.dim_organizing_unit`
- `analytics.v_event_overview`
- `analytics.v_monthly_event_summary`
- `analytics.v_category_performance`
- `analytics.v_organizing_unit_performance`
- `analytics.v_country_performance`
- `analytics.v_attendance_quality`
- `analytics.v_data_quality_summary`
- `analytics.v_etl_run_summary`

## Date Table
- Use `analytics.dim_date` as the official date table
- Mark `full_date` as the date column
- Sort month names by `month_number`

## Relationships
- One-to-many from each dimension to `fact_events`
- Single-direction filtering from dimensions to fact
- One-to-many from `dim_date` to `fact_events`
- If views are imported, keep them disconnected from the base star schema for comparison only

## Hidden Technical Fields
- `event_key`
- `source_event_id`
- surrogate keys
- ETL audit fields not needed by report consumers

## Data Types
- IDs: whole number
- Counts: whole number
- Rates: decimal / percentage
- Dates: date
- Timestamps: datetime
- Flags: true/false

## Sort Columns
- `month_name` by `month_number`
- `day_name` by `weekday_number`
- category and host names by their display labels unless custom sort is required

## Measure Table
- Create a dedicated measure table in Power BI for DAX measures
- Keep fact-table measures grouped in display folders

## Naming Conventions
- Use `KPI -` or descriptive measure prefixes
- Keep column names close to warehouse names for traceability
- Rename only for end-user readability

## Null-Attendance Rules
- Missing attendance remains blank in Power BI
- Do not replace blanks with zero in averages
- Only count rows with reported attendance in attendance-rate measures

## Refresh Assumptions
- Refresh from PostgreSQL after ETL loads complete
- Reimport dimensions and facts together for consistency
- Use the view layer only for validation or simplified pages

## Star Schema Versus Views
- Prefer the direct star schema for analysis and slicers
- Use views for QA, reconciliation, and simple presentation pages
- Use `v_event_overview` for row-level browsing
- Use summary views for monthly, category, host, and country dashboards
