from aiohttp import ClientSession
import asyncio
import re
from typing import List


HREF_RE = (
    r"href=\""
    r"(?P<url>https?\:\/\/(www\.)?(\S+\.)+[a-z]{2,}(\/[^\s\'\"]+)*\/?)\""
)
HREF_PROG = re.compile(HREF_RE)


async def fetch_html(session: ClientSession, url: str) -> str:
    """Get the HTML string of `url`."""
    async with session.get(url) as response:
        return await response.text()


def get_urls_from_html(html: str) -> List[str]:
    """Get a list of all links in `html`."""
    href_matches = HREF_PROG.findall(html)
    return [href_match[0] for href_match in href_matches]


def is_image_url(url: str) -> bool:
    """Return `True` if `url` is the URL to an image."""
    return (
        url.endswith(".ico") or url.endswith(".png") or url.endswith(".jpg") or
        url.endswith(".gif")
    )


def get_domain_urls(urls: List[str], domain_url: str) -> List[str]:
    """
    Get the subset of URLs from `urls` that begin with `domain_url` and are not
    images.
    """
    return [
        url for url in urls
        if url.startswith(domain_url) and not is_image_url(url)
    ]


def get_image_urls(urls: List[str]) -> List[str]:
    """Get the subset of URLs from `urls` that are links to images."""
    return [url for url in urls if is_image_url(url)]


async def build_site_map(starting_url: str, max_depth: int = 10):
    json_site_map = {}
    async with ClientSession() as session:
        html = await fetch_html(session, starting_url)
    urls = get_urls_from_html(html)
    domain_urls = get_domain_urls(urls, starting_url)
    image_urls = get_image_urls(urls)
    return json_site_map


loop = asyncio.get_event_loop()
domain = "https://www.mozilla.org"
loop.run_until_complete(build_site_map(domain))
