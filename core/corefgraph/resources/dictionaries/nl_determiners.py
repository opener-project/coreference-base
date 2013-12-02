__author__ = 'josubg'

from ..lambdas import equality_checker, list_checker


#indefinite_articles = set(("a", "an"))
indefinite_articles = list_checker(("een","een"))

#quantifiers = set(("not", "every", "any", "none", "everything", "anything", "nothing", "all", "enough"))
quantifiers = list_checker(("niet", "iedere", "ieder", "geen", "alle", "alles", "niets", "voldoende", "genoeg",
                    "enkele", "enige", "sommige", "elk", "elke", "heleboel", "menig", "menige", "niks"))

#partitives = set(("half", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten" , "hundred",
#    "thousand", "million", "billion", "tens", "dozens", "hundreds", "thousands", "millions", "billions",
#    "group", "groups", "bunch", "number", "numbers", "pinch", "amount", "amount", "total", "all", "mile",
#    "miles", "pounds"))

partitives = list_checker(("half", "halve", "een", "twee", "drie", "vier", "vijf", "zes", "zeven", "acht", "negen", "tien" ,
                  "honderd","duizend", "miljoen", "biljoen", "tientallen",  "honderden", "duizenden", "miljoenen",
                  "biljoenen","groep", "groepen", "aantal", "aantallen", "hoeveelheid", "hoeveelheden", "totaal",
                  "alle", "pond", "kilo", "meter","kilometer", "kilometers", "ponden", "kilo's",  "stapels"))

partitive_particle = equality_checker("of")
