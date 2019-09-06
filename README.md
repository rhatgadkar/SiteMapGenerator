About this program
------------------
This program builds a site map of a given domain URL at a certain max depth.
When going deeper into the site, only domain URL site maps are generated.
The result is outputted into a `site_map.json` file.

Each site map contains information about the page's URL, the non-image links of
the page, and the image links of the page.
Here is an example site map for a non-existing "example.org" domain:
```
    [
        {
            "page_url": "https://www.example.org/en-US/",
            "links": [
                "https://www.example.org/en-US/about/",
                "https://play.example.com/store/",
            ]
            "images": ["https://www.example.org/media/contentcards.png"]
        },
        {
            "page_url": "https://www.example.org/en-US/developer/",
            "links": [
                "https://www.example.org/en-US/about/",
                "https://play.example.com/store/",
            ]
            "images": ["https://www.example.org/media/contentcards.png"]
        },
        ...
    ]
```

How to run this program
-----------------------
1. This program can only be run using Python 3.
2. Install the dependencies of this program from the `requirements.txt` file
   using this command: `pip3 install -r requirements.txt`.
   (May require superuser privileges to install.)
3. Unit tests can be run using this command: `python3 test.py`.
4. Run the program using this command: `python3 generate_site_map.py`.
5. A `site_map.json` file will be generated as the output.
