from adblock_check import *
import logging 
import csv

logging.basicConfig(level=logging.DEBUG)

# Countries we have results for currently
countrycodes = ['US', 'JP', 'AU', 'DE']

# Open the files and create containers for results
WPMobjects = {cc:WPMResults("../openwpm_top25{}.sqlite".format(cc)) for cc in countrycodes}
results_trackers = {cc:[] for cc in countrycodes}
results_ads = {cc:[] for cc in countrycodes}

# Generate Adblock rules list
trackers = WPMResults.rulesFromURL(WPMResults.TRACKING_LIST)
ads = WPMResults.rulesFromURL(WPMResults.AD_LIST)

# What are we querying
query = "SELECT url, top_url from http_requests"

# Loop through each country code and check all URLs within to see if it matches
# an Adblock rule.
for cc in countrycodes:
    obj = WPMobjects[cc]
    results_ads[cc] = obj.check(ads, query)
    results_trackers[cc] = obj.check(trackers, query)
    
# Generate CSV
header = ['Country', 'Rule_Set', 'Top_URL', 'Number_Requests', 'Number_Hits']
csv_buffer = {cc:[] for cc in countrycodes}
for cc in countrycodes:
    # trackers
    for topurl in results_trackers[cc]:
        this = results_trackers[cc][topurl]
        n = len(this)
        hits = len([url for url in this if this[url] == True])
        topurl_str = ".".join(topurl)
        row = [cc, 'trackers', topurl_str, n, hits]
        csv_buffer[cc].append(row)
        
    # ads
    for topurl in results_ads[cc]:
        this = results_ads[cc][topurl]
        n = len(this)
        hits = len([url for url in this if this[url] == True])
        topurl_str = ".".join(topurl)
        row = [cc, 'ads', topurl_str, n, hits]
        csv_buffer[cc].append(row)

# Write CSV files
for cc in csv_buffer:
    fn = "results-adblock-{}.csv".format(cc)
    logging.getLogger(__name__).info("Writing output to {}".format(fn))
    with open(fn, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(csv_buffer[cc])        