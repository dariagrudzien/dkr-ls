#!/usr/bin/env python3

import argparse
import shlex, subprocess

# $ docker images
# REPOSITORY                    TAG                 IMAGE ID            CREATED             SIZE
# daria-k8s-example             latest              4b7887b8c2d3        5 days ago          882MB
# daria-example                 latest              393f0e8bf585        5 days ago          882MB
# <none>                        <none>              f23e4f6c4d32        5 days ago          882MB
# <none>                        <none>              35c46893ce8b        5 days ago          882MB
# <none>                        <none>              6845d517696b        5 days ago          882MB
# python                        buster              bbf31371d67d        9 days ago          882MB
# gcr.io/k8s-minikube/kicbase   v0.0.12-snapshot3   25ac91b9c8d7        5 weeks ago         952MB

def calculateAge(number, unit):
    if unit == 'days':
        return int(number)
    elif unit == 'weeks':
        return int(number)*7
    elif unit == 'months':
        return int(number)*30
    else:
        raise TypeError('Couldn\'t calculate age of the image. Check if image processing was successful.')

def getImages(cmd):
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT, encoding='utf-8')
    output = ps.communicate()[0]
    images = []
    for line in output.splitlines():
        if not 'IMAGE ID' in line:
            l = shlex.split(line)
            image = {
                'repository': l[0],
                'tag': l[1],
                'id': l[2],
                'created': f'{l[3]} {l[4]} ago',
                'age': calculateAge(l[3], l[4]),
                # TODO: this needs to be separated into size and unit
                'size': int(l[6].replace('MB',''))
            }
            images.append(image)
    return images

def getRepos(images, args = {}):
    print(images)

def main():
    usage = 'Usage: %prog [options]'
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log-level', help='Set logging at a specific level. Options include DEBUG,INFO,WARNING,ERROR.',
                        metavar='LOG_LEVEL', default='INFO')
    subparsers = parser.add_subparsers()

    r_parser = subparsers.add_parser('repos', help='List all Docker repositories')

    t_parser = subparsers.add_parser('tags', help='List all Docker image tags')
    t_parser.add_argument('--minAge', help='List only images older than minAge days', metavar='AGE', type=int, default=None)
    t_parser.add_argument('--prefix', help='List only images with these repository prefixes; accepts multiple prefixes.', nargs='*', action='append', metavar='PREFIX', type=str, default=None)
    t_parser.add_argument('--maxTags', help='List only maxTags number of tags of each image.', metavar='TAGS', type=str, default=None)
    t_parser.add_argument('--minSize', help='List only images bigger than minSize in human-readable format.', metavar='SIZE', type=str, default=None)
    t_parser.add_argument('--sum', help='Sum all image sizes and print them at the end of the listing.', action='store_true', default=False)

    args = parser.parse_args()
    print(args)

    # images = getImages('docker images')
    # getRepos(images)

if __name__ == '__main__':
    main()
