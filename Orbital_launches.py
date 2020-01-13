import requests
import datetime
import csv
from bs4 import BeautifulSoup

file_reader = open("URL.txt", "r")
file_reader1 = open("1.txt", "w")
url = file_reader.read()

orbital_wiki = requests.get(url)
orbital_soup = BeautifulSoup(orbital_wiki.content, 'html.parser')

mw_content_text = orbital_soup.find(id='mw-content-text')
mw_content_text = mw_content_text.find_all('div')[0]
orbital_launches = mw_content_text.find_all('table')

file_reader1.write(orbital_launches[3].prettify())
orbital_launches = orbital_launches[3].find('tbody')
orbital_launches = orbital_launches.find_all('tr')

launches = dict()
index = 4
while(index < len(orbital_launches)):
	columns = orbital_launches[index].find_all('td')
	if(len(orbital_launches[index].find_all(recursive=False)) > 1):
		rowspan = columns[0]['rowspan']

		date = columns[0].text
		
		if(len(date.split("(")) > 1):
			date = date.split("(")[0]
			if(len(date.split(")")) > 1):
				date = date.split(")")[1]
		date = date.split("[")[0]
		date = date.strip()
		if(len(date.split(":")) == 3):
			date = date + "2019"
		elif(len(date.split(":")) == 2):
			date = date + ":002019"
		else:
			date = date + "00:00:002019"


		date = datetime.datetime.strptime(date, '%d %B%H:%M:%S%Y')
		value = 0
		# print(date.date())
		end_index = index + int(rowspan)
		index = index + 1
		while(index < end_index):
			payload = orbital_launches[index].find_all('td')
			status = payload[len(payload) - 1].text
			status = status.strip()
			if(status == "Successful" or status == "Operational" or status == "En Route"):
				value = value + 1
				index = end_index
			else:
				index = index + 1

		if date.date() in launches.keys():
			launches[date.date()] = launches[date.date()] + 1
		else:
			launches[date.date()] = (value)


		index = end_index
	else:
		index = index + 1



sdate = datetime.date(2019, 1, 1)   # start date
edate = datetime.date(2019, 12, 31)   # end date

delta = edate - sdate       # as timedelta

alldates = dict()
for i in range(delta.days + 1):
    day = sdate + datetime.timedelta(days=i)
    if day not in launches.keys():
    	# date = datetime.datetime.strptime(day, '%Y-%M-%d')
    	alldates[day] = 0
    	print(day, alldates[day])

# launches.update(alldates)
launches = dict(launches,**alldates)
for key, value in launches.items():
	print(key ,value)

dictlist = []
for key, value in launches.items():
	# print(key.isoformat() + "," + str(value))
	temp = [key.isoformat(), value]
	dictlist.append(temp)

with open("output.csv", 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)
    for a in dictlist:
    	csvwriter.writerow(a)

    csvfile.close()