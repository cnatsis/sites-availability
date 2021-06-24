CREATE TABLE success_requests
(
    id bigserial NOT NULL,
    request_time timestamp,
    type character varying(255),
    site_url character varying(255),
    response_time_sec double precision,
    status_code int,
    regex_search character varying(255)
)

ALTER TABLE ONLY success_requests
    ADD CONSTRAINT success_requests_pkey PRIMARY KEY (id);