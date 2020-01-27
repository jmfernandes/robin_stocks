import os
# content of test_robin.py
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4

def test_username():
    assert os.environ['robin_username'] == "joshfernandes@mac.com"
