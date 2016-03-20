# bugzira
feature extraction from JIRA

## tl;dr

    ./find_commits.sh ../hadoop | python fetch_and_extract.py csv

## preparation
run

    ./find_commits.sh git_folder
for example

    ./find_commits.sh ../cassandra > cassandra.map.txt
by default, the basename of the folder is taken to be the component name

## extraction
(note: the project is python3.4+)

run 

    python fetch_and_extract.py < map_filename

for example

    python fetch_and_extract.py < cassandra.map.txt
