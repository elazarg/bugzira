import json
import sys
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor as Executor
import base64

import utils

URL = 'https://issues.apache.org/jira/'
FIELDS = ( ('issuetype', 'name'),
           ('status', 'id'),
           ('resolution', 'id'),
           ('priority', 'id'),
           ('description', '') )


def fetch(issue_id):
    '''There is a Python api for jira: pip install jira
    but we wanted to avoid dependencies. and it's simple.''' 
    raw_issue = utils.fetch(URL + 'rest/api/2/issue/' + issue_id + '?fields='+','.join(f for f, rep in FIELDS))
    return json.loads(raw_issue)


def extract(issue):
    fs = issue['fields']
    return [utils.getitem(fs[f], rep) if rep else json.dumps(fs[f])
            for f, rep in FIELDS]


def csv(sha, issue_id, features):
    return '{},{},{}'.format(sha, issue_id, ','.join(features))


@utils.retry_or_return_exception(times=2)
@lru_cache(maxsize=1024)
def fetch_feature(issue_id):
    return extract(fetch(issue_id))


def make_feature_vector(sha_issueid):
    sha, issue_id = sha_issueid
    features = fetch_feature(issue_id)
    if not isinstance(features, Exception):
        utils.output(csv(sha, issue_id, features))

        
def flatten_lines(lines):
    '''lines are [sha1 bug_id bug_id bug_id...]
    This function flatten them into [sha1 bug_id]''' 
    for line in lines:
        sha1, *issue_ids = line.split()
        for issue_id in issue_ids:
            yield (sha1, issue_id)


def main():
    lines = utils.read_lines(sys.argv[1])
    worklist = flatten_lines(lines)
    with Executor(max_workers=20) as executor:
        utils.exhaust(executor.map(make_feature_vector, worklist))


if __name__ == '__main__':
    main()
