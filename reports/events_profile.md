# IEEE Event Dataset Profiling Report

## Dataset Overview
- Source file: `C:\Users\Eya\ieee-event-intelligence\data\processed\events_clean.csv`
- Rows: 6198
- Columns: 40
- Fully duplicated rows: 0
- Fully empty columns: 1
- Event ID column detected: `id`

## Column Summary
| Column | Dtype | Non-null | Missing | Missing % | Class | Status |
| --- | --- | ---: | ---: | ---: | --- | --- |
| id | int64 | 6198 | 0 | 0.00 | Low | Populated |
| title | str | 6198 | 0 | 0.00 | Low | Populated |
| description | str | 6198 | 0 | 0.00 | Low | Populated |
| start_time | str | 6198 | 0 | 0.00 | Low | Populated |
| end_time | str | 6198 | 0 | 0.00 | Low | Populated |
| time_zone | str | 6198 | 0 | 0.00 | Low | Populated |
| city | str | 3939 | 2259 | 36.45 | Medium | Populated |
| building | str | 1649 | 4549 | 73.39 | High | Populated |
| room_number | str | 989 | 5209 | 84.04 | Critical | Populated |
| address1 | str | 3126 | 3072 | 49.56 | High | Populated |
| latitude | float64 | 2795 | 3403 | 54.90 | High | Populated |
| longitude | float64 | 2795 | 3403 | 54.90 | High | Populated |
| location_type | str | 6198 | 0 | 0.00 | Low | Populated |
| virtual | bool | 6198 | 0 | 0.00 | Low | Populated |
| cancelled | bool | 6198 | 0 | 0.00 | Low | Populated |
| publish | bool | 6198 | 0 | 0.00 | Low | Populated |
| registration_start_time | str | 2083 | 4115 | 66.39 | High | Populated |
| registration_end_time | str | 2083 | 4115 | 66.39 | High | Populated |
| registration_url | str | 2513 | 3685 | 59.45 | High | Populated |
| cost | bool | 6198 | 0 | 0.00 | Low | Populated |
| max_registrations | float64 | 583 | 5615 | 90.59 | Critical | Populated |
| ieee_attending | float64 | 4465 | 1733 | 27.96 | Medium | Populated |
| guests_attending | float64 | 4465 | 1733 | 27.96 | Medium | Populated |
| tags | str | 6198 | 0 | 0.00 | Low | Populated |
| speakers | float64 | 0 | 6198 | 100.00 | Critical | Fully empty |
| speaker_count | int64 | 6198 | 0 | 0.00 | Low | Populated |
| primary_host_name | str | 6198 | 0 | 0.00 | Low | Populated |
| primary_host_spoid | str | 6198 | 0 | 0.00 | Low | Populated |
| primary_host_type | str | 6198 | 0 | 0.00 | Low | Populated |
| primary_host_section_spoids | str | 6132 | 66 | 1.06 | Low | Populated |
| primary_host_region_spoids | str | 6177 | 21 | 0.34 | Low | Populated |
| primary_host_society_spoids | str | 3731 | 2467 | 39.80 | Medium | Populated |
| category_id | int64 | 6198 | 0 | 0.00 | Low | Populated |
| subcategory_id | float64 | 3121 | 3077 | 49.65 | High | Populated |
| country_id | float64 | 3939 | 2259 | 36.45 | Medium | Populated |
| state_id | float64 | 3939 | 2259 | 36.45 | Medium | Populated |
| link | str | 6198 | 0 | 0.00 | Low | Populated |
| created_at | str | 6198 | 0 | 0.00 | Low | Populated |
| updated_at | str | 6198 | 0 | 0.00 | Low | Populated |
| is_valid_date | bool | 6198 | 0 | 0.00 | Low | Populated |

## Missing-Data Summary
| Column | Missing Count | Missing % | Class |
| --- | ---: | ---: | --- |
| id | 0 | 0.00 | Low |
| title | 0 | 0.00 | Low |
| description | 0 | 0.00 | Low |
| start_time | 0 | 0.00 | Low |
| end_time | 0 | 0.00 | Low |
| time_zone | 0 | 0.00 | Low |
| city | 2259 | 36.45 | Medium |
| building | 4549 | 73.39 | High |
| room_number | 5209 | 84.04 | Critical |
| address1 | 3072 | 49.56 | High |
| latitude | 3403 | 54.90 | High |
| longitude | 3403 | 54.90 | High |
| location_type | 0 | 0.00 | Low |
| virtual | 0 | 0.00 | Low |
| cancelled | 0 | 0.00 | Low |
| publish | 0 | 0.00 | Low |
| registration_start_time | 4115 | 66.39 | High |
| registration_end_time | 4115 | 66.39 | High |
| registration_url | 3685 | 59.45 | High |
| cost | 0 | 0.00 | Low |
| max_registrations | 5615 | 90.59 | Critical |
| ieee_attending | 1733 | 27.96 | Medium |
| guests_attending | 1733 | 27.96 | Medium |
| tags | 0 | 0.00 | Low |
| speakers | 6198 | 100.00 | Critical |
| speaker_count | 0 | 0.00 | Low |
| primary_host_name | 0 | 0.00 | Low |
| primary_host_spoid | 0 | 0.00 | Low |
| primary_host_type | 0 | 0.00 | Low |
| primary_host_section_spoids | 66 | 1.06 | Low |
| primary_host_region_spoids | 21 | 0.34 | Low |
| primary_host_society_spoids | 2467 | 39.80 | Medium |
| category_id | 0 | 0.00 | Low |
| subcategory_id | 3077 | 49.65 | High |
| country_id | 2259 | 36.45 | Medium |
| state_id | 2259 | 36.45 | Medium |
| link | 0 | 0.00 | Low |
| created_at | 0 | 0.00 | Low |
| updated_at | 0 | 0.00 | Low |
| is_valid_date | 0 | 0.00 | Low |

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
| max_registrations | 0 | 0.00 |
| ieee_attending | 0 | 0.00 |
| guests_attending | 0 | 0.00 |
| speakers | 0 | 0.00 |
| speaker_count | 0 | 0.00 |
| category_id | 0 | 0.00 |
| subcategory_id | 0 | 0.00 |
| country_id | 0 | 0.00 |
| state_id | 0 | 0.00 |

## Categorical-Value Summary
### location_type
`physical`, `virtual`, `hybrid`

### primary_host_type
`Section`, `Student Branch Chapter`, `Society`, `Affinity`, `Student Branch`, `Chapter`, `Joint Chapter`, `Local Group`, `Region`, `Sub-section`, `Standards Working Group`, `Committee`, `Council`

### primary_host_region_spoids
`R2`, `R0`, `R8`, `R9`, `R6`, `R1`, `R3`, `R5`, `R4`, `R7`

## Detected Risks and Recommended Next Actions
### Risks
- 1 columns are fully empty and should be removed or backfilled from source data.
- 11 columns have high or critical missingness and may require filtering or imputation.

### Recommended Next Actions
- Remove or source-fill fully empty columns: speakers.
- Treat the high-missingness fields as optional in Power BI or mask them behind a drill-through page.
- Use location and registration fields selectively because they are sparsely populated for many events.
- Keep attendance metrics but add null-handling measures in BI because attendance and capacity fields are not complete.
