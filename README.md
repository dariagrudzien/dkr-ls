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

You can change the logging level, e.g. to see detailed logs:

```sh
  ./dkrls.py -l 'DEBUG' repos
```

```sh
  usage: dkrls.py [-h] [-l LOG_LEVEL] {repos,tags} ...

  positional arguments:
    {repos,tags}
      repos               List all Docker repositories
      tags                List all Docker image tags

  optional arguments:
    -h, --help            show this help message and exit
    -l LOG_LEVEL, --log-level LOG_LEVEL
                          Set logging at a specific level. Options include: DEBUG,INFO,WARNING,ERROR,CRITICAL.
```

## Local Installation

This instruction assumes that you have your favorite virtual environment activated already:

`pip install -e .`

## Testing

Run unit tests with `make test`.

## Building Docker Image

From root directory run `make build` - it will build the `dkr-ls` image with a `latest` tag.
