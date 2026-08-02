# Pull Request

## Title

Load and verify IEEE event star schema ETL

## Summary

- Added reusable ETL utilities for database access, logging, normalization, and validation.
- Added the IEEE event-to-star-schema mapping.
- Loaded date, category, subcategory, country, state, location, and organizing-unit dimensions.
- Resolved warehouse surrogate keys.
- Loaded one FactEvents row per valid IEEE event.
- Added audit run and source-file logging.
- Added structured data-quality issue logging.
- Preserved missing attendance as NULL rather than converting it to zero.
- Added ETL verification and unit tests.
- Verified repeatable, idempotent loading.

## Live ETL Results

- Source rows extracted: 6198
- Fact rows loaded: 6197
- Rejected rows: 1
- FactEvents final row count: 6197
- First ETL run ID: 3
- Second ETL run ID: 4
- First-run warnings: 1204
- First-run errors: 1
- Second-run warnings: 1204
- Second-run errors: 1
- Idempotency: PASS
- Schema verification: PASS
- ETL verification: PASS
- Tests: 7 passed

## Warehouse Row Counts

- analytics.dim_date: 524
- analytics.dim_category: 7
- analytics.dim_subcategory: 22
- analytics.dim_country: 236
- analytics.dim_state: 2176
- analytics.dim_location: 2877
- analytics.dim_organizing_unit: 2278
- analytics.fact_events: 6197
- audit.etl_run: 4
- audit.source_file: 20
- audit.data_quality_issue: 16546

## Most Frequent Data-Quality Issues

- DQ-EVT-005 INFO: 6154
- DQ-EVT-007 INFO: 4518
- DQ-EVT-014 INFO: 3464
- DQ-EVT-016 WARNING: 2240
- DQ-EVT-015 WARNING: 168
- DQ-EVT-002 ERROR: 2

## Testing Performed

- PostgreSQL connection test
- Database schema verification
- First live ETL load
- ETL verification
- ETL unit tests
- Second ETL load
- Idempotency verification

## Known Limitations

- One event was rejected because its start date was invalid.
- Attendance remains missing for a subset of events.
- Some category, subcategory, state, country, and physical-location references are incomplete.
- Speaker data remains deferred.
- Registration conversion, no-show, feedback, satisfaction, promotion, and reporting-compliance analytics are not supported by the current source.

## Review Checklist

- Confirm no secrets or datasets are committed.
- Confirm missing attendance remains NULL.
- Confirm one row per event is preserved in FactEvents.
- Confirm surrogate-key lookups use unknown or not-applicable members appropriately.
- Confirm the second ETL run does not create duplicate facts.
- Confirm audit and data-quality records are correct.
- Confirm the branch is ready to merge into main.
