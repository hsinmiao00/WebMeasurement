from adblock_check import *
import logging 
import csv

def go(path, cc):

    # Countries we have results for currently
    countrycodes = [cc]

    # Open the files and create containers for results
    WPMobjects = {cc:WPMResults(path.format(cc)) for cc in countrycodes}
    results_trackers = {cc:[] for cc in countrycodes}

    # Generate Adblock rules list
    trackers = WPMResults.rulesFromURL(WPMResults.TRACKING_LIST)

    # What are we querying
    query = "SELECT url, top_url from http_requests"

    # Loop through each country code and check all URLs within to see if it matches
    # an Adblock rule.
    for cc in countrycodes:
        obj = WPMobjects[cc]
        results_trackers[cc] = obj.check(trackers, query)

    # Generate CSV
    header = ['Country', 'Rule_Set', 'Top_URL', 'Number_Requests', 'Number_Hits']
    csv_buffer = {cc:[] for cc in countrycodes}
    for cc in countrycodes:
        # trackers
        fn = "reqs-trackers-{}.csv".format(cc)
        with open(fn, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            
            
            for topurl in results_trackers[cc]:
                this = results_trackers[cc][topurl]
                n = len(this)
                hits = len([url for url in this if this[url] == True])
                topurl_str = ".".join(topurl)
                row = [cc, 'trackers', topurl_str, n, hits]
                csv_buffer[cc].append(row)
                writer.writerow(row)
            
if __name__ == '__main__':
    import threading, argparse
    p = argparse.ArgumentParser()
    p.add_argument('path', metavar='PATH', help='Path to sqlite databases with country denoted by {}')
    args = p.parse_args()

    if args.path:
        logging.basicConfig(level=logging.DEBUG)
        for cc in ('US', 'JP', 'AU', 'DE'):
            threading.Thread(target=go, args=(args.path, cc)).start()

    
