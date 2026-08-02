-- KPI-001 Total Events
SELECT 'KPI-001 Total Events' AS kpi, COUNT(*) AS value FROM analytics.fact_events;

-- KPI-001b Distinct Event IDs
SELECT 'Distinct Event IDs' AS kpi, COUNT(DISTINCT source_event_id) AS value FROM analytics.fact_events;

-- Publication / cancellation / virtual
SELECT 'Published Count' AS kpi, COUNT(*) AS value FROM analytics.fact_events WHERE published;
SELECT 'Published Rate' AS kpi, COUNT(*)::numeric / NULLIF((SELECT COUNT(*) FROM analytics.fact_events), 0) AS value FROM analytics.fact_events WHERE published;
SELECT 'Cancelled Count' AS kpi, COUNT(*) AS value FROM analytics.fact_events WHERE cancelled;
SELECT 'Cancelled Rate' AS kpi, COUNT(*)::numeric / NULLIF((SELECT COUNT(*) FROM analytics.fact_events), 0) AS value FROM analytics.fact_events WHERE cancelled;
SELECT 'Virtual Count' AS kpi, COUNT(*) AS value FROM analytics.fact_events WHERE virtual;
SELECT 'Virtual Rate' AS kpi, COUNT(*)::numeric / NULLIF((SELECT COUNT(*) FROM analytics.fact_events), 0) AS value FROM analytics.fact_events WHERE virtual;

-- Attendance
SELECT 'Attendance Reporting Count' AS kpi, COUNT(*) AS value FROM analytics.fact_events WHERE attendance_available;
SELECT 'Attendance Reporting Rate' AS kpi, COUNT(*)::numeric / NULLIF((SELECT COUNT(*) FROM analytics.fact_events), 0) AS value FROM analytics.fact_events WHERE attendance_available;
SELECT 'Total IEEE Attendance' AS kpi, SUM(ieee_attending) AS value FROM analytics.fact_events;
SELECT 'Total Guest Attendance' AS kpi, SUM(guests_attending) AS value FROM analytics.fact_events;
SELECT 'Total Attendance' AS kpi, SUM(total_attendance) AS value FROM analytics.fact_events;
SELECT 'Average IEEE Attendance' AS kpi, AVG(ieee_attending) FILTER (WHERE ieee_attending IS NOT NULL) AS value FROM analytics.fact_events;
SELECT 'Average Guest Attendance' AS kpi, AVG(guests_attending) FILTER (WHERE guests_attending IS NOT NULL) AS value FROM analytics.fact_events;
SELECT 'Average Total Attendance' AS kpi, AVG(total_attendance) FILTER (WHERE total_attendance IS NOT NULL) AS value FROM analytics.fact_events;
SELECT 'Median Total Attendance' AS kpi, percentile_cont(0.5) WITHIN GROUP (ORDER BY total_attendance) FILTER (WHERE total_attendance IS NOT NULL) AS value FROM analytics.fact_events;
SELECT 'Events With Attendance' AS kpi, COUNT(*) AS value FROM analytics.fact_events WHERE attendance_available;
SELECT 'Events Missing Attendance' AS kpi, COUNT(*) AS value FROM analytics.fact_events WHERE NOT attendance_available;

-- Geography / organizing
SELECT 'Distinct Countries' AS kpi, COUNT(DISTINCT country_key) AS value FROM analytics.fact_events;
SELECT 'Distinct Organizing Units' AS kpi, COUNT(DISTINCT organizing_unit_key) AS value FROM analytics.fact_events;
SELECT 'Events by Category' AS kpi, category_key, COUNT(*) AS value FROM analytics.fact_events GROUP BY category_key ORDER BY COUNT(*) DESC;
SELECT 'Attendance by Category' AS kpi, category_key, SUM(total_attendance) AS value FROM analytics.fact_events GROUP BY category_key ORDER BY SUM(total_attendance) DESC;
SELECT 'Events by Organizing Unit Type' AS kpi, ou.primary_host_type, COUNT(*) AS value FROM analytics.fact_events f LEFT JOIN analytics.dim_organizing_unit ou ON ou.organizing_unit_key = f.organizing_unit_key GROUP BY ou.primary_host_type ORDER BY COUNT(*) DESC;

-- Data quality / ETL
SELECT 'Data-Quality Issues by Severity' AS kpi, severity, COUNT(*) AS value FROM audit.data_quality_issue GROUP BY severity ORDER BY COUNT(*) DESC;
SELECT 'Data-Quality Issues by Rule' AS kpi, rule_code, COUNT(*) AS value FROM audit.data_quality_issue GROUP BY rule_code ORDER BY COUNT(*) DESC;
SELECT 'Latest ETL Run' AS kpi, etl_run_id, status, rows_extracted, rows_loaded, rows_rejected FROM audit.etl_run ORDER BY etl_run_id DESC LIMIT 1;
