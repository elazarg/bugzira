import os
import urllib.request as request
import os.path as path
import operator as op

from utils import write_lines, write_file, read_file, read_lines, fetch

def cached_fetch(url, f, filename): 
    if os.path.isfile(filename):
        return read_lines(filename)
    os.makedirs(path.dirname(filename), exist_ok=True)
    html = fetch(url)
    data = f(html)
    if isinstance(data, str):
        write_file(filename, data)
    else:
        write_lines(filename, data)
    return data

def cached_retrieve(url, filename):
    os.makedirs(path.dirname(filename), exist_ok=True)
    if not os.path.isfile(filename):
        request.urlretrieve(url, filename)


class LocalMirrorDict:
    'Baseclass of a lazy persistent dictionary for remote html'
    def item_filename_url(self, key):
        raise NotImplementedError

    @property
    def keys_filename_url_extractor(self):
        raise NotImplementedError
    
    def fetch_remote(self, k):
        filename, url = self.item_filename_url(k)
        cached_retrieve(url, filename)
    
    def __getitem__(self, k):
        self.fetch_remote(k)
        filename, _ = self.item_filename_url(k)
        return read_file(filename)
    
    def values(self):
        return map(op.itemgetter(1), self.items())
    
    def items(self):
        return [(k, self[k]) for k in self.keys()]
    
    def keys(self):
        filename, url, extractor = self.keys_filename_url_extractor
        return cached_fetch(url, extractor, filename)
