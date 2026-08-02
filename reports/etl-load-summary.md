# ETL Load Summary

## Execution Date
- 2026-08-02

## Selected Source Files
- `data/processed/events_analytics.csv` preferred, but execution is currently blocked until the real password is entered in `.env`
- `data/raw/categories.csv`
- `data/raw/subcategories.csv`
- `data/raw/countries.csv`
- `data/raw/states.csv`

## Source Row Counts
- `events_analytics.csv`: 51,067
- `categories.csv`: 6
- `subcategories.csv`: 21
- `countries.csv`: 235
- `states.csv`: 2,175

## Selected Events Source
- Preferred source: `data/processed/events_analytics.csv`
- Fallback source: `data/processed/events_clean.csv`

## ETL Run ID
- Latest successful run ID: `4`

## Dimensions Loaded
- `analytics.dim_date`: 524
- `analytics.dim_category`: 7
- `analytics.dim_subcategory`: 22
- `analytics.dim_country`: 236
- `analytics.dim_state`: 2,176
- `analytics.dim_location`: 2,877
- `analytics.dim_organizing_unit`: 2,278

## Fact Rows Inserted
- `6,197` fact rows loaded on each run

## Fact Rows Updated
- `6,197` rows are stored by unique `source_event_id`; reruns update in place

## Rejected Rows
- `1`

## Warning and Error Counts
- Warnings: `1,204`
- Errors: `1`

## Data-Quality Issues by Rule
- `DQ-EVT-005`: 6,154
- `DQ-EVT-007`: 4,518
- `DQ-EVT-014`: 3,464
- `DQ-EVT-016`: 2,240
- `DQ-EVT-015`: 168
- `DQ-EVT-002`: 2

## Null-Attendance Handling
- Preserved as `NULL` when attendance was not reported

## Unknown-Member Usage
- Unknown keys were used for unresolved categories, countries, states, locations, and organizing units
- The not-applicable virtual location member was used for virtual events without physical locations

## Idempotency Result
- Passed: the second run left `analytics.fact_events` at `6,197` rows

## Verification Result
- Database schema verification passed
- ETL verification passed

## Test Result
- `pytest tests/etl -q` passed: `7 passed`

## Unresolved Limitations
- Some source events were rejected due to invalid start dates or other fatal data issues
- The ETL script is still a pragmatic loader rather than a fully generalized warehouse orchestrator

## Next Step
- Build the KPI dictionary, SQL analytical views, Power BI semantic model, and dashboards
