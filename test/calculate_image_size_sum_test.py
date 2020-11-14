import pytest

from dkrls import calculate_image_size_sum

def test_calculate_image_size_sum():
    fixture = [
        {'size': '987654312', 'id': 'abc'},
        {'size': '987654312', 'id': 'abc'},
        {'size': '987654312', 'id': 'abc'},
        {'size': '987654312', 'id': 'xyz'},
        {'size': '987654312', 'id': 'xyz'},
    ]

    assert calculate_image_size_sum(fixture) == '2.0GB'
