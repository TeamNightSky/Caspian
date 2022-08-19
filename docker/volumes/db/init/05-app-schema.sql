create schema if not exists app_schema authentication supabase_admin;

grant usage on schema storage to postgres, authenticated, service_role;

/* Table of all songs (shared between users) */
create app_schema.song_metadata (
    "song_path" text UNIQUE,
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
    "created_at" timestamptz default current_timestamp,
    "updated_at" timestamptz default current_timestamp,
    primary key ("uuid")
);

/* Table of scraper logs */
CREATE app_schema.scraper_logs (
    "uuid" uuid default uuid_generate_v4() primary key,
    "source" text,
    "url" text,
    "log_path" text,
    "timestamp" timestamp default current_timestamp,
    "status" integer,
);

/* Table of user-specific song-specific statistics */
CREATE app_schema.song_stats (
    "user_id" uuid UNIQUE,
    "song_id" uuid UNIQUE,
    "plays" integer default 0,
    "liked" boolean default false,
    "disliked" boolean default false,
    primary key ("user_id", "song_id")
    CONSTRAINT "user_playlists_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id")
    CONSTRAINT "user_playlists_song_id_fkey" FOREIGN KEY ("song_id") REFERENCES "app_schema"."song_metadata"("uuid")
);

/* Table of user playlists */
CREATE app_schema.user_playlists (
    "user_id" uuid UNIQUE,
    "playlist_id" uuid UNIQUE default uuid_generate_v4(),
    "name" text,
    "cover_path" text default null,
    "songs" text[],
    "created_at" timestamptz default current_timestamp,
    "updated_at" timestamptz default current_timestamp,
    primary key ("playlist_id")
    CONSTRAINT "user_playlists_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id")
);
