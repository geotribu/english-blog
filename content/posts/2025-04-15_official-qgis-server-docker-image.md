---
title: "What’s under the hood of the official QGIS Server Docker image?"
subtitle: (boo !)
authors:
    - pblottiere
categories:
    - article
comments: true
date: 2025-04-18
description: "The Mysteries of the Official QGIS Server Docker Image"
icon: material/docker
image:
license: default
links:
  - Original version (French): https://geotribu.fr/articles/2025/2025-04-15_official-qgis-server-docker-image/
tags:
    - Docker
    - QGIS
    - QGIS Server
---

# What’s under the hood of the official QGIS Server Docker image?

## Introduction

![logo QGIS](https://cdn.geotribu.fr/img/logos-icones/logiciels_librairies/qgis.png){: .img-thumbnail-left }

The last Geotribu article about [deploying QGIS Server](https://geotribu.fr/articles/2010/2010-09-03_creer_diffuser_services_wms_avec_qgis/) dates back to 2010 :scream:! At the time, Docker wasn’t part of deployment practices, since it only became available in 2013. So now, with the official QGIS Server Docker image released last year, it’s time for us to catch up!

As a quick reminder, QGIS Server is an open-source web mapping server solution—similar to [GeoServer](https://geoserver.org/) or [MapServer](https://mapserver.org/)—that allows you to serve maps and geospatial data on the web. It relies on OGC (Open Geospatial Consortium) standards to provide interoperable services. QGIS Desktop offers a graphical interface for users to create and edit their maps.

The official QGIS Server documentation explains in detail how to [install QGIS Server](https://docs.qgis.org/3.40/fr/docs/server_manual/getting_started.html) natively, i.e. directly from your platform or distribution’s package repositories. However, there are very few resources available when it comes to containerized deployment. That’s why in this article, we’ll take a look at how and why using the official QGIS Server Docker image makes deployment much easier.

## Technical ecosystem

![logo Docker](https://cdn.geotribu.fr/img/logos-icones/logiciels_librairies/docker.svg){: .img-thumbnail-left }

Yes, there has been an official QGIS Server Docker image since 2024 :tada:... but what does that actually mean? Let’s start by first reviewing the underlying tech stack and a bit of vocabulary.

`Docker`

:   Docker is a platform that allows you to create, deploy, and run applications in containers, ensuring their portability and isolation. These applications can be distributed as images through specialized platforms or rebuilt from source code.

`Dockerfile`

:   A [Dockerfile](https://docs.docker.com/reference/dockerfile/) is a script that defines the steps to build a custom Docker image.

`Docker Hub`

:   [Docker Hub](https://hub.docker.com/) is an online platform that allows you to store, share, and distribute Docker images, providing a centralized repository for applications and their components.

`docker compose`

:   Composition – typically via the [Docker Compose](https://docs.docker.com/compose/) tool – allows you to define and manage multi-container applications using a configuration file that describes the services, networks, and volumes required for the application.

`Cluster cloud`

:   Clustering – not covered in this article – refers to the management of multiple Docker instances distributed across several physical or virtual machines to increase the availability, resilience, and scalability of the application. It typically involves cloud environments, such as those based on [Kubernetes](https://kubernetes.io/).

Many QGIS Server Docker images are available online, each with its own specificities related to its use and configuration. However, since 2024, the image originally provided by [OPENGIS.ch](https://www.opengis.ch/) is now available as an official image on the [QGIS.org repository on Docker Hub](https://hub.docker.com/r/qgis/qgis-server). To get it, it’s as simple as:

```bash title="Downloading the official QGIS Server image"
docker pull qgis/qgis-server:ltr
```

## Study of the content

To deploy QGIS Server as an application, it is necessary to integrate third-party services into the container to ensure its proper functioning. As stated in the documentation, QGIS Server is an application:

- Requiring a graphical server.
- Based on the FastCGI communication protocol to interact with a web server.
- Depending on the web server used (Apache, NGINX, etc.), a specific utility may be required to launch the underlying FCGI process.

To meet these requirements, several technical solutions can be considered, which partly explains the diversity of QGIS Server Docker images available online. The image provided by OPENGIS.ch relies on:

- [Xvfb](https://www.x.org/archive/X11R7.7/doc/man/man1/Xvfb.1.xhtml) (X virtual framebuffer) as the graphical server.
- [NGINX](https://nginx.org/) as the web sever.
- [spawn-fcgi](https://linux.die.net/man/1/spawn-fcgi) as the utility to run the QGIS Server FastCGI application.

### QGIS Server and FastCGI

![logo X11](https://cdn.geotribu.fr/img/logos-icones/logiciels_librairies/x11.png){: .img-thumbnail-left }

It is possible to easily test the QGIS Server application from the command line as long as a graphical server is running. To do this, you need to simulate the passing of environment variables to the FCGI process, as a web server would do. For example, you can send a request to QGIS Server using the `REQUEST_URI` environment variable:

```bash title="Execution of a request by the QGIS Server FCGI process"
# Starting a shell in a QGIS Server container
$ docker run -it qgis/qgis-server:ltr /bin/bash

# Running the virtual Xvfb graphical server in the background and redirecting
# standard output (file descriptor 1) and standard error (file descriptor 2)
# to /dev/null to suppress any output
$ /usr/bin/Xvfb :99 > /dev/null 2>&1 &

# Sending a request to QGIS Server and redirecting the logs to /dev/null
$ REQUEST_URI="MAP=fake.qgs" /usr/lib/cgi-bin/qgis_mapserv.fcgi 2>/dev/null
Content-Length: 195
Content-Type: text/xml; charset=utf-8
Server:  QGIS FCGI server - QGIS version 3.43.0-Master
Status:  500

<?xml version="1.0" encoding="UTF-8"?>
<ServerException>Project file error. For OWS services: please provide a SERVICE and a MAP parameter pointing to a valid QGIS project file</ServerException>
```

Here, we observe a `500` error code from QGIS Server indicating that the `fake.qgs` project specified via `REQUEST_URI="MAP=fake.qgs"` does not exist. The exception `<ServerException>Project file error.</ServerException>` is therefore returned by QGIS Server.

!!! note
    `Xvfb :99` starts a virtual X server with the display number `:99`, meaning that graphical applications running with this X server instance will not be displayed on a real monitor but will be rendered in memory. Once this virtual X server is started, the environment variable `ENV DISPLAY :99` is set in the [Dockerfile](https://github.com/qgis/qgis-docker/blob/main/server/Dockerfile) so that the QGIS Server application knows where to render in memory.

### Startup script

Previously, we started the QGIS Server container in interactive mode using the `-i` option and the `/bin/bash` command. Without these options, the QGIS Server application starts normally based on the `CMD` or `ENTRYPOINT` instruction specified in the Dockerfile.

The startup script used, located in the container's filesystem, can be found at `/usr/local/bin/start-xvfb-nginx.sh`, and its path can be obtained by inspecting the image.

```bash title="Inspecting the image to locate the startup script"
# Retrieving the startup script path
$ docker inspect -f '{{.Config.Cmd}}' qgis/qgis-server:ltr
[/bin/sh -c /usr/local/bin/start-xvfb-nginx.sh]

# Displaying the contents of the startup script
$ docker run qgis/qgis-server:ltr cat /usr/local/bin/start-xvfb-nginx.sh
```

By examining the contents of this script, we can observe the startup sequence of the third-party utilities mentioned above:

- the graphical server `Xvfb`
- `spawn-fcgi`, which launches QGIS Server while specifying TCP port `9993` for communication between the web server and the FCGI process
- `NGINX`, if needed, depending on the `SKIP_NGINX` environment variable set at runtime

```bash title="Retrieving the path of the startup script"
[...]
/usr/bin/Xvfb :99 -ac -screen 0 1280x1024x16 +extension GLX +render -noreset >/dev/null &
XVFB_PID=$(waitfor /usr/bin/Xvfb)

if [ -z "$SKIP_NGINX" ] || [ "$SKIP_NGINX" == "false" ] || [ "$SKIP_NGINX" == "0" ]; then
    nginx
    NGINX_PID=$(waitfor /usr/sbin/nginx)
fi

spawn-fcgi -n -u ${QGIS_USER:-www-data} -g ${QGIS_USER:-www-data} -d ${HOME:-/var/lib/qgis} -P /run/qgis.pid -p 9993 -- /usr/lib/cgi-bin/qgis_mapserv.fcgi &
[...]
```

### NGINX configuration

![logo nginx](https://cdn.geotribu.fr/img/logos-icones/logiciels_librairies/nginx.svg){: .img-thumbnail-left }

The NGINX web server configuration is deployed by replacing the default configuration file `/etc/nginx/nginx.conf`:

```bash title="Displaying the contents of the NGINX configuration file"
$ docker run -it qgis/qgis-server:ltr cat /etc/nginx/nginx.conf
[...]
    location /ogc/ {
        rewrite ^/ogc/(.*)$ /qgis/qgis_mapserv.fcgi?map=/io/data/$1/$1.qgs;
    }
    # Direct access without map rewrite
    location /ows/ {
        rewrite ^/ows/$ /qgis/qgis_mapserv.fcgi;
    }
    location /wfs3/ {
        rewrite ^/wfs3/(.*)$ /qgis/qgis_mapserv.fcgi;
    }
    location /qgis/ {
        internal; # Used only by the OGC rewrite
        root /var/www/data;
        fastcgi_pass  localhost:9993;
[...]
```

In this configuration, we distinguish three public entry points and one internal entry point:

- Access via `/ogc/my_project`, which specifically expects a QGIS project located at `/io/data/my_project/my_project.qgs`.
- Access via `/ows/` and `/wfs3/`.
- An internal access point via `/qgis`, used by the other endpoints, enabling communication with the FCGI process via the socket `localhost:9993`.

Entry point number 1 therefore requires mounting the `/io/data/` directory to work with a dedicated directory for each project.

## Container startup

Now that we've explored the features of our image, we can test the different launch configurations.

### Default configuration

It is possible to start the QGIS Server container with the default configuration using the parameters below:

- Redirecting local port `8080` to port `80` of the container's web server (`-p` option).
- Mounting the QGIS project directory to `/io/data` inside the container (`-v` option).

```bash title="Starting a QGIS Server container"
# Cloning the QGIS QGIS-Training-Data repository
git clone https://github.com/qgis/QGIS-Training-Data

# Preparing the world/world.qgs project directory for use as a mount point
# /io/data
cp -r QGIS-Training-Data/exercise_data/qgis-server-tutorial-data/ \
    QGIS-Training-Data/exercise_data/world

# Starting a container by mounting the QGIS project directory from the tutorial
docker run \
    -v ./QGIS-Training-Data/exercise_data/:/io/data \
    -p 8080:80 \
    qgis/qgis-server:ltr
```

Once the container is deployed, it is possible to send requests to QGIS Server through the NGINX entry points described in the previous section.

```bash title="Entry points /ogc, /ows and /wfs3"
# WMS request to /ogc on the NGINX web server of the container to access the project
# /io/data/world/world.qgs
curl "http://localhost:8080/ogc/world?SERVICE=WMS&REQUEST=GetCapabilities"

# WMS request to /ows, explicitly specifying the project path via the MAP parameter
curl "http://localhost:8080/ows/?MAP=/io/data/qgis-server-tutorial-data/world.qgs&SERVICE=WMS&REQUEST=GetCapabilities"

# OGC API Features request to /wfs3, explicitly specifying the project path via the
# MAP parameter
curl "http://localhost:8080/wfs3/collections.json?MAP=/io/data/qgis-server-tutorial-data/world.qgs"
```

The OGC API Features protocol, also known as WFS3, also provides HTML rendering, allowing direct access via your browser to a web page for exploring the underlying data.

```bash title="URL of an HTML rendering page for OGC API Features"
http://localhost:8080/wfs3/collections/countries/items/65.html?MAP=/io/data/qgis-server-tutorial-data/world.qgs
```

![OGC API Features Landing Page](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2025/qgis_server_docker/ogcapif.png "OGC API Feeatures Landing Page"){: .img-center loading=lazy }

### Composition with external NGINX

![logo docker compose](https://cdn.geotribu.fr/img/logos-icones/logiciels_librairies/docker-compose.png){: .img-thumbnail-left }

As mentioned earlier, an environment variable `SKIP_NGINX` allows using the QGIS Server container without the integrated web server. In this case, the QGIS Server container operates solely as a graphical rendering `backend`. It is then possible to use composition to create a multi-container application with:

- A QGIS Server container for graphical rendering.
- An NGINX container as the web server that redirects requests to the FCGI process via socket `9993`.

First, the NGINX configuration file describes an access point and how to communicate with QGIS Server:

```Nginx title="NGINX configuration file nginx.conf"
events {
    worker_connections  1024;
}

http {
    upstream qgis-fcgi {
        server qgis-server:9993;
    }
    server {
        location /qgisserver/ {
            fastcgi_pass  qgis-fcgi;
            fastcgi_param QUERY_STRING $query_string;
            include fastcgi_params;
        }
    }
}
```

Next, a configuration file for the `docker compose` tool must be written to describe our multi-container application:

```yml title="docker-compose.yml configuration file"
services:
  nginx:
    image: "nginx"
    volumes:
      # mounting the NGINX configuration file into the container
      - ./nginx.conf:/etc/nginx/nginx.conf
    ports:
      - "8080:80"
    depends_on:
      - qgis-server
  qgis-server:
    image: "qgis/qgis-server:ltr"
    environment:
      # disabling the internal NGINX server
      SKIP_NGINX: "true"
    volumes:
      # mounting the project directory
      - ./QGIS-Training-Data/exercise_data/:/io/data
```

!!! warning
    The configuration scripts above are intentionally simplified for the reader’s understanding and should not be used in a production environment :bomb:

Finally, we just need to run our containers using the `docker compose` command, which will automatically read the configuration file named `docker-compose.yml` located in the current directory:

```bash
# Running the containers in detached mode
$ docker compose up -d
[+] Running 3/3
 ✔ Network tmp_default          Created
 ✔ Container tmp-qgis-server-1  Started
 ✔ Container tmp-nginx-1        Started

# Status of the running NGINX and QGIS Server containers
$ docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED             STATUS             PORTS                                               NAMES
30dce3dd878f   nginx                  "/docker-entrypoint.…"   3 seconds ago       Up 2 seconds       0.0.0.0:8081->80/tcp, [::]:8081->80/tcp             test-nginx-1
8b73de48d754   qgis/qgis-server:ltr   "/bin/sh -c /usr/loc…"   3 seconds ago       Up 2 seconds       80/tcp, 9993/tcp                                    test-qgis-server-1

# GET request to /qgisserver, explicitly specifying the project path using the MAP parameter
$ curl "http://localhost:8080/qgisserver/?MAP=/io/data/qgis-server-tutorial-data/world.qgs&SERVICE=WMS&REQUEST=GetCapabilities"
```

## What about the plugins?

![logo pyqgis](https://cdn.geotribu.fr/img/logos-icones/programmation/pyqgis.png){: .img-thumbnail-left }

Since the beginning of this article, we’ve had fun (for sure! :sparkles:!) exploring the official QGIS Server image through some reverse engineering. However, it is also possible to refer to the [documentation](https://github.com/qgis/qgis-docker/blob/main/server/README.md) or examine the [Dockerfile](https://github.com/qgis/qgis-docker/blob/main/server/Dockerfile) used to build this image.

Looking at this file more closely, we can see the presence of the instruction `ENV QGIS_PLUGINPATH /io/plugins`. This implies that QGIS Server expects to have Python plugins in the specified directory. To test this mechanism, the [wfsOutputExtension](https://plugins.qgis.org/plugins/wfsOutputExtension/) plugin from [3Liz](https://www.3liz.com/) can be deployed:

```bash title="Deployment of the wfsOutputExtension plugin"
# Creating a dedicated directory for plugins
mkdir plugins

# Cloning the wfsOutputExtension server plugin
git clone https://github.com/3liz/qgis-wfsOutputExtension plugins

# Starting a container by mounting the QGIS project and plugin directories
docker run \
    -v ./QGIS-Training-Data/exercise_data/:/io/data \
    -v ./plugins/:/io/plugins \
    -p 8080:80 \
    qgis/qgis-server:ltr
```

Thanks to the `wfsOutputExtension` plugin, it is possible to specify various additional formats through the `OUTPUTFORMAT` parameter of the WFS `GetFeature` request. For example, we can specify the `csv` format, which is not natively supported by QGIS Server:

```bash title="Executing a WFS GetFeature request"
$ curl "http://localhost:8080/ows/?MAP=/io/data/qgis-server-tutorial-data/world.qgs&SERVICE=WFS&REQUEST=GetFeature&TYPENAME=countries&FEATUREID=countries.1&OUTPUTFORMAT=csv"
gml_id,id,name
countries.1,1,Antigua and Barbuda
```

## Conclusion

The official QGIS Server Docker image greatly simplifies the deployment of this map server solution, offering a ready-to-use configuration that is easily adaptable. With Docker, deploying QGIS Server becomes easy, portable, and isolated, without worrying about complex dependencies like graphic servers or web servers.

By integrating `NGINX`, `Xvfb`, and `FastCGI`, the image ensures smooth operation of QGIS Server in a containerized environment. It also provides the option to use an external web server, like NGINX, to separate functions and have better control over configurations

<!-- geotribu:authors-block -->
