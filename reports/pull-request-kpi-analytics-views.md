# Pull Request

## Title

Add KPI layer and analytics views

## Summary

- Added a documented KPI dictionary for supported event, attendance, organizational-unit, category, geography, and data-quality metrics.
- Added PostgreSQL analytics views.
- Added KPI validation SQL.
- Added automated view deployment and verification scripts.
- Added live KPI validation results.
- Added Power BI semantic-model guidance.
- Added DAX measure definitions.
- Added dashboard blueprints.
- Added analytics tests.

## Validation

- Database connection: PASS
- Schema verification: PASS
- ETL verification: PASS
- Analytics-view deployment: PASS
- Analytics-view verification: PASS
- Event-overview row count: 6197
- Event-overview uniqueness: PASS
- Monthly reconciliation: PASS
- Category reconciliation: PASS
- Attendance-null handling: PASS
- Tests: 9 passed

## Current Snapshot

- Total events: 6,197
- Published events: 6,197
- Cancelled events: 36
- Virtual events: 2,528
- Events with attendance: 4,465
- Total attendance: 232,940
- Distinct countries: 92
- Distinct organizing units: 2,276

## Deferred Analytics

- registration conversion
- no-show rate
- feedback
- satisfaction
- promotion effectiveness
- reporting compliance
- cost-per-attendee analysis

## Review Checklist

- Confirm KPI definitions and formulas.
- Confirm attendance NULL handling.
- Confirm view reconciliation.
- Confirm one row per event.
- Confirm no unsupported KPIs were introduced.
- Confirm no credentials or datasets were committed.
- Confirm Power BI guidance matches the warehouse.
