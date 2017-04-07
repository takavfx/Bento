Bento
====================

[![Houdini Tools](https://img.shields.io/badge/Houdini-Tools-orange.svg?style=flat)](https://img.shields.io/badge/Houdini-Tools-orange.svg)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/takavfx/Bento/blob/develop/LICENSE.md)

## Description
Bento is a toolset for Houdini.


## Feature

### Shelf tool

![alt tag](docs/img/ss_shelf_tool.png)

* [Cache Dependency](docs/cacheDependency.md)
* [Creat Delayed Load Procedural](docs/create-dlp.md)
* [Color Nodes](docs/color-nodes.md)

### Python Panel

* [Cache Manager](docs/cacheManager.md)

![alt tag](docs/img/ss_cache_manager_0001.png)

### Scripts

* [Color Nodes(OnCreated)](docs/color-nodes.md)

## Install
1. Clone or Download this repository to your place you want to download.
2. Place this repository to houdini-accessible place.
3. Open **houdini.env**.
4. Add `HOUDINI_PATH` in the **houdini.env** file.
  * Ex: `HOUDINI_PATH = /anywhere/you/want/to/install/Bento:&` (Linux)
  * Ex: `HOUDINI_PATH = \anywhere\you\want\to\install\Bento;&` (Windows)
  * To add `&` is important to keep original Houdini Path.


* Recommended to install with `git clone` and `git submodule init` & `git submodule update` or `git clone --recursive` to download this repository and depended submodules, to keep tracking updates and also downgrade installed this repository.
