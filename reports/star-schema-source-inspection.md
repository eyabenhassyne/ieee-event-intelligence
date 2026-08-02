# Star Schema Source Inspection

## Summary
This inspection was limited to source file headers and a small sample of rows to map the proposed star schema without loading data into PostgreSQL.

## Source Files

### `data/processed/events_clean.csv`
- Rows: 51,067
- Columns: 40
- Key fields: `id`, `category_id`, `subcategory_id`, `country_id`, `state_id`, `primary_host_spoid`, `link`, `start_time`
- Candidate business keys: `id` for events, `category_id`, `subcategory_id`, `country_id`, `state_id`, `primary_host_spoid`
- Fields required by schema: `id`, `title`, `description`, `start_time`, `end_time`, `time_zone`, location fields, attendance fields, host fields, category and geography keys
- Fields present: event identity, schedule, location, attendance, host, category, geography, source metadata
- Fields missing: no separate feedback, satisfaction, registration conversion, reporting-compliance, or detailed speaker table fields
- Naming differences: `publish` in source is mapped to `published` in FactEvents; `link` is mapped to `source_link`; `is_valid_date` is retained as a validation flag

### `data/processed/events_analytics.csv`
- Rows: 51,067
- Columns: 48
- Key fields: same event grain as `events_clean.csv`
- Candidate business keys: `id`
- Fields required by schema: derived fields such as `event_year`, `event_month`, `event_date`, and `total_attendance`
- Fields present: cleaned analytics-ready event fields plus derived flags
- Fields missing: no new source-only business entities beyond what is already in `events_clean.csv`
- Naming differences: `speakers` has been removed in the analytics output because it is fully empty

### `data/raw/categories.csv`
- Rows: 6
- Columns: 3
- Key fields: `category_id`
- Candidate business keys: `category_id`
- Fields required by schema: `category_id`, `name`, `archived`
- Fields present: category identifier, name, archived flag
- Fields missing: no surrogate key in the source; surrogate key will be generated in the warehouse
- Naming differences: `name` maps to `category_name`

### `data/raw/subcategories.csv`
- Rows: 21
- Columns: 4
- Key fields: `subcategory_id`, `category_id`
- Candidate business keys: `subcategory_id`
- Fields required by schema: `subcategory_id`, `category_id`, `name`, `archived`
- Fields present: subcategory identifier, name, parent category identifier, archived flag
- Fields missing: no warehouse surrogate key in source
- Naming differences: `name` maps to `subcategory_name`

### `data/raw/countries.csv`
- Rows: 235
- Columns: 3
- Key fields: `country_id`
- Candidate business keys: `country_id`
- Fields required by schema: `country_id`, `name`, `abbreviation`
- Fields present: country identifier, country name, abbreviation
- Fields missing: no warehouse surrogate key in source
- Naming differences: `name` maps to `country_name`

### `data/raw/states.csv`
- Rows: 2,175
- Columns: 4
- Key fields: `state_id`, `country_id`
- Candidate business keys: `state_id`
- Fields required by schema: `state_id`, `country_id`, `name`, `abbreviation`
- Fields present: state identifier, state name, abbreviation, parent country identifier
- Fields missing: no warehouse surrogate key in source
- Naming differences: `name` maps to `state_name`

## Required Schema Fields Map
- Event grain: `id`
- Category mapping: `category_id` -> `analytics.dim_category.source_category_id`
- Subcategory mapping: `subcategory_id` -> `analytics.dim_subcategory.source_subcategory_id`
- Country mapping: `country_id` -> `analytics.dim_country.source_country_id`
- State mapping: `state_id` -> `analytics.dim_state.source_state_id`
- Organizing unit mapping: `primary_host_spoid` -> `analytics.dim_organizing_unit.primary_host_spoid`
- Location mapping: `city`, `address1`, `building`, `room_number`, `latitude`, `longitude`, `location_type`
