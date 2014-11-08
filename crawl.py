from automation import TaskManager
import time
import os
import argparse

def crawl(sites, output):
    # Load sites
    with open(sites) as f:
        sites = ["http://" + site for site in f.readlines()]
        
    # The list of sites that we wish to crawl
    NUM_BROWSERS = 1

    # Saves a crawl output DB to the Desktop
    db_loc = os.path.expanduser('~/Desktop/{}'.format(output))

    # Loads 3 copies of the default browser preference dictionaries
    browser_params = TaskManager.load_default_params(NUM_BROWSERS)

    #Enable flash for all three browsers
    for i in xrange(NUM_BROWSERS):
        browser_params[i]['disable_flash'] = False
        browser_params[i]['headless'] = True

    # Instantiates the measurement platform
    # Launches two (non-headless) Firefox instances and one headless instance
    # logging data with MITMProxy
    # Commands time out by default after 60 seconds
    manager = TaskManager.TaskManager(db_loc, browser_params, NUM_BROWSERS)

    # Visits the sites with both browsers simultaneously, 5 seconds between visits
    for site in sites:
        manager.get(site, index='**') # ** = synchronized browsers
        time.sleep(5)

    # Shuts down the browsers and waits for the data to finish logging
    manager.close()

if __name__ == '__main__':
    p = argparse.ArgumentParser(description="Run an Openwpm crawl of all URLs in a certain file.")
    p.add_argument('file', metavar='SITELIST', help='Text file with list of sites, one per line.')
    args = p.parse_args()
    output = "openwpm_{}.sqlite".format(os.path.basename(args.file).replace(".txt", ""))
    crawl(args.file, output)
    
