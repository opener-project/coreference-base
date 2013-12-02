__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '3/14/13'


plural = ("wijzelf", "onszelf", "julliezelf", "henzelf", "hunzelf", "zijzelf" ,"wij", "we",  "ons", "jullie", "hen", "hun", "zij" ,"ze", "onze")


singular = ("ikzelf","mezelf", "mijzelf", "jijzelf", "jezelf", "jouzelf", "uzelf", "hijzelf", "hemzelf", "zijzelf", "haarzelf", "zichzelf","ik", 
            "me", "mij", "mijn", "mijne", "jij", "je", "jou", "jouw", "jouwe", "hij", "zij", "ze", "haar", "zijn", "het")

female = ("zij", "ze", "haar", "hare", "haarzelf", "zijzelf")

male =  ("hij", "zijn", "hijzelf", "hem", "hemzelf" )

neutral = ("het", "waar", "hier", "daar", "waarvan")

animate =("ikzelf","mezelf", "mijzelf", "jijzelf", "jezelf", "jouzelf", "uzelf", "hijzelf", "hemzelf", "zijzelf", "haarzelf", "zichzelf",
          "ik", "me", "mij", "mijn", "mijne", "jij", "je", "jou", "jouw", "jouwe", "hij", "zij", "ze", "haar", "zijn","wijzelf", "onszelf", 
          "julliezelf", "henzelf", "hunzelf", "zijzelf" ,"wij", "we",  "ons", "jullie", "hen", "hun", "zij" ,"ze", "onze", "ikzelf","mezelf", 
          "mijzelf", "jijzelf", "jezelf", "jouzelf", "uzelf", "hijzelf", "hemzelf", "zijzelf", "haarzelf", "zichzelf","ik", "me", "mij", 
          "mijn", "mijne", "jij", "je", "jou", "jouw", "jouwe", "hij", "zij", "ze", "haar", "zijn")

inanimate = ("het", "waar", "waarvan", "daar")

indefinite = set(("ander", "iemand", "iets", "ieder", "iedere",  "genoeg", "iedereen","allemaal", "alles", "alle", "minder", 
             "veel", "geen enkele", "niemand", "geen enkel","niets", "niks","een", "ander", "veel", "beide","minder", "weinig",
             "weinigen", "velen", "enige", "enkele", "sommige", "verscheidene", "verschillende", "meer", "meest", "geen", "zulke"))
 
relative = ("dat", "die", "wiens", "waarvan", "welke", "waarop", "waaronder", "waarover", "aan wie", "van wie", "waaraan", "waarbij", "bij wie", "waar")
 
reflexive = ("ja",)

no_organization = ("ja",)

third_person = ("ja",)

second_person = ("ja",)

first_person = ("ja",)

others = ("who", "whom", "whose", "where", "when", "which")

all = set(first_person + second_person + third_person + others)

pleonastic = ("it",)
