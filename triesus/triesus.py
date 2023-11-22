#!/usr/bin/env python3


from collections import Counter
from triesus.trie import *
from triesus.cover_set import solve_cover_set


class TrieSUS(Trie):
    def __init__(self, collection: dict):
        super().__init__()
        self.item_counts = self.get_item_counts(collection)
        self.sorted_items = self.sort_keys_by_value(self.item_counts)
        self.symbol_ranks = self.rank_dict_from_keys_list(self.sorted_items)
        self.counts_to_symbols = self.reverse_mapping(self.item_counts)
        self.collection = self.sort_collection_by_other_list_order(
            collection, self.sorted_items
        )
        words = [item for key, item in self.collection.items()]
        for word in words:
            self.insert(word)

    def reverse_mapping(self, A: dict) -> dict:
        """Creates a new dictionary B from an existing dictionary A with values as keys and list of corresponding keys as values.

        Args:
            A: A dictionary where different keys are mapped to different values. All keys are different but some values can be the same.

        Returns:
            A new dictionary B where the keys are the values of dictionary A, and the values are the list of corresponding keys in dictionary A.
        """

        B = {}

        for key, value in A.items():
            if value not in B:
                B[value] = set()

            B[value].add(key)

        return B

    def transpose_dict(self, A: dict):
        """
        Create a new dictionary of sets B, where the keys are the items found in the sets
        of dictionary A, and the values are the corresponding keys in the dictionary A.

        Parameters:
        - A (dict): The input dictionary of sets.

        Returns:
        - dict: The new dictionary of sets B.
        """
        B = {}

        for key, value_set in A.items():
            for item in value_set:
                if item not in B:
                    B[item] = set()
                B[item].add(key)

        return B

    def get_item_counts(self, collection: dict) -> dict:
        item_list = []
        for key, item in collection.items():
            item_list = item_list + item
        item_count_dict = {}
        for item_str in item_list:
            if item_str in item_count_dict:
                item_count_dict[item_str] += 1
            else:
                item_count_dict[item_str] = 1
        return item_count_dict

    def find_most_frequent_item(self, list_of_sets):
        """Returns the item that appears most frequently in a list of sets.

        Args:
          set_list: A list of sets.

        Returns:
          The item that appears most frequently in the sets, or None if the list is empty.
        """

        # Create a counter object to track the frequency of each item.
        counter = Counter()
        for set in list_of_sets:
            for item in set:
                counter[item] += 1

        most_frequent_item = counter.most_common(1)[0][0]

        return most_frequent_item

    def sort_keys_by_value(self, dict_obj: dict) -> list:
        items = list(dict_obj.items())
        items.sort(key=lambda x: x[1], reverse=True)
        sorted_keys = [item[0] for item in items]
        return sorted_keys

    def rank_dict_from_keys_list(self, keys_list: list):
        rank_dict = {}
        for i, key in enumerate(keys_list):
            rank_dict[key] = i + 1
        return rank_dict

    def sort_list_by_other_list_order(self, my_list: list, other_list: list) -> list:
        item_to_index = {
            item: other_list.index(item) for item in my_list if item in other_list
        }
        sorted_list = sorted(
            my_list, key=lambda x: item_to_index.get(x, len(other_list))
        )
        return sorted_list

    def sort_collection_by_other_list_order(
        self, collection_dict: dict, sorted_items_list: list
    ) -> dict:
        for key in collection_dict.keys():
            collection_dict[key] = self.sort_list_by_other_list_order(
                collection_dict[key], sorted_items_list
            )
        return collection_dict

    def get_prefix_symbols(self, node: TrieNode):
        prefix = [node.symbol]
        prefix = prefix + [x.symbol for x in self.prefix_from_node(node)]
        prefix = prefix[:-1]
        prefix = list(reversed(prefix))
        return prefix

    def get_common_ancestor(self, node_a, node_b):
        a_nodes = {node_a}
        node = node_a
        while node != self.root:
            node = node.parent
            a_nodes.add(node)

        node = node_b
        found = False
        while found == False:
            if node in a_nodes:
                found = True
            else:
                node = node.parent

        return node

    def find_sus(self, word):
        word_end_node = self.end_node_for_word(word)
        other_end_nodes = [node for node in self.end_nodes if node != word_end_node]

        if len(word_end_node.children) != 0 or word_end_node.words_ending_here > 1:
            # if word_end_node has children, or there is an identical word,
            # the SUS doesn't exist, terminate here
            return []

        candidate_symbols = []  # list of sets

        for end_node in other_end_nodes:
            current_word_node = word_end_node

            unique_items = set()

            trie_word = set(self.get_prefix_symbols(end_node))

            # determine where the two words intersect in the trie
            common_ancestor_node = self.get_common_ancestor(word_end_node, end_node)

            while current_word_node != common_ancestor_node:
                if current_word_node.symbol not in trie_word:
                    unique_items.add(current_word_node.symbol)

                current_word_node = current_word_node.parent

            if len(unique_items) == 0:
                return []

            candidate_symbols.append(unique_items)

        candidates_dict = {}
        for i in range(len(candidate_symbols)):
            candidates_dict[i] = candidate_symbols[i]
        sets_to_cover = self.transpose_dict(candidates_dict)

        sus, status = solve_cover_set(sets_to_cover)

        return sus
