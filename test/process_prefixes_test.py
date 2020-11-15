import pytest

from dkrls import process_prefixes

def test_process_prefixes():

    prefixes = [['latest'], ['buster']]
    fixture = [
        {'repository': 'python:buster'},
        {'repository': 'python:3.8'},
        {'repository': 'python:latest'},
        {'repository': 'python'},
        {'repository': 'nginx:latest'},
        {'repository': 'nginx'}
    ]

    processed_images = [
        {'repository': 'python:buster'},
        {'repository': 'python:latest'},
        {'repository': 'nginx:latest'}
    ]

    assert process_prefixes(fixture, prefixes) == processed_images

