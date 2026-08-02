INSERT INTO analytics.dim_category (
    category_key, source_category_id, category_name, archived, is_unknown, created_at, updated_at
)
SELECT 0, NULL, 'Unknown', NULL, TRUE, current_timestamp, current_timestamp
WHERE NOT EXISTS (
    SELECT 1 FROM analytics.dim_category WHERE category_key = 0
);
SELECT setval(pg_get_serial_sequence('analytics.dim_category', 'category_key'),
              GREATEST((SELECT COALESCE(MAX(category_key), 0) FROM analytics.dim_category), 1),
              true);

INSERT INTO analytics.dim_subcategory (
    subcategory_key, source_subcategory_id, category_key, subcategory_name, archived, is_unknown, created_at, updated_at
)
SELECT 0, NULL, 0, 'Unknown', NULL, TRUE, current_timestamp, current_timestamp
WHERE NOT EXISTS (
    SELECT 1 FROM analytics.dim_subcategory WHERE subcategory_key = 0
);
SELECT setval(pg_get_serial_sequence('analytics.dim_subcategory', 'subcategory_key'),
              GREATEST((SELECT COALESCE(MAX(subcategory_key), 0) FROM analytics.dim_subcategory), 1),
              true);

INSERT INTO analytics.dim_country (
    country_key, source_country_id, country_name, abbreviation, is_unknown, created_at, updated_at
)
SELECT 0, NULL, 'Unknown', NULL, TRUE, current_timestamp, current_timestamp
WHERE NOT EXISTS (
    SELECT 1 FROM analytics.dim_country WHERE country_key = 0
);
SELECT setval(pg_get_serial_sequence('analytics.dim_country', 'country_key'),
              GREATEST((SELECT COALESCE(MAX(country_key), 0) FROM analytics.dim_country), 1),
              true);

INSERT INTO analytics.dim_state (
    state_key, source_state_id, country_key, state_name, abbreviation, is_unknown, created_at, updated_at
)
SELECT 0, NULL, 0, 'Unknown', NULL, TRUE, current_timestamp, current_timestamp
WHERE NOT EXISTS (
    SELECT 1 FROM analytics.dim_state WHERE state_key = 0
);
SELECT setval(pg_get_serial_sequence('analytics.dim_state', 'state_key'),
              GREATEST((SELECT COALESCE(MAX(state_key), 0) FROM analytics.dim_state), 1),
              true);

INSERT INTO analytics.dim_location (
    location_key, city, address1, building, room_number, latitude, longitude, location_type,
    location_signature, is_unknown, is_not_applicable, created_at
)
SELECT 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'unknown', TRUE, FALSE, current_timestamp
WHERE NOT EXISTS (
    SELECT 1 FROM analytics.dim_location WHERE location_key = 0
);
INSERT INTO analytics.dim_location (
    location_key, city, address1, building, room_number, latitude, longitude, location_type,
    location_signature, is_unknown, is_not_applicable, created_at
)
SELECT 1, NULL, NULL, NULL, NULL, NULL, NULL, 'virtual', 'not-applicable-virtual', FALSE, TRUE, current_timestamp
WHERE NOT EXISTS (
    SELECT 1 FROM analytics.dim_location WHERE location_key = 1
);
SELECT setval(pg_get_serial_sequence('analytics.dim_location', 'location_key'),
              GREATEST((SELECT COALESCE(MAX(location_key), 0) FROM analytics.dim_location), 1));

INSERT INTO analytics.dim_organizing_unit (
    organizing_unit_key, primary_host_spoid, primary_host_name, primary_host_type,
    section_spoids, region_spoids, society_spoids, is_unknown, created_at, updated_at
)
SELECT 0, NULL, 'Unknown', NULL, NULL, NULL, NULL, TRUE, current_timestamp, current_timestamp
WHERE NOT EXISTS (
    SELECT 1 FROM analytics.dim_organizing_unit WHERE organizing_unit_key = 0
);
SELECT setval(pg_get_serial_sequence('analytics.dim_organizing_unit', 'organizing_unit_key'),
              GREATEST((SELECT COALESCE(MAX(organizing_unit_key), 0) FROM analytics.dim_organizing_unit), 1),
              true);
