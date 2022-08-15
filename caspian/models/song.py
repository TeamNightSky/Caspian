from datetime import datetime
from pydantic import BaseModel



class ImportProcess(BaseModel):
    download_id: str
    status: str
    start_time: datetime = datetime.now()
    end_time: datetime | None = None


class ListeningStatistics(BaseModel):
    listening_count: int = 0
    last_listened_at: datetime | None = None


class Song(BaseModel):
    file_path: str
    date_added: datetime = datetime.now()
    statistics: ListeningStatistics = ListeningStatistics()
    source: str = "local"
