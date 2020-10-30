#!/usr/bin/env python3

import argparse, shlex, subprocess, re

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
        # this rounds up a month to 30 days
        return int(number)*30
    elif unit == 'years':
        # this ignores leap years
        return int(number)*365
    else:
        # this assumes hours, minutes, seconds
        return 1

def processSize(size):
    number = re.search('([0-9]*)', size)[1]
    unit = re.search('(\D+)', size)[1].upper()

    if unit == 'GB':
        number = number * 1024
    elif unit == 'KB':
        number = round(number / 1024, 2)

    return number

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
                'size': processSize(l[6])
            }
            images.append(image)
    return images

def getRepos(images, args = {}):
    print('REPOSITORY')
    repos = []
    for image in images:
        if image['repository'] not in repos:
            # print(repos)
            repos.append(image['repository'])
            print(image['repository'])

def getTags(images, args = {}):

    column_names = ['REPOSITORY', 'TAG', 'IMAGE ID', 'CREATED', 'SIZE']

    col_width = max(len(str(value)) for image in images for (key, value) in image.items()) + 2  # padding
    print("".join(name.ljust(col_width) for name in column_names))

    for image in images:
        image_details = []
        image_details.append(image['repository'].ljust(col_width))
        image_details.append(image['tag'].ljust(col_width))
        image_details.append(image['id'].ljust(col_width))
        image_details.append(image['created'].ljust(col_width))
        image_details.append((image['size'] + 'MB').ljust(col_width))

        print("".join(image_details))


def main():
    # usage = 'Usage: %prog [options]'
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-l', '--log-level', help='Set logging at a specific level. Options include DEBUG,INFO,WARNING,ERROR.',
    #                     metavar='LOG_LEVEL', default='INFO')
    # subparsers = parser.add_subparsers()

    # r_parser = subparsers.add_parser('repos', help='List all Docker repositories')

    # t_parser = subparsers.add_parser('tags', help='List all Docker image tags')
    # t_parser.add_argument('--minAge', help='List only images older than minAge days', metavar='AGE', type=int, default=None)
    # t_parser.add_argument('--prefix', help='List only images with these repository prefixes; accepts multiple prefixes.', nargs='*', action='append', metavar='PREFIX', type=str, default=None)
    # t_parser.add_argument('--maxTags', help='List only maxTags number of tags of each image.', metavar='TAGS', type=str, default=None)
    # t_parser.add_argument('--minSize', help='List only images bigger than minSize in human-readable format.', metavar='SIZE', type=str, default=None)
    # t_parser.add_argument('--sum', help='Sum all image sizes and print them at the end of the listing.', action='store_true', default=False)

    # args = parser.parse_args()
    # print(args)

    images = getImages('docker images')
    # getRepos(images)
    getTags(images)

if __name__ == '__main__':
    main()
