# Geotribu: English blogs

[![🚀 Deployment](https://github.com/geotribu/english-blog/actions/workflows/deploy.yml/badge.svg)](https://github.com/geotribu/english-blog/actions/workflows/deploy.yml) [![🎳 Markdown Linter](https://github.com/geotribu/english-blog/actions/workflows/pr_linter_markdown.yml/badge.svg)](https://github.com/geotribu/english-blog/actions/workflows/pr_linter_markdown.yml) [![🧹 PR Cleaner](https://github.com/geotribu/english-blog/actions/workflows/pr_cleaner_post_merge.yml/badge.svg)](https://github.com/geotribu/english-blog/actions/workflows/pr_cleaner_post_merge.yml) [![👀 PR Preview](https://github.com/geotribu/english-blog/actions/workflows/pr_preview_netlify.yml/badge.svg)](https://github.com/geotribu/english-blog/actions/workflows/pr_preview_netlify.yml)

[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

Geotribu in English, translated or original blog posts around GIS and geo\*.

## Tester le site en local

Si vous voulez vérifier que votre contribution est valide,
voici comment tester le site en local.

### Créer un environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

### Servir le site en local

```bash
properdocs serve -f properdocs.yml
```

Une fois cette commande lancée, le site sera accessible
à <http://localhost:8000>. Pour arrêter le server : `ctl + c`
