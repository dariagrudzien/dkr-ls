import pytest

from dkrls import list_repos

def test_list_repos():
    fixture = [
        {'repository': 'python'},
        {'repository': 'python'},
        {'repository': 'nginx'}
    ]

    assert list_repos(fixture) == ['python', 'nginx']
