---
authors:
  - gallaman
categories:
  - Article
comments: true
date: 2024-12-02
description: "Some news about QChat and the features provided by the new 1.1 version. #GISChat #GISTribe"
icon: material/chat
license: beerware
links:
  - QTribu documentation: https://qtribu.geotribu.fr/
  - Initial introduction: content/posts/2024-10-18_introducing-QChat-chat-rooms-in-QGIS.md
pin: false
tags:
    - GISChat
    - GISTribe
    - QChat
    - QGIS
    - QTribu
title: "Some news about QChat, the chat within QGIS"
subtitle:
---

# Some news about QChat, the chat within QGIS

![icône globe speech GIS Chat - Credits: Global Market by DARAYANI from Noun Project (CC BY 3.0)](https://cdn.geotribu.fr/img/logos-icones/divers/globe_speech_GISChat.svg){: .img-thumbnail-left }

In October [we introduced "QChat"](./2024-10-18_introducing-QChat-chat-rooms-in-QGIS.md), the plugin for chatting with other QGIS users, directly inside QGIS.

![QGIS screen with chat messages in QChat](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/qchat/qchat_screenshot_en.webp)

Since then, we have been working on some evolutions, and new geo oriented features are now available.

<!-- more -->

[Leave a comment :fontawesome-solid-comments:](#__comments "Go to comments"){: .md-button }
{: align=middle }

Those new features are provided by the QTribu plugin, that can be downloaded from the official QGIS plugin repository. Latest version is `1.1.0` :

![QGIS - QTribu plugin installation in the QGIS plugin manager](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/qchat/qtribu_install_en_v110.webp){: .img-center loading=lazy }

Here are the new available features :tada:

## User registration

It is possible to register in the connected room, and to see which users are registered and present in the room.

Actually, the plugin will automatically register you, except if the `Incognito mode` setting is checked, which will prevent the plugin from sending a registration message when connecting to a room :

![QGIS - Incognito mode in QTribu plugin settings](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/qchat/qchat_setting_incognito.webp){: .img-center loading=lazy }

In the QChat panel, the `List Users` button (next to the room list) will display who is present (and registered) in the room. It is possible to fetch it using [an API call](https://gischat.geotribu.net/docs#/default/get_connected_users_room__room__users_get).

## Automatic reconnection

If you choose to automatically reconnect in the QTribu settings,
the QChat will start and auto-connect to the last room when QGIS starts.

## Like a QChat message

You can now like a QChat message :thumbsup: !

By simply right-clicking on a message in the chat, the sender will be notified that you liked his/her message.

N.B.: the sender must be registered in order to receive your like notification. If he/she is in incognito mode, there will not be any notification.

## Send a vector layer in the QChat

When connected to a room, you can share a vector layer in the chat by right-clicking on a layer in QGIS layer tree panel. A `Send on QChat` action is proposed and will send the layer via geojson in the websocket, thus being transmitted to the other
users in the room :

![QGIS - Send a vector layer on QChat](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/qchat/qchat_action_send_vector_layer.webp){: .img-center loading=lazy }

When receiving such a layer message in the chat, just click on it or use the right-click action to load it into your QGIS :

![QGIS - Load a vector layer from QChat](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/qchat/qchat_load_vector_layer.webp){: .img-center loading=lazy }

N.B.: in order to avoid layers that would be too big, the server blocks from sharing to the other users the layers that have more than 500 features.

## Send other geo stuff

The bottom side of the QChat panel allows you other types of shares :

![QGIS - Send actions](https://cdn.geotribu.fr/img/articles-blog-rdp/articles/2024/qchat/qchat_actions_send.webp){: .img-center loading=lazy }

- `Send Image` : this will open FileDialog to select file images to share on the chat (allowed formats are JPG and PNG). Big images are scaled down by the server before being broadcast.

- `Send QGIS screenshot` : this will take a screenshot of your current QGIS and send it on the chat, thus allowing people to visually share what they are working on

- `Send Extent` : this will share the current extent of your QGIS canvas. When receiving such a message, clicking on it or using the right-click action makes QGIS canvas fit the shared extent

- `Send CRS` : this will share in the chat the CRS you are currently using
