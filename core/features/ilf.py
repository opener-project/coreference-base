"""Generated form a dependency graph a context graph similar to DRT "boxes".

   The algorithm build a hierarchy that has a similar to concept of 'DRS's`accessibility' but generated from a dependency
   hierarchy.


   >>> CG =  ContextGenerator()

   >>> context_graph = CG.process_graph(a_dependency_graph)

   >>> CG.show_graph(context_graph)


"""


__author__ = 'Josu Bermudez<josu.bermudez@deusto.es>'

from graph_tool.all import *
from features.grendel import GenderNumberExtractor
from graph.utils import GraphWrapper

from graph_tool import GraphView

class ContextGenerator:
    """ A builder of  a directed graph based on a similar to concept of 'DRS's`accessibility' but generated from a
    dependency hierarchy.

    """

    accessibility_edge_type = "accessibility"

    _relations_denotes_referent = {"mock"}
    """Dependency relations that denotes a referent."""

    _governed_dependencies_denotes_referent = {}
    """Governed dependencies that denotes a dircourse referent."""

    _POS_tags_denotes_referent = {"NE", "PRP", "NNP", "NNPS"}
    """POS tags that denotes a dircourse referent."""

    _POS_tags_denotes_global_referent = {"NE", "NNP"}
    """POS tag of the elements that generates global referents """

    _relations_denotes_condition = {"advcl"}
    """Dependency relations that marks dependant as condition of the goberned."""

    _relations_denotes_subordination = {"mock"}
    """Dependency relations that marks dependant as subordinated."""

    _governed_relations_denotes_subordination = {"neg"}
    """Governded Dependency relations that marks gobernor as subordinated."""

    _governed_relations_denotes_conditional = {"advcl"}

    _POS_tags_denotes_subordination = {"mock"}
    """POS tags that denotes a dircourse subordination."""

    shape= "diamond"
    color= "lightgoldenrod"

    colors= {
        "female": "pink",
        "male": "lightskyblue1",
        "neutral" : "ivory3",
        "unknown" : "olivedrab3",
        }
    shapes= {
        "singular": "circle",
        "plural": "doublecircle",
        "unknown" : "Mcircle",
        }

    def __init__(self, graph_builder):
        self.graph_builder = graph_builder
        self.gender_classifier = GenderNumberExtractor()
        self.bat = Bat()

    @classmethod
    def get_context_parent(cls, context):
        """ Return the  parent of a node(Only expected to be one)."""
        graph = context.get_graph()
        for relation in context.in_edges():
            if graph.edge_properties["type"][relation] == "subordinated":
                if graph.vertex_properties["type"][relation.source()] == "context":
                    return relation.source()

    def _extract_discourse_referents(self, global_context, context, word, relation):
        """Extract from a dependency graph node possible discourse referents."""
        referents = []
        # Graphs
        word_graph = word.get_graph()
        context_graph = context.get_graph()
        # Word useful information
        pos = word_graph.vertex_properties["pos"][word]
        form = word_graph.vertex_properties["form"][word]
        ner = word_graph.vertex_properties["ner"][word]
        governed_dependencies = set([edge.get_graph().edge_properties["type"][edge] for edge in word.out_edges()])
        # Add more info useful for rules here
        # ...
        # Check the rules
        is_referent =(
            (relation in self._relations_denotes_referent) or
            (governed_dependencies & self._governed_dependencies_denotes_referent) or
            (pos in self._POS_tags_denotes_referent)
            # Add here new Rules
            )

        is_global_referent = ( pos in self._POS_tags_denotes_global_referent)
        if is_global_referent:
            context = global_context

        # If word is a referent, create, fill and add a referent node to the graph.
        if is_referent:
            referent_node = context_graph.add_vertex()
            # Add referent info
            GraphWrapper.set_properties(vertex_properties={
                "type": "referent",
                "label": form,
                "gender":self.gender_classifier.get_gender(form, pos),
                "number": self.gender_classifier.get_number(form, pos, ner),
                "color":self.colors[context_graph.vertex_properties["gender"][referent_node]],
                "shape":self.shapes[context_graph.vertex_properties["number"][referent_node]],
                })
            # link bi-directionally with the context
            GraphWrapper.link(context_graph, context, referent_node,
                type="referent", weight=1,
                label="{}:{}".format("referent", 1)
            )
            GraphWrapper.link(context_graph, referent_node, context,
                type="referent", weight=1,
                label="{}:{}".format("is_referent", 1)
            )
            # Accessibility links of the new referent
            self._link_referent_accessibility(context_graph, referent_node)
        return referents

    def _link_context(self, previous_context, actual_context, word, dependency_relation):
        """ Generates, and returns, a context for the node.

        The new context is linked with the previous context (previous node's context) in a 'same level' or 'subordination'
        relation. The link type is selected in base of dependency with parent's type(node edge type) and some especial
        child existence(I.E negation).

        """
        # Retrieve the graph
        context_graph = previous_context.get_graph()
        word_graph = word.get_graph()
        # Word useful information
        pos = word_graph.vertex_properties["pos"][word]
        governed_dependencies = set([word_graph.edge_properties["type"][edge] for edge in word.out_edges()])
        # Add more info useful for rules here
        # ...
        # Select the link nature. Extracted From if for ease the reading

        is_subordinated = (
            (dependency_relation in self._relations_denotes_subordination) or
            (pos in self._POS_tags_denotes_subordination) or
            (governed_dependencies & self._governed_relations_denotes_subordination)
            # Add here new subordination conditions
            # ...
            )

        # Conditional
        is_conditional = (governed_dependencies & self._governed_relations_denotes_conditional)

        is_if_clause = (dependency_relation in self._relations_denotes_condition)

        # Link the context
        if is_subordinated:
            GraphWrapper.link(context_graph, previous_context, actual_context, type="subordinated", weight=1,
                label="{}:{}".format("subordinated",1)
            )
        elif is_conditional:
            condition_context = GraphWrapper.new_node(context_graph, type="context", token=word, label="condition",
                shape=self.shape, color=self.color)
            GraphWrapper.link(context_graph, condition_context, actual_context, type="subordinated", weight=1,
                label="{}:{}".format("subordinated",1)
                )
            GraphWrapper.link(context_graph, previous_context, condition_context, type="subordinated", weight=1,
                label="{}:{}".format("subordinated",1)
                )
        elif is_if_clause:
            # For if clauses the link is with the parent of the previous context
            parent_context = self.get_context_parent(previous_context)
            GraphWrapper.link(context_graph, parent_context, actual_context, type="equal", weight=1,
                label="{}:{}".format("equal",1)
            )
            GraphWrapper.link(context_graph, actual_context, parent_context, type="equal", weight=1,
                label="{}:{}".format("reversed",1)
            )
        else:
            # Equality relations are reciprocal
            GraphWrapper.link(context_graph, previous_context, actual_context, type="equal", weight=1,
                label="{}:{}".format("equal",1)
                )
            GraphWrapper.link(context_graph, actual_context, previous_context, type="equal", weight=1,
                label="{}:{}".format("reversed",1)
                )

    def _link_referent_accessibility(self, graph, referent):
        """ Add accessibility edges to previous reachable referents"""
        # Only referents graphs
        referents_graph = self.graph_builder.get_referent_graph(graph)

        # Only edges usable in accessible referents searches
        navigable_graph = self.graph_builder.get_navigable_graph(graph)

        weight = navigable_graph.edge_properties["weight"]
        # Calculate the distance of all accessible referents
        distances, predecessors =  graph_tool.search.dijkstra_search(navigable_graph, referent,weight, infinity=100000)
        # Store this info in edges
        target_referents = referents_graph.vertices()
        # Track the binding of the referent
        binded = False
        for target_referent in target_referents:
            # We want a target referent that can access to all the graph
            target_referent = graph.vertex(target_referent)
            # Remove the unreachable referents and the referent itself
            if (distances[target_referent] < 100000) and (target_referent != referent):
                # make the accessibility
                GraphWrapper.link(graph, referent, target_referent,
                    weight=distances[target_referent],
                    type=self.accessibility_edge_type,
                    label="accessibility:{}".format(distances[target_referent])
                )
                # Get the target  reference entity
                target_entity = self.bat.get_entity(target_referent, graph)
                # Determine the Coreference.
                if self.bat.is_bindable(referent, target_entity, graph):
                    self.bat.bind(referent, target_entity, graph)
                    binded = True
            # If a referent ist not bind Accommodate it
        if not binded:
            self.bat.accommodate(referent, graph)

    def _recursive_processing(self, dependency_graph, global_context, previous_context, word, relation):
        """ Process each node generates their context and discourse referents then iterate over their children."""
        # Generate the new context and fill with the discourse referents and the token
        context_graph = previous_context.get_graph()
        # Generate the context of this node
        context = GraphWrapper.new_node(context_graph,
            type="context", token=word, label=dependency_graph.vertex_properties["form"][word],
            shape=self.shape, color=self.color)
        # Link this node
        self._link_context(previous_context, context, word, relation)
        # Extract the referent discourses
        self._extract_discourse_referents(global_context, context, word, relation)
        # List and order the dependency children
        out_edges = sorted(
            [(dependency.target(), GraphWrapper.get_edge_property(dependency, "type"))
                for dependency in word.out_edges()],
            key=lambda child : GraphWrapper.get_node_property(child[0], "ord")
        )
        # You can't use iterator directly if you want add vertex
        for (child, child_relation) in out_edges:
            try:
                self._recursive_processing(dependency_graph, global_context, context, child, child_relation)
            except Exception as ex:
                print "Error{}{}{}".format(ex, type(ex),child)

    def process_graph(self, base_graph, root, context_graph=None, base_context=None):
        """ Process a dependency graph into a context graph.

        Iterate all over the graph generating the context for each word(node). Each context is linked with the previous
        context (previous node's context) in a 'same level' or 'subordination' relation. The link type is selected in base
        of dependency with parent's type(node edge type) and some especial child existence( I.E negation).

        :dependency_graph: The graph that contains the original dependency structure.
        :original_context: The node that represent de global context(optional).

        """
        # Generate the new graph and set their properties
        dependency_graph = self.graph_builder.get_dendency_graph()
        root = dependency_graph.vertex(root)
        if not context_graph:
            context_graph = Graph()
        # Generate graph, vertex and edges properties.
        GraphWrapper.define_properties(context_graph,
            graph_properties={'global_context':context_graph.new_graph_property('python::object'),
                            },
            vertex_properties={'token':context_graph.new_vertex_property('python::object'),
                            'label':"string",
                            'type':"string",
                            'gender':"string",
                            'number':"string",
                            'color':"string",
                            'shape':"string",
                            },
            edge_properties={'type':"string",
                            'weight':"int32_t",
                            'label':"string",
                            },
            )

        # Determine the global Context
        if context_graph.graph_properties['global_context'][context_graph]:
            global_context = context_graph.graph_properties['global_context'][context_graph]
        elif base_context:
            global_context = base_context
            # log.warning("No global context in graph using base context")
        else:
            # self.log.warning("Generating new global context")
            global_context = GraphWrapper.new_node(context_graph, type="context", token=None,
                label= "global_context", color=self.color, shape=self.shape)
            context_graph.graph_properties['global_context'][context_graph]= global_context
        # Assure the base context
        if  not base_context:
            if global_context:
                # self.log.info("Using global context as base context")
                base_context = global_context
        # Process root node
        root_relation = "ROOT"
        self._recursive_processing(base_graph, global_context, base_context, root, root_relation)
        # Return the filled graph
        return context_graph


