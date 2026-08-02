# Database Design Summary

## Implementation Date
- 2026-08-02

## Source Files Inspected
- `data/processed/events_clean.csv`
- `data/processed/events_analytics.csv`
- `data/raw/categories.csv`
- `data/raw/subcategories.csv`
- `data/raw/countries.csv`
- `data/raw/states.csv`
- `docs/data-dictionary/events-data-dictionary.md`
- `reports/events_analytics_preparation.md`
- `reports/star-schema-source-inspection.md`

## Schemas Created
- `raw`
- `staging`
- `analytics`
- `audit`

## Dimensions Created
- `analytics.dim_date`
- `analytics.dim_category`
- `analytics.dim_subcategory`
- `analytics.dim_country`
- `analytics.dim_state`
- `analytics.dim_location`
- `analytics.dim_organizing_unit`

## Fact Table Created
- `analytics.fact_events`

## Grain
- One row per IEEE event

## Dimension Relationships
- `dim_subcategory -> dim_category`
- `dim_state -> dim_country`
- `fact_events -> dim_date`
- `fact_events -> dim_category`
- `fact_events -> dim_subcategory`
- `fact_events -> dim_country`
- `fact_events -> dim_state`
- `fact_events -> dim_location`
- `fact_events -> dim_organizing_unit`

## Fact Foreign Keys
- `date_key`
- `category_key`
- `subcategory_key`
- `country_key`
- `state_key`
- `location_key`
- `organizing_unit_key`
- `etl_run_id`

## Measures
- `duration_hours`
- `ieee_attending`
- `guests_attending`
- `total_attendance`
- `max_registrations`
- `speaker_count`
- `event_count`

## Flags
- `virtual`
- `cancelled`
- `published`
- `is_valid_date`
- `attendance_available`
- `registration_available`
- `has_capacity`
- `has_location`
- `has_subcategory`

## Unknown-Member Strategy
- Surrogate key `0` is used where practical
- `dim_location` also includes a not-applicable virtual member
- ETL should map missing source values to unknown rows and virtual events to the virtual no-location row when appropriate

## Null-Attendance Strategy
- Missing attendance remains `NULL`
- Attendance calculations must only use events with reported attendance
- If only one attendance field is present, preserve that value and keep the other field `NULL`

## Physical Versus Virtual Location Strategy
- Real physical locations are stored in `dim_location`
- Virtual events may use the not-applicable virtual location member
- Virtual events may legitimately have no country, state, or physical location

## Constraints
- Date range and weekday checks in `dim_date`
- Nonnegative checks on fact measures
- End time cannot precede start time
- Attendance consistency check allows partial attendance
- Unique source event id in the fact table

## Indexes
- Date and foreign-key indexes on the fact table
- Status and attendance indexes on the fact table
- Organizing unit lookup indexes on host type and host name

## Audit Design
- `audit.etl_run`
- `audit.source_file`
- `audit.data_quality_issue`

## Fields Intentionally Excluded
- `DimEventStatus` as a separate dimension
- `FactAttendance`
- Feedback KPIs
- Satisfaction KPIs
- Promotion KPIs
- Registration conversion KPIs
- Reporting-compliance KPIs
- Detailed speaker dimensioning

## Unsupported KPI Areas
- Feedback
- Satisfaction
- Promotion
- No-show
- Registration conversion
- Reporting-compliance

## Verification Outcome
- Not yet executed because the database password placeholder in `.env` must be replaced before schema application and verification can run

## Next Step
Build the ETL loader that loads dimensions first, resolves surrogate keys, loads FactEvents, logs the ETL run, and records data-quality issues.
