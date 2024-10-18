---
authors:
  - gallaman
  - jmoura
categories:
  - Announcements
comments: true
date: 2024-10-18
description: "In 2024, it's time to leave Teams and IRC behind to enter a new era where you can chat directly from QGIS with other GIS fellows. #GISChat #GISTribe"
icon: material/chat
license: beerware
links:
  - QTribu documentation: https://qtribu.geotribu.fr/
  - French announcement: https://geotribu.fr/articles/2024/2024-10-15_qchat/
pin: true
tags:
    - GISChat
    - GISTribe
    - QChat
    - QGIS
    - QTribu
title: "Introducing QChat: a chat to collaborate directly within QGIS!"
subtitle: Bring your GIS conversations to life with QChat in QGIS
---

# Introducing QChat: a chat room right into QGIS!

![icône globe speech GIS Chat - Credits: Global Market by DARAYANI from Noun Project (CC BY 3.0)](https://cdn.geotribu.fr/img/logos-icones/divers/globe_speech_GISChat.svg){: .img-thumbnail-left }

We're excited to announce the release of a new feature integrated into our [QTribu](https://plugins.qgis.org/plugins/qtribu/) plugin for QGIS: QChat! This new addition allows you to collaborate in real time with your team or other GIS fellows directly from QGIS.

We're in 2024 (unless you're reading this in 2025, or 2026, or... well, you get the idea), and let's be honest, Teams or IRC are outdated. Plus, you can't even use the hashtag #GISchat there, you can't meet fellow GIS enthusiasts and you definitely can't win Geotribu stickers :wink:... Honestly, it's time for something new.

Introducing a new way to chat directly in QGIS: `QChat`, a feature that lets you communicate with your peers within the best desktop GIS software around. The question is: why? And the answer: why not?

<!-- more -->

