import pytest
from dateutil import parser

from dkrls import process_images

class MockImage(object):
    """
    A base class for representing a single object on the server, mocking Docker Image object.
    """
    def __init__(self):
        self.attrs = {
            'Id': 'sha256:f5e423f5ce1f833fb2d6d7a521f13e8784bae08380d0145db7ab0af8b52e8b56', 'RepoTags': ['python:3.8-buster'],
            'Created': '2020-10-20T17:49:45.733794289Z',
            'Size': 881916878
        }

def test_process_images():
    fixture = [MockImage()]

    processed_images = [{
        'repository': 'python',
        'tag': '3.8-buster',
        'id': 'f5e423f5ce1f',
        'created': parser.parse('2020-10-20T17:49:45.733794289Z'),
        'size': 881916878
    }]

    assert process_images(fixture) == processed_images
