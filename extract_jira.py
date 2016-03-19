# details for issues can be found at
# https://confluence.atlassian.com/jira063/what-is-an-issue-683542485.html 
# issue_key: A unique identifier for this issue, for example: ANGRY-304

# TODO: add JSON formatted output
import json
import sys
                        
import utils

URL = 'https://issues.apache.org/jira/'
#           field     ,    subfield
FIELDS = (('issuetype',     'name'),
           ('priority',     'id'),
           ('status',       'id'),
           ('resolution',   'id')
           #,('summary',      '')
           #,('description',  '')
           )

@utils.retry(times=2)
def fetch_issue(issue_key):
    '''There is a Python api for jira: pip install jira
    but we wanted to avoid dependencies. and it's simple.''' 
    raw_issue = utils.fetch(URL + 'rest/api/2/issue/' + issue_key \
                                + '?fields=' + ','.join(f for f, _rep in FIELDS))
    return json.loads(raw_issue)


def extract(issue):
    fs = issue['fields']
    for f, rep in FIELDS:
        return [utils.getitem(fs[f], rep) if rep else repr(fs[f])
            for f, rep in FIELDS]


def to_csv(sha, issue_key, features):
    issue_cat, issue_num = issue_key.split('-')
    return utils.to_csv([sha, issue_cat, issue_num] + features)


def fetch_feature(issue_key):
    return extract(fetch_issue(issue_key))


def make_feature_vector(sha_issuekey):
    sha, issue_key = sha_issuekey
    try:
        json_features = fetch_issue(issue_key)
        json_features['sha'] = sha
        utils.output(json.dumps(json_features))
    except Exception:
        # we intentionally ignore failed fetches
        # TODO: log such failures 
        pass
    
        
def flatten_lines(lines):
    '''lines are [sha1 issue_key issue_key issue_key...]
    This function flatten them into [sha1 issue_key] [sha1 issue_key]...''' 
    for line in lines:
        sha1, *issue_keys = line.strip().split()
        for issue_key in issue_keys:
            yield (sha1, issue_key)


def main():
    '''stdin is assumed to be the output of 
         ./sha1_issue.sh [some project directory] [some project name]'''
    worklist = flatten_lines(sys.stdin)
    from concurrent.futures import ThreadPoolExecutor as Executor
    with Executor(max_workers=150) as executor:
        utils.exhaust(executor.map(make_feature_vector, worklist))


if __name__ == '__main__':
    main()
