# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from . import logger
from ..resources.dictionaries import verbs
from ..resources.tagset import dependency_tags


class Literator:
    """ Find speech type and speaker for mentions.
    """

    # The subject dependency valid types for a subject of a reporting verb,
    # TODO MULTILANGUAGE mover a tagset
    invalid_speakers = ("-", "")

    def __init__(self, graph, graph_builder):
        self.graph = graph
        self.graph_builder = graph_builder

    def _find_speaker(self, constituent):
        """ Find a plausible speaker for a mention inside a direct speech(Text inside quotations).

        Find closest reporting verb and select their subject as speaker.

        """

        sentence_root = self.graph_builder.get_root(constituent)
        # Set the sentences where find the speaker
        previous_sentence = self.graph_builder.get_prev_sentence(sentence_root)
        next_sentence = self.graph_builder.get_next_sentence(sentence_root)
        sentences = (sentence_root, previous_sentence, next_sentence)
        for root in sentences:
            # If the current sentence is the first or the last.
            if root:
                sentence_terms = self.graph_builder.get_sentence_words(sentence=root)
                for term in sentence_terms:
                    if term["lemma"] in verbs.reporting and term["utterance"] != constituent["utterance"]:
                        for word, dependency in self.graph_builder.get_dependant_words(term):
                            if dependency_tags.subject(dependency["value"]):
                                return word
        head_word = self.graph_builder.get_head_word(constituent)
        return head_word["speaker"]

    def speaker_extractor(self, syntatic_element, head_word):
        """ Return a speaker, if exist, of the element.
        """
        if syntatic_element["quoted"]:
            return self._find_speaker(syntatic_element)
        else:
            return head_word["speaker"]

    def _check_span(self, quoted_char_span, mention_char_spam):
        """ Check if constituent is inside the quotation
        """
        return (mention_char_spam[0] >= quoted_char_span[0]) and (mention_char_spam[1] <= quoted_char_span[1])

    def speech_extractor(self, syntactic_element, head_word):
        """ Return the speech type of a syntactic element: conversational, non-conversational or None.
        """
        root = self.graph_builder.get_root(syntactic_element)
        offset = root["begin"]

        if head_word["speaker"] and head_word["speaker"] not in self.invalid_speakers:
            return "direct"

        #TODO improve
        quotes = [i for i, ltr in enumerate(root["form"]) if ltr == "'"]
        if len(quotes) > 1:
            for index in range(len(quotes)/2):
                if self._check_span(
                        quoted_char_span=(offset + quotes[index * 2], offset + quotes[(index * 2) + 1]),
                        mention_char_spam=(syntactic_element["begin"], syntactic_element["end"])):
                    return "indirect"

        quotes += [i for i, ltr in enumerate(root["form"]) if ltr == '"']
        if len(quotes) > 1:
            for index in range(len(quotes)/2):

                if self._check_span(
                        quoted_char_span=(offset + quotes[index * 2], offset + quotes[(index * 2) + 1]),
                        mention_char_spam=(syntactic_element["begin"], syntactic_element["end"])):
                    return "indirect"
        return None