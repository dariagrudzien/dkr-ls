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
                'age': calculateAge(l[3], l[4]),
                'size': int(l[6].replace('MB',''))
            }
            images.append(image)
    return images

def getRepos(images, args = {}):
    print(images)


images = getImages('docker images')
getRepos(images)

