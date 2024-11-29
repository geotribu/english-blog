#! python3  # noqa: E265

"""Insert social share buttons in content.

Related resources:

- https://squidfunk.github.io/mkdocs-material/tutorials/blogs/engage/
- https://stackoverflow.com/questions/10713542/how-to-make-a-custom-linkedin-share-button
- https://stackoverflow.com/questions/24823114/post-to-reddit-via-url
- https://docs.bsky.app/docs/advanced-guides/intent-links
"""

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
import re
import urllib.parse
from textwrap import dedent

# Mkdocs
import mkdocs.plugins
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page

# ###########################################################################
# ########## Global ################
# ##################################


logger = logging.getLogger("mkdocs")

regex_pattern_include = re.compile(r"posts/[1-9].*")

share_url_base_bluesky = "https://bsky.app/intent/compose"
share_url_base_mastodon = "https://mastodonshare.com/share"
share_url_base_linkedin = "https://www.linkedin.com/shareArticle"
share_url_base_reddit = "http://www.reddit.com/submit"

# ###########################################################################
# ########## Functions #############
# ##################################


@mkdocs.plugins.event_priority(-100)
def on_page_markdown(markdown: str, page: Page, config: MkDocsConfig, **kwargs):

    if not regex_pattern_include.match(page.file.src_uri):
        return markdown

    # prepare data
    page_authors = urllib.parse.quote(", ".join([a.get("name") for a in page.authors]))
    page_description = urllib.parse.quote(page.meta.get("description") + "\n")
    page_tags = "%20".join(
        [
            urllib.parse.quote(f"#{tag.replace(' ', '')}")
            for tag in page.meta.get("tags")
        ]
    )

    page_title = urllib.parse.quote(page.title + "\n")
    page_url = config.site_url + page.url

    # urls
    share_url_bluesky = (
        f"{share_url_base_bluesky}?text="
        + f"{page_title}%0A{page_description}%0Aby%20{page_authors}.%20%0A%0A%0A%23GISTribe%0A%0ACheck%20it%20on%20@geotribu.bsky.social%20:%20{page_url}"
    )
    share_url_linkedin = (
        f"{share_url_base_linkedin}?url={page_url}"
        "&mini=true"
        # f"&title={page_title}"
        # f"&summary={page_description}"
        f"&source=Geotribu"
        f"&text=Check%20this%20blog%20post%20{page_title}%20by%20{page_authors}%20"
        "on%20%40Geotribu%0A"
        f"{page_description}%0A%0A%20"
        f"%0A%23GISTribe%20{page_tags}"
    )
    share_url_mastodon = (
        f"{share_url_base_mastodon}?url={page_url}"
        f"&text=Check%20this%20blog%20post%20{page_title}%20by%20{page_authors}%20"
        "on%20%40geotribu%40mapstodon.space%0A"
        f"{page_description}%0A%0A%20"
        # f"%0A%23GISTribe%20{page_tags}"
    )
    share_url_reddit = f"{share_url_base_reddit}?title={page_title}%20by%20{page_authors}&url={page_url}"

    return markdown + dedent(
        f"""\n\nShare it: [:fontawesome-brands-bluesky:]({share_url_bluesky}) [:fontawesome-brands-linkedin:]({share_url_linkedin}) [:fontawesome-brands-mastodon:]({share_url_mastodon}) [:fontawesome-brands-reddit:]({share_url_reddit})
        {{: align=middle .md-source }}
    """
    )
