# details for issues can be found at
# https://confluence.atlassian.com/jira063/what-is-an-issue-683542485.html 
# issue_key: A unique identifier for this issue, for example: ANGRY-304
import json
import sys
                        
import utils

RAW = sys.argv[1:] == ['raw']
CSV = sys.argv[1:] == ['csv']

URL = 'https://issues.apache.org/jira/'
#           field     ,    subfield
FIELDS = (('issuetype',     'name'),
           ('priority',     'id'),
           ('status',       'id'),
           ('resolution',   'id'),
           ('summary',      ''),
           ('description',  '')
           )

@utils.retry(times=2)
def fetch_issue(issue_key):
    '''There is a Python api for jira: pip install jira
    but we wanted to avoid dependencies. and it's simple.'''
    query = URL + 'rest/api/2/issue/' + issue_key
    query += '?fields=' + ','.join(f for f, _rep in FIELDS)
    raw_issue = utils.fetch(query)
    return json.loads(raw_issue)


def fetch_and_compose(sha_issuekey):
    sha, issue_key = sha_issuekey
    res = fetch_issue(issue_key)
    if not RAW:
        res = get_filtered(res)
        res['commit'] = sha
        if CSV:
            res = utils.to_csv([v for _, v in sorted(res.items())])
        else:
            res = json.dumps(res, sort_keys=True, separators=(',', ':'))
    utils.output(res)


def get_filtered(issue):
    'translates complicated issue into simple format, with relevant items only'
    res = {}
    res['project'], res['key'] = issue['key'].split('-')
    for field, subfield in FIELDS:
        res[field] = issue['fields'][field]
        if subfield and not isinstance(res[field], (str, type(None))):
            res[field] = res[field].get(subfield)
    return res


def flatten_lines(lines):
    '''lines are [sha1 issue_key issue_key issue_key...]
    This function flatten them into [sha1 issue_key] [sha1 issue_key]...''' 
    for line in lines:
        sha1, *issue_keys = line.strip().split()
        for issue_key in issue_keys:
            yield (sha1, issue_key)



def main():
    '''stdin is assumed to be the output of 
         ./find_commits.sh [some project directory] [some project name]'''
    worklist = flatten_lines(sys.stdin)
    from concurrent.futures import ThreadPoolExecutor as Executor
    with Executor(max_workers=150) as executor:
        utils.exhaust(executor.map(fetch_and_compose, worklist))


if __name__ == '__main__':
    main()
