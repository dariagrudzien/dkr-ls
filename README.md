# dkr-ls

CLI listing docker images in the local registry.

## Usage

```sh
usage: dkr-ls.py [-h] [-l LOG_LEVEL] {repos,tags} ...

positional arguments:
  {repos,tags}
    repos               List all Docker repositories
    tags                List all Docker image tags

optional arguments:
  -h, --help            show this help message and exit
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Set logging at a specific level. Options include DEBUG,INFO,WARNING,ERROR.
```

### Tags

Usage:

```sh
usage: dkr-ls.py tags [-h] [--minAge AGE] [--prefix [PREFIX [PREFIX ...]]] [--maxTags TAGS] [--minSize SIZE] [--sum]

optional arguments:
  -h, --help            show this help message and exit
  --minAge AGE          List only images older than minAge days
  --prefix [PREFIX [PREFIX ...]]
                        List only images with these repository prefixes; accepts multiple prefixes.
  --maxTags TAGS        List only maxTags number of tags of each image.
  --minSize SIZE        List only images bigger than minSize in human-readable format.
  --sum                 Sum all image sizes and print them at the end of the listing.
```
