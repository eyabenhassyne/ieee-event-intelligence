CREATE OR REPLACE VIEW analytics.v_event_overview AS
SELECT
    f.source_event_id,
    f.title,
    d.full_date,
    d.year_number,
    d.month_number,
    d.month_name,
    c.category_name,
    s.subcategory_name,
    co.country_name,
    st.state_name,
    ou.organizing_unit_key,
    ou.primary_host_spoid,
    ou.primary_host_name,
    ou.primary_host_type,
    l.city,
    l.location_type,
    f.virtual,
    f.cancelled,
    f.published,
    f.ieee_attending,
    f.guests_attending,
    f.total_attendance,
    f.attendance_available,
    f.max_registrations,
    f.is_valid_date,
    f.start_time,
    f.end_time,
    f.duration_hours
FROM analytics.fact_events f
JOIN analytics.dim_date d ON d.date_key = f.date_key
LEFT JOIN analytics.dim_category c ON c.category_key = f.category_key
LEFT JOIN analytics.dim_subcategory s ON s.subcategory_key = f.subcategory_key
LEFT JOIN analytics.dim_country co ON co.country_key = f.country_key
LEFT JOIN analytics.dim_state st ON st.state_key = f.state_key
LEFT JOIN analytics.dim_location l ON l.location_key = f.location_key
LEFT JOIN analytics.dim_organizing_unit ou ON ou.organizing_unit_key = f.organizing_unit_key;

CREATE OR REPLACE VIEW analytics.v_monthly_event_summary AS
SELECT
    d.year_number,
    d.month_number,
    d.month_name,
    COUNT(*) AS total_events,
    COUNT(*) FILTER (WHERE f.published) AS published_events,
    COUNT(*) FILTER (WHERE f.cancelled) AS cancelled_events,
    COUNT(*) FILTER (WHERE f.virtual) AS virtual_events,
    COUNT(*) FILTER (WHERE NOT f.virtual AND f.location_key <> 1) AS physical_events,
    COUNT(*) FILTER (WHERE f.virtual AND f.location_key = 1) AS hybrid_events,
    COUNT(*) FILTER (WHERE f.attendance_available) AS events_with_attendance,
    COUNT(*) FILTER (WHERE NOT f.attendance_available) AS events_missing_attendance,
    COUNT(*) FILTER (WHERE f.attendance_available)::numeric / NULLIF(COUNT(*), 0) AS attendance_reporting_rate,
    SUM(f.ieee_attending) AS total_ieee_attendance,
    SUM(f.guests_attending) AS total_guest_attendance,
    SUM(f.total_attendance) AS total_attendance,
    AVG(f.total_attendance) FILTER (WHERE f.total_attendance IS NOT NULL) AS average_total_attendance
FROM analytics.fact_events f
JOIN analytics.dim_date d ON d.date_key = f.date_key
GROUP BY d.year_number, d.month_number, d.month_name
ORDER BY d.year_number, d.month_number;

CREATE OR REPLACE VIEW analytics.v_category_performance AS
SELECT
    c.category_key,
    c.category_name,
    COUNT(*) AS event_count,
    COUNT(*)::numeric / NULLIF((SELECT COUNT(*) FROM analytics.fact_events), 0) AS category_share,
    COUNT(*) FILTER (WHERE f.attendance_available) AS events_with_attendance,
    COUNT(*) FILTER (WHERE f.attendance_available)::numeric / NULLIF(COUNT(*), 0) AS attendance_reporting_rate,
    SUM(f.ieee_attending) AS total_ieee_attendance,
    SUM(f.guests_attending) AS total_guest_attendance,
    SUM(f.total_attendance) AS total_attendance,
    AVG(f.total_attendance) FILTER (WHERE f.total_attendance IS NOT NULL) AS average_total_attendance
FROM analytics.fact_events f
LEFT JOIN analytics.dim_category c ON c.category_key = f.category_key
GROUP BY c.category_key, c.category_name
ORDER BY event_count DESC, c.category_name;

