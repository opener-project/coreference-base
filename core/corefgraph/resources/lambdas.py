# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


import re


matcher = lambda r: re.compile(r).match
list_checker = lambda l: lambda element: element in l
equality_checker = lambda x: lambda value: x == value
fail = lambda x: False
