#!/usr/bin/env python3

# Alessandro Lussana <alussana@ebi.ac.uk>

from triesus.trienode import *
    
class TrieSUS:
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