class Bat:
    """ Provides the actions an check necessaries for Binding and Accommodation Theory. """

    # Vertex properties that have to match with entity properties
    pair_filters = ["gender","number"]

    # Vertex properties that values as * . Each values is for the filter in the same position. I.E. Second filters uses
    # The second joker value as *
    joker_values = ["nil","unknown"]

    def __init__(self, pair_filters=None, joker_values=None):
        if pair_filters:
            self.pair_filters = pair_filters
        if joker_values:
            self.joker_values = joker_values
        if not(len(self.joker_values) == len(self.pair_filters)):
            raise Exception("Bat object: filters numbers and joker values doesn`t match")

    def get_entity(self, referent, graph):
        """ Return the entity of a referent (Only expected to be one)."""
        if not graph:
            graph = referent.get_graph()
        for relation in referent.in_edges():
            if graph.edge_properties["type"][relation] == "reference":
                if graph.vertex_properties["type"][relation.source()] == "entity":
                    return relation.source()

    def bind(self, referent, entity, graph=None):
        """Bind a referent to it's entity"""
        if not graph:
            graph = referent.get_graph()
        coreference_link = GraphWrapper.link(graph, entity, referent,
            type="reference",
            label="reference_{0}_{1}".format(entity, referent),
            )
        return coreference_link

    def accommodate(self, referent, graph=None):
        """ Accommodate a referent generating new entity"""
        if not graph:
            graph = referent.get_graph()

        gender = graph.vertex_properties["gender"]
        number = graph.vertex_properties["number"]
        # Create new entity for the reference
        entity = graph.add_vertex()
        graph.vertex_properties["label"][entity] = "entity{0}".format(entity)
        graph.vertex_properties["type"][entity] = "entity"
        gender[entity] = gender[referent]
        number[entity] = number[referent]
        # Add referent new info here
        # Bind entity and referent, return the link
        return self.bind(referent, entity, graph)

    def is_bindable(self, referent, entity, graph=None):
        """ Return if the referent element is considered co referent to the antecedent(and their possible coreferent chain)
        """
        if not graph:
            graph = referent.get_graph()
        # Filter properties to determine coregraph
        for pair_filter, joker in zip(self.pair_filters, self.joker_values):
            prop = graph.vertex_properties[pair_filter]
            if not((prop[referent] == prop[entity])) or (prop[referent] == joker) or (prop[entity] == joker):
                return False
        return True


class CandidateExtractor:

    def __init__(self, graph):
        self.graph= graph
        self.accessibility_graph = GraphView(graph,
            vfilt= lambda v:
            GraphWrapper.get_node_property(v, "type") == ContextGenerator.accessibility_edge_type)

    def sorting_function(self, referent, referent_candidate):
        #if GraphWrapper.get_node_property(referent,"type")
        pass

    def filter_function(self, referent):
        return True

    def enumerate_candidates_of(self, referent):
        """ Return the referent candidates of this referent that may point to the same entity.
        """
        filtered_referent = self.accessibility_graph.get_vertex(referent)
        candidates = filter(self.filter_function,
            sorted(filtered_referent.out_neibourgh(),
            key= lambda ref: self.sorting_function(referent, ref)
            ))

        return candidates





