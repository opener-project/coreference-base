# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '11/15/12'

from ... import properties

import os


locations_and_demonyms = []
demonyms = []

demonym_by_location = {}


def load_dict(file_name):
    """ Load the demonym and place in memory."""
    demonym_file = open(file_name)
    for line in demonym_file:
        line = line.lower()
        if line[0] != "#":
            tokens = line.split("\t")
            locations_and_demonyms.extend(tokens)
            demonyms.extend(tokens[1:])
            demonym_by_location[tokens[0]] = set(tokens[1:])
    locations_and_demonyms.extend(locations_and_demonyms)

load_dict(os.path.join(properties.module_path, "files/demonym/{0}.txt".format(properties.lang)))
