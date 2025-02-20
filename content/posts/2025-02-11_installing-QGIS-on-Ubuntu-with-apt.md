---
title: Installing QGIS on Ubuntu with apt
subtitle: apt install qgis-zen-mode
authors:
    - jmoura
categories:
    - Tutorial
comments: true
date: 2025-02-11
description: Installing the most widely used open-source GIS software on the most popular Linux distribution should be straightforward, yet it often raises questions and even problems. This guide walks you through the process so you can refer back to it whenever needed.
icon: fontawesome/brands/ubuntu
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

![Geographer taming a penguin](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2023/qgis_installation_ubuntu/geographe_contre_linux_dall-e.webp "Geographer taming a penguin - Credits: DALL·E 1"){: .img-center loading=lazy }

The challenge isn't just technical. [QGIS's official installation documentation](https://qgis.org/resources/installation-guide/#debian--ubuntu), while thorough, can be difficult to navigate for those who aren't developers or seasoned Linux users. Plus, regular updates and changes in the software lifecycle can introduce unexpected hurdles for everyday users.

That said, there's no point in complaining, it’s free software and open-source contributors deserve appreciation, not frustration! And I speak from experience. :wink:

<!-- more -->

Since I don't install or reinstall QGIS every day, I've put together this guide as a personal reference and to help others. Given that this is a constantly evolving topic, I’ll try to keep this guide updated from time to time. However, feel free to [report issues](https://github.com/geotribu/english-blog/issues) or [suggest improvements](https://contribuer.geotribu.fr/edit/fix_content_from_website/).

[Leave a comment :fontawesome-solid-comments:](#__comments "Go to comments"){: .md-button }
{: align=middle }

----

## Prerequisites

- administrator privileges on your system
- an internet connection that allows access to <https://qgis.org/> and can handle a 1.5GB download without choking

----

## Choosing the right version

Before installing, you need to decide: which version of QGIS do you want?

Personally, I prefer opting for **QGIS LTR (Long Term Release)** (version 3.34.15 at the time of writing) on **Ubuntu LTS (Long Term Support)** (24.04.1 at the time of writing) using **the official QGIS package repository**.

Yes, I value stability.
Yes, the [`ubuntugis-unstable`](https://wiki.ubuntu.com/UbuntuGIS) repository lives up to its name.  
No, non-LTR versions aren’t stable enough, especially before they reach at least six bugfix releases (the last digit in the version number).

Sure, I don’t get the latest buzzworthy features making the rounds on GIS news sites (like Geotribu). My versions of GDAL and PROJ might be older than my kids… but my setup works™. :sunglasses:  
And I can focus on my work without worrying about the next update breaking something. :person_in_lotus_position:

![People installing non-LTR QGIS](https://media.giphy.com/media/nneVpy2YnHZNm/giphy.gif){: .img-center loading=lazy }

> :person_juggling: Those who install non-LTR QGIS without patch releases :person_juggling:
{: align=middle }

!!! note "Versions availability"
    The version of your Ubuntu distribution matters. Not all QGIS versions are packaged for all Ubuntu versions due to dependency constraints. For example, on [Ubuntu 20.04](https://ubuntu.qgis.org/ubuntu-ltr/dists/focal/main/binary-amd64/Packages), you won’t find QGIS versions beyond 3.22.

----

## Installing dependencies

First, ensure your system is up to date. Here, we're assuming you’re starting from a fresh system. If your machine is cluttered with old setups, consider [cleaning it up](#cleanup) before proceeding.

```sh title="Update your package lists and install the required tools"
sudo apt update
sudo apt install ca-certificates gnupg lsb-release software-properties-common
```

----

## Adding the official QGIS repository (PPA)

The QGIS project maintains an official packages repository (PPA) for Debian-based distributions, including Ubuntu. To use it, we need to authenticate and configure it properly.

### Authenticating the repository

To install anything from this repository, you need to be able to authenticate it to the system.

We start by downloading the PPA's authentication key and storing it in the appropriate system directory:

```sh title="Download and store the QGIS PPA authentication key"
sudo mkdir -p /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/qgis-archive-keyring.gpg https://download.qgis.org/downloads/qgis-archive-keyring.gpg
```

### Adding the repository to our list of packages sources

Now, we add the QGIS repository to our package sources by creating a dedicated file in `/etc/apt/sources.list.d/`:

<!-- markdownlint-disable MD046 -->
=== ":person_in_lotus_position: QGIS LTR"

    ```sh
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/qgis-archive-keyring.gpg] https://qgis.org/ubuntu-ltr \
    $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/qgis.list > /dev/null
    ```

    Then, verify that the file was successfully written:

    ```sh
    less -F /etc/apt/sources.list.d/qgis.list
    ```

    Result on Ubuntu 24.04 should be:

    ```debsources title="/etc/apt/sources.list.d/qgis.list"
    deb [arch=amd64 signed-by=/etc/apt/keyrings/qgis-archive-keyring.gpg] https://qgis.org/ubuntu-ltr noble main
    ```

=== ":person_juggling: QGIS latest release"

    ```sh
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/qgis-archive-keyring.gpg] https://qgis.org/ubuntu \
    $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/qgis.list > /dev/null
    ```

    Then, verify that the file was successfully written:

    ```sh
    less -F /etc/apt/sources.list.d/qgis.list
    ```

    Result on Ubuntu 24.04 should be:

    ```debsources title="/etc/apt/sources.list.d/qgis.list"
    deb [arch=amd64 signed-by=/etc/apt/keyrings/qgis-archive-keyring.gpg] https://qgis.org/ubuntu noble main
    ```

<!-- markdownlint-enable MD046 -->

#### Alternatively: the `qgis.sources` file

There is another way of referencing the repository in the list of sources: [the DEB822 format](https://repolib.readthedocs.io/en/latest/deb822-format.html), which aims to solve issues related to the historical one-liner. Well, don't mind, the information stored is the same, but not structured in the same way. Let's say it's the new way to format packages source files.

In this case, the repository is referenced in a `/etc/apt/sources.list.d/qgis.sources` file:

<!-- markdownlint-disable MD046 -->
=== ":person_in_lotus_position: QGIS LTR"

    ```sh
    echo \
    "Types: deb deb-src
    URIs: https://qgis.org/ubuntu-ltr
    Suites: $(lsb_release -cs)
    Architectures: amd64
    Components: main
    Signed-By: /etc/apt/keyrings/qgis-archive-keyring.gpg" | sudo tee /etc/apt/sources.list.d/qgis.sources > /dev/null
    ```

    Then, verify that the file was successfully written:

    ```sh
    less -F /etc/apt/sources.list.d/qgis.sources
    ```

    Result on Ubuntu 24.04 should be:

    ```yaml title="/etc/apt/sources.list.d/qgis.sources"
    Types: deb deb-src
    URIs: https://qgis.org/ubuntu-ltr
    Suites: noble
    Architectures: amd64
    Components: main
    Signed-By: /etc/apt/keyrings/qgis-archive-keyring.gpg
    ```

=== ":person_juggling: QGIS latest release"

    ```sh
    echo \
    "Types: deb deb-src
    URIs: https://qgis.org/ubuntu
    Suites: $(lsb_release -cs)
    Architectures: amd64
    Components: main
    Signed-By: /etc/apt/keyrings/qgis-archive-keyring.gpg" | sudo tee /etc/apt/sources.list.d/qgis.sources > /dev/null
    ```

    Then, verify that the file was successfully written:

    ```sh
    less -F /etc/apt/sources.list.d/qgis.sources
    ```

    Result on Ubuntu 24.04 should be:

    ```yaml title="/etc/apt/sources.list.d/qgis.sources"
    Types: deb deb-src
    URIs: https://qgis.org/ubuntu
    Suites: noble
    Architectures: amd64
    Components: main
    Signed-By: /etc/apt/keyrings/qgis-archive-keyring.gpg
    ```
<!-- markdownlint-enable MD046 -->

----

## Installing QGIS

![QGIS logo](https://cdn.geotribu.fr/img/logos-icones/logiciels_librairies/qgis.png "QGIS logo"){: .img-thumbnail-left }

With everything set up, we can now install QGIS!  
First, update your package list:

```sh
sudo apt update
```

To see available QGIS-related packages, start typing `sudo apt install qgis` and press ++tab++ for autocomplete suggestions.

```sh title="List QGIS related packages eligible to installation"
$ sudo apt install qgis
qgis                      qgis-plugin-grass-common  qgis-server-common        qgis-server-wms
qgis3-survex-import       qgis-provider-grass       qgis-server-dummy         qgis-server-wmts
qgis-api-doc              qgis-providers            qgis-server-landingpage   qgis-sip
qgis-common               qgis-providers-common     qgis-server-wcs  
qgis-dbg                  qgis-server               qgis-server-wfs  
qgis-plugin-grass         qgis-server-bin           qgis-server-wfs3
```

![Available packages starting par 'qgis'](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2023/qgis_installation_ubuntu/ubuntu_apt_install_qgis_autocompletion.webp){: .img-center loading=lazy }

Unless you have special needs, it's always best to install only the minimum required. In my case, that's `qgis`... and that's more than enough, as it's already collecting a whole bunch of packages:

```sh
sudo apt install qgis
```

![Downloaded and installed dependencies for a classic QGIS installation on Ubuntu](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2023/qgis_installation_ubuntu/ubuntu_apt_install_qgis_dependances.webp){: .img-center loading=lazy }

----

## Cleaning up { #cleanup }

If things go wrong, perhaps due to a botched upgrade or conflicting repositories, you may need to clean up your system before retrying.

![Drastic cleanup](https://media.tenor.com/QdYwnFzWm4oAAAAd/flaming-sword-boom.gif){: .img-center loading=lazy }

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

<!-- specific abbreviations -->
*[PPA]: PPAs, for Personal Package Archive, are package repositories characteristic of Debian-based distributions and allow you to install software not available in the official repositories of a distribution (Ubuntu in our case).
