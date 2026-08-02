# Power BI Dashboard Blueprint

## 1. Executive Overview
- Management question: How is the IEEE event portfolio performing overall?
- KPI cards: total events, published events, cancellation rate, virtual rate, attendance reporting rate, total attendance
- Charts: monthly event trend, attendance trend, modality split
- Tables: top categories, top organizing units
- Filters: year, month, country, category, host type
- Drill-through: event detail
- Tooltip content: event counts, attendance, data-quality status
- Export purpose: leadership summary
- Supported/unsupported: supported for portfolio monitoring; not for registration or satisfaction analysis

## 2. Event Inventory
- Management question: What events exist and how are they classified?
- KPI cards: total events, events missing subcategory, events using unknown country
- Charts: events by category, events by subcategory, events by host type
- Tables: event overview
- Filters: date, category, subcategory, host, location type
- Drill-through: event-level inspection
- Tooltip content: source event ID, start/end time, attendance
- Export purpose: catalog export
- Supported/unsupported: supported for inventory; not for behavioral conversion metrics

## 3. Attendance Analytics
- Management question: How much attendance is being reported?
- KPI cards: total attendance, average attendance, attendance reporting rate
- Charts: attendance by month, category, organizing unit
- Tables: events with missing attendance, events exceeding capacity
- Filters: year, category, host type, country
- Drill-through: event detail
- Tooltip content: reported attendance, capacity, missingness
- Export purpose: attendance review
- Supported/unsupported: supported only where attendance is reported

## 4. Organizational Unit Performance
- Management question: Which organizing units are most active?
- KPI cards: distinct organizing units, active organizing units, events per unit
- Charts: event counts by host, attendance by host, host type mix
- Tables: organizing-unit performance
- Filters: host type, region, society, section
- Drill-through: host detail
- Tooltip content: first and latest event date, published/cancelled/virtual counts
- Export purpose: host scorecard
- Supported/unsupported: not a replacement for host CRM or membership analytics

## 5. Category Analysis
- Management question: Which topics are driving the portfolio?
- KPI cards: events by category, category share, attendance by category
- Charts: category mix, subcategory breakdown
- Tables: category performance
- Filters: category, subcategory, year
- Drill-through: event list by category
- Tooltip content: attendance reporting rate, average attendance
- Export purpose: thematic analysis
- Supported/unsupported: not a replacement for content taxonomy governance

## 6. Geographic Analysis
- Management question: Where are events occurring?
- KPI cards: distinct countries, events with known physical location, physical events
- Charts: events by country, events by state, map by location
- Tables: country performance, state performance
- Filters: country, state, virtual/physical
- Drill-through: event detail
- Tooltip content: physical-location coverage
- Export purpose: geography review
- Supported/unsupported: virtual-event geography is limited by source data

## 7. Data Quality and ETL
- Management question: What data quality and load issues need attention?
- KPI cards: rejected rows, load success rate, issue counts by severity
- Charts: issue counts by rule, ETL run status trend
- Tables: data-quality summary, ETL run summary
- Filters: severity, rule, run ID
- Drill-through: issue detail
- Tooltip content: invalid start dates, missing references, unknown members
- Export purpose: operations review
- Supported/unsupported: not a user-facing KPI page

## 8. Monthly Export
- Management question: What monthly snapshot should be exported for leadership?
- KPI cards: monthly events, monthly attendance, monthly reporting rate
- Charts: monthly trend lines, monthly stacked modality counts
- Tables: monthly summary
- Filters: year, month
- Drill-through: event detail
- Tooltip content: summary totals
- Export purpose: PDF / Excel export for monthly leadership pack
- Supported/unsupported: summary only; no unsupported metrics included
