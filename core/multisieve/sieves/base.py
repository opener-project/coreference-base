from graph.utils import GraphWrapper
from output.progressbar import Fraction, ProgressBar
from ..syntatic_tree_utils import SyntacticTreeUtils

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class Sieve(object):

    sort_name = "XXX"

    def __init__(self, multi_sieve_processor):

        self.multi_sieve_processor = multi_sieve_processor
        self.graph = self.multi_sieve_processor.graph

        self.tree_utils = SyntacticTreeUtils(graph=self.graph)

        self.relation_value = GraphWrapper.edge_property("value", self.graph)
        self.relation_type = GraphWrapper.edge_property("type", self.graph)
        self.node_type = GraphWrapper.node_property("type", self.graph)

        self.mention_form = GraphWrapper.node_property("form", self.graph)
        self.mention_tag = GraphWrapper.node_property("tag", self.graph)
        self.mention_type = GraphWrapper.node_property("mention_type", self.graph)
        self.mention_pos = GraphWrapper.node_property("pos", self.graph)
        self.mention_ner = GraphWrapper.node_property("ner", self.graph)
        self.mention_head = GraphWrapper.node_property("head", self.graph)
        self.mention_gender = GraphWrapper.node_property("gender", self.graph)
        self.mention_animacy = GraphWrapper.node_property("animate", self.graph)
        self.mention_number = GraphWrapper.node_property("number", self.graph)

    def link(self, entity, candidates,log, candidate_index, candidate):
        """Link the candidate to the entity. Remove from candidates.
        :param candidate: The candidate that is going to be promoted into mention entity.
        :param candidates: The candidate list of the entity.
        :param entity: The entity that is going to receive the mention
        """
        candidates[candidate_index].remove(candidate)
        entity.append(candidate)

    def are_coreferent(self, entity, index, candidate):
        """ Determine if the candidate is a valid entity coreferent.
        :param candidate: The candidate that is going evaluated.
        :param index: The index of the first mention of the entity that is valid for this sieve.
        :param entity: The entity that is going to be evaluated.
        """
        return False

    def valid_entity_index(self, entity):
        """Look up in the entity for the first valid mention. In no one is founded return None.
        :param entity: The entity that is going to be examined.
        """
        for index, mention in enumerate(entity):
            if self.validate(mention):
                return index
        return None

    def validate(self, mention):
        """ Determine if the mention is valid for this sieve.
        :param mention: The mention to check.
        """
        return self.mention_type[mention] != "indefinite_mention"

    def merge(self, clusters):
        """ Merge the cluster in a transitive function.
        Start for the first text appearance cluster(determined by his first mention)
        and merge entities but maintains the first cluster candidates.
        :param clusters: The list of pair entity candidatures that conform a text coreference proposal.
        """
        # For each cluster visit the others
        index = 0
        for entity, candidates, log in clusters:
            forward_index = index + 1
            for new_entity, new_candidates, new_log in clusters[forward_index:]:
                # Search if any other cluster is linked to this cluster
                for mention in entity:
                    # Search for a common mention
                    if mention in new_entity:
                        # The next cluster is coreferent to the original cluster
                        # Add the mentions to first entity
                        for mention_index, new_mention in enumerate(new_entity):
                            if new_mention not in entity:
                                entity.append(new_mention)
                                candidates.append(new_candidates[mention_index])
                                log.append(self.sort_name + "|" + new_log[mention_index])

                        #TODO Add the mention in correct position of the cluster
                        # Extract the mixed cluster
                        del clusters[forward_index]
                        forward_index -= 1
                        # this cluster was erased so next cluster has the same index
                        #  No further checks with the death cluster
                        break
                forward_index += 1
            index += 1

    def resolve(self, clusters):
        """Compare each cluster, formed by a tuple of a list of mentions and a list of candidates.
        :param clusters: The list of pair entity candidatures that conform a text coreference proposal.
        """
        self.clusters = clusters
        # TODO Question: merge after each link or at the end?
        widgets = ['Passing sieve {0}: '.format(self.__class__), Fraction()]
        progress_bar = ProgressBar(widgets=widgets, maxval=len(clusters), force_update=True).start()
        for cluster_index, (entity, candidates, log) in enumerate(clusters):
            candidate_index = self.valid_entity_index(entity)
            if candidate_index is not None:
                for candidate in candidates[candidate_index]:
                    if self.are_coreferent(entity, candidate_index, candidate):
                        # If passed the sieve link candidate and stop search for that entity
                        self.link(entity, candidates, log ,candidate_index, candidate)
                        # Break the search of candidates for this mention. Only one is elected
                        break
            progress_bar.update(cluster_index + 1)
        progress_bar.finish()
        self.merge(clusters)
        return clusters

    def entities_of_a_mention(self, mention):
        """ Return all the entities where a mention appears.
        :param mention: The mention whose entities are fetched.
        """
        return [entity for entity, candidates, log in self.clusters if mention in entity]

    def get_terminal_head(self, mention):
        """ Get the head WORD of a mention.
        :param mention: the mention whose head word is fetched.
        """
        for relation in mention.out_edges():
            # Only navigate syntactic relations
            if self.relation_type[relation] == "syntactic":
                child = relation.target()
                # Terminals always are unique
                if self.relation_value[relation] == "terminal":
                    return child
                else:
                    # If not a terminal deep into the head
                    if self.mention_head[child]:
                        return self.get_terminal_head(child)
                        # Everything gone wrong
        return None

    def entity_property(self, entity, property_name):
        return set([GraphWrapper.node_property(property_name, self.graph)[mention]
                    for mention in entity])

    def candidate_property(self, candidate, property_name):
        return set([GraphWrapper.node_property(property_name, self.graph)[mention]
                    for entity_involved in self.entities_of_a_mention(candidate) for mention in entity_involved])
