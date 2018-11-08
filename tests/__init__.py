from unittest import TestSuite, TestLoader
from os.path import dirname

suite = TestSuite([TestLoader().discover(dirname(__file__))])