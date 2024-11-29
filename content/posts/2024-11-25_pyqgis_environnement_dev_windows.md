---
authors:
  - nicogodet
categories:
  - Tutorial
comments: true
date: 2024-11-25
description: "For Intellisense happiness"
icon: material/microsoft-visual-studio-code
license: beerware
links:
    - "Cooking with Gispo: QGIS Plugin Development in VS Code": https://www.gispo.fi/en/blog/qgis-plugin-development-in-vs-code/
    - IDE settings for writing and debugging plugins (official PyQGIS cookbook): https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/plugins/ide_debugging.html
    - French version: https://geotribu.fr/articles/2024/2024-11-25_pyqgis_environnement_dev_windows/
pin: false
tags:
    - Plugin QGIS
    - PyQGIS
    - Python
    - VS Code
    - Windows
title: "Creating a Python virtual environment for PyQGIS development with VS Code on Windows"
subtitle: Keep our env safe, for our PyQGIS children
---

# Creating a Python virtual environment for developing QGIS plugin with VS Code on Windows

## Introduction

![PyQGIS logo](https://cdn.geotribu.fr/img/logos-icones/programmation/pyqgis.png){: .img-thumbnail-left }

Anyone who has tried it, knows that configuring a Python, PyQGIS, and PyQt environment on Windows for developing QGIS plugins is a real challenge. Often, it feels like a losing battle...

Well, not anymore! After scouring the depths of the internet and exploring tips provided by [Julien](https://geotribu.fr/team/julien-moura/), here is one method to have (almost) all the auto-completions for PyQGIS, PyQt and more in VS Code.

<!-- more -->

[Leave a comment :fontawesome-solid-comments:](#__comments "Go to comments"){: .md-button }
{: align=middle }

----

## Creating the Virtual Environment

I will assume that you have installed QGIS in the `C:\OSGeo4W` directory (the procedure is the same whether QGIS is installed via the OSGeo4W network installer or the MSI package; the paths in this article just need to be adapted to your installation).

1. Open an OSGeo4W Shell and navigate to the location where you want to create the virtual environment.  
   For example, a freshly created plugin template using the [QGIS Plugin Templater](https://gitlab.com/Oslandia/qgis/template-qgis-plugin).

1. Run the following commands:

    ```cmd title="Creating a virtual environment in the OSGeo4W Shell"
    C:\OSGeo4W\bin\python-qgis.bat -m venv --system-site-packages .venv
    C:\OSGeo4W\bin\python-qgis.bat -c "import pathlib;import qgis;print(str((pathlib.Path(qgis.__file__)/'../..').resolve()))" > .venv\qgis.pth
    ```

    The `--system-site-packages` option allows the virtual environment to inherit libraries specific to the Python environment in QGIS.

1. To ensure VS Code recognizes `processing` imports, add the following line to the `.venv\qgis.pth` file:  
    `C:\OSGeo4W\apps\qgis\python\plugins`

    Your file should look like this:

    ```text title="Content of .venv\qgis.pth file"
    C:\OSGeo4W\apps\qgis\python
    C:\OSGeo4W\apps\qgis\python\plugins
    ```

    Make sure the encoding of the `.venv\qgis.pth` file is set to UTF-8.

1. Create a `sitecustomize.py` file in the `.venv\Lib\site-packages` folder with the following content:

    ```python title=".venv\Lib\site-packages\sitecustomize.py"
    import os

    os.add_dll_directory("C:/OSGeo4W/bin")
    os.add_dll_directory("C:/OSGeo4W/apps/qgis/bin")
    os.add_dll_directory("C:/OSGeo4W/apps/Qt5/bin")
    ```

1. In the `.venv\pyvenv.cfg` file, modify the occurrences of `C:\OSGeo4W\bin` to `C:\OSGeo4W\apps\Python312`:

    ```ini title=".venv\pyenv.cfg"
    home = C:\OSGeo4W\apps\Python312
    include-system-site-packages = true
    version = 3.12.6
    executable = C:\OSGeo4W\apps\Python312\python.exe
    command = C:\OSGeo4W\apps\Python312\python.exe -m venv --system-site-packages <The full path to your venv>
    ```

----

## In VS Code

If you open VS Code in the folder where you just created the virtual environment, VS Code will automatically detect the environment (otherwise, install the [VS Code Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)), and as you type code, VS Code will suggest PyQGIS objects or methods.

![Import completion](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/pyqgis_environnement_dev_windows/vscode_intellisense_completion_imports.webp){: .img-center loading=lazy }

![Method completion](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/pyqgis_environnement_dev_windows/vscode_intellisense_completion_methodes.webp){: .img-center loading=lazy }

To also have all the completions related to PyQt, it seems necessary to install an additional Python library called `PyQt5-stubs` (although it is no longer maintained, it still works).  
In the VS Code terminal, run the following command:

```powershell title="Install PyQT completion in the virtual environment"
pip install PyQt5-stubs
```

![PyQt](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/pyqgis_environnement_dev_windows/vscode_pyqt.webp){: .img-center loading=lazy }

All of this just to have colorful code :smiley:!

![Contribute to GeoPF Altimétrie](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/pyqgis_environnement_dev_windows/vscode_geopf.webp){: .img-center loading=lazy }
