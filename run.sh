#!/bin/bash
./find_commits.sh $1 | python fetch_and_extract.py $2
