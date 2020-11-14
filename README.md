# dkr-ls

A Python CLI listing docker images in the local Docker registry.

## Usage

### Repos

List all local Docker repositories:

```sh
  usage: dkrls.py repos [-h]

  optional arguments:
    -h, --help  show this help message and exit
```

### Tags

List all tags in the local Docker repository:

Usage:

```sh
  usage: dkrls.py tags [-h] [--minAge DAYS] [--prefix [PREFIX [PREFIX ...]]] [--maxTags NUMBER] [--minSize SIZE] [--sum]

  optional arguments:
    -h, --help            show this help message and exit
    --minAge DAYS         List only images older than minAge days (e.g. --minAge 20)
    --prefix [PREFIX [PREFIX ...]]
                          List only images with these repository prefixes; accepts multiple prefixes (e.g. --prefix python --prefix nginx)
    --maxTags NUMBER      List only maxTags number of tags of each image (e.g. --maxTags 3)
    --minSize SIZE        List only images bigger than specified in MB (e.g. --minSize 800)
    --sum                 Sum all image sizes and print them at the end of the listing.
```

## Logging

## Local Installation

This instruction assumes that you have your favorite virtual environment activated already:

```pip install -e .`

## Building Docker Image

From root directory run `make build` - it will build the `dkr-ls` image with a `latest` tag.
