__author__ = 'josubg'

import properties

pronouns = __import__("{0}_pronouns".format(properties.lang), globals(), locals())
stopwords = __import__("{0}_stopwords".format(properties.lang), globals(), locals())
verbs = __import__("{0}_verbs".format(properties.lang), globals(), locals())
determiners = __import__("{0}_determiners".format(properties.lang), globals(), locals())
