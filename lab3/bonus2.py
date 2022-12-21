from bs4 import BeautifulSoup
import json
import requests

import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
TRAM_URL_FILE = 'static/tram-url.json'







def main(): 
    url = 'https://www.vasttrafik.se/reseplanering/hallplatslista/'

    doc = requests.get(url)
    soup = BeautifulSoup(doc.text, 'html.parser')
    timetable_url = 'https://avgangstavla.vasttrafik.se/?source=vasttrafikse-stopareadetailspage&stopAreaGid='
    stop_url = 'https://www.vasttrafik.se/reseplanering/hallplatslista/'
    tram_stops = []
    gids = []
    for links in soup.find_all('section'):
        for link in links.find_all('a'):
        
            stop = link.text.replace("\r\n", "").strip()
            stop = stop.split(',')[0]
            if stop == '0771-414300':
                break
            tram_stops.append(stop)

            gid = link['href'][27:43]
            gids.append(gid)

    url_dict = dict()
    for i in range(len(tram_stops)):
        url_dict[tram_stops[i]] = {'url': stop_url+gids[i]+'/', 'timetable': timetable_url+gids[i] }
    
    with open(TRAM_URL_FILE, 'w') as f:
        json.dump(url_dict, f) 


if __name__ == '__main__':
    main()