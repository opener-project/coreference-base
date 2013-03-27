__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

locations_and_demonyms = []
demonyms = []

demonym_by_location = {}

indefinite_articles = set(("a", "an"))
indefinite_pronouns = set(("another", "anybody", "anyone", "anything", "each", "either", "enough", "everybody",
    "everyone", "everything", "less", "little", "much", "neither", "no one", "nobody",
    "nothing", "one", "other", "plenty", "somebody", "someone", "something", "both",
    "few", "fewer", "many", "others", "several", "all", "any", "more", "most", "none",
    "some", "such"))

quantifiers = set(("not", "every", "any", "none", "everything", "anything", "nothing", "all", "enough"))
partitives = set(("half", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten" , "hundred",
    "thousand", "million", "billion", "tens", "dozens", "hundreds", "thousands", "millions", "billions",
    "group", "groups", "bunch", "number", "numbers", "pinch", "amount", "amount", "total", "all", "mile",
    "miles", "pounds"))

stop_words = set(("a", "an", "the", "of", "at", "on", "upon", "in", "to", "from", "out", "as", "so", "such", "or",
    "and", "those", "this", "these", "that", "for", ",", "is", "was", "am", "are", "'s", "been", "were"
    ))

copulative_verbs = set((
    "act", "acts", "acting", "acted",
    "appear", "appears", "appearing", "appeared",
    "be", "am", "are",  "is", "was", "were", "being", "been",
    "isn't", "aren't", "wasn't", "weren't", "'m", "'re" "'s", "isn't", "aren't", "wasn't", "weren't",
    "become", "becomes", "becoming", "became",
    "come", "comes", "coming", "came"
                               "come out", "comes out", "coming out", "came out",
    "end up", "ends up", "ending up", "ended up",
    "get", "gets", "getting", "got", "got", "gotten"
                                            "go", "goes", "going", "went", "gone",
    "grow", "grows", "growing", "grew", "grown",
    "fall", "falls", "falling", "fell", "fallen",
    "feel", "feels", "feeling", "felt",
    "keep", " keeps", "keeping", "kept",
    "leave", "leaves", "leaving", "left",
    "look", "looks", "looking", "looked",
    "prove", "proves", "proving", "proved", "proved", "proven",
    "remain ", "remains", "remaining", "remained",
    "seem",  "seems",  "seeming", "seemed",
    "smell", "smells", "smelling", "smelled", "smelt",
    "sound", "sounds", "sounding", "sounded",
    "stay", "stays", "staying",  "stayed",
    "taste", "tastes", "tasting", "tasted",
    "turn", "turns", "turning", "turned",
    "turn up", "turns up", "turning up", "turned up",
    ))

UNKNOWN = "unknown"

relative_pronoun = ("that", "who", "which", "whom", "where", "whose")

subordinated_clause_tag = ("SBAR",)

person_ner_tag = ("PERSON", "PER")
nouns_pos = ("NN", "NNS")
mod_forms = ["NN", "NNS", "JJ", "JJR", "JJS"]
noun_phrase_tag = "NP"
conjuntion_tag = "CC"


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

load_dict("resources/files/demonym/{0}.txt".format("en"))


