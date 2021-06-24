CREATE TABLE error_requests
(
    id bigserial NOT NULL,
    request_time timestamp,
    type character varying(255),
    site_url character varying(255),
    exception_type character varying(255)
)

ALTER TABLE ONLY error_requests
    ADD CONSTRAINT error_requests_pkey PRIMARY KEY (id);