# coding=utf-8
""" Contains the necesary elements to extract the speaker of text fragments.

"""
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from . import logger
from ..resources.dictionaries import verbs
from ..resources.tagset import dependency_tags


class SpeakerExtractor:
    """ Find speech type and speaker for mentions.
    """

    # The subject dependency valid types for a subject of a reporting verb,
    invalid_speakers = ("-", "")

    def __init__(self, graph, graph_builder):

        self.graph = graph
        self.graph_builder = graph_builder

    def _find_speaker(self, syntactic_element, head_word):
        """ Find a plausible speaker for a mention inside a direct speech(Text inside quotations).

        Find closest reporting verb and select their subject as speaker.

        """
        constituent_utterance = syntactic_element["utterance"]
        current_sentence = self.graph_builder.get_root(syntactic_element)

        # Set the sentences where find the speaker
        previous_sentence = self.graph_builder.get_prev_sentence(current_sentence)
        next_sentence = self.graph_builder.get_next_sentence(current_sentence)
        sentences = (current_sentence, previous_sentence, next_sentence)
        # Search over the sentences
        for root in sentences:
            # If the current sentence is the first or the last one of the roots is None.
            if root:
                sentence_terms = self.graph_builder.get_sentence_words(sentence=root)
                for term in sentence_terms:
                    # Search for a reporting verb that is outside of the constituent utterance
                    if term["lemma"] in verbs.reporting and term["utterance"] != constituent_utterance:
                        # Search the subject of the reporting verb.
                        for word, dependency in self.graph_builder.get_dependant_words(term):
                            if dependency_tags.subject(dependency["value"]):
                                return word
        return head_word["speaker"]

    def extract(self, syntactic_element, head_word):
        """ Determines the speaker of a syntactic element of a sentence.

        @param syntactic_element: a word or constituent
        @param head_word: The head word of the constituent
        @return:  meta-speaker(str) or a word(dict)
        """

        if syntactic_element["quoted"]:
            return self._find_speaker(syntactic_element, head_word)
        else:
            return head_word["speaker"]

    #@staticmethod
    #def _check_span(quoted_char_span, mention_char_spam):
    #    """ Check if constituent is inside the quotation
    #    """
    #    return (mention_char_spam[0] >= quoted_char_span[0]) and (mention_char_spam[1] <= quoted_char_span[1])
    #
    #def speech_extractor(self, syntactic_element, head_word):
    #    """Return the speech type of a syntactic element: direct or indirect
    #
    #    @param syntactic_element:
    #    @param head_word:
    #    @return: "direct" or "indirect"
    #    """
    #
    #    root = self.graph_builder.get_root(syntactic_element)
    #    offset = root["begin"]
    #
    #    if head_word["speaker"] and head_word["speaker"] not in self.invalid_speakers:
    #        return "direct"
    #
    #    quotes = [i for i, ltr in enumerate(root["form"]) if ltr == "'"]
    #    if len(quotes) > 1:
    #        for index in range(len(quotes)/2):
    #            if self._check_span(
    #                    quoted_char_span=(offset + quotes[index * 2], offset + quotes[(index * 2) + 1]),
    #                    mention_char_spam=(syntactic_element["begin"], syntactic_element["end"])):
    #                return "indirect"
    #
    #    quotes += [i for i, ltr in enumerate(root["form"]) if ltr == '"']
    #    if len(quotes) > 1:
    #        for index in range(len(quotes)/2):
    #
    #            if self._check_span(
    #                    quoted_char_span=(offset + quotes[index * 2], offset + quotes[(index * 2) + 1]),
    #                    mention_char_spam=(syntactic_element["begin"], syntactic_element["end"])):
    #                return "indirect"
    #    return None