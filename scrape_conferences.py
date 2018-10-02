import requests
import csv
from BeautifulSoup import BeautifulSoup
url = 'https://webdocs.cs.ualberta.ca/~zaiane/htmldocs/ConfRanking.html'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html)
table = soup.findAll('ul')
list_of_rows = []
rank = 1
conf_id = 1
for conf_list in soup.findAll('ul'):
    for conf in conf_list.findAll('span'):
        cells = []
        text = conf.text
        cells.append(conf_id)
        index = text.find(':')
        track = text[1:3]
        cells.append(track)
        conf_code = text[5:index]
        cells.append(conf_code)
        conf_name = text[index+1:]
        cells.append(conf_name)
        cells.append(rank)
        if track != ".." :
            list_of_rows.append(cells)
            conf_id = conf_id + 1
    rank = rank + 1
        # text = cell.text.replace('&amp;', ' ')
'''        track_code = text[:2]
        track_name = text[3:]
        list_of_tracks.append(track_code)
        list_of_tracks.append(track_name)
        list_of_rows.append(list_of_tracks)'''
print conf_id
outfile = open('data/conf.csv', 'wb')
writer = csv.writer(outfile)
writer.writerow(['id', 'track', 'code', 'name', 'prestige'])
writer.writerows(list_of_rows)
