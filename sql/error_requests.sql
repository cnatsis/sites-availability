CREATE TABLE IF NOT EXISTS error_requests
(
    id bigserial NOT NULL PRIMARY KEY,
    request_time timestamp,
    type character varying(255),
    site_url character varying(255),
    exception_type character varying(255)
);