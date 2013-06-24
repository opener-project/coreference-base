from graph.kafx import SyntacticTreeUtils
from graph.xutils import GraphWrapper
from output.progressbar import Fraction, ProgressBar

__author__ = 'Josu Bermudez <josu.bermudez@deusto.es>'


class Sieve(object):

    sort_name = "XXX"

    def __init__(self, multi_sieve_processor):

        self.multi_sieve_processor = multi_sieve_processor
        self.graph = self.multi_sieve_processor.graph
        self.graph_builder = GraphWrapper.get_graph_property(self.graph, "graph_builder")

        self.tree_utils = SyntacticTreeUtils(graph=self.graph)

    def link(self, entity, candidate):
        """Link the candidate to the entity. Remove from candidates.
        :param candidate: The candidate that is going to be promoted into mention entity.
        :param candidates: The candidate list of the entity.
        :param entity: The entity that is going to receive the mention
        """

        entity.append(candidate)

    def are_coreferent(self, entity, mention, candidate):
        """ Determine if the candidate is a valid entity coreferent.
        :param candidate: The candidate that is going evaluated.
        :param mention: The index of the first mention of the entity that is valid for this sieve.
        :param entity: The entity that is going to be evaluated.
        """
        return False

    def valid_mention(self, entity):
        """Look up in the entity for the first valid mention. In no one is founded return None.
        :param entity: The entity that is going to be examined.
        """
        for mention in entity:
            if self.validate(self.graph.node[mention]):
                return mention
        return None

    def validate(self, mention):
        """ Determine if the mention is valid for this sieve.
        :param mention: The mention to check.
        """
        return mention["mention"] != "undefined_mention"

    def merge(self, clusters, registers):
        """ Merge the cluster in a transitive function.
        Start for the first text appearance cluster(determined by his first mention)
        and merge entities but maintains the first cluster candidates.
        :param clusters: The list of pair entity candidatures that conform a text coreference proposal.
        :param registers: The list of strings that keep the record of merges that suffers a cluster.
        """

        index = 0
        # For each cluster(Base Cluster) visit the next clusters
        for entity in clusters:
            forward_index = index + 1
            # Search if next clusters(Mergeable) are linked to this cluster
            for new_entity in clusters[forward_index:]:
                # Two clusters are linked in have at least one common mention
                # Search for a common mention
                for mention in entity:
                    # Are linked?
                    if mention in new_entity:
                        # The next cluster is coreferent to the original cluster
                        # Add the new mentions to first cluster
                        for new_mention in new_entity:
                            # A mention is new if doesn't exist in original cluster
                            if new_mention not in entity:
                                entity.append(new_mention)
                                # Add a register for debug proposes
                                registers[index] += self.sort_name + "|" + registers[forward_index]
                        # Reorder the mixed cluster
                        entity.sort(key=lambda x: self.graph.node[x]["span"])
                        #TODO reorder the mentions in textual order in the cluster
                        # remove the merged cluster
                        del clusters[forward_index]
                        del registers[forward_index]
                        # this cluster was erased so next cluster has the same index
                        forward_index -= 1
                        # No further checks with the death cluster
                        break
                # Nest cluster (Mergeable cluster)
                forward_index += 1
            # Next cluster (Base cluster)
            index += 1

    def resolve(self, clusters, candidates_per_mention, register):
        """Compare each cluster, formed by a tuple of a list of mentions and a list of candidates.
        :param clusters: The list of pair entity candidatures that conform a text coreference proposal.
        """
        self.clusters = clusters
        # TODO Question: merge after each link or at the end?
        widgets = ['Passing sieve {0}: '.format(self.__class__), Fraction()]
        progress_bar = ProgressBar(widgets=widgets, maxval=len(clusters) or 1, force_update=True).start()
        for cluster_index, entity in enumerate(clusters):
            # Get the first mention of the entity that is valid for the sieve
            mention = self.valid_mention(entity)
            if mention is not None:
                for candidate in candidates_per_mention[mention]:
                    if self.are_coreferent(entity, self.graph.node[mention], self.graph.node[candidate]):
                        # If passed the sieve link candidate and stop search for that entity
                        self.link(entity, candidate)
                        # Break the search of candidates for this mention. Only one is elected
                        break
            progress_bar.update(cluster_index + 1)
        progress_bar.finish()
        self.merge(clusters, register)
        return clusters

    def entities_of_a_mention(self, mention):
        """ Return all the entities where a mention appears.
        :param mention: The mention whose entities are fetched.
        """
        return [
            entity
            for entity in self.clusters if mention["id"] in entity]

    def entity_property(self, entity, property_name):
        return set((
            self.graph.node[mention][property_name]
            for mention in entity))

    def candidate_property(self, candidate, property_name):
        return set((
            property_value
            for entity_involved in self.entities_of_a_mention(candidate)
            for property_value in self.entity_property(entity_involved, property_name)))
