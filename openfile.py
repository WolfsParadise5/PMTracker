#Import required modules
import csv
import os.path
import time
from requests_html import HTMLSession
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import date

def MainScreen():
    
    print("Welcome to the financial tracker!")
    print("Currently only overseeing Public Mutual")

    print("Pick an option: (1/2/3)")
    print(" ")

    print("1. Read current financial data")
    print("2. Create a financial CSV file")
    print("3. Check the Difference")
    print("4. Create auto check")
    print("5. Exit")
    print(" ")

    numinput = 99
    
    while numinput > 5 or numinput <= 0:
        
        numinput = int(input("Enter preffered input: "))
        if numinput > 5 or numinput <= 0:
            print("Invalid input, please try again.")
            
    
    return numinput

def Switch(option):
    
    if option == 1:
        ReadData()

    elif option == 2:
        if os.path.exists('publicmutual.csv'):
            optionNow = input("File already exists, Continue anyway? (Y/N)")
            if optionNow == "Y":
                CreateCSVFile()
        else:
            CreateCSVFile()

    elif option == 3:
        if os.path.exists('publicmutual.csv'):
            CheckDifference()
        else:
            print("File already exists")

    elif option == 4:
        AutoMaker()


def GetData():
    #Data prep
    my_url = 'https://www.publicmutual.com.my/Our-Products/UT-Fund-Prices'

    #Opening a connection
    session = HTMLSession()
    client = session.get(my_url)

    print("Loading data...")
    client.html.render(sleep=5)
    page_html = client.html.html

    #HTML Parsing
    pagesoup = BeautifulSoup(page_html, "html.parser")
    container = pagesoup.find("table", {"class":"fundtable col-sm-12"})

    #Container has all the funds
    getfunds = container.find_all("td")
    return getfunds


def ReadData():
    datalist = []
    funds = GetData()

    #Organize the data
    for j in range(154):
        for i in range(6):
            datalist.append(funds[i+(j*6)].text)
        print("Fund {}({}): {}".format(datalist[1], datalist[2], datalist[3]))
        datalist = []   #Reset for the next row display

        print(" ")
    
    input("Enter to continue")


def CreateCSVFile():
    datalist = []
    funds = GetData()

    #Open CSV File to put the column
    with open('publicmutual.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date: ", "Fund: ", "Abbreviation: ", "Price: ", "Rise/Descend: ", "Percentage Change: "])
    
    #Put the data in the CSV
    with open('publicmutual.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        
        for j in range(154):
            for i in range(6):
                datalist.append(funds[i+(j*6)].text)
            writer.writerow(datalist)
            datalist = [] #Reset for the next row input

    print("CSV File Generated!")
    input("Enter to continue")


def CheckDifference():
    #Data Gathering
    existingDataList = []
    newDataList = []
    differencelist = []
    datalist = []
    fundlist = []
    fundShortForm = []
    difference = 0
    

    #Open Existing CSV
    fileopener = open('publicmutual.csv', 'r')
    collectiondata = csv.reader(fileopener, delimiter=',')

    #Get Current data
    funds = GetData()

    #Get both existing and current funds together
    for row in collectiondata:
        existingDataList.append(row[3])
        
    for j in range(154):
        for i in range(6):
            datalist.append(funds[i+(j*6)].text)
        
        newDataList.append(datalist[3])
        fundlist.append(datalist[1])
        fundShortForm.append(datalist[2])

        datalist = []

    existingDataList.pop(0)

    for i in range(len(existingDataList)):  #Can be either existingDataList or newDataList
        difference = float(newDataList[i]) - float(existingDataList[i])

        #Get properly formatted price        
        difference = round(difference, 2)
        differencelist.append(difference)

    for j in range(len(newDataList)):
        print("Fund {}({}): RM{}".format(fundlist[j], fundShortForm[j], differencelist[j]))

    print("  ")
    input("Enter to continue. ")

def AutoMaker():

    def MenuOption():
        time = date.today().strftime("%d/%m/%Y")
        
        print("Today is {}".format(time))
        
        print(" ")
        print("How would you like your automation to be saved?")
        
        print(" ")
        print("1. Daily")
        print("2. Weekly")
        print("3. Monthly")
        print(" ")

        saveOption = 1
        while saveOption < 1 or saveOption > 3: 
            
            saveOption = int(input("Enter option: "))
            if saveOption < 1 or saveOption > 3:
                print("Invalid input, please try again")
            else:
                return saveOption
    
    saveOption = MenuOption()
    
    if saveOption == 1:
        listsave = ["D", time.time(),'86400']

    elif saveOption == 2:
        listsave = ["W", time.time(),'604800']

    elif saveOption == 3:
        listsave = ["M", time.time()]
        nexttime = 18144000 #30days

        #Number of days based of months
        

    
    input("Enter to continue. ")

#Check for auto-check setting
if os.path.exists('auto.sav'):
    print("Checking recent changes...")

option = 0
while option != 5:
    option = MainScreen()
    Switch(option)

