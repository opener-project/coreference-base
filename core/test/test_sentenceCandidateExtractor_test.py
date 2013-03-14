from __future__ import unicode_literals
from unittest import TestCase
from multisieve.core import SentenceCandidateExtractor
from graph.graph_builder import BaseGraphBuilder

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '2/4/13'


class TestSentenceCandidateExtractor(TestCase):
    def setUp(self):
        self.graph_builder = BaseGraphBuilder()
        self.test_graph = self.graph_builder.new_graph()
        self.candidate_extractor = SentenceCandidateExtractor(graph=self.test_graph)
        self.root_node = self.graph_builder.add_sentence(self.test_graph, 0, "test_sentence", "test_sentence", 0)

    def test_validate_np_node_without_filter(self):

        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "NN",
                                                self.root_node)
        self.assertFalse(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                         "a word is fetched as NP candidate")

        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", True, None, "NP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "NP candidate is not fetched")

    def test_validate_pronouns_node_without_filter(self):

        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", None, "PRP")
        self.assertFalse(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                         "NP candidate is fetched as PRP")

        # pronoun_pos = ("PRP", "PRP$", "WP", "WP$")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "PRP not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "PRP$",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "PRP$ not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "WP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "WP not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "WP$",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "WP$ not fetched as candidate")

    def test_validate_ne_node_without_filter(self):
        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", None, "VP")
        self.assertFalse(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                         "VP candidate is fetched")
        #"PERSON", "NORP", "FACILITY", "ORGANIZATION", "GPE", "LOCATION", "PRODUCT", "EVENT", "WORK OF ART","LAW",
        # "LANGUAGE", "DATE", "TIME"

        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", "PERSON", "VP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "PERSON chunk candidate is not fetched")
        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", "NORP", "VP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "NORP chunk candidate is not fetched")
        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", "FACILITY",
                                                 "VP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "FACILITY chunk candidate is not fetched")
        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", "GPE", "VP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "GPE chunk candidate is not fetched")
        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", "LOCATION",
                                                 "VP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "LOCATION chunk candidate is not fetched")
        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", "PRODUCT",
                                                 "VP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "PRODUCT chunk candidate is not fetched")
        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", "EVENT", "VP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "EVENT chunk candidate is not fetched")
        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", "WORK OF ART",
                                                 "VP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "WORK OF ART chunk candidate is not fetched")
        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", "LAW", "VP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "LAW chunk candidate is not fetched")
        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", "LANGUAGE",
                                                 "VP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "LANGUAGE chunk candidate is not fetched")
        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", "DATE", "VP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "DATE chunk candidate is not fetched")
        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", "TIME", "VP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "TIME chunk candidate is not fetched")

        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "NN",
                                                self.root_node)
        self.assertFalse(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                         "a word is fetched as NE candidate")
        #"PERSON", "NORP", "FACILITY", "ORGANIZATION", "GPE", "LOCATION", "PRODUCT", "EVENT", "WORK OF ART","LAW",
        # "LANGUAGE", "DATE", "TIME"
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "PERSON", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "PERSON WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "NORP", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "NORP WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "FACILITY", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "FACILITY WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "ORGANIZATION",
                                                "PRP", self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "ORGANIZATION WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "GPE", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "GPE WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "LOCATION", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "LOCATION WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "PRODUCT", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "PRODUCT WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "EVENT", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "EVENT WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "WORK OF ART",
                                                "PRP", self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "WORK OF ART WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "LAW", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "LAW WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "LANGUAGE", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "LANGUAGE WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "DATE", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "DATE WORD not fetched as candidate")
        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "TIME", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node, filter_candidates=False),
                        "TIME WORD not fetched as candidate")

    def test_validate_node_filter_stopwords(self):
        STOPWORDS = ("there", 'ltd.', 'etc', "'s", 'hmm')
        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", "PERSON", "VP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node),
                        "PERSON chunk candidate is not fetched")
        for form in STOPWORDS:
            test_node = self.graph_builder.add_chunk(form, self.test_graph, "true", "mention", "true", "PERSON", "VP")
            self.assertFalse(self.candidate_extractor.validate_node(mention_candidate=test_node),
                             "NE candidate with {0} form is fetched".format(form))

        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node),
                        "PRP not fetched as candidate")
        for form in STOPWORDS:
            test_node = self.graph_builder.add_word(form, self.test_graph, "1", "apple", "apple", "O", "PRP",
                                                    self.root_node)
            self.assertFalse(self.candidate_extractor.validate_node(mention_candidate=test_node),
                             "PRP candidate with {0} form is fetched ".format(form))

        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", "true", None, "NP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node),
                        "NP candidate is not fetched")

        for form in STOPWORDS:
            test_node = self.graph_builder.add_chunk(form, self.test_graph, "true", "mention", "true", None, "NP")
            self.assertFalse(self.candidate_extractor.validate_node(mention_candidate=test_node),
                             "NP candidate with {0} is fetched".format(form))

    def test_validate_node_filter_larger_mention(self):
        head_node = self.graph_builder.add_chunk("an apple", self.test_graph, True, "mention", "no_head", "PERSON",
                                                 "VP")
        no_head_node = self.graph_builder.add_chunk("an apple", self.test_graph, False, "mention", "head", "PERSON",
                                                    "VP")
        parent_node = self.graph_builder.add_chunk("an apple", self.test_graph, True, "mention", "parent", "PERSON",
                                                   "VP")
        self.graph_builder.syntax_tree_link(child=head_node, parent=parent_node)
        self.graph_builder.syntax_tree_link(child=no_head_node, parent=parent_node)
        self.candidate_extractor.set_mention_type(parent_node, self.candidate_extractor.proper_mention)
        self.assertFalse(self.candidate_extractor.validate_node(mention_candidate=head_node),
                         "head of a mention is fetched")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=no_head_node),
                        "no head of a mention is not fetched")

    def test_validate_node_filter_invalid_ner(self):
        INVALIDS_NER = ("PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL")
        test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", True, "PERSON", "NP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node),
                        "PERSON chunk candidate is not fetched")
        for ner in INVALIDS_NER:
            test_node = self.graph_builder.add_chunk("an apple", self.test_graph, "true", "mention", True, ner, "NP")
            self.assertFalse(self.candidate_extractor.validate_node(mention_candidate=test_node),
                             "NP candidate with invalid NE{0} is fetched".format(ner))

        test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", "O", "PRP",
                                                self.root_node)
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node),
                        "PRP not fetched as candidate")

        for ner in INVALIDS_NER:
            test_node = self.graph_builder.add_word("an apple", self.test_graph, "1", "apple", "apple", ner, "PRP",
                                                    self.root_node)
            self.assertFalse(self.candidate_extractor.validate_node(mention_candidate=test_node),
                             "PRP candidate with invalid NE({0})  form is fetched ".format(ner))

    def test_validate_node_filter_quantifier_or_partitive_expressions(self):
        test_node = self.graph_builder.add_chunk("apples", self.test_graph, "true", "mention", True, None, "NP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node),
                        "NP candidate is not fetched")

        test_node = self.graph_builder.add_chunk("million of apples", self.test_graph, True, "mention",
                                                 "millions of apples", None, "NP")
        self.assertFalse(self.candidate_extractor.validate_node(mention_candidate=test_node),
                         "partitive candidate is fetched")

        test_node = self.graph_builder.add_chunk("any apples", self.test_graph, True, "mention", "millions of apples",
                                                 None, "NP")
        self.assertFalse(self.candidate_extractor.validate_node(mention_candidate=test_node),
                         "quantifier candidate is fetched")

    def test_validate_node_filter_pleonastic_it(self):
        self.fail("TODO")

    def test_validate_node_filter_nations_acronyms(self):
        self.fail("TODO")

    def test_validate_node_filter_nationality(self):
        test_node = self.graph_builder.add_chunk("apples", self.test_graph, True, "mention", "apples", None, "NP")
        self.assertTrue(self.candidate_extractor.validate_node(mention_candidate=test_node),
                        "NP candidate is not fetched")

        test_node = self.graph_builder.add_chunk("American", self.test_graph, True, "mention", "millions of apples",
                                                 None, "NP")
        self.assertFalse(self.candidate_extractor.validate_node(mention_candidate=test_node),
                         "nationality candidate is fetched")

    def test_skip_root(self):

        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "ROOT", "SentenceTest", 1)
        conll_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "ROOT", "SentenceTest", 1)
        s_chunk = self.graph_builder.add_chunk("the way of samurai", self.test_graph, True, "s", "the way of samurai",
                                               None, "S")
        root_chunk = self.graph_builder.add_chunk("dummyRoot", self.test_graph, True, "dummyroot", "dummyRoot", None,
                                                  "ROOT")
        plain_chunk = self.graph_builder.add_chunk("apples", self.test_graph, True, "mention", "apples", None, "NP")
        self.graph_builder.syntax_tree_link(s_chunk, root_chunk)
        self.graph_builder.syntax_tree_link(root_chunk, stanford_sentence_root)

        self.graph_builder.syntax_tree_link(s_chunk, conll_sentence_root)
        self.graph_builder.syntax_tree_link(plain_chunk, s_chunk)

        self.assertEqual(s_chunk, self.candidate_extractor.skip_root(stanford_sentence_root), "root not skipped")
        self.assertEqual(s_chunk, self.candidate_extractor.skip_root(conll_sentence_root), "root not skipped")
        self.assertEqual(s_chunk, self.candidate_extractor.skip_root(s_chunk), "no ROOT chunk skipped")

    def test_get_syntactic_parent(self):

        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "ROOT", "SentenceTest", 1)
        root_chunk = self.graph_builder.add_chunk("dummyRoot", self.test_graph, True, "dummyroot", "dummyRoot", None,
                                                  "ROOT")
        s_chunk = self.graph_builder.add_chunk("the way of samurai", self.test_graph, True, "s", "the way of samurai",
                                               None, "S")
        plain_chunk = self.graph_builder.add_chunk("apples", self.test_graph, True, "mention", "apples", None, "NP")

        self.graph_builder.syntax_tree_link(plain_chunk, s_chunk)
        self.graph_builder.syntax_tree_link(s_chunk, root_chunk)
        self.graph_builder.syntax_tree_link(root_chunk, stanford_sentence_root)

        self.assertEqual(s_chunk, self.candidate_extractor.get_syntactic_parent(plain_chunk),
                         "No direct parent fetched")
        self.assertIsNone(self.candidate_extractor.get_syntactic_parent(stanford_sentence_root),
                          "Parent fetched for root")

    def test_get_syntactic_children(self):

        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "ROOT", "SentenceTest", 1)
        root_chunk = self.graph_builder.add_chunk("dummyRoot", self.test_graph, True, "dummyroot", "dummyRoot", None,
                                                  "ROOT")
        s_chunk = self.graph_builder.add_chunk("the way of samurai", self.test_graph, True, "s", "the way of samurai",
                                               None, "S")
        plain_chunk = self.graph_builder.add_chunk("apples", self.test_graph, True, "mention", "apples", None, "NP")

        self.graph_builder.syntax_tree_link(plain_chunk, s_chunk)
        self.graph_builder.syntax_tree_link(s_chunk, root_chunk)
        self.graph_builder.syntax_tree_link(root_chunk, stanford_sentence_root)

        self.assertListEqual([root_chunk], self.candidate_extractor.get_syntactic_children(stanford_sentence_root),
                             "No children fetched")
        self.assertListEqual([], self.candidate_extractor.get_syntactic_children(plain_chunk),
                             "Parent fetched for leaf")

    def test_order_constituent_simple(self):
        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "DummyRoot", "SentenceTest", 1)

        s_chunk = self.graph_builder.add_chunk("He played a song", self.test_graph, False,
                                               "S He played a song", "he played a song", None, "S")

        he_NP_chunk = self.graph_builder.add_chunk("He", self.test_graph, True,
                                                   "NP he", "he", None, "NP")
        he_PRP_word = self.graph_builder.add_word("He", self.test_graph, "word_O",
                                                  "PRP He", "he", "O", "PRP", stanford_sentence_root)
        self.graph_builder.set_head(he_PRP_word)

        played_VP_chunk = self.graph_builder.add_chunk("played", self.test_graph, True,
                                                       "VP played", "played", None, "VP")
        played_VBD_word = self.graph_builder.add_word("played", self.test_graph, "word_1",
                                                      "VBD played", "played", "O", "VBD", stanford_sentence_root)

        a_new_song_NP_chunk = self.graph_builder.add_chunk("a new song", self.test_graph, False,
                                                           "NP a new song", "a new song", None, "NP")
        a_DET_word = self.graph_builder.add_word("a", self.test_graph, "word_1",
                                                 "DET a", "a", "O", "DET", stanford_sentence_root)
        new_JJ_word = self.graph_builder.add_word("new", self.test_graph, "word_2",
                                                  "JJ new", "new", "O", "JJ", stanford_sentence_root)
        song_NN_word = self.graph_builder.add_word("song", self.test_graph, "word_3",
                                                   "NN song", "song", "O", "NN", stanford_sentence_root)

        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.syntax_tree_link(s_chunk, stanford_sentence_root)

        self.graph_builder.syntax_tree_link(he_PRP_word, he_NP_chunk)
        self.graph_builder.syntax_tree_link(he_NP_chunk, s_chunk)
        self.graph_builder.set_head(played_VBD_word)

        self.graph_builder.syntax_tree_link(played_VBD_word, played_VP_chunk)
        self.graph_builder.syntax_tree_link(played_VP_chunk, s_chunk)

        self.graph_builder.syntax_tree_link(a_new_song_NP_chunk, s_chunk)
        self.graph_builder.syntax_tree_link(a_DET_word, a_new_song_NP_chunk)
        self.graph_builder.syntax_tree_link(new_JJ_word, a_new_song_NP_chunk)
        self.graph_builder.syntax_tree_link(song_NN_word, a_new_song_NP_chunk)
        self.graph_builder.set_head(song_NN_word)

        self.graph_builder.syntax_tree_link(point_word, s_chunk)

        candidatures, next_sentence_candidates = self.candidate_extractor.process_sentence(stanford_sentence_root, [])

        self.assertEqual(len(candidatures), 2)
        self.assertListEqual(candidatures, [([he_NP_chunk], []), ([a_new_song_NP_chunk], [he_NP_chunk])])

    def test_order_constituent_double(self):

        next_sentence_candidates = []

        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "DummyRoot", "SentenceTest", 1)
        s_chunk = self.graph_builder.add_chunk("John is a musician", self.test_graph, False,
                                               "S Jhon is a musician", "jhon is a musician", None, "S")
        #(NP (NNP John))
        john_NP_chunk = self.graph_builder.add_chunk("John", self.test_graph, True,
                                                     "NP John", "john", "PERSON", "NP")
        john_NNP_word = self.graph_builder.add_word("John", self.test_graph, "word_O",
                                                    "NNP John", "john", "PERSON", "NNP", stanford_sentence_root)
        #(VP (VBZ is)
        is_VP_chunk = self.graph_builder.add_chunk("is", self.test_graph, True,
                                                   "VP is", "is", None, "VP")
        is_VBZ_word = self.graph_builder.add_word("is", self.test_graph, "word_1",
                                                  "VBZ is", "be", "O", "VBZ", stanford_sentence_root)
        #(NP (DT a) (NN musician)))
        a_musician_NP_chunk = self.graph_builder.add_chunk("a musician", self.test_graph, False,
                                                           "NP a musician", "a musician", None, "NP")
        a_DET_word = self.graph_builder.add_word("a", self.test_graph, "word_2",
                                                 "DET a", "a", "O", "DET", stanford_sentence_root)
        musician_NN_word = self.graph_builder.add_word("musician", self.test_graph, "word_3",
                                                       "NN musician", "musician", "O", "NN", stanford_sentence_root)
        #(. .)
        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.syntax_tree_link(s_chunk, stanford_sentence_root)

        self.graph_builder.syntax_tree_link(john_NNP_word, john_NP_chunk)
        self.graph_builder.syntax_tree_link(john_NP_chunk, s_chunk)
        self.graph_builder.set_head(john_NNP_word)

        self.graph_builder.syntax_tree_link(is_VBZ_word, is_VP_chunk)
        self.graph_builder.syntax_tree_link(is_VP_chunk, s_chunk)
        self.graph_builder.set_head(is_VBZ_word)

        self.graph_builder.syntax_tree_link(a_musician_NP_chunk, s_chunk)
        self.graph_builder.syntax_tree_link(a_DET_word, a_musician_NP_chunk)
        self.graph_builder.syntax_tree_link(musician_NN_word, a_musician_NP_chunk)
        self.graph_builder.set_head(musician_NN_word)

        self.graph_builder.syntax_tree_link(point_word, s_chunk)

        candidatures, next_sentence_candidates = self.candidate_extractor.process_sentence(
            stanford_sentence_root, next_sentence_candidates)

        self.assertEqual(len(candidatures), 2)
        self.assertListEqual(candidatures,
                             [([john_NP_chunk], []),
                              ([a_musician_NP_chunk], [john_NP_chunk]),
                              ])

        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "DummyRoot", "SentenceTest", 1)
        s_chunk = self.graph_builder.add_chunk("He played a song", self.test_graph, False,
                                               "S He played a song", "he played a song", None, "S")

        he_NP_chunk = self.graph_builder.add_chunk("He", self.test_graph, True,
                                                   "NP he", "he", None, "NP")
        he_PRP_word = self.graph_builder.add_word("He", self.test_graph, "word_O",
                                                  "PRP He", "he", "O", "PRP", stanford_sentence_root)

        played_VP_chunk = self.graph_builder.add_chunk("played", self.test_graph, True,
                                                       "VP played", "played", None, "VP")
        played_VBD_word = self.graph_builder.add_word("played", self.test_graph, "word_1",
                                                      "VBD played", "played", "O", "VBD", stanford_sentence_root)

        a_new_song_NP_chunk = self.graph_builder.add_chunk("a new song", self.test_graph, False,
                                                           "NP a new song", "a new song", None, "NP")
        a_DET_word = self.graph_builder.add_word("a", self.test_graph, "word_1",
                                                 "DET a", "a", "O", "DET", stanford_sentence_root)
        new_JJ_word = self.graph_builder.add_word("new", self.test_graph, "word_2",
                                                  "JJ new", "new", "O", "JJ", stanford_sentence_root)
        song_NN_word = self.graph_builder.add_word("song", self.test_graph, "word_3",
                                                   "NN song", "song", "O", "NN", stanford_sentence_root)

        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.syntax_tree_link(s_chunk, stanford_sentence_root)

        self.graph_builder.syntax_tree_link(he_PRP_word, he_NP_chunk)
        self.graph_builder.syntax_tree_link(he_NP_chunk, s_chunk)
        self.graph_builder.set_head(he_PRP_word)

        self.graph_builder.syntax_tree_link(played_VBD_word, played_VP_chunk)
        self.graph_builder.syntax_tree_link(played_VP_chunk, s_chunk)
        self.graph_builder.set_head(played_VBD_word)

        self.graph_builder.syntax_tree_link(a_new_song_NP_chunk, s_chunk)
        self.graph_builder.syntax_tree_link(a_DET_word, a_new_song_NP_chunk)
        self.graph_builder.syntax_tree_link(new_JJ_word, a_new_song_NP_chunk)
        self.graph_builder.syntax_tree_link(song_NN_word, a_new_song_NP_chunk)
        self.graph_builder.set_head(song_NN_word)

        self.graph_builder.syntax_tree_link(point_word, s_chunk)

        candidatures, next_sentence_candidates = self.candidate_extractor.process_sentence(
            stanford_sentence_root, next_sentence_candidates)

        self.assertEqual(len(candidatures), 2)
        self.assertListEqual(candidatures, [([he_NP_chunk], [john_NP_chunk, a_musician_NP_chunk]),
                                            ([a_new_song_NP_chunk], [he_NP_chunk, john_NP_chunk, a_musician_NP_chunk]),
                                            ])

    def test_order_constituent_full(self):

        next_sentence_candidates = []

        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "DummyRoot", "SentenceTest", 1)
        s_chunk = self.graph_builder.add_chunk("John is a musician", self.test_graph, False,
                                               "S John is a musician", "john is a musician", None, "S")
        #(NP (NNP John))
        john_NP_chunk = self.graph_builder.add_chunk("John", self.test_graph, True,
                                                     "NP John", "john", "PERSON", "NP")
        john_NNP_word = self.graph_builder.add_word("John", self.test_graph, "word_O",
                                                    "NNP John", "john", "PERSON", "NNP", stanford_sentence_root)
        #(VP (VBZ is)
        is_VP_chunk = self.graph_builder.add_chunk("is", self.test_graph, True,
                                                   "VP is", "is", None, "VP")
        is_VBZ_word = self.graph_builder.add_word("is", self.test_graph, "word_1",
                                                  "VBZ is", "be", "O", "VBZ", stanford_sentence_root)
        #(NP (DT a) (NN musician)))
        a_musician_NP_chunk = self.graph_builder.add_chunk("a musician", self.test_graph, False,
                                                           "NP a musician", "a musician", None, "NP")
        a_DT_word = self.graph_builder.add_word("a", self.test_graph, "word_2",
                                                "DT a", "a", "O", "DT", stanford_sentence_root)
        musician_NN_word = self.graph_builder.add_word("musician", self.test_graph, "word_3",
                                                       "NN musician", "musician", "O", "NN", stanford_sentence_root)
        #(. .)
        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.syntax_tree_link(s_chunk, stanford_sentence_root)

        self.graph_builder.syntax_tree_link(john_NNP_word, john_NP_chunk)
        self.graph_builder.syntax_tree_link(john_NP_chunk, s_chunk)
        self.graph_builder.set_head(john_NNP_word)

        self.graph_builder.syntax_tree_link(is_VBZ_word, is_VP_chunk)
        self.graph_builder.syntax_tree_link(is_VP_chunk, s_chunk)
        self.graph_builder.set_head(is_VBZ_word)

        self.graph_builder.syntax_tree_link(a_musician_NP_chunk, s_chunk)
        self.graph_builder.syntax_tree_link(a_DT_word, a_musician_NP_chunk)
        self.graph_builder.syntax_tree_link(musician_NN_word, a_musician_NP_chunk)
        self.graph_builder.set_head(musician_NN_word)

        self.graph_builder.syntax_tree_link(point_word, s_chunk)

        candidatures, next_sentence_candidates = self.candidate_extractor.process_sentence(
            stanford_sentence_root, next_sentence_candidates)

        self.assertEqual(len(candidatures), 2)
        self.assertListEqual(candidatures,
                             [([john_NP_chunk], []),
                              ([a_musician_NP_chunk], [john_NP_chunk]),
                              ])

        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "DummyRoot", "SentenceTest", 1)
        s_chunk = self.graph_builder.add_chunk("He played a song", self.test_graph, False,
                                               "S He played a song", "he played a song", None, "S")

        he_NP_chunk = self.graph_builder.add_chunk("He", self.test_graph, True,
                                                   "NP he", "he", None, "NP")
        he_PRP_word = self.graph_builder.add_word("He", self.test_graph, "word_O",
                                                  "PRP He", "he", "O", "PRP", stanford_sentence_root)

        played_VP_chunk = self.graph_builder.add_chunk("played", self.test_graph, True,
                                                       "VP played", "played", None, "VP")
        played_VBD_word = self.graph_builder.add_word("played", self.test_graph, "word_1",
                                                      "VBD played", "played", "O", "VBD", stanford_sentence_root)

        a_new_song_NP_chunk = self.graph_builder.add_chunk("a new song", self.test_graph, False,
                                                           "NP a new song", "a new song", None, "NP")
        a_DT_word = self.graph_builder.add_word("a", self.test_graph, "word_1",
                                                "DT a", "a", "O", "DT", stanford_sentence_root)
        new_JJ_word = self.graph_builder.add_word("new", self.test_graph, "word_2",
                                                  "JJ new", "new", "O", "JJ", stanford_sentence_root)
        song_NN_word = self.graph_builder.add_word("song", self.test_graph, "word_3",
                                                   "NN song", "song", "O", "NN", stanford_sentence_root)

        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.syntax_tree_link(s_chunk, stanford_sentence_root)

        self.graph_builder.syntax_tree_link(he_PRP_word, he_NP_chunk)
        self.graph_builder.syntax_tree_link(he_NP_chunk, s_chunk)
        self.graph_builder.set_head(he_PRP_word)

        self.graph_builder.syntax_tree_link(played_VBD_word, played_VP_chunk)
        self.graph_builder.syntax_tree_link(played_VP_chunk, s_chunk)
        self.graph_builder.set_head(played_VBD_word)

        self.graph_builder.syntax_tree_link(a_new_song_NP_chunk, s_chunk)
        self.graph_builder.syntax_tree_link(a_DT_word, a_new_song_NP_chunk)
        self.graph_builder.syntax_tree_link(new_JJ_word, a_new_song_NP_chunk)
        self.graph_builder.syntax_tree_link(song_NN_word, a_new_song_NP_chunk)
        self.graph_builder.set_head(song_NN_word)

        self.graph_builder.syntax_tree_link(point_word, s_chunk)

        candidatures, next_sentence_candidates = self.candidate_extractor.process_sentence(
            stanford_sentence_root, next_sentence_candidates)

        self.assertEqual(len(candidatures), 2)
        self.assertListEqual(candidatures, [([he_NP_chunk], [john_NP_chunk, a_musician_NP_chunk]),
                                            ([a_new_song_NP_chunk], [he_NP_chunk, john_NP_chunk, a_musician_NP_chunk]),
                                            ])
        # ROOT (S
        stanford_sentence_root = self.graph_builder.add_sentence(self.test_graph, 0, "DummyRoot", "SentenceTest", 1)
        s_chunk = self.graph_builder.add_chunk("A girl was listening to the song", self.test_graph, False,
                                               "S A girl was listening to the song", "A girl was listening to the song",
                                               None, "S")
        # (NP (DT A) (NN girl))
        a_girl_NP_chunk = self.graph_builder.add_chunk("a girl", self.test_graph, False,
                                                       "NP a girl", "a girl", None, "NP")
        a_DT_word = self.graph_builder.add_word("a", self.test_graph, "word_2",
                                                "DT a", "a", "O", "DT", stanford_sentence_root)
        girl_NN_word = self.graph_builder.add_word("girl", self.test_graph, "word_3",
                                                   "NN girl", "girl", "O", "NN", stanford_sentence_root)
        # (VP (VBD was) (VP (VBG listening)
        was_listening_VP_chunk = self.graph_builder.add_chunk("was listening", self.test_graph, True,
                                                              "VP was listening", "be listen", None, "VP")
        was_VBD_word = self.graph_builder.add_word("was", self.test_graph, "word_1",
                                                   "VBD is", "be", "O", "VBD", stanford_sentence_root)
        listening_VBG_word = self.graph_builder.add_word("listening", self.test_graph, "word_1",
                                                         "VBG listening", "listen", "O", "VBG", stanford_sentence_root)

        # (PP (TO to) (NP (DT the) (NN song)))))
        to_the_song_PP_chunk = self.graph_builder.add_chunk("to the song", self.test_graph, False,
                                                            "PP to the song", "to the song", None, "PP")
        to_TO_word = self.graph_builder.add_word("to", self.test_graph, "word_2",
                                                 "TO to", "to", "O", "TO", stanford_sentence_root)
        the_song_NP_chunk = self.graph_builder.add_chunk("the song", self.test_graph, False,
                                                         "NP the song", "the song", None, "NP")
        the_DT_word = self.graph_builder.add_word("the", self.test_graph, "word_2",
                                                  "DT the", "the", "O", "DT", stanford_sentence_root)
        song_NN_word = self.graph_builder.add_word("song", self.test_graph, "word_3",
                                                   "NN song", "song", "O", "DT", stanford_sentence_root)
        # (. .)
        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.syntax_tree_link(s_chunk, stanford_sentence_root)

        self.graph_builder.syntax_tree_link(a_DT_word, a_girl_NP_chunk)
        self.graph_builder.syntax_tree_link(girl_NN_word, a_girl_NP_chunk)
        self.graph_builder.syntax_tree_link(a_girl_NP_chunk, s_chunk)
        self.graph_builder.set_head(girl_NN_word)

        self.graph_builder.syntax_tree_link(was_VBD_word, was_listening_VP_chunk)
        self.graph_builder.syntax_tree_link(listening_VBG_word, was_listening_VP_chunk)
        self.graph_builder.syntax_tree_link(was_listening_VP_chunk, s_chunk)
        self.graph_builder.set_head(listening_VBG_word)

        self.graph_builder.syntax_tree_link(the_DT_word, the_song_NP_chunk)
        self.graph_builder.syntax_tree_link(song_NN_word, the_song_NP_chunk)
        self.graph_builder.syntax_tree_link(the_song_NP_chunk, to_the_song_PP_chunk)
        self.graph_builder.set_head(song_NN_word)
        self.graph_builder.syntax_tree_link(to_TO_word, to_the_song_PP_chunk)
        self.graph_builder.syntax_tree_link(to_the_song_PP_chunk, s_chunk)
        self.graph_builder.set_head(the_song_NP_chunk)

        self.graph_builder.syntax_tree_link(point_word, s_chunk)

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
        s_chunk = self.graph_builder.add_chunk('"It is my favorite", John said to her.', self.test_graph, False,
                                               'S "It is my favorite", John said to her.',
                                               '"It is my favorite", John said to her.', None, "S")
        # (S
        inner_s_chunk = self.graph_builder.add_chunk('"It is my favorite"', self.test_graph, False,
                                                     'S "It is my favorite"',
                                                     '"It is my favorite"', None, "S")
        # (`` ``)
        open_word = self.graph_builder.add_word("``", self.test_graph, "word_4",
                                                "`` ``", "``", "O", ",", stanford_sentence_root)
        # (NP (PRP It))
        it_NP_chunk = self.graph_builder.add_chunk("It", self.test_graph, True,
                                                   "NP It", "it", None, "NP")
        it_PRP_word = self.graph_builder.add_word("It", self.test_graph, "word_O",
                                                  "PRP It", "it", "O", "PRP", stanford_sentence_root)

        # (VP (VBZ is)
        is_VP_chunk = self.graph_builder.add_chunk("is", self.test_graph, True,
                                                   "VP is", "is", None, "VP")
        is_VBZ_word = self.graph_builder.add_word("is", self.test_graph, "word_1",
                                                  "VBZ is", "be", "O", "VBZ", stanford_sentence_root)

        # (NP (PRP$ my) (JJ favorite)))
        my_favorite_NP_chunk = self.graph_builder.add_chunk("my favorite", self.test_graph, False,
                                                            "NP my favorite", "my favorite", None, "NP")
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
        john_NP_chunk = self.graph_builder.add_chunk("John", self.test_graph, True,
                                                     "NP John", "john", "PERSON", "NP")
        john_NNP_word = self.graph_builder.add_word("John", self.test_graph, "word_O",
                                                    "NNP John", "john", "PERSON", "NNP", stanford_sentence_root)
        # (VP (VBD said)
        said_VP_chunk = self.graph_builder.add_chunk("said", self.test_graph, True,
                                                     "VP said", "said", None, "VP")
        said_VBD_word = self.graph_builder.add_word("said", self.test_graph, "word_1",
                                                    "VBD said", "say", "O", "VBD", stanford_sentence_root)
        # (PP (TO to) (NP (PRP her))))
        to_her_PP_chunk = self.graph_builder.add_chunk("to her", self.test_graph, False,
                                                       "PP to her", "to the song", None, "PP")
        to_TO_word = self.graph_builder.add_word("to", self.test_graph, "word_2",
                                                 "TO to", "to", "O", "TO", stanford_sentence_root)
        her_NP_chunk = self.graph_builder.add_chunk("her", self.test_graph, False,
                                                    "NP her", "her", None, "NP")
        her_PRP_word = self.graph_builder.add_word("her", self.test_graph, "word_2",
                                                   "PRP her", "her", "O", "PRP", stanford_sentence_root)

        # (. .))
        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.syntax_tree_link(s_chunk, stanford_sentence_root)

        self.graph_builder.syntax_tree_link(open_word, inner_s_chunk)

        self.graph_builder.syntax_tree_link(it_PRP_word, it_NP_chunk)
        self.graph_builder.syntax_tree_link(it_NP_chunk, inner_s_chunk)
        self.graph_builder.set_head(it_PRP_word)

        self.graph_builder.syntax_tree_link(is_VP_chunk, is_VBZ_word)
        self.graph_builder.syntax_tree_link(is_VBZ_word, inner_s_chunk)
        self.graph_builder.set_head(is_VBZ_word)

        self.graph_builder.syntax_tree_link(my_PRP_word, my_favorite_NP_chunk)
        self.graph_builder.syntax_tree_link(favorite_JJ_word, my_favorite_NP_chunk)
        self.graph_builder.syntax_tree_link(my_favorite_NP_chunk, inner_s_chunk)
        self.graph_builder.set_head(favorite_JJ_word)

        self.graph_builder.syntax_tree_link(close_word, inner_s_chunk)

        self.graph_builder.syntax_tree_link(inner_s_chunk, s_chunk)

        self.graph_builder.syntax_tree_link(coma_word, s_chunk)

        self.graph_builder.syntax_tree_link(john_NNP_word, john_NP_chunk)
        self.graph_builder.syntax_tree_link(john_NP_chunk, s_chunk)
        self.graph_builder.set_head(john_NNP_word)

        self.graph_builder.syntax_tree_link(said_VBD_word, said_VP_chunk)
        self.graph_builder.syntax_tree_link(said_VP_chunk, s_chunk)
        self.graph_builder.set_head(said_VBD_word)

        self.graph_builder.syntax_tree_link(her_PRP_word, her_NP_chunk)
        self.graph_builder.syntax_tree_link(her_NP_chunk, to_her_PP_chunk)
        self.graph_builder.set_head(her_PRP_word)
        self.graph_builder.syntax_tree_link(to_TO_word, to_her_PP_chunk)
        self.graph_builder.set_head(her_NP_chunk)
        self.graph_builder.syntax_tree_link(to_her_PP_chunk, s_chunk)

        self.graph_builder.syntax_tree_link(point_word, s_chunk)
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

        s_chunk = self.graph_builder.add_chunk("He played a song", self.test_graph, False,
                                               "S He played a song", "he played a song", None, "S")

        he_NP_chunk = self.graph_builder.add_chunk("He", self.test_graph, True,
                                                   "NP he", "he", None, "NP")
        he_PRP_word = self.graph_builder.add_word("He", self.test_graph, "word_O",
                                                  "PRP He", "he", "O", "PRP", stanford_sentence_root)
        self.graph_builder.set_head(he_PRP_word)

        played_VP_chunk = self.graph_builder.add_chunk("played", self.test_graph, True,
                                                       "VP played", "played", None, "VP")
        played_VBD_word = self.graph_builder.add_word("played", self.test_graph, "word_1",
                                                      "VBD played", "played", "O", "VBD", stanford_sentence_root)

        a_new_song_NP_chunk = self.graph_builder.add_chunk("a new song", self.test_graph, False,
                                                           "NP a new song", "a new song", None, "NP")
        a_DET_word = self.graph_builder.add_word("a", self.test_graph, "word_1",
                                                 "DET a", "a", "O", "DET", stanford_sentence_root)
        new_JJ_word = self.graph_builder.add_word("new", self.test_graph, "word_2",
                                                  "JJ new", "new", "O", "JJ", stanford_sentence_root)
        song_NN_word = self.graph_builder.add_word("song", self.test_graph, "word_3",
                                                   "NN song", "song", "O", "NN", stanford_sentence_root)

        point_word = self.graph_builder.add_word(".", self.test_graph, "word_4",
                                                 ". .", ".", "O", ".", stanford_sentence_root)

        self.graph_builder.syntax_tree_link(s_chunk, stanford_sentence_root)

        self.graph_builder.syntax_tree_link(he_PRP_word, he_NP_chunk)
        self.graph_builder.syntax_tree_link(he_NP_chunk, s_chunk)
        self.graph_builder.set_head(played_VBD_word)

        self.graph_builder.syntax_tree_link(played_VBD_word, played_VP_chunk)
        self.graph_builder.syntax_tree_link(played_VP_chunk, s_chunk)

        self.graph_builder.syntax_tree_link(a_new_song_NP_chunk, s_chunk)
        self.graph_builder.syntax_tree_link(a_DET_word, a_new_song_NP_chunk)
        self.graph_builder.syntax_tree_link(new_JJ_word, a_new_song_NP_chunk)
        self.graph_builder.syntax_tree_link(song_NN_word, a_new_song_NP_chunk)
        self.graph_builder.set_head(song_NN_word)

        self.graph_builder.syntax_tree_link(point_word, s_chunk)

        candidatures, next_sentence_candidates = self.candidate_extractor.process_sentence(stanford_sentence_root, [])

        self.assertEqual(len(candidatures), 2)
        self.assertListEqual(candidatures, [([he_NP_chunk], []), ([a_new_song_NP_chunk], [he_NP_chunk])])

    def test_process(self):
        self.fail("TODO")
