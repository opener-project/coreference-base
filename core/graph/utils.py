__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

from graph_tool.all import *


class GraphWrapper():

    @classmethod
    def blank_graph(cls):
        return Graph()

    @classmethod
    def link(cls, graph, origin, target, node_type=None, weight=None, label=None, value=None, ):
        relation = graph.add_edge(origin, target)
        if node_type:
            graph.edge_properties['type'][relation] = node_type
        if value:
            graph.edge_properties['value'][relation] = value
        if weight:
            graph.edge_properties['weight'][relation] = weight
        if label:
            graph.edge_properties['label'][relation] = label
        return relation

    @classmethod
    def new_node(cls, graph, **argn):
        """
        :rtype : graph_tool.Vertex
        """
        node = graph.add_vertex()
        for name, value in argn.items():
            graph.vertex_properties[name][node] = value
        return node

    @classmethod
    def define_properties(cls, graph, graph_properties=None, vertex_properties=None, edge_properties=None):
        """
        :type graph_properties: dict
        """
        if graph_properties:
            for name, property_type_name in graph_properties.items():
                if not name in graph.graph_properties:
                    graph.graph_properties[name] = graph.new_graph_property(property_type_name)
        if vertex_properties:
            for name, property_type_name in vertex_properties.items():
                if not name in graph.vertex_properties:
                    graph.vertex_properties[name] = graph.new_vertex_property(property_type_name)
        if edge_properties:
            for name, property_type_name in edge_properties.items():
                if not name in graph.edge_properties:
                    graph.edge_properties[name] = graph.new_edge_property(property_type_name)

    if graph_tool.__version__.startswith("2.2.19 "):

        @classmethod
        def set_properties(cls, graph=None, node=None, edge=None, graph_properties=None, vertex_properties=None,
                           edge_properties=None):
            if graph_properties:
                for name, property_value in graph_properties.items():
                    graph.graph_properties[name] = property_value
            if vertex_properties:
                for name, property_value in vertex_properties.items():
                    graph.vertex_properties[name][node] = property_value
            if edge_properties:
                for name, property_value in edge_properties.items():
                    graph.edge_properties[name][edge] = property_value

        @classmethod
        def get_graph_property(cls, graph, property_name):
            return graph.graph_properties[property_name]

        @classmethod
        def set_graph_property(cls, graph, property_name, value):
            graph.graph_properties[property_name] = value
    else:

        @classmethod
        def set_properties(cls, graph=None, node=None, edge=None, graph_properties=None, vertex_properties=None,
                           edge_properties=None):
            if graph_properties:
                for name, property_value in graph_properties.items():
                    #graph.graph_properties[name][graph] = property_value
                    graph.graph_properties[name] = property_value
            if vertex_properties:
                for name, property_value in vertex_properties.items():
                    graph.vertex_properties[name][node] = property_value
            if edge_properties:
                for name, property_value in edge_properties.items():
                    graph.edge_properties[name][edge] = property_value

        @classmethod
        def get_graph_property(cls, graph, property_name):
            #return graph.graph_properties[property_name][graph]
            return graph.graph_properties[property_name]
        @classmethod
        def set_graph_property(cls, graph, property_name, value):
            #graph.graph_properties[property_name][graph] = value
            graph.graph_properties[property_name] = value

    @classmethod
    def node_property(cls, name, graph):
        return graph.vertex_properties[name]

    @classmethod
    def edge_property(cls, name, graph):
        return graph.edge_properties[name]

    @classmethod
    def get_node_property(cls, node, name, graph=None):
        graph = graph or node.get_graph()
        return graph.vertex_properties[name][node]

    @classmethod
    def get_edge_property(cls, edge, name, graph=None):
        graph = graph or edge.get_graph()
        return graph.edge_properties[name][edge]

    @classmethod
    def get_filtered_by_type_out_neighbours(cls, node, relation_type, graph=None):
        graph = graph or node.get_graph()
        edge_type = graph.edge_properties["type"]
        return [edge.target() for edge in filter(lambda x: edge_type[x] == relation_type, node.out_edges())]

    @classmethod
    def get_filtered_by_type_in_neighbours(cls, node, relation_type, graph=None):
        graph = graph or node.get_graph()
        edge_type = graph.edge_properties["type"]
        return [edge.source() for edge in filter(lambda x: edge_type[x] == relation_type, node.in_edges())]

    @classmethod
    def get_in_edges_filtered_by_types(cls, node, relation_type, graph=None):
        graph = graph or node.get_graph()
        edge_type = graph.edge_properties["type"]
        return [edge for edge in filter(lambda x: edge_type[x] == relation_type, node.in_edges())]

    @classmethod
    def get_out_edges_filtered_by_types(cls, node, relation_type, graph=None):
        graph = graph or node.get_graph()
        edge_type = graph.edge_properties["type"]
        return [edge for edge in filter(lambda x: edge_type[x] == relation_type, node.out_edges())]

    @classmethod
    def get_vertex_by_id(cls, graph, vertex_id):
        return find_vertex(graph, graph.vertex_properties['id'], vertex_id)[0]

    @classmethod
    def get_all_vertex_by_type(cls, graph, vertex_type):
        return find_vertex(graph, graph.vertex_properties['type'], vertex_type)

    @classmethod
    def get_all_vertex_by_property(cls, graph, vertex_property, value):
        return find_vertex(graph, graph.vertex_properties[vertex_property], value)

    @classmethod
    def showGraph(cls, graph, root=None, vcolor=None, vshape=None, vlabel="label", elabel="type", output="",
                  layout="dot", **args):
        """ Prints the dependency graph using grahpviz.
        graph: The graph to output.
        output: The filename to output or screen if is equal to "".
        layout: The layout of the graph representation.

        """
        vprops = {}
        eprops = {}
        gprops = {}
        if vlabel:
            vprops['label'] = graph.vertex_properties[vlabel]
        if vcolor:
            vprops['fillcolor'] = graph.vertex_properties[vcolor]
        if vshape:
            vprops['shape'] = graph.vertex_properties[vshape]
        if elabel:
            eprops['label'] = graph.edge_properties[elabel]
        if root:
            gprops['root'] = graph.graph_properties[root]

        graphviz_draw(graph, layout=layout, output=output, gprops=gprops, vprops=vprops, eprops=eprops, **args)

    @classmethod
    def show_graph_as_strings(cls, graph):
        """Show graph as string ternas => dependency(governor_word, dependant_word) """
        dependencies_string = []
        for edge in graph.edges():
            dependencies_string.append("{}({}, {})".format(
                graph.edge_properties['type'][edge],
                graph.vertex_properties['form'][edge.source()],
                graph.vertex_properties['form'][edge.target()]
            ))
        dependencies_string.append("\n")
        print  "\n".join(dependencies_string)

    @classmethod
    def unlink(cls, origin, target):
        graph = origin.get_graph()
        for edge in graph.edge(origin, target, all_edges=True):
            graph.remove_edge(edge)
