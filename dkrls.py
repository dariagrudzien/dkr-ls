#!/usr/bin/env python3

import argparse, re, datetime, logging
from datetime import datetime, timedelta, timezone

import docker
from dateutil import parser, rrule, relativedelta

class DkrlsError(Exception):
    pass

def calculateAge(created, now):
    """
    Pprepare a Docker CLI-like output of image age.
    After researching `datetime`, `dateutil` and other libraries
    I decided to do this manually to get as close as possible to
    Docker CLI output.
    `created` and `now` are both datetime.datetime objects.
    """

    age = {}
    rdelta = relativedelta.relativedelta(now, created)
    difference = now - created

    if rdelta.years > 0:
        age['number'] = rdelta.years
        age['unit'] = 'years'
    elif rdelta.years == 0 and difference >= timedelta(days=60):
        age['number'] = rdelta.months
        age['unit'] = 'months'
    elif rdelta.years == 0 and difference < timedelta(days=60) and difference >= timedelta(days=14):
        days = 0
        if rdelta.months == 1:
            days = 30
        days += rdelta.days
        weeks = round(days / 7)
        age['number'] = weeks
        age['unit'] = 'weeks'
    elif rdelta.years == 0 and difference < timedelta(days=14) and difference >= timedelta(days=1):
        age['number'] = rdelta.days
        age['unit'] = 'days'
    elif rdelta.years == 0 and difference < timedelta(days=1) and rdelta.hours >= 1:
        age['number'] = rdelta.hours
        age['unit'] = 'hours'
    elif rdelta.years == 0 and difference < timedelta(days=1) and rdelta.hours < 1 and rdelta.minutes > 0:
        age['number'] = rdelta.minutes
        age['unit'] = 'minutes'
    elif rdelta.years == 0 and difference < timedelta(days=1) and rdelta.hours < 1 and rdelta.minutes <= 0 and rdelta.seconds > 0:
        age['number'] = rdelta.seconds
        age['unit'] = 'seconds'
    elif rdelta.years == 0 and difference < timedelta(days=1) and rdelta.hours < 1 and rdelta.minutes <= 0 and rdelta.seconds <= 0:
        age['number'] = 1
        age['unit'] = 'second'
    else:
        raise DkrlsError(f'Encountered age of an image which this CLI can\'t handle: {rdelta}')
    return age

def processSize(size):
    """
    Docker SDK provides size in bytes, which is processed here to
    provide Docker CLI-like output.
    """
    final_size = ''
    if size < 1000:
        final_size = f'{size} B'
    elif size > 1000 and size < 1000000:
        size = round(size / 1000, 1)
        final_size = f'{size}KB'
    elif size > 1000000 and size < 1000000000 :
        size = round(size / 1000000, 1)
        final_size = f'{size}MB'
    elif size > 1000000000:
        size = round(size / 1000000000, 1)
        final_size = f'{size}GB'

    return final_size

def processImages(images):
    """
    This takes a list with image attributes as provided by Docker Image class
    https://docker-py.readthedocs.io/en/stable/images.html#docker.models.images.Image
    and saves only the relevant data.
    """
    processed_images = []
    for image in images:
        attrs = image.attrs
        # Docker CLI uses 12 first characters, while short_id is only 10, so we need to strip
        # the long id which comes in `sha:<characters>` format
        image_id = attrs['Id'].split(':')[1][0:11]
        if len(attrs['RepoTags']) != 0:
            for repo_tag in attrs['RepoTags']:
                repo = repo_tag.split(':')[0]
                tag = repo_tag.split(':')[1]
                image = {
                    'repository': repo,
                    'tag': tag,
                    'id': image_id,
                    'created': parser.parse(attrs['Created']),
                    'size': attrs['Size']
                }
                processed_images.append(image)
        else:
            created = parser.parse(attrs['Created'])
            image = {
                'repository': '<none>',
                'tag': '<none>',
                'id': image_id,
                'created': created,
                'size': attrs['Size']
            }
            processed_images.append(image)
    return processed_images

def addImageAge(images, now):
    """
    Docker SDK provides date of image creations as a date in ISO format.
    It is processed here to provide Docker CLI-like output.
    """
    formatted_images = []
    for image in images:
        age_number = calculateAge(image['created'], now)['number']
        age_unit = calculateAge(image['created'], now)['unit']
        formatted_age = f'{age_number} {age_unit} ago'
        image['age'] = formatted_age
        formatted_images.append(image)
    return formatted_images

def listRepos(images, args):
    """
    Create output for `repos` argument.
    """
    logging.info('REPOSITORY')
    repos = []
    for image in images:
        if image['repository'] not in repos:
            repos.append(image['repository'])
            logging.info(image['repository'])

def filterImages(images, now, args):
    """
    A filter to select only those images which match
    specified size and age conditions.
    """
    minSize = 0
    pastDate = None

    if args.minSize:
        minSize = (int(re.search('([0-9]*)', args.minSize)[1]) * 1000000)
    if args.minAge:
        pastDate = now - timedelta(days=args.minAge)

    if args.minAge and not args.minSize:
        return [image for image in images if image['created'] < pastDate]
    elif not args.minAge and args.minSize:
        return [image for image in images if image['size'] > minSize]
    elif args.minAge and args.minSize:
        return [image for image in images if image['created'] < pastDate if image['size'] > minSize]
    else:
        return images

