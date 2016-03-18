from utils import read_lines
import re
import urllib.parse as parse
import json
import net_utils as net

DATA_FOLDER = '../bugzilla_data/'
    

class BugsHtml(net.LocalMirrorDict):
    def item_filename_url(self, bid):
        params = {'id': bid, 'type':self.ctype}
        filename = self.host_folder + 'bugs_{type}/{id}.{type}'.format(**params)
        url = self.url + 'show_bug.cgi?ctype={type}&id={id}'.format(**params)
        return filename, url

    @property
    def keys_filename_url_extractor(self):
        filename = self.host_folder + 'bug_ids.txt'
        query = 'buglist.cgi?field0-0-0=short_desc&field0-0-1=content&limit=0&order=bug_id&query_format=advanced&resolution=FIXED&type0-0-0=substring&type0-0-1=matches&value0-0-0=commit&value0-0-1="commit"'
        def extractor(html):
            return sorted(set(map(int, re.findall(r'show_bug\.cgi\?id=(\d+)', html))))
        return filename, (self.url + query), extractor
    
    def __init__(self, url, ctype='html'):
        assert ctype in ['html', 'xml']
        self.url = url
        host = parse.urlparse(self.url).netloc
        self.host_folder = DATA_FOLDER + '{}/'.format(host) 
        self.ctype = ctype
    
    def fetch_all_bugs(self):            
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=30) as executor:
            for x in self.keys():
                executor.submit(self.fetch_remote, x)
        

class BugsRest(net.LocalMirrorDict):
    def item_filename_url(self, bid):
        params = {'id': bid, 'type': 'json'}
        filename = self.host_folder + 'bugs_{type}/{id}.{type}'.format(**params)
        url = self.url + 'rest/bug/{id}'.format(**params)
        return filename, url

    @property
    def keys_filename_url_extractor(self):
        filename = self.host_folder + 'bug_ids.txt'
        query = 'rest/bug?quicksearch=FIXED%20commit&include_fields=id'
        def extractor(json_text):
            js = json.loads(json_text)
            return [b['id'] for b in js['bugs']]
        return filename, (self.url + query), extractor
    
    def __init__(self, url, ctype='json'):
        assert ctype in ['json']
        self.url = url
        host = parse.urlparse(self.url).netloc
        self.host_folder = DATA_FOLDER + '{}/'.format(host) 
        self.ctype = ctype
    
    def fetch_all_bugs(self):            
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=30) as executor:
            for x in self.keys():
                executor.submit(self.fetch_remote, x)


if __name__ == '__main__':
    for url in read_lines(DATA_FOLDER + 'hosts_simple.txt'):
        print(url,':')
        b = BugsHtml(url)
        b.fetch_all_bugs()
