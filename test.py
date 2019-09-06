import unittest

from generate_site_map import (
    get_all_links_from_html,
    strip_http_www,
    get_domain_links,
    is_image_link,
    get_image_links,
    get_non_image_links,
)


TEST_HTML = """<meta name="twitter:app:name:iphone" content="Firefox">
    <meta name="twitter:app:id:iphone" content="989804926">
    <meta name="twitter:app:name:ipad" content="Firefox">
    <meta name="twitter:app:id:ipad" content="989804926">
    <link rel="apple-touch-icon" type="image/png" sizes="180x180" href="https://www.mozilla.org/media/img/favicon/apple-touch-icon-180x180.8772ec154918.png">
    <link rel="icon" type="image/png" sizes="196x196" href="https://www.mozilla.org/media/img/favicon/favicon-196x196.c80e6abe0767.png">
    <link rel="shortcut icon" href="https://www.mozilla.org/media/img/favicon.d4f1f46b91f4.ico">
    <link rel="apple-touch-icon" type="image/png" sizes="180x180" href="https://www.mozilla.org/media/img/favicon/apple-touch-icon-180x180.8772ec154918.png">
        <link rel="canonical" href="https://www.mozilla.org/en-US/">
    <link rel="alternate" hreflang="x-default" href="https://www.mozilla.org/en-US/">
    <link rel="alternate" hreflang="an" href="https://www.mozilla.org/an/" title="aragonés">
        <link rel="alternate" hreflang="ar" href="https://www.mozilla.org/ar/" title="عربي">
        <link rel="alternate" hreflang="az" href="https://www.mozilla.org/az/" title="Azərbaycanca">
    <link rel="alternate" hreflang="an" href="https://www.mozilla.org/an/" title="aragonés">
        <link rel="alternate" hreflang="be" href="https://www.mozilla.org/be/" title="Беларуская">
        <link rel="alternate" hreflang="bg" href="https://www.mozilla.org/bg/" title="Български">
        <link rel="alternate" hreflang="bs" href="https://www.mozilla.org/bs/" title="Bosanski">
        <link rel="alternate" hreflang="ca" href="https://www.mozilla.org/ca/" title="Català">"""  # noqa
TEST_LINKS = [
    "https://example.com/",
    "http://example2.com",
    "https://example2.com//",
    "http://example.com",
    "http://example.com/img1.png",
    "http://example2.com/img2.ico",
]


class TestGenerateSiteMap(unittest.TestCase):
    def test_get_all_links_from_html(self):
        """
        Verify `get_all_links_from_html()` returns unique links from an HTML
        string.
        """
        self.assertEqual(
            set(get_all_links_from_html(TEST_HTML)),
            {"https://www.mozilla.org/media/img/favicon/apple-touch-icon-180x180.8772ec154918.png", "https://www.mozilla.org/media/img/favicon/favicon-196x196.c80e6abe0767.png", "https://www.mozilla.org/media/img/favicon.d4f1f46b91f4.ico", "https://www.mozilla.org/en-US/", "https://www.mozilla.org/an/", "https://www.mozilla.org/ar/", "https://www.mozilla.org/az/", "https://www.mozilla.org/be/", "https://www.mozilla.org/bg/", "https://www.mozilla.org/bs/", "https://www.mozilla.org/ca/"}  # noqa
        )

    def test_strip_http_www(self):
        """
        Verify `test_strip_http_www()` removes trailing "/"s and leading
        "https://", "http://", and "www.".
        """
        # verify with leading "https://"
        self.assertEqual(strip_http_www("https://example.com"), "example.com")

        # verify with leading "http://"
        self.assertEqual(strip_http_www("http://example.com"), "example.com")

        # verify with leading "https://www."
        self.assertEqual(
            strip_http_www("https://www.example.com"),
            "example.com",
        )

        # verify with leading "http://www."
        self.assertEqual(
            strip_http_www("http://www.example.com"),
            "example.com",
        )

    def test_get_domain_links(self):
        """Verify `get_domain_links()` correctly outputs only domain links."""
        # verify domain link with leading "https:"
        self.assertEqual(
            set(get_domain_links(TEST_LINKS, "https://example.com")),
            {"https://example.com/", "http://example.com"},
        )

        # verify domain link with leading "https://www."
        self.assertEqual(
            set(get_domain_links(TEST_LINKS, "https://www.example.com//")),
            {"https://example.com/", "http://example.com"},
        )

        # verify domain link with leading "http:"
        self.assertEqual(
            set(get_domain_links(TEST_LINKS, "http://example.com")),
            {"https://example.com/", "http://example.com"},
        )

        # verify domain link with leading "http://www."
        self.assertEqual(
            set(get_domain_links(TEST_LINKS, "http://www.example.com")),
            {"https://example.com/", "http://example.com"},
        )

        # verify correct selection of "example2.com" domain
        self.assertEqual(
            set(get_domain_links(TEST_LINKS, "http://www.example2.com///")),
            {"https://example2.com//", "http://example2.com"},
        )

    def test_is_image_link(self):
        """Verify `is_image_link()` correctly identifies an image link."""
        # test non-image link
        self.assertFalse(is_image_link("https://example.com"))

        # test invalid ".ico" link
        self.assertFalse(is_image_link("https://example.com/img1.ico/"))

        # test invalid ".png" link
        self.assertFalse(is_image_link("https://example.com/img1.PNG/"))

        # test ".jpg" link
        self.assertTrue(is_image_link("https://example.com/img1.jpg"))

        # test ".gif" link
        self.assertTrue(is_image_link("https://example.com/img1.GIF"))

    def test_get_image_links(self):
        """Verify `get_image_links()` correctly returns image links."""
        self.assertEqual(
            set(get_image_links(TEST_LINKS)),
            {"http://example.com/img1.png", "http://example2.com/img2.ico"},
        )

    def test_get_non_image_links(self):
        """Verify `get_non_image_links()` correctly returns non-image links."""
        self.assertEqual(
            set(get_non_image_links(TEST_LINKS)),
            {
                "https://example.com/",
                "http://example2.com",
                "https://example2.com//",
                "http://example.com",
            },
        )


if __name__ == "__main__":
    unittest.main()
