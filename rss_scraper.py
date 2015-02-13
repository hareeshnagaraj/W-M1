from bs4 import BeautifulSoup
import requests
import re
import feedparser


rss_generic_free_link = "http://%s.craigslist.org/search/zip?query=%s&format=rss"


def get_rss(site, term=""):
	rss_link = rss_generic_free_link % (site, term)
	return feedparser.parse(rss_link)

def parse_item(item):
	result = {}
	result['url'] = item['dc_source']
	result['title'] = item['title']
	result['summary'] = item['summary']
	result['picture'] = None
	if item.get('enc_enclosure'):
		result['picture'] = item['enc_enclosure'].get('resource')
	return result

def parse_item_list(rss):
	return map(parse_item, rss.entries)

def parse_rss_feed(site, term=""):
	rss = get_rss(site, term)
	return parse_item_list(rss)


# Get the html for a specific webpage

def getItemHTML( url ):
    resp = requests.get("http://" + url)
    data = resp.text
    return data

# Parse the url with BeautifulSoup and return the relevant data

def getItemData( url ):
    data = getItemHTML( url )
    soup = BeautifulSoup(data)                                #if theres nothing in the array no pic
    mapwrap = soup.find_all(href=re.compile("maps.google.com"))    #if theres nothing in the array, no map
    replylink = soup.find(id="replylink")
    emailRequest = requests.get("http://norfolk.craigslist.com" + replylink.get('href'))
    emailRequestData = emailRequest.text
    emailSoup = BeautifulSoup(emailRequestData)
    replyEmail = emailSoup.find_all(class_="anonemail")[0].text
    returnData = { }
    returnData['map'] = mapwrap
    returnData['replyemail'] = replyEmail
    return returnData

if __name__ == "__main__":
	parse_rss_feed()