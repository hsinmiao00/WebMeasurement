import requests
import sqlite3
import logging
import tldextract
from itertools import groupby
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
        # Turn plaintext URLs into parsed URLs, and strip newlines
        cleaned = [(url, tldextract.extract(topurl.strip())) for url, topurl in result]
        # Group all subrequests by their top URL and turn into a dict (top:sublist)
        grouped = {top:list(url for url, top in subgroup) for top, subgroup in groupby(cleaned, lambda row: row[1])} 
        return grouped
        
    def check(self, rules, query):
        # Cache rules checks as they take a long time. 
        # A query hash = hash of the reprs of (rules+query+db object)
        checkHash = hash("{}{}{}".format(rules,query,self.db_connection))
        
        if checkHash in self.cache:
            return self.cache[checkHash]
        else:    
            self.log.info("Running query {}".format(query))
            self.query.execute(query)
            results = self.query.fetchall()
            n = len(results)
            results = self.cleanQuery(results)
            self.log.info("Query returned {} results".format(n))
        
            self.log.info("Checking rules set {}".format(rules))
            checked = {}
            for top in results:
                this_n = len(results[top])
                checked[top] = {}
                self.log.info("Checking {} subrequests from {}".format(this_n, top))
                for i, url in enumerate(results[top]):
                    if i % 20 == 0 or i == n:
                        self.log.info("Checking URL {}/{}".format(i,this_n))
                        checked[top][url] = rules.should_block(url)
            self.cache[checkHash] = checked
            
            return checked
        
def summarize(results):
    n = len(results)
    hits = [r for r in results.values() if r == True]
    print "{} URLs with {} hits.".format(n, len(hits))
    
    
        