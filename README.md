<h1 align="center">QuickWall</h1>

<div align="center" style="padding-top: 2em !important; padding-bottom: 2em; !important">
    <img src="qw.gif" style="border-radius: 4px !important;">
</div>


<div align="center">
<br/>

<a href="#how-it-works">How It Works</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#requirements">Requirements</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#installation">Installation</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#usage">Usage</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#to-do">TODO</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="#acknowledgements">Acknowledgements</a>&nbsp;&nbsp;&nbsp;
<br/><br/>

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)<br/><br/>
![Travis (.org)](https://img.shields.io/travis/deepjyoti30/QuickWall?style=for-the-badge) [![License](https://img.shields.io/badge/License-MIT-pink.svg?style=for-the-badge)](LICENSE) ![PyPI](https://img.shields.io/pypi/v/QuickWall?style=for-the-badge) ![PyPI - Downloads](https://img.shields.io/pypi/dm/QuickWall?style=for-the-badge) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-purple.svg?style=for-the-badge)](http://makeapullrequest.com)

</div>

## How It Works

### It uses [Unsplash](https://unsplash.com) API to get wallpapers and set them using nitrogen.
### The images are downloaded to ```~/.QuickWall/``` and then set by nitrogen.

## Requirements

1. Python 3.6+
2. Currently supported wallpaper setters

    - [nitrogen](https://github.com/l3ib/nitrogen)
    - [feh](https://github.com/derf/feh)

> **NOTE**: These dependencies in linux can be installed in other variants.  
> For *arch linux*, you can use **pacman** package manager accordingly.

## Installation

* It is available in Pypi

```sh
pip3 install QuickWall
```

* Available in AUR [here](https://aur.archlinux.org/packages/quickwall/)

```sh
yay -S quickwall
```

### OR

* Run the following command in the root directory to install QuickWall.

```sh
python setup.py install
```

> **NOTE**: If you get **permission denied** error, run the above command with sudo.

## Usage

```console

usage: QuickWall [-h] [--version] [--clear-cache] [--setter SETTER] [-d]
                 [--remove-id ID] [--dir DIR] [--id ID] [--random]
                 [--search TERM]

QuickWall - Quickly set latest wallpapers from Unsplash directly from the
commandline.

optional arguments:
  -h, --help            show this help message and exit
  --version             show the program version number and exit
  --clear-cache         Clear the cache from the cache folder (~/.QuickWall)
  --setter SETTER       Wallpaper setter to be used. Currently supported ones:
                        nitrogen, feh (default: nitrogen)
  -d, --disable-blacklist
                        Disable adding the image to blacklisted ones.
  --remove-id ID        Remove the passed ID from the blacklist.
  --dir DIR             Directory to download the wallpapers
  --id ID               Get a photo by its ID.
  --random              Get random wallpapers.
  --search TERM         Show wallpapers based on the passed term

```

## TODO

- Add tests
- Add support for different wallpaper setters (raise an issue if you want me to support some particular one)
- Handle errors better
- ~~Add a logger~~
- ~~Add support to search~~

## Acknowledgements

### [Unsplash](https://unsplash.com) for their awesome API.