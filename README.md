# fetch-mp3-from-xml
Download mp3 from XML where url=[.mp3] is within an <enclosure> tag.

url variable:
	findAll('enclosure', url=re.compile('http.*\.mp3'))
	Uses regex to get http*.mp3 from within the <enclosure> tag.

retest variable:
	re.sub("\?.*$", "", enclosure['url'])
	Uses regex to remove the question mark and * after .mp3 in url variable
