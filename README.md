<h1 align="center">QuickWall</h1>

<div align="center" style="padding-top: 2em !important; padding-bottom: 2em; !important">
    <img src="qw.gif" style="border-radius: 4px !important;">
</div>


1. [How It Works](#how-it-works)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [TODO](#todo)
6. [Acknowledgements](#acknowledgements)

## How It Works

### It uses [Unsplash](https://unsplash.com) API to get wallpapers and set them using nitrogen.
### The images are downloaded to ```~/.QuickWall/``` and then set by nitrogen.

## Requirements

1. Python 3.4+
2. Currently supported wallpaper setters

    - [nitrogen](https://github.com/l3ib/nitrogen)
    - [feh](https://github.com/derf/feh)

> **NOTE**: These dependencies in linux can be installed in other variants.  
> For *arch linux*, you can use **pacman** package manager accordingly.

## Installation

* Run the following command in the root directory to install QuickWall.

```sh
python setup.py install
```

> **NOTE**: If you get **permission denied** error, run the above command with sudo.

## Usage


```

usage: QuickWall [-h] [--version] [--clear-cache] [--setter SETTER]

QuickWall - Quickly set latest wallpapers from Unsplash directly from the
commandline.

optional arguments:
  -h, --help       show this help message and exit
  --version        show the program version number and exit
  --clear-cache    Clear the cache from the cache folder (~/.QuickWall)
  --setter SETTER  Wallpaper setter to be used. Currently supported ones:
                   nitrogen, feh (default: nitrogen)


```

## TODO

 - ~~Add a logger~~
 - Add support for different wallpaper setters
 - Handle errors better

## Acknowledgements

### [Unsplash](unsplash.com) for their awesome API.