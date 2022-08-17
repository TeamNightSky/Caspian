"""Module for scraping YouTube data."""
import asyncio

from api.scrapers.base import Scraper


class YoutubeScraper(Scraper, source="youtube"):
    """Scraper for Youtube."""

    async def start(
        self, stdout, stderr, stdin
    ) -> asyncio.subprocess.Process:  # pylint: disable=no-member
        """Starts the YouTube scraper subprocess."""
        return await asyncio.create_subprocess_shell(
            f'youtube-dl --add-metadata --yes-playlist -x --audio-format mp3 --audio-quality 0 --retries infinite --socket-timeout 30 --prefer-ffmpeg --no-call-home -i --output "{self.download_dir}/%(channel)s - %(title)s.%(ext)s" "{self.url}"',
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            close_fds=True,
        )
