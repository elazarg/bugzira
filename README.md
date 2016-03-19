# bugzira
feature extraction from JIRA

## tl;dr

    ./sha1_issue.sh ../hadoop | python extract_jira.py

## preparation
run

    ./sha1_issue.sh git_folder
for example

    ./sha1_issue.sh ../cassandra > cassandra.map.txt
by default, the basename of the folder is taken to be the component name

## extraction
(note: the project is python3.4+)

run 

    python extract_jira.py < map_filename

for example

    python extract_jira.py < cassandra.map.txt
