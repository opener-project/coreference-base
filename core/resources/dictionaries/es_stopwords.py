# coding=utf-8
__author__ = 'Rodrigo Agerri <rodrigo.agerri@ehu.es>'


stop_words = set(('unas', 'una', 'unos','un','del','al','el','la','los','lo','las','de','en','sobre','por','dentro','hacia','desde','fuera','como','así','tal','o','y','esos','esas','este','esta','aquellas','aquellos','ese','esa','para',',','es','fue','era','soy','eres','sido','eras'))

non_words = ('ejem', 'ajá','hm','jo')
invalid_stop_words = ("SA", "SL", "etc", "hm")

#TODO RODRIGO
temporals = ("second", "minute", "hour", "day", "week", "month", "year", "decade", "century", "millennium",
      "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "now",
      "yesterday", "tomorrow", "age", "time", "era", "epoch", "morning", "evening", "day", "night", "noon", "afternoon",
      "semester", "trimester", "quarter", "term", "winter", "spring", "summer", "fall", "autumn", "season",
      "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december")
