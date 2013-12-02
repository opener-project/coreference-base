# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from . import logger

import marshal


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
    """ Load the bergsma file into a dict of tuples. Try to keep a marshaled version of the file.
    If you changes the file remember to erase the marshalled version.
    """
    marshal_filename = filename + ".marshal"
    try:
        with open(marshal_filename, 'r') as data_file:
            data = marshal.load(data_file)
        return data
    except Exception as ex:
        logger.info("No marshal file")
        logger.debug("Reason: %s", ex)
        with open(filename, 'r') as data_file:
            data = dict()
            for line in data_file:
                try:
                    form, stats = line.split("\t")
                    data[form] = tuple([int(x) for x in stats.split()])
                except Exception as ex:
                    pass
                    logger.debug("line sipped: {0}: {1}".format(line, ex))
            try:
                with open(marshal_filename, 'w') as data_file:
                    marshal.dump(data, data_file, -1)
                logger.warning("Created marshal file")
                logger.debug("path: %s", marshal_filename)
            except Exception as ex:
                logger.error("Marshal file not created:%s", ex)
                pass
        return data