---
title: Contributing
subtitle: A GIS letter to the posterity
authors:
    - geotribu
categories:
    - contribution
comments: true
date: 2024-11-18
description: How to publish a blog post on Geotribu.
tags:
    - about
    - contribution
    - guide
    - Geotribu
hide:
    - tags
---

# Want to publish on Geotribu?

## How to write

- it's just Markdown
- well, let's be more specific: it's [Markdown according to Material for Mkdocs](https://squidfunk.github.io/mkdocs-material/reference/).
- you can have a look to our [contribution guide](https://contribuer.geotribu.fr/). Yes it's in French. For now... or maybe forever, who knows? In the meanwhile, see that like a great opportunity to try [Firefox Translation](https://support.mozilla.org/en-US/kb/website-translation) :grin:.
- the repository comes with a Visual Studio Code configuration (recommended extensions and settings). It might help you if you use this editor.

## Process

1. Get your own working copy. 2 cases:
    1. If you've never did it before, [fork this project on GitHub](https://github.com/geotribu/english-blog/fork)
    1. If you've already forked before, just sync it:

    ![GitHub - Sync a fork](https://cdn.geotribu.fr/img/internal/contribution/github_geotribu_english_fork_sync.webp)

1. Create a branch for your article. Something like: `article/title-slugged`
1. Make sure to add/update your authoring information in the [`.authors.yml` file](https://github.com/geotribu/english-blog/blob/main/content/.authors.yml).
1. Add a new file under [the `posts` folder](https://github.com/geotribu/english-blog/tree/main/content/posts) following the name structure (feel inspired by the files already present)
1. Create a [Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) with a title and description
1. Get ready for proofreading

### Images

- do not push images to the Git project
- ask the team for credentials to upload your images to our pseudo-cdn: <https://cdn.geotribu.fr/>.