CREATE OR REPLACE VIEW analytics.v_organizing_unit_performance AS
SELECT
    ou.organizing_unit_key,
    ou.primary_host_spoid,
    ou.primary_host_name,
    ou.primary_host_type,
    COUNT(*) AS event_count,
    COUNT(*) FILTER (WHERE f.published) AS published_events,
    COUNT(*) FILTER (WHERE f.cancelled) AS cancelled_events,
    COUNT(*) FILTER (WHERE f.virtual) AS virtual_events,
    COUNT(*) FILTER (WHERE f.attendance_available) AS events_with_attendance,
    COUNT(*) FILTER (WHERE f.attendance_available)::numeric / NULLIF(COUNT(*), 0) AS attendance_reporting_rate,
    SUM(f.total_attendance) AS total_attendance,
    AVG(f.total_attendance) FILTER (WHERE f.total_attendance IS NOT NULL) AS average_total_attendance,
    MIN(d.full_date) AS first_event_date,
    MAX(d.full_date) AS latest_event_date
FROM analytics.fact_events f
LEFT JOIN analytics.dim_organizing_unit ou ON ou.organizing_unit_key = f.organizing_unit_key
JOIN analytics.dim_date d ON d.date_key = f.date_key
GROUP BY ou.organizing_unit_key, ou.primary_host_spoid, ou.primary_host_name, ou.primary_host_type
ORDER BY event_count DESC, ou.primary_host_name;

CREATE OR REPLACE VIEW analytics.v_country_performance AS
SELECT
    co.country_key,
    co.country_name,
    COUNT(*) AS event_count,
    COUNT(*) FILTER (WHERE f.attendance_available) AS events_with_attendance,
    COUNT(*) FILTER (WHERE f.attendance_available)::numeric / NULLIF(COUNT(*), 0) AS attendance_reporting_rate,
    SUM(f.total_attendance) AS total_attendance,
    AVG(f.total_attendance) FILTER (WHERE f.total_attendance IS NOT NULL) AS average_total_attendance,
    COUNT(*) FILTER (WHERE f.virtual) AS virtual_event_count,
    COUNT(*) FILTER (WHERE f.location_key = 0 AND NOT f.virtual) AS known_physical_location_count
FROM analytics.fact_events f
LEFT JOIN analytics.dim_country co ON co.country_key = f.country_key
GROUP BY co.country_key, co.country_name
ORDER BY event_count DESC, co.country_name;

CREATE OR REPLACE VIEW analytics.v_attendance_quality AS
SELECT
    f.source_event_id,
    f.title,
    d.full_date AS event_date,
    c.category_name,
    ou.primary_host_name AS organizing_unit_name,
    f.ieee_attending,
    f.guests_attending,
    f.total_attendance,
    f.attendance_available,
    f.max_registrations,
    (f.max_registrations IS NOT NULL AND f.total_attendance IS NOT NULL AND f.total_attendance > f.max_registrations) AS attendance_exceeds_capacity,
    (NOT f.attendance_available) AS missing_attendance
FROM analytics.fact_events f
JOIN analytics.dim_date d ON d.date_key = f.date_key
LEFT JOIN analytics.dim_category c ON c.category_key = f.category_key
LEFT JOIN analytics.dim_organizing_unit ou ON ou.organizing_unit_key = f.organizing_unit_key;

CREATE OR REPLACE VIEW analytics.v_data_quality_summary AS
SELECT
    rule_code,
    severity,
    resolved,
    COUNT(*) AS issue_count
FROM audit.data_quality_issue
GROUP BY rule_code, severity, resolved
ORDER BY issue_count DESC, rule_code;

CREATE OR REPLACE VIEW analytics.v_etl_run_summary AS
SELECT
    etl_run_id,
    process_name,
    started_at,
    completed_at,
    status,
    rows_extracted,
    rows_loaded,
    rows_rejected,
    warning_count,
    error_count,
    CASE
        WHEN rows_extracted = 0 THEN NULL
        ELSE rows_loaded::numeric / NULLIF(rows_extracted, 0)
    END AS load_success_rate
FROM audit.etl_run
ORDER BY etl_run_id DESC;
