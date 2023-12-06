<p align="center">
  <img width="312" height="312" src="https://i.imgur.com/uGRbTRH.png">
  <br>
  Find the Smallest Unique Subset (SUS), fast
  <br>
</p>

![Build and publish to PyPI badge](https://github.com/alussana/triesus/actions/workflows/build_and_publish_to_pypi.yml/badge.svg)

> Current version: `0.5.2`
>
> Please note that this software is still in development. It is supposed to work as intended in the current state and you are welcome to use it. The main changes expected before version `1.0.0` should involve documentation, code cleanup, and more flexible input options.

# Installation

## PyPI

```bash
pip install triesus
```

## From source

```bash
python -m build
pip install dist/triesus-*.whl
```

# Usage

Consider the following collection of sets. The first field denotes the set id, the following fields include the elements of the set. Fields are tab-separated:

```
1       C
2       A       B       D
3       B       E
4       A       D
```

The smallest unique subset (SUS) for each set in this collection can be found running:

```
triesus tests/examples/sets2.tsv
```

This will print in `STDOUT`:

```
1       C
2       D       B
3       E
4
```

Note that the SUS for set `4` does not exist.

# Performance

Below it's displayed the performance of TrieSUS compared with the [brute force baseline](#brute-force-approach) on randomly generated set collections. This analysis can be reproduced by cloning the [TrieSUS benchmark repository](https://github.com/alussana/TrieSUS-benchmark).

<p align="center">
  <br>
  <img width="900" height="" src="https://i.imgur.com/koe4Zut.png">
  <br>
</p>

The input size parameter is a number corresponding to three quantities: the number of sets in the collection, the number of items in the universe, and the maximum number of items in each set.

# Algorithm

Given a collection of sets, TrieSUS maps each set to the smallest possible combination of its elements that uniquely identifies the set, here called a smallest unique subset, or SUS.

## Brute force approach

To find the SUS of a set, a naive brute force approach would involve enumerating the non-empty subsets of the set from the smallest to the largest (for example using the [Gosper's Hack](https://read.seas.harvard.edu/~kohler/class/cs207-s12/lec12.html), as implemented in `naive_sus.find_sus()`), until finding one that is a solution, *i.e.* that is not a subset of any other set in the collection. This approach, even after taking some relatively obvious precautions such as making sure that potential solutions containing the least frequent elements in the collection are tested first, scales very badly with input size (see [Performance](#performance)). In fact, it has exponential time complexity of $O(2^n*m)$, where $n$ is the number of elements in each set (assuming all sets have equal size) and $m$ is the number of sets in the collection.

## TrieSUS

TrieSUS implements a series of linear-time operations to first greatly reduce the problem size, and to eventually transform it into the equivalent of a [set cover problem](https://en.wikipedia.org/wiki/Set_cover_problem). The set cover is an [NP-hard](https://en.wikipedia.org/wiki/NP-hardness) problem, but because of the reduced size of the input it will be treatable. TrieSUS uses Google's [OR-Tools](https://developers.google.com/optimization) constraint programming to solve it.

The algorithm starts by first ranking all the elements found in the sets of the collection from the most frequent to the least frequent, and sorting the elements in the sets according to these ranks. Each set is then treated as a sorted list to build a prefix tree (trie), where each leaf corresponds to a set. The construction of such a trie is not a strictly necessary step, but it may have advantages depending on the specific input. It can marginally reduce the number of operations in the following steps and it allows to immediately identify sets of the collection for which a solution doesn't exist, i.e. sets that don't have a SUS. Regardless, the construction of the trie is linear in time complexity and therefore doesn't significantly impact the performance of the algorithm.

The main part of the algorithm then performs a series of operations on the trie to find a SUS, if it exists, for each one of the sets, as implemented in `triesus.TrieSUS.find_sus()`. This method leverages the trie structure to efficiently track unique symbols among different words and applies a cover set solution to determine the smallest set of symbols that cover these unique items across different subsets within the trie.

The following is a high-level breakdown of the steps taken within the `find_sus()` method to identify the SUS for a set, here represented by a given "word" of ordered symbols:

1. Identify the end node for the given word:
    * Determine the end node within the trie structure that represents the given word.

2. Gather the other end nodes:
    * Collect all other end nodes within the trie that don't represent the given word. These nodes correspond to other words (sets) stored in the trie.

3. Check conditions for SUS existence: 
    * Verify conditions to determine if a SUS exists for the given word:
      * If the end node of the given word has children or if there's more than one identical word in the trie, then a SUS doesn't exist. The method returns an empty list in this case.

4. Identify unique symbols for each other end node:
    * For each of the other end nodes collected earlier:
      * Trace back from the end node of the given word to the common ancestor node shared with the other end node
      * Along this path, collect symbols unique to the given word that are not present in the other word.

5. Assemble candidate symbols:
    * Compile the sets of unique symbols obtained from the previous step into a list of sets.

6. Construct a dictionary of sets to cover:
    * Transform the list of sets into a dictionary where keys are items (symbols) of the sets and values are indexes of the sets. This prepares the data structure to solve the cover set problem. Finding the cover set on the indexes ensures that a minimum amount of candidate unique symbols is used to discriminate the given set from all the other sets of the collection.

7. Solve the cover set problem:
    * Use the OR-Tools constraint programming solver to find a solution. The solution [...] is a SUS of the given set.

8. Return the result:
    * Return the identified SUS or an empty list if no unique subset satisfying the conditions is identified.

## The unique subset problem in the wild

The algorithmic problem that TrieSUS is intended to solve is discussed in several occasions, of which some are highlighted here:

* In this [Stack Overflow question](https://stackoverflow.com/questions/63514798) (Aug 21, 2020), a solution was proposed to find the SUS of a set `s` by first counting how many times each element in `s` appears in the other sets. It then sorts the elements in `s` based on this count, and considers all possible sub-arrays of `s`, returning the first one that satisfies the condition that it appears in exactly one set in the collection. If no such subset is found, the function returns `null`.
This procedure is repeated for every set in the collection.

* The same problem also appears in this [Stack Exchange question](https://math.stackexchange.com/questions/2436161) (Sep 19, 2017), where no answer was given at the time of writing.

* The code implementing a brute force approach that compares all the powersets was shared in an answer to this [Stack Overflow question](https://stackoverflow.com/questions/48459376/finding-the-unique-subset-of-elements-in-list-of-sets0) (Jan 26, 2018).