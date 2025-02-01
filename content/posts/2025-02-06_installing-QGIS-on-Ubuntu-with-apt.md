---
title: Installing QGIS on Ubuntu with apt
subtitle: apt install qgis-zen-mode
authors:
    - jmoura
categories:
    - Article
comments: true
date: 2023-02-06
description: Installing the most widely used open-source GIS software on the most popular Linux distribution should be straightforward, yet it often raises questions and even problems. This guide walks you through the process so you can refer back to it whenever needed.
icon: fontawesome/brands/ubuntu
image: https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2023/qgis_installation_ubuntu/qgis_ubuntu_linux.png
license: beerware
links:
  - Original version (French): https://geotribu.fr/articles/2023/2023-01-05_installer-qgis-sur-ubuntu/
tags:
    - Linux
    - QGIS
    - Ubuntu
---

# Installing QGIS on Ubuntu: a simple and effective guide

![Ubuntu logo](https://cdn.geotribu.fr/img/logos-icones/logiciels_librairies/ubuntu.svg "Ubuntu logo"){: loading=lazy .img-thumbnail-left }

It may sound surprising, but installing the most widely used open-source GIS software on the most popular Linux distribution is still not as seamless as it should be. Even experienced users sometimes struggle with repository configurations, package dependencies, authentication keys and other system administration intricacies.

![Geographer taming a penguin](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2023/qgis_installation_ubuntu/geographe_contre_linux_dall-e.webp "Geographer taming a penguin - Credits: DALL·E"){: .img-center loading=lazy }

The challenge isn't just technical. QGIS's official installation documentation, while thorough, can be difficult to navigate for those who aren't developers or seasoned Linux users. Plus, regular updates and changes in the software lifecycle can introduce unexpected hurdles for everyday users.

That said, there's no point in complaining, it’s free software and open-source contributors deserve appreciation, not frustration! Since I don't install or reinstall QGIS every day, I've put together this guide as a personal reference and to help others.

<!-- more -->

[Leave a comment :fontawesome-solid-comments:](#__comments "Go to comments"){: .md-button }
{: align=middle }

----

## Prerequisites

- administrator privileges on your system
- an internet connection that allows access to <https://qgis.org/> and can handle a 1.5GB download

----

## Choosing the right version

Before installing, you need to decide: which version of QGIS do you want?

Personally, I prefer installing **QGIS LTR (Long Term Release)** (version 3.34.15 at the time of writing) on **Ubuntu LTS (Long Term Support)** (24.04.1 at the time of writing) using **the official QGIS package repository**.

Yes, I value stability.
Yes, the [`ubuntugis-unstable`](https://wiki.ubuntu.com/UbuntuGIS) repository lives up to its name.  
No, non-LTR versions aren’t stable enough, especially before they reach at least six patch releases.  
<!-- more -->

[Leave a comment :fontawesome-solid-comments:](#__comments "Go to comments"){: .md-button }
{: align=middle }

Sure, I don’t get the latest flashy features making the rounds on GIS news sites. My versions of GDAL and PROJ might be older than my kid, but my setup just works(tm).
And I can focus on my work without worrying about the next update breaking something. :person_in_lotus_position:

![People installing non-LTR QGIS](https://media.giphy.com/media/nneVpy2YnHZNm/giphy.gif "People installing non-LTR QGIS"){: .img-center loading=lazy }

> :person_juggling: Those who install non-LTR QGIS without patch releases :person_juggling:
{: align=middle }

!!! note "Version Availability"
    The version of your Ubuntu distribution matters. Not all QGIS versions are packaged for all Ubuntu versions due to dependency constraints. For example, on Ubuntu 20.04, you won’t find QGIS versions beyond 3.22.

----

## Installing dependencies

First, ensure your system is up to date and install essential packages:

```sh
sudo apt update
sudo apt install ca-certificates gnupg lsb-release software-properties-common
```

----

## Adding the official QGIS repository

The QGIS project maintains an official repository for Debian-based distributions, including Ubuntu. To use it, we need to authenticate and configure it properly.

### Authentication key

We start by downloading the repository's authentication key and storing it in the appropriate system directory:

```sh
sudo mkdir -p /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/qgis-archive-keyring.gpg https://download.qgis.org/downloads/qgis-archive-keyring.gpg
```

### Adding the repository

Now, we add the QGIS repository to our package sources by creating a file in `/etc/apt/sources.list.d/`.

<!-- markdownlint-disable MD046 -->
=== "QGIS LTR"

    ```sh
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/qgis-archive-keyring.gpg] https://qgis.org/ubuntu-ltr \
    $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/qgis.list > /dev/null
    ```

=== "Latest QGIS Release"

    ```sh
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/qgis-archive-keyring.gpg] https://qgis.org/ubuntu \
    $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/qgis.list > /dev/null
    ```
<!-- markdownlint-enable MD046 -->

----

## Installing QGIS

![QGIS logo](https://cdn.geotribu.fr/img/logos-icones/logiciels_librairies/qgis.png "QGIS logo"){: .img-thumbnail-left }

With everything set up, we can now install QGIS.

First, update your package list:

```sh
sudo apt update
```

To see available QGIS-related packages, start typing `sudo apt install qgis` and press ++tab++ for autocomplete suggestions.

```sh
sudo apt install qgis
```

For most users, installing `qgis` is sufficient:

```sh
sudo apt install qgis
```

----

## Cleaning up

If things go wrong—perhaps due to a botched upgrade or conflicting repositories—you may need to clean up your system before retrying.

![Drastic cleanup](https://media.tenor.com/fQmZ_N0b57kAAAAC/kaamelott-leodagan.gif){: .img-center loading=lazy }

Remove QGIS:

```sh
sudo apt --purge remove qgis*
```

If you’ve experimented with `ubuntugis` or other repositories, remove potentially conflicting dependencies:

```sh
sudo apt --purge remove gdal-* proj-*
```

Then, clean up lingering repository references:

```sh
sudo rm /etc/apt/sources.list.d/qgis*
sudo apt autoremove
sudo apt update
```

Now, you're ready to restart the installation process from the beginning.

----

## Credits

- The header image is sourced from [Instrutor GIS](https://www.instrutorgis.com.br/)

<!-- specific abbreviations -->
*[PPA]: PPAs, for Personal Package Archive, are package repositories characteristic of Debian-based distributions and allow you to install software not available in the official repositories of a distribution (Ubuntu in our case).
