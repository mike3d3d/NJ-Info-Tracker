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

def weatherAlerts():
  html_text = requests.get('https://weather.com/weather/tenday/l/a598be7242b5e38c214b05c9e8009a313c4a45c0ba93ff764f1fbe2c7aaee911').text
  soup = BeautifulSoup(html_text, 'lxml') #Instantiates BeautifulSoup 

  day_list = soup.find('div', class_ = "DailyForecast--DisclosureList--msYIJ")
  today = day_list.find('details', class_ = "Disclosure--themeList--25Q0H") #Contains today's forecast

  #Today's forecast
  today_date = today.summary.h2.get_text(" ") #Contains today's date
  today_temp_low = today.find('span', class_ = "DetailsSummary--lowTempValue--3H-7I").get_text(" ") #Contains today's current temp
  today_condition = today.find('span', class_ = "DetailsSummary--extendedData--365A_").get_text(" ") #Contains today's weather specifics
  today_precipitation = today.find('div', class_ = "DetailsSummary--precip--1ecIJ").get_text(" ") #Contains today's precipitation

  #Skips to tomorrow
  tomorrow = today.find_next_sibling('details')
  tomorrow_date = tomorrow.summary.h2.get_text(" ") #Contains tomorrow's date
  tomorrow_temp_low = tomorrow.find('span', class_ = "DetailsSummary--lowTempValue--3H-7I").get_text(" ") #Contains tomorrow's low temp
  tomorrow_temp_high = tomorrow.find('span', class_ = "DetailsSummary--highTempValue--3Oteu").get_text(" ") #Contains tomorrow's high temp
  tomorrow_condition = tomorrow.find('span', class_ = "DetailsSummary--extendedData--365A_").get_text(" ") #Contains tomorrow's weather specifics
  tomorrow_precipitation = tomorrow.find('div', class_ = "DetailsSummary--precip--1ecIJ").get_text(" ") #Contains tomorrow's precipitation

  #Skips to day after tomorrow
  second_day = tomorrow.find_next_sibling('details')
  second_date = second_day.summary.h2.get_text(" ") #Contains tomorrow's date
  second_temp_low = second_day.find('span', class_ = "DetailsSummary--lowTempValue--3H-7I").get_text(" ") #Contains next day's low temp
  second_temp_high = second_day.find('span', class_ = "DetailsSummary--highTempValue--3Oteu").get_text(" ") #Contains next day's high temp
  second_condition = second_day.find('span', class_ = "DetailsSummary--extendedData--365A_").get_text(" ") #Contains next day's weather specifics
  second_precipitation = second_day.find('div', class_ = "DetailsSummary--precip--1ecIJ").get_text(" ") #Contains next day's precipitation


  #Skips to third day
  third_day = second_day.find_next_sibling('details')
  third_date = third_day.summary.h2.get_text(" ") #Contains tomorrow's date
  third_temp_low = third_day.find('span', class_ = "DetailsSummary--lowTempValue--3H-7I").get_text(" ") #Contains third day's low temp
  third_temp_high = third_day.find('span', class_ = "DetailsSummary--highTempValue--3Oteu").get_text(" ") #Contains third day's high temp
  third_condition = third_day.find('span', class_ = "DetailsSummary--extendedData--365A_").get_text(" ") #Contains third day's weather specifics
  third_precipitation = third_day.find('div', class_ = "DetailsSummary--precip--1ecIJ").get_text(" ") #Contains third day's precipitation

  print(" ")
  print("Today's forecast")
  print("-----------------")
  print(today_date, ":", today_temp_low, "|", today_condition, "|", today_precipitation, "\n")
  print("Next Three Day's Forecast")
  print("--------------------------")
  print(tomorrow_date, ":", tomorrow_temp_high, "/", tomorrow_temp_low, "|", tomorrow_condition, "|", tomorrow_precipitation, "\n")
  print(second_date, ":", second_temp_high, "/", second_temp_low, "|", second_condition, "|", second_precipitation, "\n")
  print(third_date, ":", third_temp_high, "/", third_temp_low, "|", third_condition, "|", third_precipitation, "\n")



if __name__ == '__main__':

  print(" ")
  print("#########################################################")
  print("#            Welcome to NJ Info Tracker!                #")
  print("#########################################################")
  print(" ")
  input = input("Would you like to track NJ Traffic, Gas, or Weather? ")
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
  
  if input == 'weather':
    while True:
      weatherAlerts()
      wait = 15
      print(f'Next update in {wait} minutes...')
      print("Press ctrl + c to exit")
      time.sleep(wait * 60) #wait for how long before refrehing     

