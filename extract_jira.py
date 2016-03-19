# details for issues can be found at
# https://confluence.atlassian.com/jira063/what-is-an-issue-683542485.html 
# issue_key: A unique identifier for this issue, for example: ANGRY-304
import json
import sys
                        
import utils

URL = 'https://issues.apache.org/jira/'
#           field     ,  subfield
FIELDS = (('issuetype', 'name'),
           ('priority', 'id'),
           ('status', 'id'),
           ('resolution', 'id'),
           ('summary', ''),
           ('description', ''))

@utils.retry_or_return_exception(times=2)
def fetch(issue_key):
    '''There is a Python api for jira: pip install jira
    but we wanted to avoid dependencies. and it's simple.''' 
    raw_issue = utils.fetch(URL + 'rest/api/2/issue/' + issue_key \
                                + '?fields=' + ','.join(f for f, _rep in FIELDS))
    return json.loads(raw_issue)


def extract(issue):
    fs = issue['fields']
    return [utils.getitem(fs[f], rep) if rep else repr(fs[f])
            for f, rep in FIELDS]


def to_csv(sha, issue_key, features):
    issue_cat, issue_num = issue_key.split('-')
    return utils.to_csv([sha, issue_cat, issue_num] + features)


def fetch_feature(issue_key):
    return extract(fetch(issue_key))


def make_feature_vector(sha_issuekey):
    sha, issue_id = sha_issuekey
    features = fetch_feature(issue_id)
    if not isinstance(features, Exception):
        utils.output(to_csv(sha, issue_id, features))

        
def flatten_lines(lines):
    '''lines are [sha1 bug_id bug_id bug_id...]
    This function flatten them into [sha1 bug_id] [sha1 bug_id]...''' 
    for line in lines:
        sha1, *issue_keys = line.strip().split()
        for issue_id in issue_keys:
            yield (sha1, issue_id)


def main():
    worklist = flatten_lines(sys.stdin)
    from concurrent.futures import ThreadPoolExecutor as Executor
    with Executor(max_workers=150) as executor:
        utils.exhaust(executor.map(make_feature_vector, worklist))


if __name__ == '__main__':
    main()
