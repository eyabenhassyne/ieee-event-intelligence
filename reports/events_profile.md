# IEEE Event Dataset Profiling Report

## Dataset Overview
- Source file: `C:\Users\Eya\ieee-event-intelligence\data\processed\events_clean.csv`
- Rows: 6198
- Columns: 40
- Fully duplicated rows: 0
- Event ID column detected: `id`

## Column Summary
| Column | Dtype | Non-null | Missing | Missing % |
| --- | --- | ---: | ---: | ---: |
| id | int64 | 6198 | 0 | 0.00 |
| title | str | 6198 | 0 | 0.00 |
| description | str | 6198 | 0 | 0.00 |
| start_time | str | 6198 | 0 | 0.00 |
| end_time | str | 6198 | 0 | 0.00 |
| time_zone | str | 6198 | 0 | 0.00 |
| city | str | 3939 | 2259 | 36.45 |
| building | str | 1649 | 4549 | 73.39 |
| room_number | str | 989 | 5209 | 84.04 |
| address1 | str | 3126 | 3072 | 49.56 |
| latitude | float64 | 2795 | 3403 | 54.90 |
| longitude | float64 | 2795 | 3403 | 54.90 |
| location_type | str | 6198 | 0 | 0.00 |
| virtual | bool | 6198 | 0 | 0.00 |
| cancelled | bool | 6198 | 0 | 0.00 |
| publish | bool | 6198 | 0 | 0.00 |
| registration_start_time | str | 2083 | 4115 | 66.39 |
| registration_end_time | str | 2083 | 4115 | 66.39 |
| registration_url | str | 2513 | 3685 | 59.45 |
| cost | bool | 6198 | 0 | 0.00 |
| max_registrations | float64 | 583 | 5615 | 90.59 |
| ieee_attending | float64 | 4465 | 1733 | 27.96 |
| guests_attending | float64 | 4465 | 1733 | 27.96 |
| tags | str | 6198 | 0 | 0.00 |
| speakers | float64 | 0 | 6198 | 100.00 |
| speaker_count | int64 | 6198 | 0 | 0.00 |
| primary_host_name | str | 6198 | 0 | 0.00 |
| primary_host_spoid | str | 6198 | 0 | 0.00 |
| primary_host_type | str | 6198 | 0 | 0.00 |
| primary_host_section_spoids | str | 6132 | 66 | 1.06 |
| primary_host_region_spoids | str | 6177 | 21 | 0.34 |
| primary_host_society_spoids | str | 3731 | 2467 | 39.80 |
| category_id | int64 | 6198 | 0 | 0.00 |
| subcategory_id | float64 | 3121 | 3077 | 49.65 |
| country_id | float64 | 3939 | 2259 | 36.45 |
| state_id | float64 | 3939 | 2259 | 36.45 |
| link | str | 6198 | 0 | 0.00 |
| created_at | str | 6198 | 0 | 0.00 |
| updated_at | str | 6198 | 0 | 0.00 |
| is_valid_date | bool | 6198 | 0 | 0.00 |

## Missing-Data Summary
| Column | Missing Count | Missing % |
| --- | ---: | ---: |
| id | 0 | 0.00 |
| title | 0 | 0.00 |
| description | 0 | 0.00 |
| start_time | 0 | 0.00 |
| end_time | 0 | 0.00 |
| time_zone | 0 | 0.00 |
| city | 2259 | 36.45 |
| building | 4549 | 73.39 |
| room_number | 5209 | 84.04 |
| address1 | 3072 | 49.56 |
| latitude | 3403 | 54.90 |
| longitude | 3403 | 54.90 |
| location_type | 0 | 0.00 |
| virtual | 0 | 0.00 |
| cancelled | 0 | 0.00 |
| publish | 0 | 0.00 |
| registration_start_time | 4115 | 66.39 |
| registration_end_time | 4115 | 66.39 |
| registration_url | 3685 | 59.45 |
| cost | 0 | 0.00 |
| max_registrations | 5615 | 90.59 |
| ieee_attending | 1733 | 27.96 |
| guests_attending | 1733 | 27.96 |
| tags | 0 | 0.00 |
| speakers | 6198 | 100.00 |
| speaker_count | 0 | 0.00 |
| primary_host_name | 0 | 0.00 |
| primary_host_spoid | 0 | 0.00 |
| primary_host_type | 0 | 0.00 |
| primary_host_section_spoids | 66 | 1.06 |
| primary_host_region_spoids | 21 | 0.34 |
| primary_host_society_spoids | 2467 | 39.80 |
| category_id | 0 | 0.00 |
| subcategory_id | 3077 | 49.65 |
| country_id | 2259 | 36.45 |
| state_id | 2259 | 36.45 |
| link | 0 | 0.00 |
| created_at | 0 | 0.00 |
| updated_at | 0 | 0.00 |
| is_valid_date | 0 | 0.00 |

## Duplicate Summary
- Fully duplicated rows: 0
- Event ID column: `id`
- Duplicate non-null event IDs: 0

## Date-Quality Summary
| Column | Invalid / Unparseable | Invalid % |
| --- | ---: | ---: |
| start_time | 0 | 0.00 |
| end_time | 0 | 0.00 |
| registration_start_time | 0 | 0.00 |
| registration_end_time | 0 | 0.00 |
| created_at | 0 | 0.00 |
| updated_at | 0 | 0.00 |

## Numeric-Quality Summary
| Column | Negative Values | Negative % of Non-null Numeric Values |
| --- | ---: | ---: |
| id | 0 | 0.00 |
| latitude | 252 | 9.02 |
| longitude | 1019 | 36.46 |
| virtual | 0 | 0.00 |
| cancelled | 0 | 0.00 |
| publish | 0 | 0.00 |
| cost | 0 | 0.00 |
| max_registrations | 0 | 0.00 |
| ieee_attending | 0 | 0.00 |
| guests_attending | 0 | 0.00 |
| speakers | 0 | 0.00 |
| speaker_count | 0 | 0.00 |
| category_id | 0 | 0.00 |
| subcategory_id | 0 | 0.00 |
| country_id | 0 | 0.00 |
| state_id | 0 | 0.00 |
| is_valid_date | 0 | 0.00 |

## Categorical-Value Summary
### location_type
`physical`, `virtual`, `hybrid`

### primary_host_type
`Section`, `Student Branch Chapter`, `Society`, `Affinity`, `Student Branch`, `Chapter`, `Joint Chapter`, `Local Group`, `Region`, `Sub-section`, `Standards Working Group`, `Committee`, `Council`

### primary_host_region_spoids
`R2`, `R0`, `R8`, `R9`, `R6`, `R1`, `R3`, `R5`, `R4`, `R7`

## Detected Risks and Recommended Next Actions
### Risks
- One or more numeric columns contain negative values that may be invalid for this dataset.
- Several columns have high missingness and may require filtering or imputation.

### Recommended Next Actions
- Review duplicate event IDs and decide whether to deduplicate or preserve versioned records.
- Inspect date fields with invalid parses before using them in time-based analysis.
- Confirm whether negative numeric values are legitimate for the affected columns.
- Assess sparse columns for removal, imputation, or separate handling in downstream modeling.
