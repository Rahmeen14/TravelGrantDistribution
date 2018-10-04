import requests
import csv
from BeautifulSoup import BeautifulSoup
url = 'https://webdocs.cs.ualberta.ca/~zaiane/htmldocs/ConfRanking.html'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html)
table = soup.find('table', attrs = {'width': '280'})
list_of_tracks = []
list_of_codes = []
list_of_rows = []
for tab in table.findAll('table'):
    for row in tab.findAll('tr'):
        list_of_tracks = []
        for cell in row.findAll('td'):
            text = cell.text.replace('&amp;', ' ')
            track_code = text[:2]
            track_name = text[3:]
            list_of_tracks.append(track_code)
            list_of_tracks.append(track_name)
        list_of_rows.append(list_of_tracks)
outfile = open('data/tracks.csv', 'wb')
writer = csv.writer(outfile)
writer.writerow(['code', 'track'])
writer.writerows(list_of_rows)