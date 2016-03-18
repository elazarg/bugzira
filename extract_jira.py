import json
import sys
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor as Executor

import utils

URL = 'https://issues.apache.org/jira/'
FIELDS = ('issuetype', 'status', 'resolution', 'priority')


def fetch(issue_id):
    '''There is a Python api for jira: pip install jira
    but we wanted to avoid dependencies. and it's simple.''' 
    raw = utils.fetch(URL + 'rest/api/2/issue/' + issue_id + '?fields='+','.join(FIELDS))
    issue = json.loads(raw)
    return issue


def extract(issue, rep='id'):
    assert rep in ['name', 'id']
    fs = issue['fields']
    return [utils.getitem(fs[f],rep) for f in FIELDS]


def csv(sha, issue_id, features):
    return '{},{},{}'.format(sha, issue_id, ','.join(features))


@lru_cache(maxsize=1024)
@utils.retry_or_return_exception
def fetch_feature(issue_id):
    return extract(fetch(issue_id))


def make_feature_vector(sha_issueid):
    sha, issue_id = sha_issueid
    features = fetch_feature(issue_id)
    if not isinstance(features, Exception):
        utils.output(csv(sha, issue_id, features))

        
def flatten_lines(lines):
    '''lines are [sha1 bug_id bug_id ...]
    This function flatten them''' 
    return [(line.split()[0], issue_id)
            for line in utils.read_lines(sys.argv[1]) 
            for issue_id in line.split()[1:]]


def main():
    worklist = flatten_lines(utils.read_lines(sys.argv[1]))
    with Executor(max_workers=200) as executor:
        list(executor.map(make_feature_vector, worklist))


if __name__ == '__main__':
    print('SHA1', 'BUG_ID', *FIELDS)
    main()
