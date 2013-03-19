from collections import defaultdict
import logging
from graph.graph_builder import BaseGraphBuilder
from graph.utils import GraphWrapper
from pykaf.kaf import KafDocument
from resources import tree

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '3/13/13'


class KafAndTreeGraphBuilder(BaseGraphBuilder):
    """Extract the info from KAF documents and TreeBank
    """

    def __init__(self, logger=logging.getLogger("OntonotesGraphBuilder")):
        self.logger = logger
        self.graph_properties["kaf"] = "object"
        self.vertex_properties["kaf_id"] = "object"

    def preprocess_sentences(self, graph, document):
        self.graph = graph
        sentences = document[1].split("\n")
        self.parse_kaf(graph, document[0])
        return sentences

    def process_sentence(self, graph, sentence, root_index, sentence_namespace):
        """Add to the graph the morphological, syntactical and dependency info contained in the sentence.

        sentence: the sentence to parse
        sentenceNamespace:: prefix added to all nodes ID strings.
        separator: character or string used for create the nodes ID string.
        """
        self.graph = graph
        sentence_id = sentence_namespace
        sentence_label = sentence_namespace
        # Sentence Root
        sentence_root_node = self.add_sentence(graph, root_index, "", sentence_label, sentence_id)

        sentence_text = self.parse_syntax(graph, sentence, sentence_root_node, sentenceNamespace=sentence_namespace)
        # Return the generated context graph
        GraphWrapper.set_properties(graph, node=sentence_root_node, vertex_properties={
            'lemma': sentence_text,
            'form': sentence_text,
        })

        self.sentenceup()
        return sentence_root_node

    def parse_kaf(self, graph, kaf_string):

        self.graph = graph
        # node and graph properties
        word_ner = GraphWrapper.node_property(name="ner", graph=graph)
        word_kaf_id = GraphWrapper.node_property(name="kaf_id", graph=graph)

        self.word_pool = []

        # Store original kaf for further recreation
        kaf = KafDocument(kaf_stream=kaf_string)
        GraphWrapper.set_graph_property(graph=graph, property_name="kaf", value=kaf)
        # Words
        kaf_words = dict([(kaf_word.attrib["wid"], kaf_word.text) for kaf_word in kaf.get_words()])
        # Terms
        term_by_id = dict()
        for term in kaf.get_terms():
            # Fetch the words values
            term_id = term.attrib["tid"]
            words = kaf.get_terms_words(term)
            form = " ".join([kaf_words[word.attrib["id"]] for word in words])
            kaf_id = "{0}#{1}".format(term_id, "|".join([word.attrib["id"] for word in words]))
            try:
                lemma = term.attrib["lemma"]
            except KeyError:
                lemma = form
            pos = term.attrib["pos"]
            label = "\n".join((form, pos, lemma, term_id))
            #Create word node
            word_node = self.add_word(form=form, wid=term_id, label=label, lemma=lemma, ner="o", pos=pos, head=True)
            word_kaf_id[word_node] = kaf_id

            # Store the words
            term_by_id[term_id] = word_node
            self.word_pool.append(word_node)
            self.wordup()

        #A dict of entities that contains a list of references. A reference is a list of terms.
        self.entities_by_id = dict()
        self.entities_by_first_word = defaultdict(set)
        self.entities_by_end_word = defaultdict(set)

        # Entities
        for entity in kaf.get_entities():
            entity_id = entity.attrib["eid"],
            entity_type = entity.attrib["type"]
            references = []
            for reference in kaf.get_entity_references(entity):
                new_reference = []
                for term in kaf.get_entity_reference_span(reference):
                    word_node = term_by_id[term.attrib["id"]]
                    word_ner[word_node] = entity_type
                    new_reference.append(word_node)
                self.entities_by_first_word[new_reference[0]].add(entity_id)
                self.entities_by_end_word[new_reference[-1]].add(entity_id)
                references.append(new_reference)
            self.entities_by_id[entity_id] = (entity_type, references)

    def parse_syntax(self, graph, sentence, syntactic_root, sentenceNamespace, syntax_count=0):
        # Convert the syntactic tree
        self.syntax_count = syntax_count
        syntactic_tree = tree.Tree(sentence)
        self.word_count += 1
        node_ner = GraphWrapper.node_property("ner", self.graph)

        def Iterate_Syntax(graph, syntactic_tree, parent_node):
            """Walk recursively over the syntax tree and add their info to the graph."""
            # Aux functions

            def syntax_leaf_process(parent_node, leaf):
                # the tree node is a leaf
                # Get the word node pointed by the leaf
                word_node = self.word_pool.pop(0)
                if "=H" in leaf or "-H" in leaf:
                    self.set_head(word_node)
                    #Link the word to the node
                self.syntactic_terminal_link(parent_node=parent_node, terminal_node=word_node)
                #link the word to the sentence
                self.link_word(sentence_root_node=syntactic_root, word_node=word_node)
                # Generate the text
                content_text = leaf
                if node_ner[word_node] != "o":
                    return content_text, self.entities_by_first_word[word_node], self.entities_by_end_word[word_node]
                return content_text, set(), set()

            def syntax_branch_process(parent_node, syntactic_tree):
                # Create a node for this element
                label = syntactic_tree.node
                head = "=H" in label
                tag = label.replace("=H", "")
                new_node = self.add_chunk(form="", graph=graph, head=head, label=label, lemma="", ner="o", tag=tag)
                # Link the child with their parent (The actual processed node)
                self.syntax_tree_link(new_node, parent_node)
                # Process the children
                content_text = []
                ner_begins = None
                ner_ends = None
                for child in syntactic_tree:
                    # Fetch the text contained and ner by the node
                    content_text_part, more_ner_begins, more_ner_ends = Iterate_Syntax(
                        graph=graph, syntactic_tree=child, parent_node=new_node)
                    # Append the text
                    content_text.append(content_text_part)
                    # Only filed first time
                    if ner_begins is None:
                        ner_begins = more_ner_begins
                        # Refiled every time
                    ner_ends = more_ner_ends
                    # Rebuild the attributes composed from children info
                content_text = " ".join(content_text)
                ner_ids = ner_begins.intersection(ner_ends)
                ner = "o"
                for ner_id in ner_ids:
                    # The type of the entity is on the first place of tuple
                    ner = self.entities_by_id[ner_id][0]

                # Set the rebuild attributes
                GraphWrapper.set_properties(graph, node=new_node, vertex_properties={
                    'label': "\n".join((content_text, tag, ner)),
                    'lemma': content_text,
                    'form': content_text,
                    'ner': ner,
                })
                return content_text, ner_begins, ner_ends

                # Determine if the syntactic tree Node is as branch or a leaf

            if type(syntactic_tree) == tree.Tree:
                content_text, ner_begins, ner_ends = syntax_branch_process(parent_node, syntactic_tree)
                self.syntax_count += 1
            else:
                content_text, ner_begins, ner_ends = syntax_leaf_process(parent_node, syntactic_tree)
            return content_text, ner_begins, ner_ends

            # Call to the recursive function

        return Iterate_Syntax(graph=graph, syntactic_tree=syntactic_tree, parent_node=syntactic_root)