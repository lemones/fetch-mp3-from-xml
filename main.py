#!/bin/python

from bs4 import BeautifulSoup as soup
import urllib.request
import requests
import re
import os.path

# Path to save folder (remember the forward slash at end)
folder = os.getenv("HOME") + "/Music/Podcasts/"

with open("list.txt") as fop:

    cont = fop.readlines()
    # Remove \n in new line
    cont = [x.strip() for x in cont]

    for line in cont:

        exist = 0
        down = 0

        rss_xml = requests.get(line)
        parse = rss_xml.text
        doc = soup(parse, 'lxml')
        # Search mp3 extension
        mp3 = doc.findAll('enclosure', url=re.compile('http.*\.mp3'))
        # Set subfolder and remove special characters
        subfolder = " ".join(re.findall("[a-öA-Ö]+", doc.title.string))
        mergedfold = folder + subfolder

        # Create folder if not exist
        if not os.path.exists(mergedfold):
            print("[*] Creating folder: %s" % (subfolder))
            os.makedirs(mergedfold)

        for enclosure in mp3:
            # Remove everything after question mark in URL
            retest = re.sub("\?.*$", "", enclosure['url'])
            # Remove everything after last forward slash to get filename
            filename = retest.split('/')[-1]
            # Put it all togheter
            full = mergedfold + "/" + filename

            if os.path.isfile(full):
                exist += 1
            else:
                print("[*] Downloading: %s -> %s" % (filename, subfolder))
                down += 1
                try:
                    data = urllib.request.urlretrieve(retest, full)
                    exist += 1
                except KeyboardInterrupt:
                    print("[E] Removing: %s/%s" % (subfolder, filename))
                    os.remove(full)
                    exit(1)
        if down > 0:
            print("[*] %s (%s/%s)" % (subfolder, exist, down))
        else:
            print("[*] %s (%s)" % (subfolder, exist))

fop.close()
