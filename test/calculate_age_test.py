import pytest
from datetime import datetime, timezone
from dateutil import parser

from dkrls import calculate_age

def test_calculate_age_seconds():
    created = parser.parse('2020-10-20T17:49:45.000000000Z')
    now = datetime.fromtimestamp(1603216190.0, tz=timezone.utc)
    age = {'number': 5, 'unit': 'seconds'}

    assert calculate_age(created, now) == age

def test_calculate_age_minutes():
    created = parser.parse('2020-10-20T17:49:45.000000000Z')
    now = datetime.fromtimestamp(1603216485.0, tz=timezone.utc)
    age = {'number': 5, 'unit': 'minutes'}

    assert calculate_age(created, now) == age

def test_calculate_age_hours():
    created = parser.parse('2020-10-20T17:49:45.000000000Z')
    now = datetime.fromtimestamp(1603234185.0, tz=timezone.utc)
    age = {'number': 5, 'unit': 'hours'}

    assert calculate_age(created, now) == age

def test_calculate_age_days():
    created = parser.parse('2020-10-20T17:49:45.000000000Z')
    now = datetime.fromtimestamp(1603648185.0, tz=timezone.utc)
    age = {'number': 5, 'unit': 'days'}

    assert calculate_age(created, now) == age

def test_calculate_age_weeks():
    created = parser.parse('2020-10-20T17:49:45.000000000Z')
    now = datetime.fromtimestamp(1604512185.0, tz=timezone.utc)
    age = {'number': 2, 'unit': 'weeks'}

    assert calculate_age(created, now) == age

def test_calculate_age_months():
    created = parser.parse('2020-10-20T17:49:45.000000000Z')
    now = datetime.fromtimestamp(1616694585.0, tz=timezone.utc)
    age = {'number': 5, 'unit': 'months'}

    assert calculate_age(created, now) == age

def test_calculate_age_years():
    created = parser.parse('2020-10-20T17:49:45.000000000Z')
    now = datetime.fromtimestamp(1761414585.0, tz=timezone.utc)
    age = {'number': 5, 'unit': 'years'}

    assert calculate_age(created, now) == age
