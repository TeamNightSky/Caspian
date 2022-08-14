"""Module for Scraper protocol."""

import uuid
import pathlib


class Scraper:
    """Base class for scrapers."""

    timeout: int = 6 * 60 * 60  # 6 hours

    def __init__(self, url):
        self.url = url
        self.download_id = f"download-{uuid.uuid4()}"

    @property
    def download_dir(self) -> pathlib.Path:
        """Return the download path."""
        path = pathlib.Path(f"downloads/{self.download_id}")
        if not path.exists():
            path.mkdir(parents=True)
        return path

    async def scrape(self) -> None:
        """Scrapes the URL and saves files."""
        raise NotImplementedError()

    def delete(self) -> None:
        """Delete the download directory."""
        if self.download_dir.exists():
            for file in self.download_dir.iterdir():
                file.unlink()
            self.download_dir.rmdir()
