# Visual to Data Mapping

## Executive Overview
- Total events -> `analytics.v_event_overview` or `analytics.fact_events`
- Published events -> `analytics.fact_events.published`
- Cancellation rate -> `analytics.fact_events.cancelled`
- Virtual rate -> `analytics.fact_events.virtual`
- Attendance reporting rate -> `analytics.fact_events.attendance_available`
- Total attendance -> `analytics.fact_events.total_attendance`
- Monthly event trend -> `analytics.v_monthly_event_summary`
- Attendance trend -> `analytics.v_monthly_event_summary`
- Top categories -> `analytics.v_category_performance`
- Top organizing units -> `analytics.v_organizing_unit_performance`
- DQ strip -> `analytics.v_data_quality_summary`, `audit.etl_run`

## Event Inventory
- Event list -> `analytics.v_event_overview`
- Missing subcategory -> `analytics.fact_events.subcategory_key`
- Unknown country -> `analytics.fact_events.country_key`
- Unknown organizing unit -> `analytics.fact_events.organizing_unit_key`

## Attendance Analytics
- Attendance totals and averages -> `analytics.fact_events.ieee_attending`, `analytics.fact_events.guests_attending`, `analytics.fact_events.total_attendance`
- Events with attendance -> `analytics.fact_events.attendance_available`
- Missing-attendance table -> `analytics.v_attendance_quality`

## Organizational Units
- Distinct and active units -> `analytics.fact_events.organizing_unit_key`, `analytics.dim_organizing_unit`
- Host type mix -> `analytics.dim_organizing_unit.primary_host_type`
- Top hosts -> `analytics.v_organizing_unit_performance`

## Category Analysis
- Category mix -> `analytics.v_category_performance`
- Subcategory breakdown -> `analytics.dim_subcategory`, `analytics.fact_events.subcategory_key`

## Geographic Analysis
- Countries and states -> `analytics.v_country_performance`, `analytics.dim_state`
- Physical-location coverage -> `analytics.fact_events.has_location`, `analytics.fact_events.virtual`

## Data Quality and ETL
- Severity and rule counts -> `audit.data_quality_issue`
- ETL run trend -> `audit.etl_run`

## Monthly Export
- Monthly snapshot -> `analytics.v_monthly_event_summary`

## Unsupported Metrics
- Do not map visuals to registration conversion, no-show rate, feedback, satisfaction, promotion effectiveness, reporting compliance, or cost-per-attendee.
