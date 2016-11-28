import urllib

import urllib.request

from bs4 import BeautifulSoup

import time

#the main function that's called in the script. searches through each line in the search.txt file in the same directory and performs the get_pages function on it
def searchfunction():
	book_urls = [line.strip() for line in open("search.txt")]
	for target in book_urls:
		get_pages(target)

#from each base url, gets all of the URLS for specialized pages like context, characters, and various chapter summaries - up to 20
def get_pages(url):
	base_url = url
	#if you need additional generalized URLs, create them with this formula and then add them to the target_urls list
	contx = "%scontext.html" % base_url
	summ = "%ssummary.html" % base_url
	chara = "%scharacters.html" % base_url
	analy = "%scanalysis.html" % base_url
	theme = "%sthemes.html" % base_url
	target_urls = [contx, summ, chara, analy, theme]
	#adds 20 section summary URLs to the target urls
	for i in range(0,20):
		target_urls.append("%ssection%s.rhtml" % (base_url, str(i)))
	for url in target_urls:
		#this is the naming convention used in the output text documents
		name = str(url.replace("http://www.sparknotes.com/lit/","").replace("/","_").replace(".","").replace("html","") + ".txt")
		print("Trying to scrape url: %s" % url)
		try:
		#performs the getplaintext function on each URL, also passing its name
			getplaintext(url, name)
		except:
			print("Failed.")
			continue
	
def getplaintext(url, name):
	#specifies the browser that is simulated interacting with the host server
	heeds = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; rv:5.0) Gecko/20100101 Firefox/5.0'}
	#creates a server request object to the target URL with the specified headers
	query = urllib.request.Request(url, headers = heeds)
	#opens the query server request object
	html = urllib.request.urlopen(query)
	#formats the html from the server using BeautifulSoup
	soup = BeautifulSoup(html, "html.parser")
	soup.prettify
	#gets rid of all the ads.  If there's another HTML element you want to get rid of, just decompose it from the soup variable
	for div in soup.find_all(class_="floatingad"):
		div.decompose()
	#navigates to the div in which all the text is located
	textboxs = soup.find(class_="studyGuideText")
	#gets all the text from the target div, replacing all the incomprehensible elements.  This is where you'd add stuff to get rid of punctuation as well
	texti = textboxs.get_text().replace("\u2192","").replace("\u2190","").replace("\u2019","'")
	#Creates a new file, since if Python calls "open" and there is no such file it'll make one.  Opens it in write mode.  If you wanted to re-open another file and append stuff to it, you'd open it in "a" mode, which would automatically add any information written to it to the end
	m = open(name, "w")
	#writes the relevant information to the file and then closes it
	m.write(texti)
	m.close()
	#waits to spoof human traffic
	time.sleep(1)
	
searchfunction()