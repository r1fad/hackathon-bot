from urllib import FancyURLopener
import json
from bs4 import SoupStrainer, BeautifulSoup
import unicodedata

#Class to provide custom user header to prevent
#blocking by Google\'s bot watchers.
class MyOpener(FancyURLopener):
  version = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
openurl = MyOpener().open

data = [] # Empty list used later to create json

base_url = 'https://mlh.io/seasons/eu-2017/events'

events_page = BeautifulSoup(openurl(base_url).read(), "lxml",
                parse_only=SoupStrainer('div',{'class':'row'}))

for event in events_page.find_all('div',{'class':'event-wrapper'}):
    eventJSON = {}
    eventJSON["url"] = event.find('a',{'class':'event-link'})['href']
    eventJSON["name"] = event.find('h3',{'itemprop':'name'}).get_text()
    eventJSON["image"] = event.find('div',{'class':'image-wrap'}).find('img')['src']
    eventJSON["logo"] = event.find('div',{'class':'event-logo'}).find('img')['src']
    eventJSON["startDate"] = event.find('meta',{'itemprop':'startDate'})["content"]
    eventJSON["endDate"] = event.find('meta',{'itemprop':'endDate'})["content"]
    eventJSON["locality"] = event.find('span',{'itemprop':'addressLocality'}).get_text()
    eventJSON["region"] = event.find('span',{'itemprop':'addressRegion'}).get_text()
    eventJSON["location"] = eventJSON["locality"]+", "+eventJSON["region"]
    if ("[" not in eventJSON["name"]):
        print eventJSON["name"]
        data.append(eventJSON)

with open('hackathons.json','w') as outfile:
    json.dump(data,outfile,sort_keys=True,indent=2)
