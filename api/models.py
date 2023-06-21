import os
from datetime import datetime
import enum
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

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]
POSTGRES_DB = os.environ["POSTGRES_DB"]

ENGINE = create_engine(
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
    echo=DEBUG,
)

Session = sessionmaker(bind=ENGINE)


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **_):
    return compiler.visit_drop_table(element) + " CASCADE"


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}

    instance_id = Column(UUID)
    id = Column(UUID, nullable=False, primary_key=True)
    aud = Column(String(255))
    role = Column(String(255))
    email = Column(String(255), unique=True)
    encrypted_password = Column(String(255))
    confirmed_at = Column(DateTime)
    invited_at = Column(DateTime)
    confirmation_token = Column(String(255))
    confirmation_sent_at = Column(DateTime)
    recovery_token = Column(String(255))
    recovery_sent_at = Column(DateTime)
    email_change_token = Column(String(255))
    email_change = Column(String(255))
    email_change_sent_at = Column(DateTime)
    last_sign_in_at = Column(DateTime)
    raw_app_meta_data = Column(JSONB)
    raw_user_meta_data = Column(JSONB)
    is_super_admin = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


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

    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"), nullable=False)
    user: Mapped["User"] = relationship()

    song: Mapped["Song"] = relationship("Song", back_populates="plays")


class Song(Base):
    __tablename__ = "songs"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(Text, nullable=False)

    artist_id: str = Column(Integer, ForeignKey("artists.id"), nullable=False)

    plays: Mapped[list[Play]] = relationship(back_populates="song")
    year = Column(Integer)
    genre = Column(Text)
    duration = Column(Float)

    content = Column(LargeBinary, nullable=False)
    cover = Column(LargeBinary)

    uploaded_by = Column(
        UUID(as_uuid=True), ForeignKey("auth.users.id")
    )
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

    started_by = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"), nullable=False)
    started = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Scraper(job_id={self.job_id}, url={self.url}, status={self.status})>"
