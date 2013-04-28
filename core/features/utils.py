__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

import collections


def load_file(file_name):
    data_file = open(file_name, 'r')
    data = [line[:-1] for line in data_file]
    data_file.close()
    return data


def split_gendername_file(filename):
    combined = open(filename, 'r')
    male = []
    female = []
    for line in combined:
        try:
            name, gender = line.replace('\n', '').split('\t')
            if gender == "MALE":
                male.append(name)
            else:
                female.append(name)
        except Exception as ex:
            pass
            #print "line skyped: {0}".format(line)
    combined.close()
    return female, male


def bergma_split(filename):
    data_file = open(filename, 'r')
    data = collections.defaultdict(lambda: (0, 0, 0, 0))
    for line in data_file:
        try:
            form, stats = line.split("\t")
            data[form] = tuple([int(x) for x in stats.split()])
        except Exception as ex:
            pass
            #print "line skyped: {0}: {1}".format(line, ex)
    data_file.close()
    return data