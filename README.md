# bugzira
feature extraction from JIRA

## Examples
    
    $ ./run.sh ../cassandra 
    Projects found: CASSANDRA
    {"commit":"26ad322358df31a6f9d6f078e45ebfb2beb52b56","issuetype":"Bug","key":"1686","priority":"4","project":"CASSANDRA","resolution":"1","status":"5","summary":"'o.a.c.dht.AbstractBounds missing serialVersionUID'"}
    {"commit":"34207f0a92e784322743e1fd2f04234d1fbdd2f7","issuetype":"Bug","key":"499","priority":"4","project":"CASSANDRA","resolution":"1","status":"5","summary":"'SSTable import tool'"}
    ...

    $ ./run.sh ../hadoop csv
    Projects found: HADOOP HDFS MAPREDUCE YARN
    e51a8c10560e5db5cf01fd530af48825cb51c9ea,Bug,4737,3,YARN,1,5,'Add CSRF filter support in YARN'
    0f72da7e281376f4fcbfbf3fb33f5d7fedcdb1aa,Improvement,6622,2,MAPREDUCE,1,5,'Add capability to set JHS job cache to a task-based limit'
    ...
    
    ./run.sh ../spark raw
    Projects found: SPARK
    {'id': '12854244', 'fields': {'summary': 'Provide R-like summary statistics for  GLMs via iteratively reweighted least squares', 'issuetype': {'id': '2', 'descri ption': 'A new feature of the product, which has yet to be developed.', 'subtask ': False, 'iconUrl': 'https://issues.apache.org/jira/images/icons/issuetypes/new feature.png', 'name': 'New Feature', 'self': 'https://issues.apache.org/jira/res t/api/2/issuetype/2'}, 'priority': {'id': '2', 'iconUrl': 'https://issues.apache .org/jira/images/icons/priorities/critical.png', 'name': 'Critical', 'self': 'ht tps://issues.apache.org/jira/rest/api/2/priority/2'}, 'resolution': {'id': '1',  'name': 'Fixed', 'description': 'A fix for this issue is checked into the tree a nd tested.', 'self': 'https://issues.apache.org/jira/rest/api/2/resolution/1'},  'status': {'id': '5', 'description': 'A resolution has been taken, and it is awa iting verification by reporter. From here issues are either reopened, or are clo sed.', 'iconUrl': 'https://issues.apache.org/jira/images/icons/statuses/resolved .png', 'name': 'Resolved', 'self': 'https://issues.apache.org/jira/rest/api/2/st atus/5', 'statusCategory': {'id': 3, 'colorName': 'green', 'key': 'done', 'name' : 'Complete', 'self': 'https://issues.apache.org/jira/rest/api/2/statuscategory/ 3'}}}, 'key': 'SPARK-9837', 'expand': 'renderedFields,names,schema,transitions,o perations,editmeta,changelog', 'self': 'https://issues.apache.org/jira/rest/api/ 2/issue/12854244'}
    ...

## Preparation
run

    ./find_commits.sh git_folder
for example

    ./find_commits.sh ../cassandra > cassandra.map.txt
by default, the basename of the folder is taken to be the component name

## Extraction
(note: the project is python3.4+)

run 

    python fetch_and_extract.py [format] < map_filename

for example

    python fetch_and_extract.py csv < cassandra.map.txt
