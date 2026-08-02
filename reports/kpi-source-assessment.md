# KPI Source Assessment

## Source Snapshot
- Live warehouse snapshot after ETL load
- Fact table rows: 6,197
- Unique source events: 6,197
- Latest ETL run status: `PARTIAL`
- Latest ETL run IDs: `3` and `4`

## Available Fact Measures
- `ieee_attending`
- `guests_attending`
- `total_attendance`
- `max_registrations`
- `speaker_count`
- `duration_hours`
- `event_count`
- `virtual`
- `cancelled`
- `published`
- `attendance_available`
- `has_location`
- `has_subcategory`
- `is_valid_date`

## Available Dimensions
- `dim_date`
- `dim_category`
- `dim_subcategory`
- `dim_country`
- `dim_state`
- `dim_location`
- `dim_organizing_unit`

## Reliable Fields
- Event identity
- Start date and time
- Category and subcategory keys
- Country and state keys
- Organizing-unit keys
- Location keys
- Virtual/cancelled/published flags
- Attendance fields where present

## Fields With Partial Completeness
- Attendance is missing for 1,732 events
- Some physical-location references are incomplete
- Some category, subcategory, state, country, and organizing-unit references use unknown members
- `speaker_count` is present, but speaker detail is deferred
- `is_valid_date` reflects source validation rather than a business KPI

## Attendance Completeness
- Attendance reported on 4,465 events
- Attendance missing on 1,732 events
- Attendance reporting rate: 72.05%

## Geographic Coverage
- Distinct countries represented in facts: 92
- Country dimension rows: 236 including unknown and reference rows
- State dimension rows: 2,176 including unknown and reference rows
- Physical-location data is uneven across events

## Organizing-Unit Coverage
- Distinct organizing units in facts: 2,276
- Organizing unit dimension rows: 2,278 including unknown
- Some events lack a usable SPOID and fall back to the unknown member

## Date Coverage
- `dim_date` rows loaded: 524
- One event had an invalid start date and was rejected

## Unsupported Analytics
- Registration conversion
- No-show rate
- Feedback completion
- Satisfaction
- Promotion effectiveness
- Reporting compliance
- Cost per attendee

## Known Data-Quality Limitations
- One event rejected for invalid start date
- Missing attendance remains NULL
- Some physical-location values are incomplete
- Some reference keys use unknown members
- `published` is 100% in the current snapshot, so publication-rate analysis is not very discriminating
