-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://github.com/pgadmin-org/pgadmin4/issues/new/choose if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public."User"
(
    id bigserial NOT NULL GENERATED ALWAYS AS IDENTITY,
    username character varying(50) NOT NULL,
    password character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    student_id character varying(15) NOT NULL,
    role_id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    PRIMARY KEY (id),
    CONSTRAINT username UNIQUE (username)
);

CREATE TABLE IF NOT EXISTS public."Role"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    name character varying(50) NOT NULL,
    description text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    PRIMARY KEY (id),
    CONSTRAINT name UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS public."Board"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    title character varying(200) NOT NULL,
    metadata text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."Post"
(
    id bigserial NOT NULL GENERATED ALWAYS AS IDENTITY,
    board_id bigint NOT NULL,
    title character varying(200) NOT NULL,
    content text,
    author_id bigserial NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."PostAttachment"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    post_id bigserial NOT NULL,
    metadata text,
    url character varying(200) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."Permission"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    role_id bigint NOT NULL,
    resource_type character varying(100) NOT NULL,
    resource_id bigint NOT NULL,
    can_read boolean NOT NULL,
    can_create boolean NOT NULL,
    can_update boolean NOT NULL,
    can_delete boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."Classroom"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    title character varying NOT NULL,
    metadata text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."Session"
(
    sesson_id uuid NOT NULL,
    user_id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    ip_address character varying,
    user_agent character varying,
    PRIMARY KEY (sesson_id)
);

ALTER TABLE IF EXISTS public."User"
    ADD CONSTRAINT role_id FOREIGN KEY (role_id)
    REFERENCES public."Role" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public."Post"
    ADD CONSTRAINT board_id FOREIGN KEY (board_id)
    REFERENCES public."Board" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public."Post"
    ADD CONSTRAINT author_id FOREIGN KEY (author_id)
    REFERENCES public."User" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE SET NULL
    NOT VALID;


ALTER TABLE IF EXISTS public."PostAttachment"
    ADD CONSTRAINT post_id FOREIGN KEY (post_id)
    REFERENCES public."Post" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public."Permission"
    ADD CONSTRAINT role_id FOREIGN KEY (role_id)
    REFERENCES public."Role" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public."Session"
    ADD CONSTRAINT user_id FOREIGN KEY (user_id)
    REFERENCES public."User" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;

END;