<p align="center">
  <img width="372" height="372" src="https://raw.githubusercontent.com/alussana/TrieSUS/7bae8f44d52fe3b4e7a813d237f2a86465c1ac2c/assets/triesus_logo.png">
  <br>
  Find the Smallest Unique Subset (SUS), in linear time
  <br>
</p>

![Build and publish to PyPI badge](https://github.com/alussana/triesus/actions/workflows/build_and_publish_to_pypi.yml/badge.svg)

## Installation

### PyPI

[TrieSUS](https://pypi.org/project/triesus/) is on the [Python Package Index](https://pypi.org) and can be installed with [pip](https://pip.pypa.io/en/stable/):

```bash
pip install triesus
```

### From source

```bash
python -m build
pip install dist/triesus-*.whl --force-reinstall
```

### Development

```bash
pip install -e .
```

## Usage

Consider the following collection of sets (the first field denotes the set id, the following fields are elements of the set. Fields are tab-separated):

```
1       C
2       A       B       D
3       B       E
4       A       D
```

The Smallest Unique Subset (SUS) for each set in this collection can be found running 

```
triesus tests/examples/sets2.tsv
```

which will print in `STDOUT`:

```
1       C
2       D       B
3       E
4
```

Note that the SUS for set `4` does not exist.

## Algorithm

Given a collection of sets, TrieSUS maps each set to the smallest possible combination of its elements that uniquely identifies the set, in linear time.

The algorithmic problem that TrieSUS is intended to solve was discussed in this [StackOverflow question](https://stackoverflow.com/questions/63514798):

> *[...]*
> 
>  I have multiple sets with elements that are unique within each set, but may not be unique across all sets. How can I find the smallest possible subset of each set such that each subset is unique?
>
> *[...]*

A solution was proposed to find the SUS of a set `s` by first counting how many times each element in `s` appears in the other sets. It then sorts the elements in `s` based on this count, and considers all possible sub-arrays of `s`, returning the first one that satisfies the condition that it appears in exactly one set in the collection. If no such subset is found, the function returns `null`.
This procedure is repeated for every set in the collection.

`TrieSUS` adopts a different approach: it first ranks all the elements found in the sets of the collection from the most frequent to the least frequent. Then, it sorts the elements in the sets according to those ranks. Each set is then treated as a sorted list to build a prefix tree. Finally, for each set an efficient procedure (see [Pseudocode](#pseudocode)) that uses the prefix tree is followed to 1) determine whether a SUS exists, and 2) if appropriate, return a SUS.

The same problem also appears in this other [StackExchange question](https://math.stackexchange.com/questions/2436161), where no answer was given at the time of writing.

### Pseudocode [TODO]

The function that returns a SUS is described below, and it corresponds to `triesus.TrieSus.find_sus()` in the codebase. It is assumed that the following relevant functions or data structures are available: 

* `word`: list of strings. The items (symbols) of the set for which we want to find the smallest unique subset.
* `symbol_ranks`: dictionary mapping each key to its corresponding rank. The item (symbol) occurring most frequently in the sets of the collection is given rank `1`.
* `trie`: a prefix tree
  * `end_nodes`: attribute of `trie`. List of nodes that mark the end of the words in the prefix tree.
  * Each node in `trie` has the following attributes:
    * `symbol`: a string. An item found in the the collection of sets
    * `parent`: the parent node of the node in the prefix tree
* `end_node_for_word`: function that takes in input a `word` and a `trie`, and returns the node that marks the end of that word in the prefix tree.

```{bash}
```

## TODO

- [ ] update pseudocode section
- [ ] add argparse features to manage input options
- [ ] add benchmark
- [ ] add another reference [SO question](https://stackoverflow.com/questions/48459376/finding-the-unique-subset-of-elements-in-list-of-sets)