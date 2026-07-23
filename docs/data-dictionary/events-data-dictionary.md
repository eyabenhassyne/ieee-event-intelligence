# IEEE Events Data Dictionary

## Scope
This dictionary documents the columns in `data/processed/events_clean.csv` and the recommended analytics treatment for the first BI version.

| Column | Detected Type | Business Meaning Inferred | Nullable / Required | Example Use in Analytics | Recommended Treatment | First BI Version |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | Integer | Unique event identifier from the source system | Required | Event grain, deduplication, drill-through | Keep as the event key | Yes |
| `title` | Text | Event title or name | Required | Event listing, search, headline cards | Keep as display field | Yes |
| `description` | Text | Event description or summary HTML/text | Required | Content analysis, event detail pages | Keep; consider HTML stripping for BI | Yes |
| `start_time` | Datetime | Scheduled event start timestamp | Required | Event trends by day/week/month | Parse as datetime and use as primary date | Yes |
| `end_time` | Datetime | Scheduled event end timestamp | Nullable | Duration analysis, schedule validation | Parse as datetime; use for duration checks | Yes |
| `time_zone` | Text | Time zone for the scheduled event | Required | Local-time interpretation, regional scheduling | Keep as reference attribute | Yes |
| `city` | Text | Event city | Nullable | Geographic distribution by city | Keep; normalize casing if needed | Yes |
| `building` | Text | Building or venue name | Nullable | Venue analysis, on-site clustering | Keep but treat as sparse attribute | No |
| `room_number` | Text | Room, suite, or hall identifier | Nullable | Venue-level detail, occupancy analysis | Keep as optional drill-down field | No |
| `address1` | Text | Street address or venue address line 1 | Nullable | Map visuals, address search | Keep for location context; may need cleaning | Yes |
| `latitude` | Decimal | Event latitude coordinate | Nullable | Map plotting, regional heatmaps | Keep; validate range and null rate | Yes |
| `longitude` | Decimal | Event longitude coordinate | Nullable | Map plotting, regional heatmaps | Keep; validate range and null rate | Yes |
| `location_type` | Text | Location mode such as physical or virtual | Required | Physical vs virtual segmentation | Keep as a key slicer | Yes |
| `virtual` | Boolean | Indicates virtual event flag | Required | Virtual event share, channel mix | Keep as a boolean dimension | Yes |
| `cancelled` | Boolean | Indicates whether the event was cancelled | Required | Cancellation rate, operational health | Keep as a status flag | Yes |
| `publish` | Boolean | Indicates whether the event is published | Required | Published vs unpublished backlog | Keep as a lifecycle flag | No |
| `registration_start_time` | Datetime | Registration opening timestamp | Nullable | Lead-time analysis, registration windows | Parse as datetime; useful for lead-time metrics | Yes |
| `registration_end_time` | Datetime | Registration closing timestamp | Nullable | Registration window analysis | Parse as datetime; useful for cutoff checks | Yes |
| `registration_url` | Text | Link to event registration page | Nullable | Click-through analysis, registration tracking | Keep as reference field, not a core BI visual field | No |
| `cost` | Boolean | Indicates whether the event has a cost/free flag | Required | Free vs paid event analysis | Treat as categorical flag | Yes |
| `max_registrations` | Decimal | Maximum capacity or cap on registrations | Nullable | Capacity planning, fill-rate analysis | Keep as numeric capacity field | Yes |
| `ieee_attending` | Decimal | Expected or recorded IEEE attendee count | Nullable | Attendance breakdown, demand analysis | Keep; derive total attendance with guests | Yes |
| `guests_attending` | Decimal | Expected or recorded guest attendee count | Nullable | Attendance breakdown, guest participation | Keep; derive total attendance with IEEE attendees | Yes |
| `tags` | Text | Hashtag or tag list associated with the event | Required | Theme analysis, topic filters | Keep; consider split into a tag bridge later | No |
| `speakers` | Empty / Unused | Speaker detail field with no populated values in this extract | Fully empty | Speaker analytics | Remove from analytics model | No |
| `speaker_count` | Integer | Count of speakers associated with the event | Required | Speaker volume, event complexity | Keep as a compact speaker metric | Yes |
| `primary_host_name` | Text | Main host organization or section | Required | Host performance, section reporting | Keep as a primary organizational dimension | Yes |
| `primary_host_spoid` | Text | Source system identifier for the primary host | Required | Host deduplication, drill-through | Keep as a technical reference key | No |
| `primary_host_type` | Text | Host classification such as section, society, or chapter | Required | Host type segmentation | Keep as a core slicer | Yes |
| `primary_host_section_spoids` | Text | Section identifiers attached to the primary host | Nullable | Section lineage and mapping | Keep as a bridge/reference field | No |
| `primary_host_region_spoids` | Text | Region identifiers attached to the host | Nullable | Regional reporting and rollups | Keep as a bridge/reference field | No |
| `primary_host_society_spoids` | Text | Society identifiers attached to the host | Nullable | Society-based reporting | Keep as a bridge/reference field | No |
| `category_id` | Integer | Primary category identifier | Required | Category mix and portfolio analysis | Keep; map to category lookup later | Yes |
| `subcategory_id` | Decimal / Integer | Secondary category identifier | Nullable | Subcategory drill-down, thematic detail | Keep and derive `has_subcategory` | Yes |
| `country_id` | Decimal / Integer | Country identifier | Nullable | Country-level distribution | Keep; map to country lookup later | Yes |
| `state_id` | Decimal / Integer | State or province identifier | Nullable | State-level distribution | Keep; map to state lookup later | Yes |
| `link` | Text | Public event page URL | Required | Event detail navigation, QA checks | Keep as a reference URL | Yes |
| `created_at` | Datetime | Record creation timestamp in the source platform | Required | Data freshness and ingestion timing | Parse as datetime for lineage and QA | No |
| `updated_at` | Datetime | Last update timestamp in the source platform | Required | Refresh tracking, recency analysis | Parse as datetime for data currency checks | No |
| `is_valid_date` | Boolean | Source-generated indicator of date validity | Required | QA flag for event schedule completeness | Keep as a validation flag, not a KPI | No |

## Notes
- The first BI version should focus on event identity, timing, geography, attendance, capacity, and host/category slicing.
- The fully empty `speakers` column should be excluded from the semantic model.
- Lookup tables for category, country, state, host, and tag expansion can be added in later BI iterations.
