import pytest

from dkrls import collect_max_tags

def test_collect_max_tags():
    fixture = [
        {'tag': 'latest', 'id': 'abc'},
        {'tag': 'buster', 'id': 'abc'},
        {'tag': '3.8', 'id': 'abc'},
        {'tag': 'latest', 'id': 'xyz'},
        {'tag': 'stable', 'id': 'xyz'},
    ]

    processed_images = [
        {'tag': 'buster', 'id': 'abc'},
        {'tag': '3.8', 'id': 'abc'},
        {'tag': 'latest', 'id': 'xyz'},
        {'tag': 'stable', 'id': 'xyz'},
    ]

    assert collect_max_tags(fixture, 2) == processed_images
