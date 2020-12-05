import csv
from requests_html import HTMLSession
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pathlib import Path

def CSVMaker(header):
    with open('publicmutual.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

def CSVEditor(updateline):
    with open('publicmutual.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(updateline)

def CSVReader():
    fileopener = open('publicmutual.csv', 'r')

    collectiondata = csv.reader(fileopener, delimiter=',')

    return collectiondata

my_url = 'https://www.publicmutual.com.my/Our-Products/UT-Fund-Prices'

#Opening a connection
session = HTMLSession()
client = session.get(my_url)

print("Loading data...")
client.html.render(sleep=3)


page_html = client.html.html

#HTML Parsing
pagesoup = BeautifulSoup(page_html, "html.parser")
container = pagesoup.find("table", {"class":"fundtable col-sm-12"})

#Container has all the funds
getfunds = container.find_all("td")

#Prepares the csv file
datalist = []


#Read in the CSV for comparing
#if filename.exists():
#    fileopen = open(filename)
#    csvfile = list(csv.reader(f))

#Make that CSV
#else:
label = ["Date: ", "Fund: ", "Abbreviation: ", "Price: ", "Rise/Descend: ", "Percentage Change: "]
#CSVMaker(label)

existingdata = CSVReader()

for j in range(154):
    
    for i in range(6):
        datalist.append(getfunds[i+(j*6)].text) 
    #CSVEditor(datalist)

    for row in existingdata:
        try:
            print("{}: ".format(row[1]))
            difference = float(datalist[3]) - float(row[3])
            print(difference)
        except:
            print("This is not integer wtf...")

    
    datalist = []

#print("CSV File Successfully Generated!")