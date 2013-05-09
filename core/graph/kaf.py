import logging
from collections import defaultdict
from resources import tree
from pykaf.kaf import KafDocument
from graph.graph_builder import BaseGraphBuilder

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'
__date__ = '3/13/13'


class KafAndTreeGraphBuilder(BaseGraphBuilder):
    """Extract the info from KAF documents and TreeBank."""

    kaf_document_property = "kaf"
    kaf_id_property = "kaf_id"

    def __init__(self, logger=logging.getLogger("KafGraphBuilder")):
        self.logger = logger
        self.graph_properties[self.kaf_document_property] = "object"
        self.vertex_properties[self.kaf_id_property] = "object"

    def preprocess_sentences(self, graph, document):
        self.graph = graph
        # node and graph properties
        self.node_kaf_id = self.get_node_property(name=self.kaf_id_property)
        sentences = document[1].split("\n")
        self.parse_kaf(kaf_string=document[0])
        return sentences

    def process_sentence(self, graph, sentence, root_index, sentence_namespace):
        """Add to the graph the morphological, syntactical and dependency info contained in the sentence.

        sentence: the sentence to parse
        sentenceNamespace:: prefix added to all nodes ID strings.
        separator: character or string used for create the nodes ID string.
        """
        self.graph = graph

        self.node_label = self.get_node_property("label")
        self.node_ner = self.get_node_property("ner")
        self.node_form = self.get_node_property("form")
        self.node_lemma = self.get_node_property("lemma")
        self.node_head = self.get_node_property("head")
        self.node_id = self.get_node_property("id")

        sentence_id = sentence_namespace
        sentence_label = sentence_namespace
        # Sentence Root
        sentence_root_node = self.add_sentence(root_index=root_index, sentence_form="", sentence_label=sentence_label,
                                               sentence_id=sentence_id)
        sentence_text = self.parse_syntax(sentence=sentence, syntactic_root=sentence_root_node,
                                          sentenceNamespace=sentence_namespace)
        # Return the generated context graph
        self.node_lemma[sentence_root_node] = sentence_text
        self.node_form[sentence_root_node] = sentence_text,

        self.statistics_sentence_up()
        return sentence_root_node

    def parse_kaf(self, kaf_string):

        self.word_pool = []
        # Store original kaf for further recreation
        kaf = KafDocument(kaf_stream=kaf_string)
        self.set_graph_property_value(self.kaf_document_property, kaf)
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
            # We want pennTreeBank tagging no kaf tagging
            pos = term.attrib["morphofeat"]
            label = "\n".join((form, pos, lemma, term_id))
            #Create word node
            word_node = self.add_word(form=form, wid=term_id, label=label, lemma=lemma, ner="o", pos=pos, head=False)
            self.node_kaf_id[word_node] = kaf_id
            # Store the words
            term_by_id[term_id] = word_node
            self.word_pool.append(word_node)
            self.statistics_word_up()

        #A dict of entities that contains a list of references. A reference is a list of terms.
        self.entities_by_id = dict()
        self.entities_by_word = defaultdict(set)

        # Entities
        for kaf_entity in kaf.get_entities():
            entity_type = kaf_entity.attrib["type"]
            entity_id = kaf_entity.attrib["eid"]
            entity = self.add_named_entity(entity_type=entity_type, entity_id=entity_id)
            self.entities_by_id[entity_id] = entity
            for reference in kaf.get_entity_references(kaf_entity):
                new_mention = []
                for term in kaf.get_entity_reference_span(reference):
                    word_node = term_by_id[term.attrib["id"]]
                    #word_ner[word_node] = entity_type
                    self.entities_by_word[word_node] = (entity, new_mention)
                    new_mention.append(word_node)

    def process_entities(self, entities):

        for entity, mention in entities:
            parents = set([self.get_syntactic_parent(word) for word in mention])
            # If all mention words have the same parent we can produce a safe ner mention
            if len(parents) == 1 and not None in parents:
                parent = parents.pop()
                entity_type = self.node_ner[entity]
                entity_id = self.node_id[entity]
                # If the Ner mention covers all the constituent word, the constituent is assigned as Ner
                if self.get_chunk_children(parent) == mention:
                    self.node_ner[parent] = entity_type
                    self.add_named_mention(named_entity=entity, mention=parent)
                else:
                    # Create a new constituent to cover the Ner mention
                    head = False
                    form = ""
                    ner_constituent = self.add_chunk(form=form, head=head, label=form, lemma="",
                                                     ner=entity_type, tag="NE:{0}".format(entity_type))
                    for word in mention:
                        form += self.node_form[word]
                        head = head or self.node_head[word]
                        self.unlink(parent, word)
                        self.syntactic_terminal_link(parent_node=ner_constituent, terminal_node=word)
                    self.node_form[ner_constituent] = form
                    self.node_head[ner_constituent] = head
                    self.add_named_mention(named_entity=entity, mention=ner_constituent)
                    self.syntax_tree_link(ner_constituent, parent)

    def parse_syntax(self, sentence, syntactic_root, sentenceNamespace, syntax_count=0):

        # Convert the syntactic tree
        self.syntax_count = syntax_count

        syntactic_tree = tree.Tree(sentence)
        self.word_count += 1

        entities = []

        def Iterate_Syntax(syntactic_tree, parent_node):
            """Walk recursively over the syntax tree and add their info to the graph."""
            # Aux functions

            def syntax_leaf_process(parent_node, leaf):
                # the tree node is a leaf
                # Get the word node pointed by the leaf
                word_node = self.word_pool.pop(0)
                text_leaf = str(leaf)
                treebank_word = leaf[0]
                if "=H" in text_leaf or "-H" in text_leaf:
                    self.set_head(word_node)
                    #Link the word to the node
                self.syntactic_terminal_link(parent_node=parent_node, terminal_node=word_node)
                #link the word to the sentence
                self.link_word(sentence_root_node=syntactic_root, word_node=word_node)
                # Generate the text
                content_text = treebank_word
                # Enlist entities that appears in the phrase
                if word_node in self.entities_by_word:
                    entities.append(self.entities_by_word.pop(word_node))
                return content_text

            def syntax_branch_process(parent_node, branch):
                # Create a node for this element
                label = branch.node
                head = "=H" in label
                tag = label.replace("=H", "")
                new_node = self.add_chunk(form="", head=head, label=label, lemma="", ner="o", tag=tag)
                # Link the child with their parent (The actual processed node)
                self.syntax_tree_link(child=new_node, parent=parent_node)
                # Process the children
                content_text = []

                for child in branch:
                    # Fetch the text contained
                    content_text_part = Iterate_Syntax(syntactic_tree=child, parent_node=new_node)
                    # Append the text
                    content_text.append(content_text_part)
                    # Rebuild the attributes composed from children info
                content_text = " ".join(content_text)

                # Set the rebuild attributes
                self.node_label[new_node] = "\n".join((content_text, tag)),
                self.node_lemma[new_node] = content_text
                self.node_form[new_node] = content_text
                self.node_ner[new_node] = "o"
                return content_text

            # Determine if the syntactic tree Node is as branch or a leaf
            if len(syntactic_tree) > 1 or type(syntactic_tree[0]) != str:
                content_text = syntax_branch_process(parent_node=parent_node, branch=syntactic_tree)
                self.syntax_count += 1
            else:
                content_text = syntax_leaf_process(parent_node=parent_node, leaf=syntactic_tree)
            return content_text
        # Call to the recursive function
        Iterate_Syntax(syntactic_tree=syntactic_tree, parent_node=syntactic_root)

        self.process_entities(entities=entities)