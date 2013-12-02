
from ..lambdas import equality_checker, list_checker

indefinite_articles = list_checker(("eine", "einer", "eines", "einem", "einen"))

quantifiers = list_checker(("nicht", "jeder", "jeder", "nein", "all", "alles", "nichts", "ausreichend",
                    "ausreichend", "einige", "einige", "einige" , "jeder", "jeder", "viel", "viele", "viele", "nichts"))


partitives = list_checker(("halb", "halbe", "eins", "zwei", "drie", "vier", "fuenf", "sechs", "sieben", "acht" , "neun zehn", "hundert", "tausend",
                  "hundertausend", "Millionen", "millionen", "Billion", "hunderten", "tausenden", "miljonen", "Zahlen", "Mengen", "Menge",
                  "alle", "pfund", "Pfund", "Kilometer", "meter"))

partitive_particle = equality_checker("of")
