import pytest

from dkrls import process_size

def test_process_size_bytes():
    size = 684
    assert process_size(size) == "684B"

def test_process_size_kb():
    size = 9487
    assert process_size(size) == "9.5KB"

def test_process_size_mb():
    size = 872943600
    assert process_size(size) == "872.9MB"

def test_process_size_gb():
    size = 27694872943600
    assert process_size(size) == "27694.9GB"
