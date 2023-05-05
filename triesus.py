#!/usr/bin/env python3

# Alessandro Lussana <alussana@ebi.ac.uk>

class TrieNode:
    def __init__(self, parent=None, symbol=None):
        self.parent = parent
        self.children = {}
        self.is_end_of_word = False
        self.symbol = symbol
    
class Trie:
    def __init__(self, symbol_ranks: dict):
        self.root = TrieNode()
        self.end_nodes = []
        self.symbol_ranks = symbol_ranks
    def insert(self, word):
        current = self.root
        for letter in word:
            if letter not in current.children:
                current.children[letter] = TrieNode(parent=current, symbol=letter)
            current = current.children[letter]
        current.is_end_of_word = True
        self.end_nodes.append(current)
    def search(self, word):
        current = self.root
        for letter in word:
            if letter not in current.children:
                return False
            current = current.children[letter]
        return current.is_end_of_word
    def starts_with(self, prefix):
        current = self.root
        for letter in prefix:
            if letter not in current.children:
                return False
            current = current.children[letter]
        return True
    def end_node_for_word(self, word):
        current = self.root
        for letter in word:
            if letter not in current.children:
                return None
            current = current.children[letter]
        return current
    def prefix_from_node(self, node):
        prefix = []
        current = node
        while current.parent != None:
            prefix.append(current.parent)
            current = current.parent
        return prefix
    def find_sus(self, word):
        sus = []
        word_end_node = self.end_node_for_word(word)
        other_end_nodes = [node for node in self.end_nodes if node != word_end_node]
        if len(word_end_node.children) != 0:
            return []
        sus.append(word_end_node.symbol)
        for end_node in other_end_nodes:
            current_word_node = word_end_node
            current_trie_node = end_node
            while self.symbol_ranks[current_trie_node.symbol] >= self.symbol_ranks[current_word_node.symbol]:
                if current_trie_node.symbol == current_word_node.symbol:
                    if current_word_node.parent.parent == None:
                        return []
                    else:
                        current_word_node = current_word_node.parent
                        if current_word_node.symbol not in sus:
                            sus.append(current_word_node.symbol)
                if current_trie_node.parent.parent != None:
                    current_trie_node = current_trie_node.parent
                else:
                    break   
        return sus
    
def read_collection(file_tsv:str) -> dict:
    with open(file_tsv) as file_fh:
        collection_dict = {}
        for line_str in file_fh:
            fields_list = line_str.strip().split('\t')
            set_id_str = fields_list.pop(0)
            collection_dict[set_id_str] = fields_list
    return collection_dict
            
def item_counts(collection_dict: dict) -> dict:
    item_list = []
    for key,item in collection_dict.items():
        item_list = item_list + item
    item_count_dict = {}
    for item_str in item_list:
        if item_str in item_count_dict:
            item_count_dict[item_str] += 1
        else:
            item_count_dict[item_str] = 1
    return item_count_dict

def sort_keys_by_value(dict_obj: dict) -> list:
    items = list(dict_obj.items())
    items.sort(key=lambda x: x[1], reverse=True)
    sorted_keys = [item[0] for item in items]
    return sorted_keys

def rank_dict_from_keys_list(keys_list: list):
    rank_dict = {}
    for i, key in enumerate(keys_list):
        rank_dict[key] = i + 1
    return rank_dict

def sort_list_by_other_list_order(my_list: list, other_list: list) -> list:
    item_to_index = {item: other_list.index(item) for item in my_list if item in other_list}
    sorted_list = sorted(my_list, key=lambda x: item_to_index.get(x, len(other_list)))
    return sorted_list

def sort_collection_by_other_list_order(collection_dict: dict, sorted_items_list: list) -> dict:
    for key in collection_dict.keys():
        collection_dict[key] = sort_list_by_other_list_order(collection_dict[key], sorted_items_list)
    return collection_dict

def run_triesus(collection_tsv: str) -> None:
    collection_dict = read_collection(collection_tsv)
    item_counts_dict = item_counts(collection_dict)
    sorted_item_list = sort_keys_by_value(item_counts_dict)
    symbol_ranks = rank_dict_from_keys_list(sorted_item_list)
    collection_dict_sorted = sort_collection_by_other_list_order(collection_dict, sorted_item_list)
    triesus = Trie(symbol_ranks)
    words = [item for key,item in collection_dict_sorted.items()]
    for word in words:
        triesus.insert(word)
    for key,item in collection_dict_sorted.items():
        sus = triesus.find_sus(item)
        sus = '\t'.join(sus)
        print(f'{key}\t{sus}')

def main():
    import sys
    run_triesus(sys.argv[1])
        
if __name__ == '__main__':
    main()