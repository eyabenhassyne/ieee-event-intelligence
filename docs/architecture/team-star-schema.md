# IEEE Event Intelligence Team Star Schema

## Business Process
The warehouse supports analysis of IEEE events at the event grain. Each fact row represents one IEEE event and captures timing, attendance, capacity, publishing, cancellation, and location context.

## Source Systems
- `data/processed/events_clean.csv`
- `data/processed/events_analytics.csv` when present
- `data/raw/categories.csv`
- `data/raw/subcategories.csv`
- `data/raw/countries.csv`
- `data/raw/states.csv`
- `docs/data-dictionary/events-data-dictionary.md` when present
- `reports/events_analytics_preparation.md` when present

## Fact Grain
- One row per IEEE event
- Natural business key: source event id
- Warehouse fact table: `analytics.fact_events`

## Dimensions
- `analytics.dim_date`
- `analytics.dim_category`
- `analytics.dim_subcategory`
- `analytics.dim_country`
- `analytics.dim_state`
- `analytics.dim_location`
- `analytics.dim_organizing_unit`

## Measures
- `duration_hours`
- `ieee_attending`
- `guests_attending`
- `total_attendance`
- `max_registrations`
- `speaker_count`
- `event_count`

## Relationships
- `dim_subcategory.category_key -> dim_category.category_key`
- `dim_state.country_key -> dim_country.country_key`
- `fact_events.date_key -> dim_date.date_key`
- `fact_events.category_key -> dim_category.category_key`
- `fact_events.subcategory_key -> dim_subcategory.subcategory_key`
- `fact_events.country_key -> dim_country.country_key`
- `fact_events.state_key -> dim_state.state_key`
- `fact_events.location_key -> dim_location.location_key`
- `fact_events.organizing_unit_key -> dim_organizing_unit.organizing_unit_key`

## Primary and Foreign Keys
- Surrogate keys are used for all dimensions
- `fact_events.source_event_id` is the protected unique source grain
- `fact_events.etl_run_id` links to `audit.etl_run`

## Unknown-Member Strategy
- Unknown dimension members use surrogate key `0` where practical
- Not-applicable virtual location uses a dedicated `dim_location` row with `is_not_applicable = true`
- ETL uses unknown members only when a source value is missing or cannot be matched

## Null-Handling Strategy
- Missing attendance remains `NULL`
- Missing attendance must never be converted to zero
- Attendance calculations only use rows with reported attendance
- Virtual events may legitimately have no country, state, or physical location

## Slowly Changing Dimension Assumptions
- Initial implementation treats dimensions as Type 1 unless later business rules require historical tracking
- Source identifier uniqueness is preserved alongside warehouse surrogate keys
- Archived flags are carried through where present in the sources

## Supported Analytics
- Event volume over time
- Event distribution by category, subcategory, geography, host, and location
- Attendance and capacity analysis
- Virtual versus physical event breakdowns
- Operational publishing and cancellation analysis

## Unsupported Analytics
- Feedback KPIs
- Satisfaction KPIs
- Promotion KPIs
- Registration conversion KPIs
- Reporting-compliance KPIs
- No-show KPIs
- Speaker-detail analysis beyond `speaker_count`

## Known Data-Quality Limitations
- Missing attendance remains `NULL`
- Some events have incomplete location fields
- Some events may be virtual and legitimately lack physical geography
- Speaker data is deferred
- Current data does not reliably support feedback, satisfaction, promotion, no-show, registration conversion, or reporting-compliance KPIs

## Diagram
See [`team-star-schema-diagram.md`](team-star-schema-diagram.md) and [`team-star-schema.mmd`](team-star-schema.mmd).
