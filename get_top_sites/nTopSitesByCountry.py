import os, sys
import experiment.alexa as alexa

def usage():
    print "Not enough arguments! See below:"
    print "python nTopSitesByCountry.py <2_letter_country_code> <output_file>"

def collect_sites_from_alexa(alexa_link="http://www.alexa.com/topsites", 
		output_file="out.txt", nsites=5, browser="firefox"):
	if(browser != "firefox" and browser != "chrome"):
		print "Illegal browser choice", browser
		return
	PATH="./"+output_file
	if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
		response = raw_input("This will overwrite file %s... Continue? (Y/n)" % output_file)
		if response == 'n':
			sys.exit(0)
	fo = open(output_file, "w")
	fo.close()
	print "Beginning Collection"
# 	os.system("python experimenter/alexa.py %s %s %s" % (output_file, alexa_link, n))
	alexa.run_script(alexa_link, output_file, nsites, browser)
	print "Collection Complete. Results stored in ", output_file

if len(sys.argv) < 3:
    usage()
    sys.exit()

country = sys.argv[1]
out_file = sys.argv[2]

collect_sites_from_alexa(nsites=250, output_file=out_file, browser="firefox", 
            alexa_link="http://www.alexa.com/topsites/countries/" + country)
