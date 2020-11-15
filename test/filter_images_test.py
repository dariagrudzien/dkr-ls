import pytest
from datetime import datetime, timezone
from dateutil import parser

from dkrls import filter_images

class MockArgs(object):
    def __init__(self, args):
        self.minSize = args['minSize']
        self.minAge = args['minAge']


def test_filter_images_no_args():
    now = datetime.fromtimestamp(1605437403.0, tz=timezone.utc)
    args = {
        'minSize': False,
        'minAge': False
    }
    mock_args = MockArgs(args)

    fixture = [
        {
            'created': parser.parse('2019-10-20T17:49:45.733794289Z'),
            'size': 872943600
        },
        {
            'created': parser.parse('2020-05-20T17:49:45.733794289Z'),
            'size': 972943600
        },
        {
            'created': parser.parse('2020-10-20T17:49:45.733794289Z'),
            'size': 772943600
        },
    ]

    assert filter_images(fixture, now, mock_args) == fixture

def test_filter_images_minSize():
    now = datetime.fromtimestamp(1605437403.0, tz=timezone.utc)
    args = {
        'minSize': '800',
        'minAge': False
    }
    mock_args = MockArgs(args)

    fixture = [
        {
            'created': parser.parse('2019-10-20T17:49:45.733794289Z'),
            'size': 872943600
        },
        {
            'created': parser.parse('2020-05-20T17:49:45.733794289Z'),
            'size': 972943600
        },
        {
            'created': parser.parse('2020-10-20T17:49:45.733794289Z'),
            'size': 772943600
        },
    ]

    filtered_images = [
        {
            'created': parser.parse('2019-10-20T17:49:45.733794289Z'),
            'size': 872943600
        },
        {
            'created': parser.parse('2020-05-20T17:49:45.733794289Z'),
            'size': 972943600
        }
    ]

    assert filter_images(fixture, now, mock_args) == filtered_images

def test_filter_images_minAge():
    now = datetime.fromtimestamp(1605437403.0, tz=timezone.utc)
    args = {
        'minSize': False,
        'minAge': 365
    }
    mock_args = MockArgs(args)

    fixture = [
        {
            'created': parser.parse('2019-10-20T17:49:45.733794289Z'),
            'size': 872943600
        },
        {
            'created': parser.parse('2020-05-20T17:49:45.733794289Z'),
            'size': 972943600
        },
        {
            'created': parser.parse('2020-10-20T17:49:45.733794289Z'),
            'size': 772943600
        },
    ]

    filtered_images = [
        {
            'created': parser.parse('2019-10-20T17:49:45.733794289Z'),
            'size': 872943600
        }
    ]

    assert filter_images(fixture, now, mock_args) == filtered_images

def test_filter_images_minAge_minSize():
    now = datetime.fromtimestamp(1605437403.0, tz=timezone.utc)
    args = {
        'minSize': '900',
        'minAge': 365
    }
    mock_args = MockArgs(args)

    fixture = [
        {
            'created': parser.parse('2019-10-20T17:49:45.733794289Z'),
            'size': 872943600
        },
        {
            'created': parser.parse('2020-05-20T17:49:45.733794289Z'),
            'size': 972943600
        },
        {
            'created': parser.parse('2020-10-20T17:49:45.733794289Z'),
            'size': 772943600
        },
    ]

    filtered_images = []

    assert filter_images(fixture, now, mock_args) == filtered_images
