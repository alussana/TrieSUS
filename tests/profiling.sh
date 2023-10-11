#!/usr/bin/env bash

python -m cProfile -o cprof_results tests/test_triesus.py
echo 'stats' | python3 -m pstats cprof_results > profile_triesus

echo

python -m cProfile -o cprof_results tests/test_naive_sus.py
echo 'stats' | python3 -m pstats cprof_results > profile_naive_sus