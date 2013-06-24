# coding=utf-8
__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'

import networkx as nx
from collections import defaultdict

class GraphWrapper():

    @classmethod
    def blank_graph(cls):
        graph = nx.MultiDiGraph()
        graph.graph["index"] = defaultdict(list)
        return graph

    @classmethod
    def link(cls, graph, origin, target, link_type=None, weight=None, label=None, value=None):
        """Link two nodes of the graph. The origin and target parameters  may be nodes ID or nodes if their ids if they
        contains their ID in an attribute called "id".
        """
        key = link_type
        properties = {}
        if link_type:
            properties['type'] = link_type
        if value:
            properties['value'] = value
        if weight:
            properties['weight'] = weight
        if label:
            properties['label'] = label
        if isinstance(origin, dict):
            origin = origin["id"]
        if isinstance(target, dict):
            target = target["id"]
        relation = graph.add_edge(origin, target, key=key, attr_dict=properties)
        return relation

    @classmethod
    def new_node(cls, graph, node_type, node_id, **narg):
        """
        :return: The key used to store the node
        """
        graph.add_node(node_id)
        node = graph.node[node_id]
        graph.graph["index"][node_type].append(node)
        node["id"] = node_id
        node["type"] = node_type
        for name, value in narg.items():
            if value is not None:
                node[name] = value
        return node

    @classmethod
    def get_graph_property(cls, graph, property_name):
        return graph.graph[property_name]

    @classmethod
    def set_graph_property(cls, graph, property_name, value):
        graph.graph[property_name] = value

    @classmethod
    def get_filtered_by_type_out_neighbours(cls, graph, node, relation_type):
        return [graph.node[target] for source, target, key in graph.out_edges_iter(node["id"], keys=True)
                if key == relation_type]

    @classmethod
    def get_filtered_by_type_in_neighbours(cls, graph, node, relation_type):
        return [graph.node[source] for source, target, key in graph.in_edges_iter(node["id"], keys=True)
                if key == relation_type]

    @classmethod
    def get_vertex_by_id(cls, graph, vertex_id):
        return graph.node[vertex_id]

    @classmethod
    def get_all_vertex_by_type(cls, graph, vertex_type):
        return graph.graph["index"][vertex_type]


    @classmethod
    def showGraph(cls, graph, root=None, vcolor=None, vshape=None, vlabel="label", elabel="label", output="",
                  layout="dot", **args):
        """ Prints the dependency graph using grahpviz.
        graph: The graph to output.
        output: The filename to output or screen if is equal to "".
        layout: The layout of the graph representation.

        """
        import matplotlib.pyplot as plt
        nx.draw(graph, )
        plt.savefig("out.png")
        plt.show()


    @classmethod
    def unlink(cls, origin, target):
        graph = origin.get_graph()
        for edge in graph.edge(origin, target, all_edges=True):
            graph.remove_edge(edge)
