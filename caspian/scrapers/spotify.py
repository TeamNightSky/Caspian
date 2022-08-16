"""Module for scraping Spotify data."""

import asyncio

from caspian.scrapers.base import Scraper


class SpotifyScraper(Scraper, source="spotify"):
    """Scraper for Spotify."""

    async def start(
        self, stdout, stderr, stdin
    ) -> asyncio.subprocess.Process:  # pylint: disable=no-member
        """Start the scraper subprocess"""
        return await asyncio.create_subprocess_shell(
            f'spotdl "{self.url}" --path-template "{self.download_dir}/{{artist}} - {{title}}.{{ext}}"',
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            close_fds=True,
        )
