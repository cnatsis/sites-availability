CREATE TABLE IF NOT EXISTS success_requests
(
    id bigserial NOT NULL PRIMARY KEY,
    request_time timestamp,
    type character varying(255),
    site_url character varying(255),
    response_time_sec double precision,
    status_code int,
    regex character varying(255),
    regex_result character varying(255)
);