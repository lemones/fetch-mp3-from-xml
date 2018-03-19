#!/bin/python

from bs4 import BeautifulSoup as soup
import urllib.request
import requests
import re
import os.path

rss_xml = requests.get("https://bitsk.libsyn.com/rss")
parse = rss_xml.text
doc = soup(parse, 'lxml')

# Get mp3 extension from url
mp3 = doc.findAll('enclosure', url=re.compile('http.*\.mp3'))

# Set folder name with removed special characters (respecting Swedish alphabet)
folder = " ".join(re.findall("[a-öA-Ö]+", doc.title.string))

# Create folder if not exist
if not os.path.exists(folder):
    print("Creating folder: %s" % (folder))
    os.makedirs(folder)

for enclosure in mp3:
    # Remove everything after question mark in URL
    retest = re.sub("\?.*$", "", enclosure['url'])
    # Remove everything after last forward slash to get filename
    filename = retest.split('/')[-1]
    # Put it all togheter
    full = folder + "/" + filename

    # If file exist:
    if os.path.isfile(full):
        print("[-] Skipping: %s" % (filename))
    else:
        print("[*] Downloading: %s -> %s" % (filename, folder))
        try:
            data = urllib.request.urlretrieve(retest, full)
        except KeyboardInterrupt:
            print("[-] Removing incomplete: %s" % (full))
            os.remove(full)
            exit(1)
