
plural = ("wir",  "uns", "ihr",  "euch", "sie", "unser","unsere", "unseres","unserem","unserer","unseren","euer","euere","euerer","eueres","eurerem",
          "eureren", "eurer","ihr", "ihre", "ihrer", "ihres", "ihrem", "ihren", "ihrer", "wir selbst","uns selbst", "ihr selbst", "euch selbst",
          "sie selbst" , "ihr selbst")


singular = ("ich", "meiner", "mir", "mein", "meinen", "meinem", "meine", "mich", "ich selbst", "mich selbst", "mir selbst", "du" , "dein", "deiner",
            "deinen", "deinem", "deine", "dir", "dich", "du selbst", "dir selbst", "dich selbst","er", "sein", "seiner", "ihm", "ihn", "ihr", "sie",
            "ihrer", "ihr", "ihre", "er selbst", "sie selbst", "ihm selbst", "ihn selbst", "ihr selbst","es", "sich selbst")

female = ("sie", "ihrer", "ihr", "ihre","sie selbst","ihr selbst")

male = ("er", "sein", "seiner", "ihm", "ihn", "ihr", "sie", "ihrer", "ihr", "ihre", "er selbst", "ihm selbst", "ihn selbst")

neutral = ("das", "wo", "hier", "dort", "wovon")

#De
animate = ("ich"," meiner"," mir"," mein"," meinen"," meinem"," meine","mich", "ich selbst","mich selbst","mir selbst","du","dein",
           "deiner","deinen","deinem","deine","dir","dich","du selbst","dir selbst","dich selbst","er","sein","seiner","ihm","ihn","ihr","sie","ihrer",
           "ihr"," ihre","er selbst","sie selbst","ihm selbst","ihn selbst","ihr selbst","es","sich selbst","wir","uns","ihr","euch","sie","unser",
           "unsere","unseres","unserem","unserer","unseren","euer","euere","euerer","eueres","eurerem","eureren","eurer","ihr","ihre","ihrer",
           "ihres","ihrem","ihren","ihrer","wir selbst","uns selbst","ihr selbst","euch selbst","sie selbst","ihr selbst")


#de
inanimate = ("das", "wo", "dort", "wovon")


#de
indefinite = set(("andere", "jede", "jeder", "genug", "wenig", "wenige", "weniger", "viele" , "kein", "viel", "keiner", "keine",
              "keines", "ein", "andere", "viele",  "weniger", "little", "paar" , "viel", "einige", "einiger", "einiges",
              "mehrere", "mehr", "meiste", "meisten"))


#de
relative = ("der", "die", "das","dessen", "deren", "dessen","dem", "der", "dem", "den", "die", "das","die", "deren","denen","die","Welcher",
           "welche", "welches")

reflexive = ("ja",)

no_organization = ("ja",)

third_person = ("ja",)

second_person = ("ja",)

first_person = ("ja",)

others = ("who", "whom", "whose", "where", "when", "which")

all = set(first_person + second_person + third_person + others)

pleonastic = ("it",)
