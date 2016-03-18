import json
import urllib.request as request


def write_json(filename, d):
    with open(filename, 'w') as f:
        json.dump(d, f, sort_keys=True, indent=0)


def read_lines(filename):
    with open(filename) as f:
        return tuple(line.strip() for line in f)


def write_lines(filename, iterable):
    with open(filename, 'w', encoding='utf8') as out:
        for t in iterable:
            print(t, file=out)


def write_file(filename, string):
    with open(filename, 'w', encoding='utf8') as out:
        out.write(string)


def read_file(filename):
    with open(filename, encoding='utf8') as f:
        return f.read()


def fetch(url):
    with request.urlopen(url) as w:
        return w.read().decode('utf8')


def getitem(m, key, default=None):
    'a helper for cases where the item is null'
    if m is None: return str(default)
    return m[key]
