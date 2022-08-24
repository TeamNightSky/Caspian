SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = on;

SET default_tablespace = '';
SET default_table_access_method = heap;


CREATE TABLE public.playlists (
    uuid uuid DEFAULT extensions.uuid_generate_v4() NOT NULL,
    user_id uuid NOT NULL,
    name text,
    cover_file text,
    songs text[],
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE public.scraper_logs (
    uuid uuid DEFAULT extensions.uuid_generate_v4() NOT NULL,
    source text,
    content_path text,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    exit_code integer
);


CREATE TABLE public.song_metadata (
    uuid uuid DEFAULT extensions.uuid_generate_v4() NOT NULL,
    liked boolean DEFAULT false,
    disliked boolean DEFAULT false,
    audio_path text,
    cover_path text,
    title text,
    artist text,
    album text,
    album_artist text,
    year integer,
    genre text,
    duration double precision,
    source text NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE public.plays (
    user_id uuid NOT NULL,
    song_id uuid NOT NULL,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
)


ALTER TABLE ONLY public.playlists
    ADD CONSTRAINT playlists_pkey PRIMARY KEY (uuid, user_id);

ALTER TABLE ONLY public.playlists
    ADD CONSTRAINT playlists_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id);


ALTER TABLE ONLY public.scraper_logs
    ADD CONSTRAINT scraper_logs_pkey PRIMARY KEY (uuid);


ALTER TABLE ONLY public.song_metadata
    ADD CONSTRAINT song_metadata_pkey PRIMARY KEY (uuid);


ALTER TABLE ONLY public.plays
    ADD CONSTRAINT plays_pkey PRIMARY KEY (song_id, user_id);

ALTER TABLE ONLY public.plays
    ADD CONSTRAINT plays_song_id_fkey FOREIGN KEY (song_id) REFERENCES public.song_metadata(uuid);


ALTER TABLE ONLY public.plays
    ADD CONSTRAINT plays_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id);
