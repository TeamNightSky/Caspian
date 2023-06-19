import os
from datetime import datetime
import enum
from sqlalchemy import UUID, Column, DateTime, Enum, Integer, ForeignKey, Text, LargeBinary, create_engine
from sqlalchemy.orm import declarative_base, Mapped, relationship, sessionmaker

from api import DEBUG

Base = declarative_base()

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]
POSTGRES_DB = os.environ["POSTGRES_DB"]

ENGINE = create_engine(
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
    echo=DEBUG
)

Session = sessionmaker(bind=ENGINE)


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)

    songs: Mapped[list["Song"]] = relationship(back_populates="artist")


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)

    owner_id = Column(UUID(as_uuid=True), ForeignKey("auth.user.id"), nullable=False)
    songs: Mapped[list["Song"]] = relationship("Song", secondary="playlist_songs")



class Play(Base):
    __tablename__ = "plays"

    id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.user.id"), nullable=False)
    song: Mapped["Song"] = relationship("Song", back_populates="plays")


class Song(Base):
    __tablename__ = "songs"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(Text, nullable=False)
    
    artist_id: str = Column(Text, ForeignKey("artists.id"), nullable=False)
    
    plays: Mapped[list[Play]] = relationship("Play", back_populates="song")
    year = Column(Integer)
    genre = Column(Text)

    content_bytes = Column(LargeBinary, nullable=False)
    cover_bytes = Column(LargeBinary)

    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("auth.user.id"), nullable=False)
    artist: Mapped[Artist] = relationship("Artist", back_populates="songs")


class JobType(enum.Enum):
    youtube = "youtube"
    spotify = "spotify"


class Scraper(Base):
    __tablename__ = "scrapers"

    id = Column(Integer, primary_key=True)
    job_id = Column(Text, unique=True)

    job_type = Column(Enum(JobType), nullable=False)
    url = Column(Text, nullable=False)

    started_by = Column(UUID(as_uuid=True), ForeignKey("auth.user.id"), nullable=False)
    started = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Scraper(job_id={self.job_id}, url={self.url}, status={self.status})>"
