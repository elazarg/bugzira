import json
import urllib.request as request


def write_lines(filename, iterable):
    with open(filename, 'w', encoding='utf8') as out:
        for t in iterable:
            print(t, file=out)


def read_lines(filename):
    with open(filename) as f:
        return [line.strip() for line in f]


def write_file(filename, string):
    with open(filename, 'w', encoding='utf8') as out:
        out.write(string)


def read_file(filename):
    with open(filename, encoding='utf8') as f:
        return f.read()


def write_json(filename, d):
    with open(filename, 'w') as f:
        json.dump(d, f, sort_keys=True, indent=0)


def fetch(url):
    with request.urlopen(url) as w:
        return w.read().decode('utf8')


def getitem(m, key, default=None):
    'a helper for cases where the item is null'
    if m is None: return str(default)
    return m[key]


import logging
logging.basicConfig(filename='data/log.txt',level=logging.DEBUG)  

def output(msg):
    printer.info(msg)

printer = logging.getLogger('printer')
printer.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(message)s'))
printer.addHandler(ch)
printer.propagate = False


def log(msg):
    logging.debug(msg)


def retry_or_return_exception(times=2):
    assert times > 0
    def retry_or_return_exception(f):
        def wrap(*args, **kwargs):
            for _ in range(times):
                try:
                    return f(*args, **kwargs)
                except Exception as ex:
                    error = ex
            return error
        return wrap
    return retry_or_return_exception

def exhaust(iterable):
    for _ in iterable:
        pass