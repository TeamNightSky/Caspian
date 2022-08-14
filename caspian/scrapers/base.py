"""Module for Scraper protocol."""

import asyncio
import os
import pathlib
import urllib.parse
import uuid
from typing import Any, AsyncGenerator, Generator


def prepare_url(url: str) -> str:
    """Prepares URL for scraping."""
    return (
        urllib.parse.urlparse(url)
        ._replace(
            scheme="https",
            fragment="",
        )
        .geturl()
    )


class Scraper:
    """Base class for scrapers."""

    LOGS_DIR = "logs"
    DOWNLOAD_DIR = "downloads"

    def __init__(self, url):
        self.url = prepare_url(url)
        self.download_id = f"download-{uuid.uuid4()}"

    @property
    def log_id(self) -> str:
        """Return the log id."""
        return f"{self.download_id}.log"

    @property
    def log_file(self) -> pathlib.Path:
        """Return the log file."""
        path = pathlib.Path(self.LOGS_DIR, self.log_id)
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        return path

    @property
    def download_dir(self) -> pathlib.Path:
        """Return the download path."""
        path = pathlib.Path(self.DOWNLOAD_DIR, self.download_id)
        if not path.exists():
            path.mkdir(parents=True)
        return path

    async def start(
        self,
        stdout: Any,
        stderr: Any,
        stdin: Any,
    ) -> asyncio.subprocess.Process:  # pylint: disable=no-member
        """Starts the scraper subprocess."""
        raise NotImplementedError()

    def downloads(self) -> Generator[pathlib.Path, None, None]:
        """Return the list of downloaded mp3 files."""
        return self.download_dir.glob("*.mp3")

    async def run(self, timeout: int) -> AsyncGenerator[bytes, None]:
        """Run the scraper."""
        proc = await self.start(
            self.log_file.open("wb"),
            asyncio.subprocess.STDOUT,
            None,
        )
        try:
            await asyncio.wait_for(proc.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            proc.kill()
        finally:
            for file in self.downloads():
                yield file.read_bytes()
                os.remove(file)
            self.download_dir.rmdir()
