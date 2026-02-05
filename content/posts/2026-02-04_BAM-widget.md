---
title: BAM (Biodiversity Around Me)
subtitle: Open biodiversity data easily accessible to everyone, everywhere!
authors:
  - camillemonchicourt
categories:
  - Article
comments: true
date: 2026-02-04
description: A new biodiversity widget to display species observed around a location.
icon: material/bee-flower
license: default
links:
  - Original version (French): https://geotribu.fr/articles/2025/2025-12-11_BAM-widget/
pin: false
tags:
    - biodiversity
    - open source
    - widget
---

# BAM (Biodiversity Around Me): Open biodiversity data easily accessible to everyone, everywhere!

![BAM widget logo](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2025/bam_widget/BAM-logo.webp){: .img-thumbnail-left }

A new, open-source biodiversity widget developed by French National Parks and recognized internationally.
It allows to display species observed around any given location.

<!-- more -->

At [Écrins national park](https://www.ecrins-parcnational.fr/) and [Cévennes national park](https://cevennes-parcnational.fr),
we love open-source geomatics, :elephant: databases, and open data!
Over the last 10 years, we have notably developed two open-source information systems:

- [Geotrek](https://geotrek.fr) for managing and promoting trails.
- [GeoNature](https://geonature.fr) for collecting, managing, and disseminating biodiversity data.

These two tools are now used by more than 250 organizations in France.
Several community members wanted to connect GeoNature and Geotrek by showcasing species observed along a hike.

Rather than developing a component or module specific to our own tools, we looked for a more global and generic solution. Together with Amandine Sahl from Cévennes National Park, we envisioned an approach that could adapt to different contexts and various data sources.

In recent years, open biodiversity data has grown exponentially thanks to international participatory programs ([iNaturalist](https://www.inaturalist.org/), [Pl@ntNet](https://plantnet.org/), [eBird](https://ebird.org/)...), professional and amateur naturalists, and national platforms like the [INPN](https://inpn.mnhn.fr/). However, these data are not always easily accessible to the general public.

Our goal was to enable anyone to integrate, in just a few clicks, a list of species observed around a lodge, a trail, an event, or even a school into their website.

This led to the creation of [BAM – Biodiversity Around Me](https://si.ecrins-parcnational.com/blog/2025-08-BAM-widget-en.html). Development began during a workshop in late 2024 with several French national parks, coordinated by Amandine Sahl (Cévennes National Park) and Jacques Fize (Écrins National Park).

![Preview of BAM in gallery mode, around Saint-Léger-les-Mélèzes (in Hautes-Alpes)](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2025/bam_widget/BAM_liste-galerie_exemple_Saint-Leger-Les-Melezes.webp){: .img-center loading=lazy }

## How does BAM work?

BAM is a ready-to-use widget that can be embedded into any webpage or application.

Simply provide a location or a search area, and the widget displays:

- The names of the species observed.
- The date of the most recent observation.
- A photo.
- Sometimes even an audio recording.

All this information comes directly from major global open databases such as [GBIF](https://www.gbif.org/) or [Wikidata](https://www.wikidata.org/).
It can also pull from local sources like [GeoNature](https://geonature.fr/) via a system of connectors that can be expanded to include new data sources.

![BAM data architecture](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2025/bam_widget/BAM_architecture_data.webp){: .img-center loading=lazy }

The tool requires no installation, no server, and no database.
It fetches up-to-date observations by querying API services.
It works worldwide and is multilingual (French :flag_fr:, English :flag_gb:, Spanish :flag_es:, Italian :flag_it:, German :flag_de:, and even Czech :flag_cz: thanks to a [recent contribution by Jiří Podhorecký](https://github.com/PnX-SI/BAM-widget/pull/83)).

Here is an example of the BAM widget integration, showing species observed within a 200m radius of the forestry school in Banco National Park, Abidjan:

<iframe
        title="BAM - Banco naational park"
        width="100%" height="640" allow="geolocation"
        src="https://pnx-si.github.io/BAM-widget/#/?widgetType=mapList&nbTaxonPerLine=4&primaryColor=009485&switchModeAvailable=true&showFilters=true&lang=en&buffer=200&x=-4.05224&y=5.38471"></iframe>

```html title="Widget source Code to integrate for this example"
<iframe
   title="BAM - Banco national park"
   width="100%" height="640" allow="geolocation"
   src="https://pnx-si.github.io/BAM-widget/#/?widgetType=mapList&nbTaxonPerLine=4&primaryColor=009485&switchModeAvailable=true&showFilters=true&lang=en&buffer=200&x=-4.05224&y=5.38471">
</iframe>
```

:gear: A [widget configurator](https://pnx-si.github.io/BAM-widget/#/config) is available to make setup and integration easy. Define the location, display mode, and options (map + list or list only, gallery or detailed view, results per row, filters, search zone, data source, colors...) and BAM! Just copy and paste the few lines of the iframe code into your site.

From nature parks and trails to schools, mountain huts, climbing sites, events, or accommodations, we hope to see the BAM widget integrated into a wide range of websites, sparking curiosity and nature awareness among new audiences.

Cévennes National Park has already integrated it into the trail webpages of its [Geotrek-rando portal](https://destination.cevennes-parcnational.fr/trek/37990-Arboretum-de-l-Hort-de-Dieu), and various use cases are available on the [project's GitHub](https://github.com/PnX-SI/BAM-widget/tree/main/docs/examples).

:mag: BAM can also be used as a standalone biodiversity data explorer. It is mobile-friendly and can be installed as a [PWA](https://fr.wikipedia.org/wiki/Progressive_web_app) by visiting [https://pnx-si.github.io/BAM-widget/](https://pnx-si.github.io/BAM-widget/).

## International Recognition

On October 24, 2025, in Bogotá, Colombia, BAM received an award at the [Ebbe Nielsen Challenge](https://www.gbif.org/news/2LugQxJfG2kCzjiJocXzVZ/winners-from-norway-and-australia-share-first-place-in-the-2025-ebbe-nielsen-challenge), organized by [GBIF](https://www.gbif.org/). This annual competition rewards the best applications using open biodiversity data.

![The National Parks team behind the BAM widget](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2025/bam_widget/BAM_equipe_parcs-nationaux.webp){: .img-center loading=lazy }

This is a nice recognition for our teams at the Cévennes and Écrins National Parks, who were previously winners of this challenge in 2019 for the GeoNature-atlas project.

With this new project, our two national parks continue their shared commitment to developing open-source tools that meet local needs through generic, global solutions. A journey that began over 10 years ago with the Geotrek and GeoNature collaborative projects.

## Learn more

- [Try the BAM tool](https://pnx-si.github.io/BAM-widget/)
- [Access the BAM widget configurator](https://pnx-si.github.io/BAM-widget/#/config)
- [Full BAM documentation](https://pnx-si.github.io/BAM-widget/docs/#/)
- [General presentation of BAM](https://si.ecrins-parcnational.com/blog/2025-08-BAM-widget-en.html)
- [BAM source code](https://github.com/PnX-SI/BAM-widget)
- [2025 Ebbe Nielsen Challenge Results](https://www.gbif.org/news/2LugQxJfG2kCzjiJocXzVZ/winners-from-norway-and-australia-share-first-place-in-the-2025-ebbe-nielsen-challenge)
