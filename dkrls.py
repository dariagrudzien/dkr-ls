#!/usr/bin/env python3

import argparse, shlex, subprocess, re, logging

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
            repos.append(image['repository'])
            print(image['repository'])

def filterImages(images, args = {}):
    if args.minAge and not args.minSize:
        return [image for image in images if image['age'] > args.minAge]
    elif not args.minAge and args.minSize:
        return [image for image in images if image['size'] > args.minSize]
    elif args.minAge and args.minSize:
        return [image for image in images if image['age'] > args.minAge if image['size'] > args.minSize]
    else:
        return images

def processPrefixes(prefixes, images):
    flatten = lambda t: [item for sublist in t for item in sublist]
    prefixes = flatten(prefixes)

    for i in reversed(range(len(images))):
        if any(prefix in images[i]['repository'] for prefix in prefixes):
            del images[i]

    return images

def processTags(tags, images):
    listed = {}
    for i in reversed(range(len(images))):
        image_id = images[i]['id']
        if image_id not in listed:
            listed[image_id] = 1
        elif image_id in listed and listed[image_id] < tags:
            listed[image_id] += 1
        else:
            del images[i]
    return images

def getTags(images, args = {}):
    column_names = ['REPOSITORY', 'TAG', 'IMAGE ID', 'CREATED', 'SIZE']
    col_width = max(len(str(value)) for image in images for (key, value) in image.items()) + 2  # padding
    print("".join(name.ljust(col_width) for name in column_names))

    filered_images = filterImages(images, args)

    if args.prefix:
        filered_images = processPrefixes(args.prefix, filered_images)

    if args.maxTags:
        filered_images = processTags(args.maxTags, filered_images)

    for image in filered_images:
        image_details = []
        image_details.append(image['repository'].ljust(col_width))
        image_details.append(image['tag'].ljust(col_width))
        image_details.append(image['id'].ljust(col_width))
        image_details.append(image['created'].ljust(col_width))
        image_details.append((image['size'] + 'MB').ljust(col_width))

        print("".join(image_details))

    if args.sum:
        size_sum = 0
        for i in reversed(range(len(filered_images))):
            size_sum += int(filered_images[i]['size'])
        print(f'TOTAL: \t {(str(size_sum) + "MB")}')


def main():
    usage = 'Usage: %prog [options]'
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log-level', help='Set logging at a specific level. Options include DEBUG,INFO,WARNING,ERROR.',
                        metavar='LOG_LEVEL', default='INFO')
    subparsers = parser.add_subparsers(dest='cmd')
    subparsers.required = True

    r_parser = subparsers.add_parser('repos', help='List all Docker repositories')

    t_parser = subparsers.add_parser('tags', help='List all Docker image tags')
    t_parser.add_argument('--minAge', help='List only images older than minAge days', metavar='AGE', type=int, default=None)
    t_parser.add_argument('--prefix', help='List only images with these repository prefixes; accepts multiple prefixes.', nargs='*', action='append', metavar='PREFIX', type=str, default=None)
    t_parser.add_argument('--maxTags', help='List only maxTags number of tags of each image.', metavar='TAGS', type=int, default=None)
    t_parser.add_argument('--minSize', help='List only images bigger than minSize in human-readable format.', metavar='SIZE', type=str, default=None)
    t_parser.add_argument('--sum', help='Sum all image sizes and print them at the end of the listing.', action='store_true', default=False)

    args = parser.parse_args()

    try:
        images = getImages('docker images')

        if args.cmd == 'repos':
            getRepos(images,args)

        if args.cmd == 'tags':
            getTags(images, args)

    except Exception as e:


if __name__ == '__main__':
    main()
