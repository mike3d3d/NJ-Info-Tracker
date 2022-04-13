from bs4 import BeautifulSoup
from pip._vendor import requests
import csv
import time


def trafficAlerts():
  #Makes request from nj1015 traffic data
  html_text = requests.get('https://nj1015.com/traffic/').text
  soup = BeautifulSoup(html_text, 'lxml') #Instantiates BeautifulSoup 
  
  #Finds the div of the class 'pod-content' which contains main text body
  main_body = soup.find('div', class_ = 'pod-content')
  
  #Skips the first <h3> tag to find the "Main Traffic Alerts: ..." tag
  garbage_tag = main_body.find('h3')
  main_alert = garbage_tag.find_next_sibling('h3').text
  
  #Replaces all <br> in mainBody with new line for formatting
  for br in main_body.find_all("br"):
    br.replace_with("\n\n")


  print("\n")  
  print(main_alert)
  
  print("------------------------------------")
  
  #Grabs all <p> in the mainBody and prints only the first category
  alert_body = main_body.find_all('p')  
  for alerts in range(3, 4):
    print(alert_body[alerts].text)
  
  
  #Loops through all siblings of garbage_tag to extract 
  #"Ongoing Advisories" tag
  print("\n")
  h3_successor = garbage_tag.find_next_siblings('h3')
  
  #Loop to print "Ongoing Advisories"
  for tags in range(1, len(h3_successor)):
    print(h3_successor[tags].text)
    
  print("-------------------")
  #Loops from "Ongoing Advisories" to end to print rest of alerts
  for alerts in range(4, len(alert_body)):
    print(alert_body[alerts].text)
    print("\n")


def gasAlerts():

  html_text = requests.get('https://www.autoblog.com/nj-gas-prices/sort-price/').text
  soup = BeautifulSoup(html_text, 'lxml') #Instantiates BeautifulSoup 


  gas_list = soup.find_all('li', class_ = "shop")
  print(" ")
  print("Top 3 Cheapest Gas Locations in NJ")
  print("-----------------------------------")
  

  for element in range(0, 3):
      data = str(gas_list[element].text.strip())
      x = data.replace("¤", "$")
      print(x)
      print("\n")




if __name__ == '__main__':

  print(" ")
  print("#########################################################")
  print("#            Welcome to NJ Info Tracker!                #")
  print("#########################################################")
  print(" ")
  input = input("Would you like to track NJ Traffic or NJ Gas? ")
  input = input.lower()
  if input == "traffic":
    while True:
      trafficAlerts()
      wait = 15  
      print(f'Next update in {wait} minutes...')
      print("Press ctrl + c to exit")
      time.sleep(wait * 60) #wait for how long before refrehing

  if input == "gas":
    while True:
      gasAlerts()
      wait = 15
      print(f'Next update in {wait} minutes...')
      print("Press ctrl + c to exit")
      time.sleep(wait * 60) #wait for how long before refrehing

