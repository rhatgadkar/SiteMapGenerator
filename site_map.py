from aiohttp import ClientSession
import asyncio
import json
import re
from typing import Dict, List, Set, Union


HREF_RE = (
    r"href=\""
    r"(?P<url>https?\:\/\/(www\.)?(\S+\.)+[a-z]{2,}(\/[^\s\'\"]+)*\/?)\""
)
HREF_PROG = re.compile(HREF_RE)
IMAGE_EXTS = [".ico", ".png", "jpg", ".gif"]


async def fetch_html(session: ClientSession, url: str) -> str:
    """Get the HTML string of `url`."""
    async with session.get(url) as response:
        return await response.text()


def get_all_links_from_html(html: str) -> List[str]:
    """Get a list of all unique links in `html`."""
    href_matches = HREF_PROG.findall(html)
    links = set([href_match[0] for href_match in href_matches])
    return list(links)


def strip_http_www(link: str) -> str:
    """Strip leading 'http' and 'www' from `link`.  Also strip trailing '/'."""
    link = link.strip("/")
    if link.startswith("https://"):
        link = link.lstrip("https://")
    elif link.startswith("http://"):
        link = link.lstrip("http://")
    if link.startswith("www."):
        link = link.lstrip("www.")
    return link


def get_domain_links(links: List[str], domain_url: str) -> List[str]:
    """
    Get the subset of links from `links` that begin with `domain_url` and are
    not images.
    """
    return [
        link for link in links
        if strip_http_www(link).startswith(strip_http_www(domain_url)) and
        not is_image_link(link)
    ]


def is_image_link(link: str) -> bool:
    """Return `True` if `link` is a link to an image."""
    return link[-4:].lower() in IMAGE_EXTS


def get_image_links(links: List[str]) -> List[str]:
    """Get the subset of links from `links` that are links to images."""
    return [link for link in links if is_image_link(link)]


def get_non_image_links(links: List[str]) -> List[str]:
    """Get the subset of links from `links` that are not links to images."""
    return [link for link in links if not is_image_link(link)]


async def build_site_map(
    starting_url: str,
    max_depth: int = 10,
    processed_sites: Set[str] = set(),
) -> List[Dict[str, Union[str, List[str]]]]:
    """
    Build a list of site maps beginning from `starting_url` and ending at a
    depth specified by `max_depth`.  Only domain URL site maps are generated.
    Site maps contain information about the page's URL, the page's links, and
    the page's images.

    Here is an example site map:
    [
        {
            "page_url": " https://www.mozilla.org/en-US/ ",
            "links": [
                "https://www.mozilla.org/en-US/about/",
                "https://play.google.com/store/",
            ]
            "images": ["https://www.mozilla.org/media/contentcards.png"]
        },
        {
            "page_url": " https://www.mozilla.org/en-US/developer/ ",
            "links": [
                "https://www.mozilla.org/en-US/about/",
                "https://play.google.com/store/",
            ]
            "images": ["https://www.mozilla.org/media/contentcards.png"]
        },
        ...
    ]

    Arguments:
    starting_url:
        The current domain URL to build the site map from.
    max_depth:
        The deepest depth of the site map.
    processed_sites:
        URLs whose site maps have already been generated.  Storing these sites
        helps to ensure that duplicate site maps do not get generated.

    Return:
        A list of all domain URL site maps.
    """
    if not max_depth:
        return []
    if not starting_url:
        raise Exception("`starting_url` was not specified.")
    async with ClientSession() as session:
        html = await fetch_html(session, starting_url)
    links = get_all_links_from_html(html)
    domain_links = get_domain_links(links, starting_url)
    image_links = get_image_links(links)
    non_image_links = get_non_image_links(links)
    site_map = [{
        "page_url": starting_url,
        "links": non_image_links,
        "images": image_links
    }]
    processed_sites.add(starting_url)
    if not domain_links:
        return site_map
    domain_link_coros = [
        build_site_map(domain_link, max_depth - 1, processed_sites)
        for domain_link in domain_links
        if domain_link not in processed_sites
    ]
    for out in await asyncio.gather(*domain_link_coros):
        if out:
            site_map.extend(out)
    return site_map


async def main(domain: str, max_depth: int) -> None:
    site_map = await build_site_map(domain, max_depth)
    with open("data.json", "w") as f:
        json.dump(site_map, f, indent=4)


if __name__ == "__main__":
    domain = ""
    while not domain:
        domain = input("Enter domain URL: ")
        if (
            not domain.startswith("http://") and
            not domain.startswith("https://")
        ):
            print("Domain URL must begin with either 'http://' or 'https://'.")
            domain = ""
    max_depth = -1
    while max_depth < 0:
        try:
            max_depth = int(input("Enter max depth: "))
            if max_depth < 0:
                raise ValueError
        except ValueError:
            print("Max depth must be a non-negative integer.")
            max_depth = -1
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(domain, max_depth))
