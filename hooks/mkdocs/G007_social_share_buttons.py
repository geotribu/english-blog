#! python3

"""Extend the share links natively provided by MaterialX's blog plugin.

The blog plugin renders the links declared in its `share_links` setting in each
post's sidebar, but only replaces `{post_url}` and `{post_title}` in them. This
hook runs after the plugin and adds, for each link:

- more placeholders: `{post_description}`, `{post_authors}`,
  `{post_categories}`, `{post_tags}` (as hashtags) and `{site_name}`;
- user-defined variables: shared ones in `extra.share_links_vars`, overridable
  per link with a `vars` mapping;
- a `text` field: a plain-text message where placeholders and variables are
  replaced, then URL-encoded as a whole and injected in `link` as `{text}`.

Every value injected in `link` is URL-encoded, so the configuration is written
in plain text. Missing metadata becomes an empty string.

Related resources:

- https://jaywhj.github.io/mkdocs-materialx/plugins/blog/#config.share_links
- https://docs.bsky.app/docs/advanced-guides/intent-links
"""

# ############################################################################
# ########## Libraries #############
# ##################################

# standard library
import logging
import re
from urllib.parse import quote

# 3rd party
import properdocs.plugins
from material.plugins.blog.plugin import BlogPlugin
from material.plugins.blog.structure import Post
from properdocs.config.defaults import MkDocsConfig

# ###########################################################################
# ########## Global ################
# ##################################

logger = logging.getLogger("mkdocs")

# placeholder left in a link after substitution, most likely a typo
regex_leftover_placeholder = re.compile(r"\{[a-z_]+\}")

# ###########################################################################
# ########## Functions #############
# ##################################


def _find_blog_plugin(config: MkDocsConfig) -> BlogPlugin | None:
    """Return the first blog plugin instance declared in the configuration."""
    for plugin in config.plugins.values():
        if isinstance(plugin, BlogPlugin):
            return plugin
    return None


def _post_values(post: Post, config: MkDocsConfig) -> dict[str, str]:
    """Build the raw (not encoded) placeholder values of a post."""
    return {
        "post_url": post.canonical_url or post.url or "",
        "post_title": post.title or "",
        "post_description": (post.meta.get("description") or "").strip(),
        "post_authors": ", ".join(author.name for author in post.authors),
        "post_categories": ", ".join(category.title for category in post.categories),
        "post_tags": " ".join(
            f"#{tag.replace(' ', '')}" for tag in post.meta.get("tags") or []
        ),
        "site_name": config.site_name or "",
    }


def _substitute(template: str, values: dict[str, str], encode: bool) -> str:
    """Replace `{name}` placeholders in template, URL-encoding values if asked."""
    for name, value in values.items():
        template = template.replace(
            f"{{{name}}}", quote(value, safe="") if encode else value
        )
    return template


@properdocs.plugins.event_priority(-100)
def on_page_context(context: dict, page, config: MkDocsConfig, **kwargs) -> dict:
    """Complete share links resolved by the blog plugin for the current post."""
    share_links = context.get("share_links")
    if not share_links or not isinstance(page, Post):
        return context

    blog = _find_blog_plugin(config)
    if blog is None:
        return context

    # the plugin builds share_links in the same order as its configuration
    declared = list(blog.config.share_links.values())
    if len(declared) != len(share_links):
        logger.warning(
            f"[G007] Share links of {page.file.src_uri} don't match the "
            "configuration, skipping."
        )
        return context

    post_values = _post_values(page, config)
    shared_vars = config.extra.get("share_links_vars") or {}

    for resolved, settings in zip(share_links, declared):
        values = {
            **{k: str(v) for k, v in shared_vars.items()},
            **{k: str(v) for k, v in (settings.get("vars") or {}).items()},
            **post_values,
        }
        if text := settings.get("text"):
            values["text"] = _substitute(text, values, encode=False).strip()

        url = _substitute(resolved["url"], values, encode=True)
        if leftover := regex_leftover_placeholder.findall(url):
            logger.warning(
                f"[G007] Unknown placeholder(s) {', '.join(set(leftover))} in "
                f"share link '{resolved['name']}'."
            )
        resolved["url"] = url

    return context
