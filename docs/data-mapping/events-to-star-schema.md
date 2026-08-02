# Events to Star Schema Mapping

## Source Selection
- Preferred source: `data/processed/events_analytics.csv`
- Fallback source: `data/processed/events_clean.csv`

## Mapping Rules
| Source File | Source Column | Target Schema | Target Table | Target Column | Transformation | Null Handling | Validation Rule | Lookup or Surrogate-Key Rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| events_analytics / events_clean | `id` | analytics | fact_events | source_event_id | cast to bigint | required | must be present and positive | unique business key for UPSERT |
| events_analytics / events_clean | `title` | analytics | fact_events | title | trim whitespace | required | non-empty | direct text |
| events_analytics / events_clean | `description` | analytics | fact_events | description | trim whitespace | nullable | none | direct text |
| events_analytics / events_clean | `start_time` | analytics | fact_events | start_time | parse timestamp | required | valid timestamp | derive `date_key` from start date |
| events_analytics / events_clean | `end_time` | analytics | fact_events | end_time | parse timestamp | nullable | end_time >= start_time when both present | direct timestamp |
| events_analytics / events_clean | `time_zone` | analytics | fact_events | time_zone | trim whitespace | nullable | none | direct text |
| events_analytics / events_clean | `link` | analytics | fact_events | source_link | trim whitespace | nullable | none | direct URL |
| events_analytics / events_clean | `created_at` | analytics | fact_events | source_created_at | parse timestamp | nullable | valid timestamp if present | direct timestamp |
| events_analytics / events_clean | `updated_at` | analytics | fact_events | source_updated_at | parse timestamp | nullable | valid timestamp if present | direct timestamp |
| events_analytics / events_clean | `virtual` | analytics | fact_events | virtual | parse boolean | default false | boolean-like | direct flag |
| events_analytics / events_clean | `cancelled` | analytics | fact_events | cancelled | parse boolean | default false | boolean-like | direct flag |
| events_analytics / events_clean | `publish` | analytics | fact_events | published | parse boolean | default false | boolean-like | direct flag |
| events_analytics / events_clean | `is_valid_date` | analytics | fact_events | is_valid_date | parse boolean | nullable | boolean-like | direct flag |
| events_analytics / events_clean | `ieee_attending` | analytics | fact_events | ieee_attending | parse integer | nullable | nonnegative if present | direct measure |
| events_analytics / events_clean | `guests_attending` | analytics | fact_events | guests_attending | parse integer | nullable | nonnegative if present | direct measure |
| events_analytics / events_clean | `max_registrations` | analytics | fact_events | max_registrations | parse integer | nullable | nonnegative if present | direct measure |
| events_analytics / events_clean | `speaker_count` | analytics | fact_events | speaker_count | parse integer | nullable | nonnegative if present | direct measure |
| events_analytics / events_clean | `category_id` | analytics | dim_category / fact_events | source_category_id / category_key | lookup category_key | unknown category key 0 when missing | source id should match a category row when present | category dimension surrogate key |
| events_analytics / events_clean | `subcategory_id` | analytics | dim_subcategory / fact_events | source_subcategory_id / subcategory_key | lookup subcategory_key | unknown subcategory key 0 when missing | source id should match a subcategory row when present | category_key resolved through category_id |
| events_analytics / events_clean | `country_id` | analytics | dim_country / fact_events | source_country_id / country_key | lookup country_key | unknown country key 0 when missing | source id should match a country row when present | country dimension surrogate key |
| events_analytics / events_clean | `state_id` | analytics | dim_state / fact_events | source_state_id / state_key | lookup state_key | unknown state key 0 when missing | source id should match a state row when present | country_key resolved through state parent country_id |
| events_analytics / events_clean | `city`, `address1`, `building`, `room_number`, `latitude`, `longitude`, `location_type` | analytics | dim_location / fact_events | location attributes / location_key | normalize whitespace, build signature, upsert location | use unknown or virtual no-location members when missing | latitude and longitude range checks | real location signature, unknown key 0, virtual not-applicable key 1 |
| events_analytics / events_clean | `primary_host_spoid`, `primary_host_name`, `primary_host_type`, `primary_host_section_spoids`, `primary_host_region_spoids`, `primary_host_society_spoids` | analytics | dim_organizing_unit / fact_events | organizing unit attributes / organizing_unit_key | normalize text and SPOID lists, upsert by primary_host_spoid | unknown organizing-unit key 0 when missing | host name required for dimension row | business key is primary_host_spoid |
| events_analytics / events_clean | `start_time` | analytics | dim_date / fact_events | date_key | derive YYYYMMDD integer from event start date | required for valid events | valid date | insert missing date rows only |
| events_analytics / events_clean | derived | analytics | fact_events | duration_hours | `(end_time - start_time)` hours when both valid | nullable | nonnegative when present | computed measure |
| events_analytics / events_clean | derived | analytics | fact_events | total_attendance | `ieee_attending + guests_attending` only when both present; preserve single reported value when only one exists | nullable | nonnegative; consistent with inputs | computed measure |
| events_analytics / events_clean | derived | analytics | fact_events | attendance_available | true only when attendance is genuinely reported | false by default | must reflect at least one attendance value | computed flag |
| events_analytics / events_clean | derived | analytics | fact_events | registration_available | true only when registration fields are supported by source | false by default | use available registration fields only | computed flag |
| events_analytics / events_clean | derived | analytics | fact_events | has_capacity | true when `max_registrations` exists | false by default | derived from presence of capacity | computed flag |
| events_analytics / events_clean | derived | analytics | fact_events | has_location | true when a real or virtual location is resolved | false by default | derived from location resolution | computed flag |
| events_analytics / events_clean | derived | analytics | fact_events | has_subcategory | true when subcategory resolves | false by default | derived from subcategory resolution | computed flag |
| events_analytics / events_clean | derived | analytics | fact_events | event_count | constant `1` | not nullable | must equal 1 | additive fact row marker |
