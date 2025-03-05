# This is meant to be a very simple introduction to testing at a high level

def func(x):
    return x + 1

def test_answer():
    assert not func(3) == 5
