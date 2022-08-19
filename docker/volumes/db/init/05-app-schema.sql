create schema if not exists app_schema authentication authenticated;

create app_schema.song_metadata (
    "song_path" text primary key,
    "uuid" uuid default uuid_generate_v4(),
    "title" text,
    "artist" text,
    "album" text,
    "album_artist" text,
    "year" integer,
    "genre" text,
    "duration" float,
    "plays" integer,
    "cover_path" text default null,
    "source" text,
    "created_at" timestamp default current_timestamp,
    "updated_at" timestamp default current_timestamp
);

CREATE app_schema.scraper_logs (
    "source" text,
    "url" text,
    "log_path" text,
    "timestamp" timestamp default current_timestamp,
    "status" integer,
);

CREATE app_schema.song_stats (
    "user_id" uuid UNIQUE,
    "song_path" text UNIQUE,
    "plays" integer default 0,
    "liked" boolean default false,
    "disliked" boolean default false,
    primary key ("user_id", "song_file")
);


CREATE app_schema.user_playlists (
    "user_id" uuid UNIQUE,
    "playlist_id" uuid UNIQUE default uuid_generate_v4(),
    "name" text,
    "cover_path" text default null,
    "songs" text[],
    "created_at" timestamp default current_timestamp,
    "updated_at" timestamp default current_timestamp,
    primary key ("user_id", "playlist_id")
);
