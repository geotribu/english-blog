# Geotribu: English blogs

[![🚀 Deployment](https://github.com/geotribu/english-blog/actions/workflows/deploy.yml/badge.svg)](https://github.com/geotribu/english-blog/actions/workflows/deploy.yml) [![🎳 Markdown Linter](https://github.com/geotribu/english-blog/actions/workflows/pr_linter_markdown.yml/badge.svg)](https://github.com/geotribu/english-blog/actions/workflows/pr_linter_markdown.yml) [![🧹 PR Cleaner](https://github.com/geotribu/english-blog/actions/workflows/pr_cleaner_post_merge.yml/badge.svg)](https://github.com/geotribu/english-blog/actions/workflows/pr_cleaner_post_merge.yml) [![👀 PR Preview](https://github.com/geotribu/english-blog/actions/workflows/pr_preview_netlify.yml/badge.svg)](https://github.com/geotribu/english-blog/actions/workflows/pr_preview_netlify.yml)

[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

Geotribu in English, translated or original blog posts around GIS and geo\*.

## How to run site locally

**Remark:** *This is a minimal version of the procedure to run the website locally. For a detailed explanation, have a look at :*

- *[Install and configure a local version of the Geotribu website](https://contribuer.geotribu.fr/edit/local_edition_setup/)*
- *[Generate the Geotribu website using Properdocs](https://contribuer.geotribu.fr/internal/generer_les_sites_web_geotribu/)*

### Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install the dependencies

```bash
pip install -r requirements.txt
```

### Serve the site locally

```bash
properdocs serve -f properdocs.yml
```

Once this command is executed, the site will be accessible at <http://localhost:8000>. To stop the server: `ctl + c`
