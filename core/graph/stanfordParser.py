__author__ = 'nasgar'

from graph.utils import GraphWrapper
from graph.graph_builder import BaseGraphBuilder

try:
    import json
except ImportError:
    import simplejson as json

import logging
from resources.tree import Tree
from stanford_corenlp_python import jsonrpc
from output.progressbar import ProgressBar, Fraction


class StanfordCoreNLPGraphBuilder(BaseGraphBuilder):
    """ A easy client to process sentences with the Stanford coreNLP launched via: stanford_corenlp_python wrapper.

    This client used a flavoured version of the library that is distributed with this code.

    """

    size = 1
    max_tries = 4
    root_namespace = "root"
    noun_phrase_tag = "NP"
    conjuntion_tag = "CC"

    def __init__(self, ip="127.0.0.1", port=8080, logger=logging.getLogger("GraphBuilder")):
        """ Build the link to the CoreNLP server.

        ip: The ip to reach the coreNLP server(default: 127.0.0.1).
        port: The port where the server is listening(default:8080).
        """
        self.logger = logger
        self.logger.info("Conecting to: %s:%s", ip, port)
        self.server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(),
                                          jsonrpc.TransportTcpIp(addr=(ip, port)))

    def parse_words(self, graph, sentence, root, root_index, sentenceNamespace, separator):
        for index, word in enumerate(sentence['words'], root_index + 1):
            word_id = self.get_compose_id(sentenceNamespace, index, separator)
            form = word[0]
            pos = word[1]['PartOfSpeech']
            ner = word[1]['NamedEntityTag']
            lemma = word[1]['Lemma']
            begin = word[1]['CharacterOffsetBegin']
            end = word[1]['CharacterOffsetEnd']
            label = "|".join((form, pos, word_id)),
            self.add_word(form, graph, word_id, label, lemma, ner, pos, root, begin, end)
            self.statistics_word_up()

    def parse_dependency(self, graph, root, sentence, sentenceNamespace, separator):
        for dependency in sentence['dependencies']:
            # Extract dependency type
            relation = dependency[0]
            # Generate unique string ID for nodes
            dependency_governor = dependency[1]
            governor_name = self.get_compose_id(sentenceNamespace, dependency_governor[1], separator)
            dependency_dependant = dependency[2]
            dependant_name = self.get_compose_id(sentenceNamespace, dependency_dependant[1], separator)
            # Find the nodes
            if dependency_governor[1]:
                governor = GraphWrapper.get_vertex_by_id(graph, governor_name)
            else:
                governor = root
            dependant = GraphWrapper.get_vertex_by_id(graph, dependant_name)
            # Add the edge to de graph and add the relation type and value
            GraphWrapper.link(graph=graph, origin=governor, target=dependant,
                              link_type=self.dependency_edge_type, value=relation,
                              weight=1, label=self.dependency_edge_type + " " + relation
            )

    def parse_syntax(self, graph, root_index, sentence, syntactic_root, sentenceNamespace, separator, syntax_count=0):
        # Convert the syntactic tree
        self.syntax_count = syntax_count
        syntactic_tree = Tree(sentence["parsetree"])
        self.word_count = root_index + 1
        ner_property = GraphWrapper.node_property("ner", graph)
        begin_property = GraphWrapper.node_property("begin", graph)
        end_property = GraphWrapper.node_property("end", graph)

        def Iterate_Syntax(graph, syntactic_tree, parent_node):
            """Walk recursively over the syntax tree and add their info to the graph."""

            # Aux functions
            def syntax_leaf_process(parent_node, syntactic_tree):
                # the tree node is a leaf
                # Get the word node pointed by the leaf
                word_id = self.get_compose_id(sentenceNamespace, self.word_count, separator)
                self.word_count += 1
                label = syntactic_tree.node

                word_node = GraphWrapper.get_vertex_by_id(graph, word_id)

                if "=H" in label:
                    self.set_head(word_node)

                #Link the word to the node
                GraphWrapper.link(graph, origin=parent_node, target=word_node,
                                  link_type=self.syntactic_edge_type, value=self.syntactic_edge_value_terminal,
                                  weight=1, label=self.syntactic_edge_type + "_" + self.syntactic_edge_value_terminal, )
                # Generate the text
                content_text = syntactic_tree
                ner_type = ner_property[word_node]
                return content_text, ner_type, begin_property[word_node], end_property[word_node]

            def syntax_branch_process( parent_node, syntactic_tree):
                # Create a node for this element
                label = syntactic_tree.node
                head = "=H" in label
                tag = label.replace("=H", "")
                new_node = self.add_chunk("", graph, head, label, "", "O", tag)
                # Link the child with their parent (The actual processed node)
                self.syntax_tree_link(parent_node, new_node)
                # Process the children
                content_text = []
                ner = []
                begin_offset = []
                end_offset = []
                for child in syntactic_tree:
                    # Fetch the text contained and ner by the node
                    content_text_part, ner_part, begin_offset_part, end_offset_part = Iterate_Syntax(
                        graph=graph,
                        syntactic_tree=child,
                        parent_node=new_node)
                    # Append the text
                    begin_offset.append(begin_offset_part)
                    end_offset.append(end_offset_part)
                    ner.append(ner_part)
                    content_text.append(content_text_part)
                    # Rebuild the attributes composed from children info
                content_text = " ".join(content_text)
                # Check if the node is a NER
                if len(set(ner)) == 1:
                    ner = ner[0]
                else:
                    ner = "O"
                    # Set the boundaries
                begin_offset = min(begin_offset)
                end_offset = max(end_offset)
                # Set the rebuild attributes
                GraphWrapper.set_properties(graph, node=new_node, vertex_properties={
                    'label': "{0}({1}-{2})\n{3} | {4}".format(content_text, begin_offset, end_offset, label, ner),
                    'lemma': content_text,
                    'form': content_text,
                    'ner': ner,
                    'begin': begin_offset,
                    'end': end_offset
                })
                return content_text, ner, begin_offset, end_offset
            if  type(syntactic_tree) == Tree:
                content_text_part, ner_part, begin_offset_part, end_offset_part = syntax_branch_process(
                    parent_node, syntactic_tree)
                self.syntax_count +=1
            else:
                content_text_part, ner_part, begin_offset_part, end_offset_part = syntax_leaf_process\
                        (parent_node, syntactic_tree)
            return content_text_part, ner_part, begin_offset_part, end_offset_part

        # Call to the recursive function
        Iterate_Syntax(graph=graph, syntactic_tree=syntactic_tree, parent_node=syntactic_root)

    def process_sentence(self, graph, sentence, root_index, sentence_namespace):
        """Add to the graph the morphological, syntactical and dependency info contained in the sentence.

        sentence: the sentence to parse
        sentenceNamespace:: prefix added to all nodes ID strings.
        separator: character or string used for create the nodes ID string.
        """
        # Sentence Root
        root_namespace = "root"
        separator = "_"
        form = self.get_compose_id(root_namespace, sentence_namespace, separator),
        label = self.get_compose_id(root_namespace, sentence_namespace, " "),
        senence_id = self.get_compose_id(root_namespace, sentence_namespace, separator),
        sentence_root_node = self.add_sentence(graph, root_index, form, label, senence_id)

        #TODO standardise the calls
        # Create Nodes for each Word
        self.parse_words(graph, sentence, sentence_root_node, root_index, sentence_namespace, separator)

        # Dependency
        # Create Edges for each dependency
        self.parse_dependency(graph, sentence_root_node, sentence, sentence_namespace, separator)

        # Syntax
        self.parse_syntax(graph, root_index, sentence, sentence_root_node, sentence_namespace, separator)
        # Return the generated context graph\
        self.statistics_sentence_up()
        return sentence_root_node

    def _send_to_coreNLP(self, text):
        """ Parse the text against the CoreNLP parser and load returned Json

        sentence:: the string of the sentence to be processed
        the dependencies are returned in a tuple whit the next format:
             (relation, (word, index), (word, index))

        """
        return json.loads(self.server.parse(text))["sentences"]

    def parse_source(self, text):
        # Ontonotes corpus used in ConLL
        if type(text) != str:
            # Progress Bar
            widgets = ['External parsing corpus: ', Fraction()]
            pbar = ProgressBar(widgets=widgets, maxval=len(text) / self.size, force_update=True).start()
            # Cut the text in slices of sentences to avoid overload the server
            sentences_parsed = []
            for sentence_index in range(len(text) / self.size):
                sentence_slice_start = self.size * sentence_index
                sentence_slice_end = self.size * (sentence_index + 1)
                # Make the sentence list into a full string
                sentence_slice = " ".join(text[sentence_slice_start:sentence_slice_end])
                # Send the text to server
                tries = 0
                slice_results = []
                while (not slice_results) and (tries < self.max_tries):
                    try:
                        slice_results = self._send_to_coreNLP(sentence_slice)
                        sentences_parsed.extend(slice_results)
                    except Exception as ex:
                        # If fails:
                        self.logger.debug("Retry %i slice %i-%i: %s",
                                          tries, sentence_slice_start, sentence_slice_end, ex)
                        # Clean the response, add one to the counter and retry
                        slice_results = []
                        tries += 1
                if tries >= self.max_tries:
                    self.logger.error("Slide Skip:%i-%i", sentence_slice_start, sentence_slice_end)

                pbar.update(sentence_index)
            pbar.finish()
        # Plain text corpus
        else:
            sentences_parsed = self._send_to_coreNLP(text)
            # With all the text parsed
        return sentences_parsed