# Data Source Mapping

## Purpose

This document identifies the data sources used by the IEEE Event Intelligence
Platform and records their ownership, structure, refresh frequency, quality,
privacy constraints, and expected use in the BI solution.

## Source Inventory

| Source ID | Source Name | Owner | Format | Location | Refresh Frequency | Main Data | Access Status |
|---|---|---|---|---|---|---|---|
| SRC-001 | IEEE vTools Events export | To confirm | CSV / Excel | To confirm | Manual / periodic | Event details and reporting status | Pending |
| SRC-002 | Local event tracking file | To confirm | Excel | To confirm | To confirm | Local event monitoring | Pending |
| SRC-003 | Registration export | To confirm | CSV / Excel | To confirm | Per event | Registration counts | Pending |
| SRC-004 | Attendance or check-in export | To confirm | CSV / Excel | To confirm | Per event | Final attendance | Pending |
| SRC-005 | Event feedback survey | To confirm | CSV / Excel | To confirm | Per event | Feedback and satisfaction | Pending |
| SRC-006 | Officer reports | To confirm | Excel / PDF / Form | To confirm | Monthly or periodic | Reporting and organizational-unit information | Pending |
| SRC-007 | Student Branch reports | To confirm | Excel / Form | To confirm | Periodic | Student Branch activities | Pending |
| SRC-008 | Promotion tracking data | To confirm | Excel / CSV | To confirm | Per event | Promotion channels and dates | Pending |

## Detailed Source Template

Complete one section for every confirmed source.

### Source Identification

- Source ID:
- Source name:
- Business owner:
- Technical contact:
- Organizational unit:
- Access status:
- Date received:
- File version:

### Technical Information

- File format:
- File name pattern:
- File location:
- Encoding:
- Sheet names:
- Delimiter:
- Approximate number of rows:
- Approximate number of columns:
- Refresh frequency:
- Historical data available:
- Earliest available date:
- Latest available date:

### Main Content

- Main entity:
- Record grain:
- Primary key candidate:
- Important fields:
- Date fields:
- Numeric fields:
- Category fields:
- Personal-data fields:

### Data Quality

- Missing-value issues:
- Duplicate issues:
- Invalid-date issues:
- Inconsistent labels:
- Unexpected values:
- Structural changes:
- Known limitations:

### Privacy and Governance

- Contains personal data:
- Requires anonymization:
- Allowed users:
- Storage restrictions:
- Retention requirements:
- Approval required:
- Notes:

### ETL Use

- Raw target table:
- Staging target table:
- Analytics target table:
- Required transformations:
- Validation rules:
- Matching fields:
- Rejection conditions:
- Expected KPI usage:

## Field-Level Mapping Template

| Source Field | Description | Example | Source Type | Target Field | Target Type | Required | Transformation | Validation Rule |
|---|---|---|---|---|---|---|---|---|
| event_id | Unique event identifier | EVT-001 | Text | event_id | Text | Yes | Trim whitespace | Must not be empty |
| event_title | Event name | AI Workshop | Text | event_title | Text | Yes | Normalize spaces | Must not be empty |
| start_date | Event start date | 2026-07-15 | Date/Text | event_start_date | Date | Yes | Parse date | Must be valid |
| end_date | Event end date | 2026-07-15 | Date/Text | event_end_date | Date | No | Parse date | Must not precede start date |
| host_unit | Responsible unit | IEEE Tunisia Section | Text | organizational_unit_name | Text | Yes | Normalize name | Must match reference list |
| category | Event category | Technical | Text | event_category | Text | No | Map accepted values | Must match category list |
| modality | Event format | Hybrid | Text | modality | Text | No | Standardize values | Must be in accepted list |
| registrations | Registration count | 120 | Number/Text | registration_count | Integer | No | Convert to integer | Must be zero or greater |
| attendance | Final attendance | 96 | Number/Text | attendance_count | Integer | No | Convert to integer | Must be zero or greater |
| report_status | Reporting state | Submitted | Text | reporting_status | Text | No | Normalize status | Must match accepted values |
| satisfaction | Average satisfaction | 4.3 | Number/Text | average_satisfaction | Decimal | No | Convert to decimal | Must fit the selected scale |

## Questions to Confirm

1. Which of the listed sources actually exist?
2. Who owns each source?
3. Which sources can be shared with the intern?
4. Are historical exports available?
5. Are event IDs consistent across sources?
6. Can registration, attendance, and feedback records be linked to events?
7. Which sources contain attendee-level personal data?
8. Which fields must be anonymized?
9. How often is each source updated?
10. Which source is considered authoritative when values conflict?
11. Are the source formats stable?
12. Are there official reference lists for categories and organizational units?
13. Is a sample export available for initial development?
14. Is API access available, or will the prototype use manual files only?

## Current Status

All sources are currently provisional until confirmed with the internship
supervisor and relevant IEEE stakeholders.