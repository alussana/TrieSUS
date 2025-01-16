<p align="center">
  <img width="312" height="312" src="https://i.imgur.com/uGRbTRH.png">
  <br>
  Find the Smallest Unique Subset (SUS), fast
  <br>
</p>

![Build and publish to PyPI badge](https://github.com/alussana/triesus/actions/workflows/build_and_publish_to_pypi.yml/badge.svg)

> Current version: `0.6.1`
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

A smallest unique subset (SUS) for each set in this collection can be found running:

```bash
triesus tests/examples/sets2.tsv
```

This will print in `STDOUT`:

```
1       C
2       D       B
3       E
4
```

Note that no SUS exists for set `4`. Also, for each set there may be more than one optimal solution, as it is the case for set `2`. To find all solutions, run use the `--extended` version of the algorithm:

```bash
triesus --extended tests/examples/sets2.tsv
```

Every SUS will be printed on a new line:

```
1       C
2       B       A
2       D       B
3       E
4
```

For a complete set of command line arguments, run `triesus -h`:

```
usage: TrieSUS [-h] [--extended] [--naive] [-o OUTPUT] [-v] input

Find the Smallest Unique Subset (SUS), fast.

positional arguments:
  input                 Path to the set collection.

optional arguments:
  -h, --help            show this help message and exit
  --extended            Reports all SUS if more than one optimal solution exists.
  --naive               Runs the brute force version of the algorithm, based on the Gosper's Hack, instead of TrieSUS.
  -o OUTPUT, --output OUTPUT
                        Main output table; if not specified it will be printed in STDOUT
  -v, --version         Print package version and exit

See https://github.com/alussana/TrieSUS
```

# Performance

Below it is displayed the performance of TrieSUS compared with the [brute force baseline](#brute-force-approach) on randomly generated set collections. This analysis can be reproduced by cloning the [TrieSUS benchmark repository](https://github.com/alussana/TrieSUS-benchmark).

<p align="center">
  <br>
  <img width="900" height="" src="https://i.imgur.com/koe4Zut.png">
  <br>
</p>

The input size parameter is a number corresponding to three quantities: the number of sets in the collection, the number of items in the universe, and the maximum number of items in each set.

# Algorithm

Given a collection of sets, TrieSUS maps each set to the smallest possible combination of its elements that uniquely identifies the set, here called a Smallest Unique Subset, or SUS. In other words, a SUS of a set is the smallest subset of its elements that does not exist as a subset of any other set in the collection.

## Brute force approach

To find the SUS of a set, a naive brute force approach would involve enumerating the non-empty subsets of the set from the smallest to the largest using the [Gosper's Hack](https://read.seas.harvard.edu/~kohler/class/cs207-s12/lec12.html), until finding one that is a solution, *i.e.* that is not a subset of any other set in the collection. Running `triesus` with the `--naive` flag will result in this behavior. This approach, even after taking some relatively obvious precautions such as making sure that potential solutions containing the least frequent elements in the collection are tested first, scales very badly with input size (see [Performance](#performance)). In fact, it has exponential time complexity of $O(2^nm)$, where $n$ is the number of elements in each set (assuming all sets have equal size) and $m$ is the number of sets in the collection.

## TrieSUS

TrieSUS implements a series of linear-time operations to first greatly reduce the problem size, and to eventually transform it into the equivalent of a [set cover problem](https://en.wikipedia.org/wiki/Set_cover_problem). The set cover is an [NP-hard](https://en.wikipedia.org/wiki/NP-hardness) problem, but because of the reduced size of the input it will be treatable. TrieSUS uses Google's [OR-Tools](https://developers.google.com/optimization) constraint programming to solve it.

The algorithm starts by first ranking all the elements found in the sets of the collection from the most frequent to the least frequent, and sorting the elements in the sets according to these ranks. Each set is then treated as a sorted list to build a prefix tree (trie), where each leaf corresponds to a set. The construction of such a trie is not a strictly necessary step, but it may have advantages depending on the specific input. It can reduce the number of operations in the following steps and it allows to immediately identify sets of the collection for which a solution doesn't exist, i.e. sets that don't have a SUS. Regardless, the construction of the trie is linear in time complexity and therefore doesn't significantly impact the performance of the algorithm.
For each one of the sets, a series of operations on the trie to find _a_ SUS (or _all_ SUS, in the `--extended` version), if it exists, is then performed as implemented in `triesus.TrieSUS.find_sus()`. This method uses a combination of trie-based data structures and constraint programming techniques. Below is a description of how the algorithm operates when reporting only a single solution for each set:

1. **Preprocessing and Trie Construction**
    - **Input:** A collection of sets represented as a dictionary, where each key corresponds to a set and the values are the elements of the set.
    - **Steps:**
      - Compute the frequency of each element in the collection This identifies how often each element appears across all sets.
      - Sort the elements by frequency in descending order. This helps optimize trie construction by prioritizing commonly occurring elements.
      - Rank the elements based on their frequency, creating a ranking dictionary for efficient lookups.
      - Reorder the elements within each set to align with the sorted order of elements. This ensures that sets with similar contents are organized consistently when inserted into the trie.
    - **Trie Construction:**
      - Each set is inserted into a trie, where the path from the root to a leaf node corresponds to the elements of a set. The order of insertion respects the element ranking derived in preprocessing.
      - Each node in the trie tracks its parent, its symbol (the corresponding element), and whether it is the endpoint of a set (leaf node).
2. **Identifying Unique Subset (SUS)**
    - **Trie operations:**
      - For a given set, traverse the trie to locate its endpoint. The endpoint signifies the completion of the path representing the set in the trie.
      - Check the endpoint's properties:
        - If it has children or multiple identical sets terminate at this node, no SUS exists for the set.
      - Compare this endpoint with the endpoints of all other sets in the trie to identify differences:
        - For each other endpoint, find the common ancestor (the deepest node in the trie shared by both sets).
        - Traverse upwards from the current set's endpoint to the common ancestor, collecting symbols not found in the other set's path.
    - **Building Constraints for Coverage:**
      - Collect sets of candidate symbols for each comparison. These represent symbols that differentiate the current set from others.
      - Construct a **Set Cover Problem** where the objective is to select the smallest number of symbols from the candidates such that all constraints are satisfied (i.e., each other set is sufficiently distinguished).
3. **Solving the Set Cover Problem**
    - The OR-Tools Constraint Programming Solver is used to solve the Set Cover Problem:
      - A binary variable is created for each candidate symbol, indicating whether it is included in the SUS.
      - Constraints ensure that the selected symbols collectively distinguish the current set from all others.
      - The objective is to minimize the number of selected symbols.
    - The solver identifies the minimal SUS and returns it as the unique distinguishing subset for the current set.
4. **Output**
    - For each set in the collection, the algorithm outputs the SUS that uniquely identifies the set.

## The unique subset problem in the wild

The algorithmic problem that TrieSUS is intended to solve is discussed in several occasions, of which some are highlighted here:

* In this [Stack Overflow question](https://stackoverflow.com/questions/63514798) (Aug 21, 2020), a solution was proposed to find the SUS of a set `s` by first counting how many times each element in `s` appears in the other sets. It then sorts the elements in `s` based on this count, and considers all possible sub-arrays of `s`, returning the first one that satisfies the condition that it appears in exactly one set in the collection. If no such subset is found, the function returns `null`.
This procedure is repeated for every set in the collection.

* The same problem also appears in this [Stack Exchange question](https://math.stackexchange.com/questions/2436161) (Sep 19, 2017), where no answer was given at the time of writing.

* The code implementing a brute force approach that compares all the powersets was shared in an answer to this [Stack Overflow question](https://stackoverflow.com/questions/48459376/finding-the-unique-subset-of-elements-in-list-of-sets0) (Jan 26, 2018).