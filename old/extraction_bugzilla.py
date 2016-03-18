import re
from html.parser import HTMLParser

import utils


def find_perfect_commits(txt):
    return tuple(set(re.findall(r'(?=\b|/)[a-z0-9]{40}\b', txt, re.IGNORECASE)))


def find_commits_regex(html):
    for pat in [r'([a-z0-9]{40}|commit\s+(?:<a href=".*?">)?[a-z0-9]{7,40})',
                '([a-z0-9]*[a-z]+[0-9]+[a-z][a-z0-9]+)']:
        yield from re.findall(pat, html)


class CommitFinder(HTMLParser):
    'BeutifulSoup would be a better option'
    def __init__(self):
        super().__init__()
        self.data = {'links':()}
        self.current = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a':
            href = attrs['href']
            if 'commit' in href:
                self.data['links'] += (href, )
        self.current = attrs.get('id')            

    def handle_data(self, data):
        if self.current == 'field_container_component':
            self.data['component'] = data
        if self.current == 'field_container_product':
            self.data['product'] = data


def find_metadata(html):
    cf = CommitFinder()
    cf.feed(html)
    return cf


def dict_with(d, k, v):
    d[k] = v
    return d


def dump_json(url):
    from bugs_rpd import BugsHtml
    bs = BugsHtml(url)
    utils.write_json(bs.host_folder + 'bug_commit.json',
                     {bid: dict_with(find_metadata(html).data,
                                     'commits', find_perfect_commits(html))
                      for bid, html in bs.items()})
    

if __name__ == '__main__':
    dump_json('https://issues.dlang.org/')
