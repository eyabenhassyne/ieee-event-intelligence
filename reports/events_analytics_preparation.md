# IEEE Event Analytics Preparation Report

## Input and Output
- Input file: `C:\Users\Eya\ieee-event-intelligence\data\processed\events_clean.csv`
- Output file: `C:\Users\Eya\ieee-event-intelligence\data\processed\events_analytics.csv`
- Input rows: 6198
- Output rows: 6198
- Input columns: 40
- Output columns: 48

## Added Columns
- total_attendance
- event_year
- event_month
- event_date
- attendance_available
- registration_available
- has_capacity
- has_location
- has_subcategory

## Removed Columns
- speakers

## Validation Results
- end_time before start_time: 0 rows
- latitude outside -90..90: 0 rows
- longitude outside -180..180: 0 rows

## Unresolved Data Limitations
- No unresolved structural limitations were detected during preparation.

## Power BI Recommendations
- Use `event_date`, `event_year`, and `event_month` as the primary time hierarchy.
- Prefer `total_attendance` and `has_capacity` for event engagement and sizing visuals.
- Keep `registration_available` and `has_location` as slicers or quality indicators.
- Exclude `speakers` from the model because it is fully empty in the source extract.
- Treat missing attendance and capacity fields as a reporting reality, not as zero.
