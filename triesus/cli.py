#!/usr/bin/env python3


import argparse
import sys
from triesus.run_triesus import run_triesus
from triesus.run_naive_sus import run_naive_sus


def parse_triesus_args():
    parser = argparse.ArgumentParser(
        prog="TrieSUS",
        description="Find the Smallest Unique Subset (SUS), fast.",
        epilog="See https://github.com/alussana/TrieSUS",
    )
    parser.add_argument("input", type=str, help="Path to the set collection.")
    parser.add_argument(
        "--extended",
        action="store_true",
        help="Reports all SUS if more than one optimal solution exists.",
    )
    parser.add_argument(
        "--naive",
        action="store_true",
        help="Runs the brute force version of the algorithm, based on the Gosper's Hack, instead of TrieSUS.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Main output table; if not specified it will be printed in STDOUT",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="v0.6.1",
        help="Print package version and exit",
    )
    args = parser.parse_args()
    return args


def main():
    print(
        f"""    
  ████████╗██████╗ ██╗███████╗███████╗██╗   ██╗███████╗
  ╚══██╔══╝██╔══██╗██║██╔════╝██╔════╝██║   ██║██╔════╝
     ██║   ██████╔╝██║█████╗  ███████╗██║   ██║███████╗
     ██║   ██╔══██╗██║██╔══╝  ╚════██║██║   ██║╚════██║
     ██║   ██║  ██║██║███████╗███████║╚██████╔╝███████║
     ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝
  
  Version 0.6.1
  Copyright (C) 2025 Alessandro Lussana
  MIT License
  
  Command: {' '.join(sys.argv)}
    """,
        file=sys.stderr,
    )

    args = parse_triesus_args()

    if args.naive:
        run_naive_sus(
            args.input,
            args.extended,
            args.output,
        )
    else:
        run_triesus(
            args.input,
            args.extended,
            args.output,
        )


if __name__ == "__main__":
    main()
