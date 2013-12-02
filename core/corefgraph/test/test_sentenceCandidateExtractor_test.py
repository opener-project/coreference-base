# coding=utf-8

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '2/4/13'


from ..multisieve.core import SentenceCandidateExtractor
from ..graph.graph_builder import BaseGraphBuilder

from unittest import TestCase


class TestSentenceCandidateExtractor(TestCase):
    def setUp(self):
        self.graph_builder = BaseGraphBuilder()
        self.test_graph = self.graph_builder.new_graph()
        self.candidate_extractor = SentenceCandidateExtractor(graph=self.test_graph)
        self.root_node = self.graph_builder.add_sentence(self.test_graph, 0, "test_sentence", "test_sentence", 0)

    def test_validate_np_node_without_filter(self):

        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "NN",
                                                self.root_node)
        self.assertFalse(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                         "a word is fetched as NP candidate")

        test_node = self.graph_builder.add_constituent("an apple", "true", None, "NP", self.test_graph, "mention", True)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "NP candidate is not fetched")

    def test_validate_pronouns_node_without_filter(self):

        test_node = self.graph_builder.add_constituent("an apple", "true", None, "PRP", self.test_graph, "mention",
                                                       "true")
        self.assertFalse(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                         "NP candidate is fetched as PRP")

        # pronoun_pos = ("PRP", "PRP$", "WP", "WP$")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "PRP not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "PRP$",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "PRP$ not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "WP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "WP not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "WP$",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "WP$ not fetched as candidate")

    def test_validate_ne_node_without_filter(self):
        test_node = self.graph_builder.add_constituent("an apple", "true", None, "VP", self.test_graph, "mention",
                                                       "true")
        self.assertFalse(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                         "VP candidate is fetched")
        #"PERSON", "NORP", "FACILITY", "ORGANIZATION", "GPE", "LOCATION", "PRODUCT", "EVENT", "WORK OF ART","LAW",
        # "LANGUAGE", "DATE", "TIME"

        test_node = self.graph_builder.add_constituent("an apple", "true", "PERSON", "VP", self.test_graph, "mention",
                                                       "true")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "PERSON chunk candidate is not fetched")
        test_node = self.graph_builder.add_constituent("an apple", "true", "NORP", "VP", self.test_graph, "mention",
                                                       "true")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "NORP chunk candidate is not fetched")
        test_node = self.graph_builder.add_constituent("an apple", "true", "FACILITY", "VP", self.test_graph, "mention",
                                                       "true")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "FACILITY chunk candidate is not fetched")
        test_node = self.graph_builder.add_constituent("an apple", "true", "GPE", "VP", self.test_graph, "mention",
                                                       "true")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "GPE chunk candidate is not fetched")
        test_node = self.graph_builder.add_constituent("an apple", "true", "LOCATION", "VP", self.test_graph, "mention",
                                                       "true")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "LOCATION chunk candidate is not fetched")
        test_node = self.graph_builder.add_constituent("an apple", "true", "PRODUCT", "VP", self.test_graph, "mention",
                                                       "true")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "PRODUCT chunk candidate is not fetched")
        test_node = self.graph_builder.add_constituent("an apple", "true", "EVENT", "VP", self.test_graph, "mention",
                                                       "true")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "EVENT chunk candidate is not fetched")
        test_node = self.graph_builder.add_constituent("an apple", "true", "WORK OF ART", "VP", self.test_graph,
                                                       "mention", "true")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "WORK OF ART chunk candidate is not fetched")
        test_node = self.graph_builder.add_constituent("an apple", "true", "LAW", "VP", self.test_graph, "mention",
                                                       "true")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "LAW chunk candidate is not fetched")
        test_node = self.graph_builder.add_constituent("an apple", "true", "LANGUAGE", "VP", self.test_graph, "mention",
                                                       "true")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "LANGUAGE chunk candidate is not fetched")
        test_node = self.graph_builder.add_constituent("an apple", "true", "DATE", "VP", self.test_graph, "mention",
                                                       "true")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "DATE chunk candidate is not fetched")
        test_node = self.graph_builder.add_constituent("an apple", "true", "TIME", "VP", self.test_graph, "mention",
                                                       "true")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "TIME chunk candidate is not fetched")

        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "NN",
                                                self.root_node)
        self.assertFalse(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                         "a word is fetched as NE candidate")
        #"PERSON", "NORP", "FACILITY", "ORGANIZATION", "GPE", "LOCATION", "PRODUCT", "EVENT", "WORK OF ART","LAW",
        # "LANGUAGE", "DATE", "TIME"
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "PERSON", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "PERSON WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "NORP", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "NORP WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "FACILITY", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "FACILITY WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "ORGANIZATION",
                                                "PRP", self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "ORGANIZATION WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "GPE", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "GPE WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "LOCATION", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "LOCATION WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "PRODUCT", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "PRODUCT WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "EVENT", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "EVENT WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "WORK OF ART",
                                                "PRP", self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "WORK OF ART WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "LAW", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "LAW WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "LANGUAGE", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "LANGUAGE WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "DATE", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "DATE WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "TIME", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node, filter_candidates=False),
                        "TIME WORD not fetched as candidate")

    def test_validate_node_filter_stopwords(self):
        STOPWORDS = ("there", 'ltd.', 'etc', "'s", 'hmm')
        test_node = self.graph_builder.add_constituent("an apple", "true", "PERSON", "VP", self.test_graph, "mention",
                                                       "true")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node),
                        "PERSON chunk candidate is not fetched")
        for form in STOPWORDS:
            test_node = self.graph_builder.add_constituent(form, "true", "PERSON", "VP", self.test_graph, "mention",
                                                           "true")
            self.assertFalse(self.candidate_extractor._validate_node(mention_candidate=test_node),
                             "NE candidate with {0} form is fetched".format(form))

        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node),
                        "PRP not fetched as candidate")
        for form in STOPWORDS:
            test_node = self.graph_builder.add_word(form, self.test_graph, "1", "apple", "apple", "O", "PRP",
                                                    self.root_node)
            self.assertFalse(self.candidate_extractor._validate_node(mention_candidate=test_node),
                             "PRP candidate with {0} form is fetched ".format(form))

        test_node = self.graph_builder.add_constituent("an apple", "true", None, "NP", self.test_graph, "mention",
                                                       "true")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node),
                        "NP candidate is not fetched")

        for form in STOPWORDS:
            test_node = self.graph_builder.add_constituent(form, "true", None, "NP", self.test_graph, "mention", "true")
            self.assertFalse(self.candidate_extractor._validate_node(mention_candidate=test_node),
                             "NP candidate with {0} is fetched".format(form))

    def test_validate_node_filter_larger_mention(self):
        head_node = self.graph_builder.add_constituent("an apple", True, "PERSON", "VP", self.test_graph, "mention",
                                                       "no_head")
        no_head_node = self.graph_builder.add_constituent("an apple", False, "PERSON", "VP", self.test_graph, "mention",
                                                          "head")
        parent_node = self.graph_builder.add_constituent("an apple", True, "PERSON", "VP", self.test_graph, "mention",
                                                         "parent")
        self.graph_builder.link_syntax_non_terminal(parent=parent_node, child=head_node)
        self.graph_builder.link_syntax_non_terminal(parent=parent_node, child=no_head_node)
        self.candidate_extractor._set_mention_type(parent_node, self.candidate_extractor.proper_mention)
        self.assertFalse(self.candidate_extractor._validate_node(mention_candidate=head_node),
                         "head of a mention is fetched")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=no_head_node),
                        "no head of a mention is not fetched")

    def test_validate_node_filter_invalid_ner(self):
        INVALIDS_NER = ("PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL")
        test_node = self.graph_builder.add_constituent("an apple", "true", "PERSON", "NP", self.test_graph, "mention",
                                                       True)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node),
                        "PERSON chunk candidate is not fetched")
        for ner in INVALIDS_NER:
            test_node = self.graph_builder.add_constituent("an apple", "true", ner, "NP", self.test_graph, "mention",
                                                           True)
            self.assertFalse(self.candidate_extractor._validate_node(mention_candidate=test_node),
                             "NP candidate with invalid NE{0} is fetched".format(ner))

        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node),
                        "PRP not fetched as candidate")

        for ner in INVALIDS_NER:
            test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", ner, "PRP",
                                                    self.root_node)
            self.assertFalse(self.candidate_extractor._validate_node(mention_candidate=test_node),
                             "PRP candidate with invalid NE({0})  form is fetched ".format(ner))

    def test_validate_node_filter_quantifier_or_partitive_expressions(self):
        test_node = self.graph_builder.add_constituent("apples", "true", None, "NP", self.test_graph, "mention", True)
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node),
                        "NP candidate is not fetched")

        test_node = self.graph_builder.add_constituent("million of apples", True, None, "NP", self.test_graph,
                                                       "mention", "millions of apples")
        self.assertFalse(self.candidate_extractor._validate_node(mention_candidate=test_node),
                         "partitive candidate is fetched")

        test_node = self.graph_builder.add_constituent("any apples", True, None, "NP", self.test_graph, "mention",
                                                       "millions of apples")
        self.assertFalse(self.candidate_extractor._validate_node(mention_candidate=test_node),
                         "quantifier candidate is fetched")

    def test_validate_node_filter_pleonastic_it(self):
        self.fail("TODO")

    def test_validate_node_filter_nations_acronyms(self):
        self.fail("TODO")

    def test_validate_node_filter_nationality(self):
        test_node = self.graph_builder.add_constituent("apples", True, None, "NP", self.test_graph, "mention", "apples")
        self.assertTrue(self.candidate_extractor._validate_node(mention_candidate=test_node),
                        "NP candidate is not fetched")

        test_node = self.graph_builder.add_constituent("American", True, None, "NP", self.test_graph, "mention",
                                                       "millions of apples")
        self.assertFalse(self.candidate_extractor._validate_node(mention_candidate=test_node),
                         "nationality candidate is fetched")

    def test_skip_root(self):

        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "ROOT", "SentenceTest", 1)
        conll_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "ROOT", "SentenceTest", 1)
        s_chunk = self.graph_builder.add_constituent("the way of samurai", True, None, "S", self.test_graph, "s",
                                                     "the way of samurai")
        root_chunk = self.graph_builder.add_constituent("dummyRoot", True, None, "ROOT", self.test_graph, "dummyroot",
                                                        "dummyRoot")
        plain_chunk = self.graph_builder.add_constituent("apples", True, None, "NP", self.test_graph, "mention",
                                                         "apples")
        self.graph_builder.link_syntax_non_terminal(root_chunk, s_chunk)
        self.graph_builder.link_syntax_non_terminal(stanford_sentence_root, root_chunk)

        self.graph_builder.link_syntax_non_terminal(conll_sentence_root, s_chunk)
        self.graph_builder.link_syntax_non_terminal(s_chunk, plain_chunk)

        self.assertEqual(s_chunk, self.candidate_extractor._skip_root(stanford_sentence_root), "root not skipped")
        self.assertEqual(s_chunk, self.candidate_extractor._skip_root(conll_sentence_root), "root not skipped")
        self.assertEqual(s_chunk, self.candidate_extractor._skip_root(s_chunk), "no ROOT chunk skipped")

    def test_get_syntactic_parent(self):

        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "ROOT", "SentenceTest", 1)
        root_chunk = self.graph_builder.add_constituent("dummyRoot", True, None, "ROOT", self.test_graph, "dummyroot",
                                                        "dummyRoot")
        s_chunk = self.graph_builder.add_constituent("the way of samurai", True, None, "S", self.test_graph, "s",
                                                     "the way of samurai")
        plain_chunk = self.graph_builder.add_constituent("apples", True, None, "NP", self.test_graph, "mention",
                                                         "apples")

        self.graph_builder.link_syntax_non_terminal(s_chunk, plain_chunk)
        self.graph_builder.link_syntax_non_terminal(root_chunk, s_chunk)
        self.graph_builder.link_syntax_non_terminal(stanford_sentence_root, root_chunk)

        self.assertEqual(s_chunk, self.candidate_extractor.get_syntactic_parent(plain_chunk),
                         "No direct parent fetched")
        self.assertIsNone(self.candidate_extractor.get_syntactic_parent(stanford_sentence_root),
                          "Parent fetched for root")

    def test_get_syntactic_children(self):

        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "ROOT", "SentenceTest", 1)
        root_chunk = self.graph_builder.add_constituent("dummyRoot", True, None, "ROOT", self.test_graph, "dummyroot",
                                                        "dummyRoot")
        s_chunk = self.graph_builder.add_constituent("the way of samurai", True, None, "S", self.test_graph, "s",
                                                     "the way of samurai")
        plain_chunk = self.graph_builder.add_constituent("apples", True, None, "NP", self.test_graph, "mention",
                                                         "apples")

        self.graph_builder.link_syntax_non_terminal(s_chunk, plain_chunk)
        self.graph_builder.link_syntax_non_terminal(root_chunk, s_chunk)
        self.graph_builder.link_syntax_non_terminal(stanford_sentence_root, root_chunk)

        self.assertListEqual([root_chunk], self.candidate_extractor.get_syntactic_children(stanford_sentence_root),
                             "No children fetched")
        self.assertListEqual([], self.candidate_extractor.get_syntactic_children(plain_chunk),
                             "Parent fetched for leaf")

    def test_order_constituent_simple(self):
        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "DummyRoot", "SentenceTest", 1)

        s_chunk = self.graph_builder.add_constituent("He played a song", False, None, "S", self.test_graph,
                                                     "S He played a song", "he played a song")

        he_NP_chunk = self.graph_builder.add_constituent("He", True, None, "NP", self.test_graph, "NP he", "he")
        he_PRP_word = self.graph_builder.add_word("He", self.test_graph, "word_O",
                                                  "PRP He", "he", "O", "PRP", stanford_sentence_root)
        self.graph_builder.set_head(he_PRP_word)

        played_VP_chunk = self.graph_builder.add_constituent("played", True, None, "VP", self.test_graph, "VP played",
                                                             "played")
        played_VBD_word = self.graph_builder.add_word("played", self.test_graph, "word_1",
                                                      "VBD played", "played", "O", "VBD", stanford_sentence_root)

        a_new_song_NP_chunk = self.graph_builder.add_constituent("a new song", False, None, "NP", self.test_graph,
                                                                 "NP a new song", "a new song")
        a_DET_word = self.graph_builder.add_word("a", self.test_graph, "word_1",
                                                 "DET a", "a", "O", "DET", stanford_sentence_root)
        new_JJ_word = self.graph_builder.add_word("new", self.test_graph, "word_2",
                                                  "JJ new", "new", "O", "JJ", stanford_sentence_root)
        song_NN_word = self.graph_builder.add_word("song", self.test_graph, "word_3",
                                                   "NN song", "song", "O", "NN", stanford_sentence_root)

        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.link_syntax_non_terminal(stanford_sentence_root, s_chunk)

        self.graph_builder.link_syntax_non_terminal(he_NP_chunk, he_PRP_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, he_NP_chunk)
        self.graph_builder.set_head(played_VBD_word)

        self.graph_builder.link_syntax_non_terminal(played_VP_chunk, played_VBD_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, played_VP_chunk)

        self.graph_builder.link_syntax_non_terminal(s_chunk, a_new_song_NP_chunk)
        self.graph_builder.link_syntax_non_terminal(a_new_song_NP_chunk, a_DET_word)
        self.graph_builder.link_syntax_non_terminal(a_new_song_NP_chunk, new_JJ_word)
        self.graph_builder.link_syntax_non_terminal(a_new_song_NP_chunk, song_NN_word)
        self.graph_builder.set_head(song_NN_word)

        self.graph_builder.link_syntax_non_terminal(s_chunk, point_word)

        candidatures, next_sentence_candidates = self.candidate_extractor.process_sentence(stanford_sentence_root, [])

        self.assertEqual(len(candidatures), 2)
        self.assertListEqual(candidatures, [([he_NP_chunk], []), ([a_new_song_NP_chunk], [he_NP_chunk])])

    def test_order_constituent_double(self):

        next_sentence_candidates = []

        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "DummyRoot", "SentenceTest", 1)
        s_chunk = self.graph_builder.add_constituent("John is a musician", False, None, "S", self.test_graph,
                                                     "S Jhon is a musician", "jhon is a musician")
        #(NP (NNP John))
        john_NP_chunk = self.graph_builder.add_constituent("John", True, "PERSON", "NP", self.test_graph, "NP John",
                                                           "john")
        john_NNP_word = self.graph_builder.add_word("John", self.test_graph, "word_O",
                                                    "NNP John", "john", "PERSON", "NNP", stanford_sentence_root)
        #(VP (VBZ is)
        is_VP_chunk = self.graph_builder.add_constituent("is", True, None, "VP", self.test_graph, "VP is", "is")
        is_VBZ_word = self.graph_builder.add_word("is", self.test_graph, "word_1",
                                                  "VBZ is", "be", "O", "VBZ", stanford_sentence_root)
        #(NP (DT a) (NN musician)))
        a_musician_NP_chunk = self.graph_builder.add_constituent("a musician", False, None, "NP", self.test_graph,
                                                                 "NP a musician", "a musician")
        a_DET_word = self.graph_builder.add_word("a", self.test_graph, "word_2",
                                                 "DET a", "a", "O", "DET", stanford_sentence_root)
        musician_NN_word = self.graph_builder.add_word("musician", self.test_graph, "word_3",
                                                       "NN musician", "musician", "O", "NN", stanford_sentence_root)
        #(. .)
        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.link_syntax_non_terminal(stanford_sentence_root, s_chunk)

        self.graph_builder.link_syntax_non_terminal(john_NP_chunk, john_NNP_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, john_NP_chunk)
        self.graph_builder.set_head(john_NNP_word)

        self.graph_builder.link_syntax_non_terminal(is_VP_chunk, is_VBZ_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, is_VP_chunk)
        self.graph_builder.set_head(is_VBZ_word)

        self.graph_builder.link_syntax_non_terminal(s_chunk, a_musician_NP_chunk)
        self.graph_builder.link_syntax_non_terminal(a_musician_NP_chunk, a_DET_word)
        self.graph_builder.link_syntax_non_terminal(a_musician_NP_chunk, musician_NN_word)
        self.graph_builder.set_head(musician_NN_word)

        self.graph_builder.link_syntax_non_terminal(s_chunk, point_word)

        candidatures, next_sentence_candidates = self.candidate_extractor.process_sentence(
            stanford_sentence_root, next_sentence_candidates)

        self.assertEqual(len(candidatures), 2)
        self.assertListEqual(candidatures,
                             [([john_NP_chunk], []),
                              ([a_musician_NP_chunk], [john_NP_chunk]),
                              ])

        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "DummyRoot", "SentenceTest", 1)
        s_chunk = self.graph_builder.add_constituent("He played a song", False, None, "S", self.test_graph,
                                                     "S He played a song", "he played a song")

        he_NP_chunk = self.graph_builder.add_constituent("He", True, None, "NP", self.test_graph, "NP he", "he")
        he_PRP_word = self.graph_builder.add_word("He", self.test_graph, "word_O",
                                                  "PRP He", "he", "O", "PRP", stanford_sentence_root)

        played_VP_chunk = self.graph_builder.add_constituent("played", True, None, "VP", self.test_graph, "VP played",
                                                             "played")
        played_VBD_word = self.graph_builder.add_word("played", self.test_graph, "word_1",
                                                      "VBD played", "played", "O", "VBD", stanford_sentence_root)

        a_new_song_NP_chunk = self.graph_builder.add_constituent("a new song", False, None, "NP", self.test_graph,
                                                                 "NP a new song", "a new song")
        a_DET_word = self.graph_builder.add_word("a", self.test_graph, "word_1",
                                                 "DET a", "a", "O", "DET", stanford_sentence_root)
        new_JJ_word = self.graph_builder.add_word("new", self.test_graph, "word_2",
                                                  "JJ new", "new", "O", "JJ", stanford_sentence_root)
        song_NN_word = self.graph_builder.add_word("song", self.test_graph, "word_3",
                                                   "NN song", "song", "O", "NN", stanford_sentence_root)

        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.link_syntax_non_terminal(stanford_sentence_root, s_chunk)

        self.graph_builder.link_syntax_non_terminal(he_NP_chunk, he_PRP_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, he_NP_chunk)
        self.graph_builder.set_head(he_PRP_word)

        self.graph_builder.link_syntax_non_terminal(played_VP_chunk, played_VBD_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, played_VP_chunk)
        self.graph_builder.set_head(played_VBD_word)

        self.graph_builder.link_syntax_non_terminal(s_chunk, a_new_song_NP_chunk)
        self.graph_builder.link_syntax_non_terminal(a_new_song_NP_chunk, a_DET_word)
        self.graph_builder.link_syntax_non_terminal(a_new_song_NP_chunk, new_JJ_word)
        self.graph_builder.link_syntax_non_terminal(a_new_song_NP_chunk, song_NN_word)
        self.graph_builder.set_head(song_NN_word)

        self.graph_builder.link_syntax_non_terminal(s_chunk, point_word)

        candidatures, next_sentence_candidates = self.candidate_extractor.process_sentence(
            stanford_sentence_root, next_sentence_candidates)

        self.assertEqual(len(candidatures), 2)
        self.assertListEqual(candidatures, [([he_NP_chunk], [john_NP_chunk, a_musician_NP_chunk]),
                                            ([a_new_song_NP_chunk], [he_NP_chunk, john_NP_chunk, a_musician_NP_chunk]),
                                            ])

    def test_order_constituent_full(self):

        next_sentence_candidates = []

        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "DummyRoot", "SentenceTest", 1)
        s_chunk = self.graph_builder.add_constituent("John is a musician", False, None, "S", self.test_graph,
                                                     "S John is a musician", "john is a musician")
        #(NP (NNP John))
        john_NP_chunk = self.graph_builder.add_constituent("John", True, "PERSON", "NP", self.test_graph, "NP John",
                                                           "john")
        john_NNP_word = self.graph_builder.add_word("John", self.test_graph, "word_O",
                                                    "NNP John", "john", "PERSON", "NNP", stanford_sentence_root)
        #(VP (VBZ is)
        is_VP_chunk = self.graph_builder.add_constituent("is", True, None, "VP", self.test_graph, "VP is", "is")
        is_VBZ_word = self.graph_builder.add_word("is", self.test_graph, "word_1",
                                                  "VBZ is", "be", "O", "VBZ", stanford_sentence_root)
        #(NP (DT a) (NN musician)))
        a_musician_NP_chunk = self.graph_builder.add_constituent("a musician", False, None, "NP", self.test_graph,
                                                                 "NP a musician", "a musician")
        a_DT_word = self.graph_builder.add_word("a", self.test_graph, "word_2",
                                                "DT a", "a", "O", "DT", stanford_sentence_root)
        musician_NN_word = self.graph_builder.add_word("musician", self.test_graph, "word_3",
                                                       "NN musician", "musician", "O", "NN", stanford_sentence_root)
        #(. .)
        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.link_syntax_non_terminal(stanford_sentence_root, s_chunk)

        self.graph_builder.link_syntax_non_terminal(john_NP_chunk, john_NNP_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, john_NP_chunk)
        self.graph_builder.set_head(john_NNP_word)

        self.graph_builder.link_syntax_non_terminal(is_VP_chunk, is_VBZ_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, is_VP_chunk)
        self.graph_builder.set_head(is_VBZ_word)

        self.graph_builder.link_syntax_non_terminal(s_chunk, a_musician_NP_chunk)
        self.graph_builder.link_syntax_non_terminal(a_musician_NP_chunk, a_DT_word)
        self.graph_builder.link_syntax_non_terminal(a_musician_NP_chunk, musician_NN_word)
        self.graph_builder.set_head(musician_NN_word)

        self.graph_builder.link_syntax_non_terminal(s_chunk, point_word)

        candidatures, next_sentence_candidates = self.candidate_extractor.process_sentence(
            stanford_sentence_root, next_sentence_candidates)

        self.assertEqual(len(candidatures), 2)
        self.assertListEqual(candidatures,
                             [([john_NP_chunk], []),
                              ([a_musician_NP_chunk], [john_NP_chunk]),
                              ])

        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "DummyRoot", "SentenceTest", 1)
        s_chunk = self.graph_builder.add_constituent("He played a song", False, None, "S", self.test_graph,
                                                     "S He played a song", "he played a song")

        he_NP_chunk = self.graph_builder.add_constituent("He", True, None, "NP", self.test_graph, "NP he", "he")
        he_PRP_word = self.graph_builder.add_word("He", self.test_graph, "word_O",
                                                  "PRP He", "he", "O", "PRP", stanford_sentence_root)

        played_VP_chunk = self.graph_builder.add_constituent("played", True, None, "VP", self.test_graph, "VP played",
                                                             "played")
        played_VBD_word = self.graph_builder.add_word("played", self.test_graph, "word_1",
                                                      "VBD played", "played", "O", "VBD", stanford_sentence_root)

        a_new_song_NP_chunk = self.graph_builder.add_constituent("a new song", False, None, "NP", self.test_graph,
                                                                 "NP a new song", "a new song")
        a_DT_word = self.graph_builder.add_word("a", self.test_graph, "word_1",
                                                "DT a", "a", "O", "DT", stanford_sentence_root)
        new_JJ_word = self.graph_builder.add_word("new", self.test_graph, "word_2",
                                                  "JJ new", "new", "O", "JJ", stanford_sentence_root)
        song_NN_word = self.graph_builder.add_word("song", self.test_graph, "word_3",
                                                   "NN song", "song", "O", "NN", stanford_sentence_root)

        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.link_syntax_non_terminal(stanford_sentence_root, s_chunk)

        self.graph_builder.link_syntax_non_terminal(he_NP_chunk, he_PRP_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, he_NP_chunk)
        self.graph_builder.set_head(he_PRP_word)

        self.graph_builder.link_syntax_non_terminal(played_VP_chunk, played_VBD_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, played_VP_chunk)
        self.graph_builder.set_head(played_VBD_word)

        self.graph_builder.link_syntax_non_terminal(s_chunk, a_new_song_NP_chunk)
        self.graph_builder.link_syntax_non_terminal(a_new_song_NP_chunk, a_DT_word)
        self.graph_builder.link_syntax_non_terminal(a_new_song_NP_chunk, new_JJ_word)
        self.graph_builder.link_syntax_non_terminal(a_new_song_NP_chunk, song_NN_word)
        self.graph_builder.set_head(song_NN_word)

        self.graph_builder.link_syntax_non_terminal(s_chunk, point_word)

        candidatures, next_sentence_candidates = self.candidate_extractor.process_sentence(
            stanford_sentence_root, next_sentence_candidates)

        self.assertEqual(len(candidatures), 2)
        self.assertListEqual(candidatures, [([he_NP_chunk], [john_NP_chunk, a_musician_NP_chunk]),
                                            ([a_new_song_NP_chunk], [he_NP_chunk, john_NP_chunk, a_musician_NP_chunk]),
                                            ])
        # ROOT (S
        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "DummyRoot", "SentenceTest", 1)
        s_chunk = self.graph_builder.add_constituent("A girl was listening to the song", False, None, "S",
                                                     self.test_graph, "S A girl was listening to the song",
                                                     "A girl was listening to the song")
        # (NP (DT A) (NN girl))
        a_girl_NP_chunk = self.graph_builder.add_constituent("a girl", False, None, "NP", self.test_graph, "NP a girl",
                                                             "a girl")
        a_DT_word = self.graph_builder.add_word("a", self.test_graph, "word_2",
                                                "DT a", "a", "O", "DT", stanford_sentence_root)
        girl_NN_word = self.graph_builder.add_word("girl", self.test_graph, "word_3",
                                                   "NN girl", "girl", "O", "NN", stanford_sentence_root)
        # (VP (VBD was) (VP (VBG listening)
        was_listening_VP_chunk = self.graph_builder.add_constituent("was listening", True, None, "VP", self.test_graph,
                                                                    "VP was listening", "be listen")
        was_VBD_word = self.graph_builder.add_word("was", self.test_graph, "word_1",
                                                   "VBD is", "be", "O", "VBD", stanford_sentence_root)
        listening_VBG_word = self.graph_builder.add_word("listening", self.test_graph, "word_1",
                                                         "VBG listening", "listen", "O", "VBG", stanford_sentence_root)

        # (PP (TO to) (NP (DT the) (NN song)))))
        to_the_song_PP_chunk = self.graph_builder.add_constituent("to the song", False, None, "PP", self.test_graph,
                                                                  "PP to the song", "to the song")
        to_TO_word = self.graph_builder.add_word("to", self.test_graph, "word_2",
                                                 "TO to", "to", "O", "TO", stanford_sentence_root)
        the_song_NP_chunk = self.graph_builder.add_constituent("the song", False, None, "NP", self.test_graph,
                                                               "NP the song", "the song")
        the_DT_word = self.graph_builder.add_word("the", self.test_graph, "word_2",
                                                  "DT the", "the", "O", "DT", stanford_sentence_root)
        song_NN_word = self.graph_builder.add_word("song", self.test_graph, "word_3",
                                                   "NN song", "song", "O", "DT", stanford_sentence_root)
        # (. .)
        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.link_syntax_non_terminal(stanford_sentence_root, s_chunk)

        self.graph_builder.link_syntax_non_terminal(a_girl_NP_chunk, a_DT_word)
        self.graph_builder.link_syntax_non_terminal(a_girl_NP_chunk, girl_NN_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, a_girl_NP_chunk)
        self.graph_builder.set_head(girl_NN_word)

        self.graph_builder.link_syntax_non_terminal(was_listening_VP_chunk, was_VBD_word)
        self.graph_builder.link_syntax_non_terminal(was_listening_VP_chunk, listening_VBG_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, was_listening_VP_chunk)
        self.graph_builder.set_head(listening_VBG_word)

        self.graph_builder.link_syntax_non_terminal(the_song_NP_chunk, the_DT_word)
        self.graph_builder.link_syntax_non_terminal(the_song_NP_chunk, song_NN_word)
        self.graph_builder.link_syntax_non_terminal(to_the_song_PP_chunk, the_song_NP_chunk)
        self.graph_builder.set_head(song_NN_word)
        self.graph_builder.link_syntax_non_terminal(to_the_song_PP_chunk, to_TO_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, to_the_song_PP_chunk)
        self.graph_builder.set_head(the_song_NP_chunk)

        self.graph_builder.link_syntax_non_terminal(s_chunk, point_word)

        self.graph_builder.set_head(was_listening_VP_chunk)

        candidatures, next_sentence_candidates = self.candidate_extractor.process_sentence(
            stanford_sentence_root, next_sentence_candidates)

        self.assertEqual(len(candidatures), 2)
        self.assertListEqual(candidatures,
                             [([a_girl_NP_chunk], [he_NP_chunk, a_new_song_NP_chunk, john_NP_chunk, a_musician_NP_chunk
                                                   ]),
                              ([the_song_NP_chunk],
                               [a_girl_NP_chunk, he_NP_chunk, a_new_song_NP_chunk, john_NP_chunk, a_musician_NP_chunk
                                ]),
                              ])

        #(ROOT (S
        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "DummyRoot", "SentenceTest", 1)
        s_chunk = self.graph_builder.add_constituent('"It is my favorite", John said to her.', False, None, "S",
                                                     self.test_graph, 'S "It is my favorite", John said to her.',
                                                     '"It is my favorite", John said to her.')
        # (S
        inner_s_chunk = self.graph_builder.add_constituent('"It is my favorite"', False, None, "S", self.test_graph,
                                                           'S "It is my favorite"', '"It is my favorite"')
        # (`` ``)
        open_word = self.graph_builder.add_word("``", self.test_graph, "word_4",
                                                "`` ``", "``", "O", ",", stanford_sentence_root)
        # (NP (PRP It))
        it_NP_chunk = self.graph_builder.add_constituent("It", True, None, "NP", self.test_graph, "NP It", "it")
        it_PRP_word = self.graph_builder.add_word("It", self.test_graph, "word_O",
                                                  "PRP It", "it", "O", "PRP", stanford_sentence_root)

        # (VP (VBZ is)
        is_VP_chunk = self.graph_builder.add_constituent("is", True, None, "VP", self.test_graph, "VP is", "is")
        is_VBZ_word = self.graph_builder.add_word("is", self.test_graph, "word_1",
                                                  "VBZ is", "be", "O", "VBZ", stanford_sentence_root)

        # (NP (PRP$ my) (JJ favorite)))
        my_favorite_NP_chunk = self.graph_builder.add_constituent("my favorite", False, None, "NP", self.test_graph,
                                                                  "NP my favorite", "my favorite")
        my_PRP_word = self.graph_builder.add_word("my", self.test_graph, "word_2",
                                                  "PRP$ my", "my", "O", "PRP$", stanford_sentence_root)
        favorite_JJ_word = self.graph_builder.add_word("favorite", self.test_graph, "word_3",
                                                       "JJ favorite", "favorite", "O", "JJ", stanford_sentence_root)

        # ('' '')
        close_word = self.graph_builder.add_word("''", self.test_graph, "word_4",
                                                 "'' ''", "''", "O", ",", stanford_sentence_root)
        # )

        # (, ,)

        coma_word = self.graph_builder.add_word(",", self.test_graph, "word_4",
                                                ", ,", ",", "O", ",", stanford_sentence_root)
        # (NP (NNP John))
        john_NP_chunk = self.graph_builder.add_constituent("John", True, "PERSON", "NP", self.test_graph, "NP John",
                                                           "john")
        john_NNP_word = self.graph_builder.add_word("John", self.test_graph, "word_O",
                                                    "NNP John", "john", "PERSON", "NNP", stanford_sentence_root)
        # (VP (VBD said)
        said_VP_chunk = self.graph_builder.add_constituent("said", True, None, "VP", self.test_graph, "VP said", "said")
        said_VBD_word = self.graph_builder.add_word("said", self.test_graph, "word_1",
                                                    "VBD said", "say", "O", "VBD", stanford_sentence_root)
        # (PP (TO to) (NP (PRP her))))
        to_her_PP_chunk = self.graph_builder.add_constituent("to her", False, None, "PP", self.test_graph, "PP to her",
                                                             "to the song")
        to_TO_word = self.graph_builder.add_word("to", self.test_graph, "word_2",
                                                 "TO to", "to", "O", "TO", stanford_sentence_root)
        her_NP_chunk = self.graph_builder.add_constituent("her", False, None, "NP", self.test_graph, "NP her", "her")
        her_PRP_word = self.graph_builder.add_word("her", self.test_graph, "word_2",
                                                   "PRP her", "her", "O", "PRP", stanford_sentence_root)

        # (. .))
        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.link_syntax_non_terminal(stanford_sentence_root, s_chunk)

        self.graph_builder.link_syntax_non_terminal(inner_s_chunk, open_word)

        self.graph_builder.link_syntax_non_terminal(it_NP_chunk, it_PRP_word)
        self.graph_builder.link_syntax_non_terminal(inner_s_chunk, it_NP_chunk)
        self.graph_builder.set_head(it_PRP_word)

        self.graph_builder.link_syntax_non_terminal(is_VBZ_word, is_VP_chunk)
        self.graph_builder.link_syntax_non_terminal(inner_s_chunk, is_VBZ_word)
        self.graph_builder.set_head(is_VBZ_word)

        self.graph_builder.link_syntax_non_terminal(my_favorite_NP_chunk, my_PRP_word)
        self.graph_builder.link_syntax_non_terminal(my_favorite_NP_chunk, favorite_JJ_word)
        self.graph_builder.link_syntax_non_terminal(inner_s_chunk, my_favorite_NP_chunk)
        self.graph_builder.set_head(favorite_JJ_word)

        self.graph_builder.link_syntax_non_terminal(inner_s_chunk, close_word)

        self.graph_builder.link_syntax_non_terminal(s_chunk, inner_s_chunk)

        self.graph_builder.link_syntax_non_terminal(s_chunk, coma_word)

        self.graph_builder.link_syntax_non_terminal(john_NP_chunk, john_NNP_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, john_NP_chunk)
        self.graph_builder.set_head(john_NNP_word)

        self.graph_builder.link_syntax_non_terminal(said_VP_chunk, said_VBD_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, said_VP_chunk)
        self.graph_builder.set_head(said_VBD_word)

        self.graph_builder.link_syntax_non_terminal(her_NP_chunk, her_PRP_word)
        self.graph_builder.link_syntax_non_terminal(to_her_PP_chunk, her_NP_chunk)
        self.graph_builder.set_head(her_PRP_word)
        self.graph_builder.link_syntax_non_terminal(to_her_PP_chunk, to_TO_word)
        self.graph_builder.set_head(her_NP_chunk)
        self.graph_builder.link_syntax_non_terminal(s_chunk, to_her_PP_chunk)

        self.graph_builder.link_syntax_non_terminal(s_chunk, point_word)
        self.graph_builder.set_head(said_VP_chunk)

        candidatures, next_sentence_candidates = self.candidate_extractor.process_sentence(
            stanford_sentence_root, next_sentence_candidates)

        #self.assertEqual(len(candidatures), 5)
        self.assertListEqual(candidatures, [([it_NP_chunk], [a_girl_NP_chunk, the_song_NP_chunk, he_NP_chunk,
                                                             a_new_song_NP_chunk, john_NP_chunk, a_musician_NP_chunk]),
                                            ([my_favorite_NP_chunk], [it_NP_chunk, a_girl_NP_chunk, the_song_NP_chunk,
                                                                      he_NP_chunk, a_new_song_NP_chunk, john_NP_chunk,
                                                                      a_musician_NP_chunk]),
                                            ([my_PRP_word], [it_NP_chunk, my_favorite_NP_chunk, a_girl_NP_chunk,
                                                             the_song_NP_chunk, he_NP_chunk, a_new_song_NP_chunk,
                                                             john_NP_chunk, a_musician_NP_chunk]),
                                            ([john_NP_chunk], [it_NP_chunk, my_favorite_NP_chunk, my_PRP_word,
                                                               a_girl_NP_chunk, the_song_NP_chunk, he_NP_chunk,
                                                               a_new_song_NP_chunk, john_NP_chunk,
                                                               a_musician_NP_chunk]),
                                            ([her_NP_chunk], [john_NP_chunk, it_NP_chunk, my_favorite_NP_chunk,
                                                              my_PRP_word, a_girl_NP_chunk, the_song_NP_chunk,
                                                              he_NP_chunk, a_new_song_NP_chunk, john_NP_chunk,
                                                              a_musician_NP_chunk])
                                            ])

    def test_process_sentence_simple(self):
        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "DummyRoot", "SentenceTest", 1)

        s_chunk = self.graph_builder.add_constituent("He played a song", False, None, "S", self.test_graph,
                                                     "S He played a song", "he played a song")

        he_NP_chunk = self.graph_builder.add_constituent("He", True, None, "NP", self.test_graph, "NP he", "he")
        he_PRP_word = self.graph_builder.add_word("He", self.test_graph, "word_O",
                                                  "PRP He", "he", "O", "PRP", stanford_sentence_root)
        self.graph_builder.set_head(he_PRP_word)

        played_VP_chunk = self.graph_builder.add_constituent("played", True, None, "VP", self.test_graph, "VP played",
                                                             "played")
        played_VBD_word = self.graph_builder.add_word("played", self.test_graph, "word_1",
                                                      "VBD played", "played", "O", "VBD", stanford_sentence_root)

        a_new_song_NP_chunk = self.graph_builder.add_constituent("a new song", False, None, "NP", self.test_graph,
                                                                 "NP a new song", "a new song")
        a_DET_word = self.graph_builder.add_word("a", self.test_graph, "word_1",
                                                 "DET a", "a", "O", "DET", stanford_sentence_root)
        new_JJ_word = self.graph_builder.add_word("new", self.test_graph, "word_2",
                                                  "JJ new", "new", "O", "JJ", stanford_sentence_root)
        song_NN_word = self.graph_builder.add_word("song", self.test_graph, "word_3",
                                                   "NN song", "song", "O", "NN", stanford_sentence_root)

        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.link_syntax_non_terminal(stanford_sentence_root, s_chunk)

        self.graph_builder.link_syntax_non_terminal(he_NP_chunk, he_PRP_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, he_NP_chunk)
        self.graph_builder.set_head(played_VBD_word)

        self.graph_builder.link_syntax_non_terminal(played_VP_chunk, played_VBD_word)
        self.graph_builder.link_syntax_non_terminal(s_chunk, played_VP_chunk)

        self.graph_builder.link_syntax_non_terminal(s_chunk, a_new_song_NP_chunk)
        self.graph_builder.link_syntax_non_terminal(a_new_song_NP_chunk, a_DET_word)
        self.graph_builder.link_syntax_non_terminal(a_new_song_NP_chunk, new_JJ_word)
        self.graph_builder.link_syntax_non_terminal(a_new_song_NP_chunk, song_NN_word)
        self.graph_builder.set_head(song_NN_word)

        self.graph_builder.link_syntax_non_terminal(s_chunk, point_word)

        candidatures, next_sentence_candidates = self.candidate_extractor.process_sentence(stanford_sentence_root, [])

        self.assertEqual(len(candidatures), 2)
        self.assertListEqual(candidatures, [([he_NP_chunk], []), ([a_new_song_NP_chunk], [he_NP_chunk])])

    def test_process(self):
        self.fail("TODO")
