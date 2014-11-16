import requests
import sqlite3
import logging
from adblockparser import AdblockRules

class WPMResults(object):
    TRACKING_LIST = "https://easylist-downloads.adblockplus.org/easyprivacy.txt"
    AD_LIST = "https://easylist-downloads.adblockplus.org/easylist.txt"

    def __init__(self, db):
        with open(db) as f: self.db_connection = sqlite3.connect(db)
        self.query = self.db_connection.cursor()    
        self.log = logging.getLogger(__name__)
        self.cache = {}
        
    @classmethod 
    def rulesFromURL(_class, url):
        logging.getLogger(__name__).info("Downloading AdBlock rules from {}".format(url))
        return AdblockRules(requests.get(url).content.splitlines())
        
    @classmethod
    def cleanQuery(_class, result):
        return map(lambda r: r[0], result)
        
    def setupRules(self):
        if not hasattr(self, 'trackers') or not hasattr(self, 'ads'):
            self.trackers = self.rulesFromURL(self.TRACKING_LIST)
            self.ads = self.rulesFromURL(self.AD_LIST)            
        
    def check(self, rules, query):
        self.setupRules()
        checkHash = hash("{}{}{}".format(rules,query,self.db_connection))
        
        if checkHash in self.cache:
            return self.cache[checkHash]
        else:    
            self.log.info("Running query {}".format(query))
            self.query.execute(query)
            results = self.cleanQuery(self.query.fetchall())
            n = len(results)
            self.log.info("Query returned {} results".format(n))
        
            self.log.info("Checking rules set {}".format(rules))
            checked = {}
            for i, url in enumerate(results):
                if i % 20 == 0 or i == n:
                    self.log.debug("Checking URL {}/{}".format(i,n))
                checked[url] = rules.should_block(url)
            self.cache[checkHash] = checked
            
            return checked
        
def summarize(results):
    n = len(results)
    hits = [r for r in results.values() if r == True]
    print "{} URLs with {} hits.".format(n, len(hits))
    
    
        