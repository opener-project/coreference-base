# coding=utf-8
__author__ = 'Rodrigo Agerri <rodrigo.agerri@ehu.es>'

from resources.lambdas import equality_checker, list_checker,fail

# extracted from Freeling dictionary by looking for DI
indefinite_articles = fail

#cuantitativos
quantifiers = list_checker(("ninguno", "todos", "alguno", "todo", "algo", "suficiente", "Varios", "mucho", "poco", "más",
                   "menos", "bastante", "demasiado", "harto", "tando"))
#
partitives = list_checker(("half", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "hundred",
                 "thousand", "million", "billion", "tens", "dozens", "hundreds", "thousands", "millions", "billions",
                 "group", "groups", "bunch", "number", "numbers", "pinch", "amount", "amount", "total", "all", "mile",
                 "miles", "pounds"))

partitive_particle = equality_checker("de")