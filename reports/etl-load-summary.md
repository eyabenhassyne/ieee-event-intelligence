# ETL Load Summary

## Execution Date
- 2026-08-02

## Selected Source Files
- `data/processed/events_analytics.csv` preferred, but execution is currently blocked until the real password is entered in `.env`
- `data/raw/categories.csv`
- `data/raw/subcategories.csv`
- `data/raw/countries.csv`
- `data/raw/states.csv`

## Source Row Counts
- `events_analytics.csv`: 51,067
- `categories.csv`: 6
- `subcategories.csv`: 21
- `countries.csv`: 235
- `states.csv`: 2,175

## Selected Events Source
- Preferred source: `data/processed/events_analytics.csv`
- Fallback source: `data/processed/events_clean.csv`

## ETL Run ID
- Not yet generated because the load cannot be executed until `.env` contains a real password

## Dimensions Loaded
- Not yet executed

## Fact Rows Inserted
- Not yet executed

## Fact Rows Updated
- Not yet executed

## Rejected Rows
- Not yet executed

## Warning and Error Counts
- Not yet executed

## Data-Quality Issues by Rule
- Not yet executed

## Null-Attendance Handling
- Designed to remain `NULL` for missing values

## Unknown-Member Usage
- Designed to use key `0` where appropriate and the virtual not-applicable location row for virtual events

## Idempotency Result
- Pending execution

## Verification Result
- Pending execution

## Test Result
- Utility tests added but ETL runtime has not been executed

## Unresolved Limitations
- `.env` still contains the placeholder password
- Live database load has not been run

## Next Step
- Replace the placeholder password in `.env`, then run the ETL loader, verification script, and pytest suite
