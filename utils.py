import json
import typing
import io
import csv
import sys
import logging
import pathlib

import urllib.request as request
import urllib.error


def write_lines(filename: str, iterable: typing.Iterable) -> None:
    with open(filename, "w", encoding="utf8") as out:
        for t in iterable:
            print(t, file=out)


def read_lines(filename: str) -> list[str]:
    with open(filename, encoding="utf8") as f:
        return [line.strip() for line in f]


def write_file(filename: str, string) -> None:
    pathlib.Path(filename).write_text(string, encoding="utf8")


def read_file(filename: str) -> str:
    return pathlib.Path(filename).read_text(encoding="utf8")


def write_json(filename: str, d: object) -> None:
    with open(filename, "w", encoding="utf8") as f:
        json.dump(d, f, sort_keys=True, indent=0)


def fetch(url: str):
    with request.urlopen(url) as w:
        return w.read().decode("utf8")


def getitem(m, key, default=None):
    """a helper for cases where the item is None"""
    if m is None:
        return str(default)
    return m[key]


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(message)s")


def output(msg: str) -> None:
    logging.info(msg)


def retry(times=2):
    assert times > 0

    def inner(f):
        def wrap(*args, **kwargs):
            for i in range(times, 0, -1):
                try:
                    return f(*args, **kwargs)
                except urllib.error.URLError:
                    if i == 1:
                        raise

        return wrap

    return inner


def exhaust(iterator: typing.Iterator) -> None:
    for _ in iterator:
        pass


def to_csv(iterable: typing.Iterable) -> str:
    with io.StringIO() as s:
        csv.writer(s).writerow(iterable)
        return s.getvalue().rstrip()
