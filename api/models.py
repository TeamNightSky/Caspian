from datetime import datetime
import enum
from sqlalchemy import Column, DateTime, Enum, Integer, ForeignKey, Text, LargeBinary
from sqlalchemy.orm import declarative_base, Mapped, relationship


Base = declarative_base()


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)

    songs: Mapped[list["Song"]] = relationship(back_populates="artist")


class Playlist(Base):
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)

    songs


class Play(Base):
    __tablename__ = "plays"

    id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)

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

    started = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Scraper(job_id={self.job_id}, url={self.url}, status={self.status})>"
