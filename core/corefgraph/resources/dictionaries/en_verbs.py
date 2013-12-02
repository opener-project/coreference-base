# coding=utf-8
""" List of verbs used in sieves and mention detection. Are based on list found Stanford CoreLP, also it may been modified.


"""

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


copulative = set((
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

# From StanfordCoreNLP
reporting = set(("accuse", "acknowledge", "add", "admit", "advise", "agree", "alert",
      "allege", "announce", "answer", "apologize", "argue",
      "ask", "assert", "assure", "beg", "blame", "boast",
      "caution", "charge", "cite", "claim", "clarify", "command", "comment",
      "compare", "complain", "concede", "conclude", "confirm", "confront", "congratulate",
      "contend", "contradict", "convey", "counter", "criticize",
      "debate", "decide", "declare", "defend", "demand", "demonstrate", "deny",
      "describe", "determine", "disagree", "disclose", "discount", "discover", "discuss",
      "dismiss", "dispute", "disregard", "doubt", "emphasize", "encourage", "endorse",
      "equate", "estimate", "expect", "explain", "express", "extoll", "fear", "feel",
      "find", "forbid", "forecast", "foretell", "forget", "gather", "guarantee", "guess",
      "hear", "hint", "hope", "illustrate", "imagine", "imply", "indicate", "inform",
      "insert", "insist", "instruct", "interpret", "interview", "invite", "issue",
      "justify", "learn", "maintain", "mean", "mention", "negotiate", "note",
      "observe", "offer", "oppose", "order", "persuade", "pledge", "point", "point out",
      "praise", "pray", "predict", "prefer", "present", "promise", "prompt", "propose",
      "protest", "prove", "provoke", "question", "quote", "raise", "rally", "read",
      "reaffirm", "realise", "realize", "rebut", "recall", "reckon", "recommend", "refer",
      "reflect", "refuse", "refute", "reiterate", "reject", "relate", "remark",
      "remember", "remind", "repeat", "reply", "add_report", "request", "respond",
      "restate", "reveal", "rule", "say", "see", "show", "signal", "sing",
      "slam", "speculate", "spoke", "spread", "state", "stipulate", "stress",
      "suggest", "support", "suppose", "surmise", "suspect", "swear", "teach",
      "tell", "testify", "think", "threaten", "told", "uncover", "underline",
      "underscore", "urge", "voice", "vow", "warn", "welcome",
      "wish", "wonder", "worry", "write"))

generics_you_verbs = "know"
pleonastic_verbs = ("is", "was", "became", "become")
alternative_a_pleonastic_verbs = ("seems", "appears", "means", "follows")
alternative_b_pleonastic_verbs = ("turns",)
