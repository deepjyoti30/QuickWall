<h1 align="center">QuickWall</h1>

<div align="center" style="padding-top: 2em !important; padding-bottom: 2em; !important">
    <img src="qw.gif" style="border-radius: 4px !important;">
</div>

1. [Philosophy](#philosophy)
2. [How It Works](#how-it-works)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [TODO](#todo)
6. [Acknowledgements](#acknowledgements)

## Philosophy

### Set latest wallpaper from Unsplash directly from the commandline.

## How It Works

### It uses [Unsplash](https://unsplash.com) API to get wallpapers and set them using nitrogen.
### The images are downloaded to ```~/.QuickWall/``` and then set by nitrogen.

## Requirements

1. Python 3.4+
2. [nitrogen](https://github.com/l3ib/nitrogen)

> **NOTE**: These dependencies in linux can be installed in other variants.  
> For *arch linux*, you can use **pacman** package manager accordingly.

## Installation

* Run the following command in the root directory to install QuickWall.

```sh
python setup.py install
```

> **NOTE**: If you get **permission denied** error, run the above command with sudo.

## TODO

 - Add a logger
 - Handle errors better

## Acknowledgements

### [Unsplash](unsplash.com) for their awesome API.