def processPrefixes(images, prefixes):
    """
    Remove any image which prefix doesn't match what was specified
    in CLI arguments. The result will include any image which
    repository name contains the requested prefix.
    Starts by flattening the list of prefixes received from
    argparse in `[['prefix1'], ['prefix2']]` format.
    """
    flatten = lambda t: [item for sublist in t for item in sublist]
    prefixes = flatten(prefixes)

    for i in reversed(range(len(images))):
        if not any(prefix in images[i]['repository'] for prefix in prefixes):
            del images[i]
    return images

def collectMaxTags(images, tags):
    """
    Keep only the images if tags did not exceed the specified amount.
    """
    listed = {}
    for i in reversed(range(len(images))):
        image_id = images[i]['id']
        image_tag = images[i]['tag']
        if image_id not in listed and image_tag != '<none>':
            listed[image_id] = 1
        elif image_id in listed and listed[image_id] < tags:
            listed[image_id] += 1
        else:
            del images[i]
    return images

def calculateImageSizeSum(images):
    """
    Sum the total size of images in the local repo recalulated to
    a reasonable unit.
    Avoids counting the same image twice.
    """
    total_size = 0
    counted = {}
    for i in reversed(range(len(images))):
        image_id = images[i]['id']
        if image_id not in counted:
            counted[image_id] = 1
            total_size += int(images[i]['size'])
    total_size = processSize(total_size)
    return total_size

def listTags(images, now, args):
    """
    Create output for `tags` argument.
    """
    column_names = ['REPOSITORY', 'TAG', 'IMAGE ID', 'CREATED', 'SIZE']
    # calculate column padding and print out the header
    col_width = max(len(str(value)) for image in images for (key, value) in image.items()) + 2
    logging.info("".join(name.ljust(col_width) for name in column_names))

    # filter images according to size and age arguments
    filtered_images = filterImages(images, now, args)

    # filter images according to specified prefixes
    if args.prefix:
        filtered_images = processPrefixes(filtered_images, args.prefix)

    # filter images according to specified amount of tags
    if args.maxTags:
        filtered_images = collectMaxTags(filtered_images, args.maxTags)

    # prepare a Docker CLI-like output
    for image in filtered_images:
        image_details = []
        image_details.append(image['repository'].ljust(col_width))
        image_details.append(image['tag'].ljust(col_width))
        image_details.append(image['id'].ljust(col_width))
        image_details.append(image['age'].ljust(col_width))
        image_details.append(processSize(image['size']).ljust(col_width))

        logging.info("".join(image_details))

    # print out a sum of image sizes
    if args.sum:
        total_size = calculateImageSizeSum(filtered_images)
        logging.info(f'TOTAL: \t {total_size}'.rjust(col_width * 4))


def main():
    usage = 'Usage: %prog [options]'
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log-level', help='Set logging at a specific level. Options include: DEBUG,INFO,WARNING,ERROR,CRITICAL.',
                        metavar='LOG_LEVEL', default='INFO')
    subparsers = parser.add_subparsers(dest='cmd')
    subparsers.required = True

    r_parser = subparsers.add_parser('repos', help='List all Docker repositories')

    t_parser = subparsers.add_parser('tags', help='List all Docker image tags')
    t_parser.add_argument('--minAge', help='List only images older than minAge days (e.g. --minAge 20)', metavar='DAYS', type=int, default=None)
    t_parser.add_argument('--prefix', help='List only images with these repository prefixes; accepts multiple prefixes (e.g. --prefix python --prefix nginx)', nargs='*', action='append', metavar='PREFIX', type=str, default=None)
    t_parser.add_argument('--maxTags', help='List only maxTags number of tags of each image (e.g. --maxTags 3)', metavar='NUMBER', type=int, default=None)
    t_parser.add_argument('--minSize', help='List only images bigger than specified in MB (e.g. --minSize 800)', metavar='SIZE', type=str, default=None)
    t_parser.add_argument('--sum', help='Sum all image sizes and print them at the end of the listing.', action='store_true', default=False)

    args = parser.parse_args()
    now = datetime.now(timezone.utc)
    filtered_images = []

    log_level = 'INFO'
    if args.log_level:
        log_level = args.log_level.upper()

    logging.basicConfig(format='%(message)s', level=log_level)

    try:
        # initiate Docker client and get a list of images in local repository
        client = docker.from_env()
        images = client.images.list()
        # process images
        processed_images = addImageAge(processImages(images), now)

        # list repos
        if args.cmd == 'repos':
            listRepos(processed_images, args)

        #list tags
        if args.cmd == 'tags':
            filtered_images = filterImages(processed_images, now, args)
            listTags(filtered_images, now, args)
    except docker.errors.DockerException as e:
        logging.error(f'Error when trying to run Docker - make sure it\'s running on your machine: {e}')

if __name__ == '__main__':
    main()