[Leave a comment :fontawesome-solid-comments:](#__comments "Go to comments"){: .md-button }
{: align=middle }

## TL;DR

1. Install [QTribu](https://plugins.qgis.org/plugins/qtribu/) through the QGIS plugins manager
1. Open the QChat widget by clicking on the :speech_balloon: icon in the plugin's toolbar
1. Click on the ':wrench: Settings' button to enter your nickname in settings panel
1. Pick the `QGIS` chat room in the dropdown list and click on the `Connect` button
1. Say hello to the GIS world by entering this message `Hi QGIS fellows! @all`.

----

## Why QChat?

!!! quote "ChatGPT's answer"
    Managing geospatial projects often involves constant back-and-forth communication between team members. Instead of switching between various tools and communication platforms, QChat offers a seamless way to discuss tasks, share updates, and troubleshoot issues, all within the QGIS environment.

Our answer: why not? :grin:

The #GISChat, born on Twitter and now on Mastodon, BlueSky, and even LinkedIn, enables interaction on geomatics-related topics.

There have already been initiatives to bring all this together in a [web application](https://gis.chat/).

And then, concerning the QGIS project in particular, there are already communication channels all over the place: [mailing lists](https://qgis.org/community/organisation/mailinglists/), [Telegram](https://t.me/joinchat/Aq2V5RPoxYYhXqUPoxRWPQ), [Discourse](https://discourse.osgeo.org/c/qgis/11), Signal, WhatsApp... But not right in QGIS! Too bad, isn't it?

----

## Installation

![logo QGIS](https://cdn.geotribu.fr/img/logos-icones/logiciels_librairies/qgis.png){: .img-thumbnail-left }

QChat is part of the QTribu plugin, published [on the official repository](https://plugins.qgis.org/plugins/qtribu). QChat is available starting from version 1.0 of the plugin, which can be installed via the QGIS plugin manager:

![QGIS - QTribu plugin installation in the QGIS plugin manager](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/qchat/qtribu_install.webp){: .img-center loading=lazy }

### :penguin: additional dependencies required on Linux

![WebSocket logo](https://cdn.geotribu.fr/img/logos-icones/divers/websocket.png){: .img-thumbnail-left }

QChat relies on [the WebSocket protocol](https://en.wikipedia.org/wiki/WebSocket), using components of the Qt framework that QGIS is based on. These components are included in the Windows versions of QGIS but must be installed manually on Linux. For example, on Ubuntu (22.04):

```sh title="apt command to install additional Qt dependencies on Debian/Ubuntu"
sudo apt install python3-pyqt5.qtmultimedia python3-pyqt5.qtwebengine python3-pyqt5.qtwebsockets
```

If these dependencies are not installed, QChat will be disabled in the plugin, and an error message will direct you to [the installation documentation](https://qtribu.geotribu.fr/installation.html#linux).

----

## Settings

Once the plugin is installed, you'll need to configure a few settings before chatting. You can find these settings in the plugin options tab, within the general QGIS settings (menu `Preferences` > `Options...`).

![QTribu plugin settings screen](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/qchat/qtribu_settings_full.webp){: .img-center loading=lazy }

!!! tip "Awesome plugin settings!"
    Need more info? You can check out the [QGIS plugin templater](https://oslandia.gitlab.io/qgis/template-qgis-plugin/index.html), which helps you generate a plugin skeleton with a settings tab and more... :wink:

Now, let's take a look at the main settings, starting with the `Attribution info` section at the bottom:

![QChat settings screen for QTribu plugin](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/qchat/qchat_settings_nickname.webp){: .img-center loading=lazy }

- `QChat nickname`: this is your nickname, shown to other chat users. It can be between 3 and 32 alphanumeric characters. Time to get creative (note: `xX_D4rth_L4mb3rt_Xx` and `B3rt1n_Le_ouf_du_78` are already taken).

- `QChat avatar`: this is the symbolic icon representing you in the chat. You can choose one of the fanciest icons from QGIS, and your avatar will be displayed next to every message you send.

Now, let's move to the `QChat` settings section:

![QChat settings screen for QTribu plugin](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/qchat/qchat_settings.webp){: .img-center loading=lazy }

- `instance URL`: this specifies which QChat instance you want to connect to. The instance rules can be checked via the `instance rules` button. As of now, two instances are available:
    - `gischat.geotribu.net`: Geotribu's English-language QChat instance, for everyone
    - `gischat.geotribu.fr`: Geotribu's French-language QChat instance, also for everyone

- `show avatars`: toggle to show or hide avatars next to chat messages
- `show admin messages`: toggle to display admin messages such as user connections and disconnections
- `enable cheatcodes`: :wink: :stuck_out_tongue_winking_eye:
- `play sounds`: toggle to play a sound when you're mentioned by another user. If enabled, you can adjust the volume and choose a notification sound.
- customize chat message colors with three color settings

----

## Let's start chatting

QChat is included in a [dock widget](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QDockWidget.html), meaning you can move and dock it wherever you like in the QGIS interface. To open the chat, you can either:

- go to the menu `Internet` > `QTribu` > `QChat`
- click on the second icon (a speech bubble) in the toolbar:

![QTribu plugin toolbar with QChat icon](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/qchat/qchat_icons.png){: .img-center loading=lazy }

And there you have it: QChat is open :tada: :

![QGIS screen with QChat panel on the right](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/qchat/qchat_qgis.webp){: .img-center loading=lazy }

!!! info
    P.S. shoutout to [tutoqgis.cnrs.fr](https://tutoqgis.cnrs.fr/)

In the `instance` section at the top, you can view the rules of the configured instance, as well as the number of users in each room via the `status` button.

To start chatting, you'll need to connect to a room by selecting one from the dropdown list. Once connected, you're ready to chat! Messages from other users will appear in the middle:

![QGIS screen with chat messages in QChat](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/qchat/qchat_messages.webp)

Note that:

- using `@all` in your message will notify all users in the room via the QGIS message bar
- double-clicking a message in QChat will allow you to mention the user who sent it

----

## Want to go further?

We've seen the client side of QChat in QGIS. To route the messages through WebSockets, there’s also a backend. [The GitHub repository is available here](https://github.com/geotribu/gischat).

### Set up your own instance

If you'd like to set up your own QChat backend, [you can follow the instructions on the repository](https://github.com/geotribu/gischat#deploy-a-self-hosted-instance). There's no need for a database, as it’s stateless and simply relies on WebSockets. It’s a [simple Docker image](https://hub.docker.com/r/gounux/gischat) that runs with a few environment variables.

There's also [a directory of QChat instances](https://github.com/geotribu/gischat/blob/main/instances.json), which you can contribute to if you set up your own instance, making it visible and available to others. The `discover instances` button in the plugin settings opens this directory in a QGIS popup.

### Develop a compatible client

If you’re interested in developing a compatible client, you can check out [the developer information on the GitHub repository](https://github.com/geotribu/gischat#developer-information).

Messages are sent over WebSocket, and there are [a few routes available](https://gischat.geotribu.net/docs) to:

- get instance rules
- retrieve room names
- check the number of open WebSockets per room
- send a message to a room via a POST request

And more features coming soon :wink:

----

## Conclusion

QChat is like having a virtual coffee corner, where technical discussions meet geographer jokes (the kind that only insiders find funny). So why not install QChat today and turn your QGIS experience into a collaborative adventure? After all, who said mapping had to be boring? With QChat, every map becomes a shared story, and every project an opportunity to laugh together. Ready to map and chat?
