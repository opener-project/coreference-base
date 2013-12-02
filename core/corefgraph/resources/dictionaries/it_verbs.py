# -*- coding: utf-8 -*-
__author__ = 'Valeria Quochi, valeria.quochi@ilc.cnr.it'
__date__ = '5/15/13'

#only intrinsic copulative verbs added: essere, sembrare, apparire, parere, divenire, diventare, restare, rimanere, risultare, stare
# TODO, see if other verb forms are useful/needed

copulative = set(("essere", "sono", "sei",  "è", "e'", "siamo", "siete", "ero",
    "eri", "era", "eravamo", "eravate", "erano", "fui" "fosti", "fu", "fummo", "foste", "furono", "sarò", "saro'", "sarai", "sarà", "sara'", "saremo", "sarete", "saranno", "sia", "siate", "siano", "fossi", "fosse", "fossimo", "fossero", "sarei", "saresti", "sarebbe", "saremmo", "sareste", "sarebbero", "essendo", "stato", "stata", "stati", "state", "sembrare", "sembro", "sembri", "sembra", "sembriamo", "sembrate", "sembrano", "sembravo", "sembravi", "sembrava", "sembravamo", "sembravate", "sembravano", "sembrai", "sembrasti", "sembrò", "sembro'", "sembrammo", "sembraste", "sembrarono", "sembrerò", "sembrero'", "sembrerai", "sembrerà", "sembrera'", "sembreremo", "sembrerete", "sembreranno", "sembriate", "sembrino", "sembrassi", "sembrasse", "sembrassimo", "sembrassero", "sembrando", "sembrato", "sembrata", "sembrati", "appaia", "appaiano", "appaio", "appaiono", "appare", "apparendo", "appari", "appariamo", "appariate", "apparimmo", "apparira'", "apparirai", "appariranno", "apparire", "apparirebbe", "apparirebbero", "apparirei", "appariremmo", "appariremo", "apparireste", "appariresti", "apparirete", "appariro'", "apparirà", "apparirò", "apparisse", "apparissero", "apparissi", "apparissimo", "appariste", "apparisti", "apparite", "appariva", "apparivamo", "apparivano", "apparivate", "apparivi", "apparivo", "apparsa", "apparse", "apparsi", "apparso", "apparve", "apparvero", "apparvi", "divenendo", "divenga", "divengano", "divengo", "divengono", "diveniamo", "diveniate", "divenimmo", "divenire", "divenisse", "divenissero", "divenissi", "divenissimo", "diveniste", "divenisti", "divenite", "diveniva", "divenivamo", "divenivano", "divenivate", "divenivi", "divenivo", "divenne", "divennero", "divenni", "diventa", "diventai", "diventammo", "diventando", "diventano", "diventare", "diventarono", "diventasse", "diventassero", "diventassi", "diventassimo", "diventaste", "diventasti", "diventata", "diventate", "diventati", "diventato", "diventava", "diventavamo", "diventavano", "diventavate", "diventavi", "diventavo", "diventera'", "diventerai", "diventeranno", "diventerebbe", "diventerebbero", "diventerei", "diventeremmo", "diventeremo", "diventereste", "diventeresti", "diventerete", "diventero'", "diventerà", "diventerò", "diventi", "diventiamo", "diventiate", "diventino", "divento", "divento'", "diventò", "divenuta", "divenute", "divenuti", "divenuto", "diverra'", "diverrai", "diverranno", "diverrebbe", "diverrebbero", "diverrei", "diverremmo", "diverremo", "diverreste", "diverresti", "diverrete", "diverro'", "diverrà", "diverrò", "diviene", "divieni", "paia", "paiamo", "paiano", "paiate", "paio", "paiono", "pare", "paremmo", "parendo", "parere", "paresse", "paressero", "paressi", "paressimo", "pareste", "paresti", "parete", "pareva", "parevamo", "parevano", "parevate", "parevi", "parevo", "pari", "parra'", "parrai", "parranno", "parrebbe", "parrebbero", "parrei", "parremmo", "parremo", "parreste", "parresti", "parrete", "parro'", "parrà", "parrò", "parsa", "parse", "parsi", "parso", "parve", "parvero", "parvi", "resta", "restai", "restammo", "restando", "restano", "restare", "restarono", "restasse", "restassero", "restassi", "restassimo", "restaste", "restasti", "restata", "restate", "restati", "restato", "restava", "restavamo", "restavano", "restavate", "restavi", "restavo", "restera'", "resterai", "resteranno", "resterebbe", "resterebbero", "resterei", "resteremmo", "resteremo", "restereste", "resteresti", "resterete", "restero'", "resterà", "resterò", "resti", "restiamo", "restiate", "restino", "resto", "resto'", "restò", "rimane", "rimanemmo", "rimanendo", "rimanere", "rimanesse", "rimanessero", "rimanessi", "rimanessimo", "rimaneste", "rimanesti", "rimanete", "rimaneva", "rimanevamo", "rimanevano", "rimanevate", "rimanevi", "rimanevo", "rimanga", "rimangano", "rimango", "rimangono", "rimani", "rimaniamo", "rimaniate", "rimarra'", "rimarrai", "rimarranno", "rimarrebbe", "rimarrebbero", "rimarrei", "rimarremmo", "rimarremo", "rimarreste", "rimarresti", "rimarrete", "rimarro'", "rimarrà", "rimarrò", "rimase", "rimasero", "rimasi", "rimasta", "rimaste", "rimasti", "rimasto", "risulta", "risultai", "risultammo", "risultando", "risultano", "risultare", "risultarono", "risultasse", "risultassero", "risultassi", "risultassimo", "risultaste", "risultasti", "risultata", "risultate", "risultati", "risultato", "risultava", "risultavamo", "risultavano", "risultavate", "risultavi", "risultavo", "risultera'", "risulterai", "risulteranno", "risulterebbe", "risulterebbero", "risulterei", "risulteremmo", "risulteremo", "risultereste", "risulteresti", "risulterete", "risultero'", "risulterà", "risulterò", "risulti", "risultiamo", "risultiate", "risultino", "risulto", "risulto'", "risultò", "sta", "stai", "stando", "stanno", "stara'", "starai", "staranno", "stare", "starebbe", "starebbero", "starei", "staremmo", "staremo", "stareste", "staresti", "starete", "staro'", "starà", "starò", "state", "stava", "stavamo", "stavano", "stavate", "stavi", "stavo", "stemmo", "stesse", "stessero", "stessi", "stessimo", "steste", "stesti", "stette", "stettero", "stetti", "stia", "stiamo", "stiano", "stiate", "sto" ))


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
