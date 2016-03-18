import utils
import json
import sys
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor as Executor


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
def fetch_feature(issue_id):
    return extract(fetch(issue_id))


def make_feature_vector(sha_issueid):
    sha, issue_id = sha_issueid
    try:
        res = csv(sha, issue_id, fetch_feature(issue_id))
    except Exception as ex:
        'Yes, the binding of ex is scoped'
        error = ex
    else:
        put(res)
        error = None
    return (sha, issue_id), error

        
def chain_worklist(lines):
    return [(line.split()[0], issue_id)
            for line in utils.read_lines(sys.argv[1]) 
            for issue_id in line.split()[1:]]


def main():
    worklist = chain_worklist(utils.read_lines(sys.argv[1]))
    errors = {}
    with Executor(max_workers=10) as executor:
        while worklist:
            print(worklist[:4])
            work = list(executor.map(make_feature_vector, worklist))
            worklist = [(sha, issue_id)
                        for (sha, issue_id), ex in work
                        if ex != errors.setdefault(issue_id)]


def put(item):
    #hopefully it will not mess up
    print(item, flush=True)


if __name__ == '__main__':
    print('SHA1', 'BUG_ID', *FIELDS)
    main()
