import os
from datetime import datetime
import enum
import uuid
from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    Enum,
    Integer,
    ForeignKey,
    Text,
    LargeBinary,
    create_engine,
    String,
    Float,
)
from sqlalchemy.orm import declarative_base, Mapped, relationship, sessionmaker
from sqlalchemy.dialects.postgresql import JSONB


from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles

from api import DEBUG

Base = declarative_base()

ENGINE = create_engine(
    os.environ["POSTGRES_URL"].replace("localhost", "host.docker.internal"),
    echo=DEBUG,
)

Session = sessionmaker(bind=ENGINE)


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **_):
    return compiler.visit_drop_table(element) + " CASCADE"


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    cover = Column(LargeBinary)

    songs: Mapped[list["Song"]] = relationship(back_populates="artist")


class Play(Base):
    __tablename__ = "plays"

    id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)

    user_id = Column(UUID(as_uuid=True), nullable=False)
    song: Mapped["Song"] = relationship(foreign_keys=[song_id], back_populates="plays")


class Song(Base):
    __tablename__ = "songs"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(Text, nullable=False)

    artist_id: str = Column(
        ForeignKey("artists.id"),
        nullable=False,
    )

    plays: Mapped[list[Play]] = relationship(back_populates="song")
    year = Column(Integer)
    genre = Column(Text)
    duration = Column(Float)

    uploaded_by: uuid.UUID = Column(UUID, ForeignKey("auth.users.id"), nullable=False)
    artist: Mapped[Artist] = relationship(back_populates="songs")


class JobType(enum.Enum):
    youtube = "youtube"
    spotify = "spotify"


class Scraper(Base):
    __tablename__ = "scrapers"

    id = Column(Integer, primary_key=True)
    job_id = Column(Text, unique=True)

    job_type = Column(Enum(JobType), nullable=False)
    url = Column(Text, nullable=False)

    started_by = Column(UUID(as_uuid=True), nullable=False)
    started = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Scraper(job_id={self.job_id}, url={self.url}, status={self.status})>"
