import sys
import json

import config


def do_filter(issue):
    res = {}
    res['project'], res['key'] = issue['key'].split('-')
    for field, subfield in config.FIELDS:
        res[field] = issue['fields'][field]
        if subfield and not isinstance(res[field], (str, type(None))):
            res[field] = res[field].get(subfield)
    return res


if __name__ == '__main__':
    for line in sys.stdin:
        print(json.dumps(do_filter(json.loads(line)),
                         separators=(',', ':'), sort_keys=True))
    
