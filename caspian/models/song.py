from datetime import datetime
import statistics
from pydantic import BaseModel


class ListeningStatistics(BaseModel):
    listening_count: int = 0
    last_listened_at: datetime | None = None


class Song(BaseModel):
    content: bytes
    date_added: datetime = datetime.now()
    statistics: ListeningStatistics = ListeningStatistics()
    source: str = "local"
