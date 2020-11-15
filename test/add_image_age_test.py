import pytest
from datetime import datetime, timezone
from dateutil import parser

from dkrls import add_image_age

def test_add_image_age():
    date = parser.parse('2020-10-20T17:49:45.733794289Z')
    now = datetime.fromtimestamp(1605437403.0, tz=timezone.utc)

    fixture = [{
        'repository': 'python',
        'tag': 'latest',
        'id': 'hu1iu2ng3mi5',
        'created': date,
        'size': 872943600
    }]

    images_with_age = [{
        'repository': 'python',
        'tag': 'latest',
        'id': 'hu1iu2ng3mi5',
        'created': date,
        'age': '4 weeks ago',
        'size': 872943600
    }]

    assert add_image_age(fixture, now) == images_with_age
