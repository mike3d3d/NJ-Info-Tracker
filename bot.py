import discord
import os
from dotenv import load_dotenv
from pip._vendor import requests
from bs4 import BeautifulSoup

load_dotenv()

def gasAlerts():

  html_text = requests.get('https://www.autoblog.com/nj-gas-prices/sort-price/').text
  soup = BeautifulSoup(html_text, 'lxml') #Instantiates BeautifulSoup 


  gas_list = soup.find_all('li', class_ = "shop")
  output = []

  for element in range(0, 3):
      data = str(gas_list[element].text.strip())
      x = data.replace("¤", "$")
      output.append(x)
      
  one = output[0]
  two = output[1]
  three = output[2]
  return one + "\n\n" + two + "\n\n" + three

def weatherAlerts():
  html_text = requests.get('https://weather.com/weather/tenday/l/a598be7242b5e38c214b05c9e8009a313c4a45c0ba93ff764f1fbe2c7aaee911').text
  soup = BeautifulSoup(html_text, 'lxml') #Instantiates BeautifulSoup 
  
  day_list = soup.find('div', class_ = "DailyForecast--DisclosureList--msYIJ")
  today = day_list.find('details', class_ = "Disclosure--themeList--25Q0H") #Contains today's forecast

  #Today's forecast
  today_date = today.summary.h3.get_text(" ") #Contains today's date
  today_temp_low = today.find('span', class_ = "DetailsSummary--lowTempValue--3H-7I").get_text(" ") #Contains today's current temp
  today_condition = today.find('span', class_ = "DetailsSummary--extendedData--365A_").get_text(" ") #Contains today's weather specifics
  today_precipitation = today.find('div', class_ = "DetailsSummary--precip--1ecIJ").get_text(" ") #Contains today's precipitation

  #Skips to tomorrow
  tomorrow = today.find_next_sibling('details')
  tomorrow_date = tomorrow.summary.h3.get_text(" ") #Contains tomorrow's date
  tomorrow_temp_low = tomorrow.find('span', class_ = "DetailsSummary--lowTempValue--3H-7I").get_text(" ") #Contains tomorrow's low temp
  tomorrow_temp_high = tomorrow.find('span', class_ = "DetailsSummary--highTempValue--3Oteu").get_text(" ") #Contains tomorrow's high temp
  tomorrow_condition = tomorrow.find('span', class_ = "DetailsSummary--extendedData--365A_").get_text(" ") #Contains tomorrow's weather specifics
  tomorrow_precipitation = tomorrow.find('div', class_ = "DetailsSummary--precip--1ecIJ").get_text(" ") #Contains tomorrow's precipitation

  #Skips to day after tomorrow
  second_day = tomorrow.find_next_sibling('details')
  second_date = second_day.summary.h3.get_text(" ") #Contains tomorrow's date
  second_temp_low = second_day.find('span', class_ = "DetailsSummary--lowTempValue--3H-7I").get_text(" ") #Contains next day's low temp
  second_temp_high = second_day.find('span', class_ = "DetailsSummary--highTempValue--3Oteu").get_text(" ") #Contains next day's high temp
  second_condition = second_day.find('span', class_ = "DetailsSummary--extendedData--365A_").get_text(" ") #Contains next day's weather specifics
  second_precipitation = second_day.find('div', class_ = "DetailsSummary--precip--1ecIJ").get_text(" ") #Contains next day's precipitation


  #Skips to third day
  third_day = second_day.find_next_sibling('details')
  third_date = third_day.summary.h3.get_text(" ") #Contains tomorrow's date
  third_temp_low = third_day.find('span', class_ = "DetailsSummary--lowTempValue--3H-7I").get_text(" ") #Contains third day's low temp
  third_temp_high = third_day.find('span', class_ = "DetailsSummary--highTempValue--3Oteu").get_text(" ") #Contains third day's high temp
  third_condition = third_day.find('span', class_ = "DetailsSummary--extendedData--365A_").get_text(" ") #Contains third day's weather specifics
  third_precipitation = third_day.find('div', class_ = "DetailsSummary--precip--1ecIJ").get_text(" ") #Contains third day's precipitation


  return today_date + ": " + today_temp_low +  " | " + today_condition + " | " +  today_precipitation + "\n\n" +  tomorrow_date + ": " + tomorrow_temp_high + " / " +tomorrow_temp_low + " | " + tomorrow_condition + " | " + tomorrow_precipitation + "\n\n" + second_date + ": " + second_temp_high + " / " + second_temp_low + " | " + second_condition + " | " + second_precipitation + "\n\n" + third_date + ": " + third_temp_high + " / " + third_temp_low + " | " + third_condition + " | " + third_precipitation + "\n\n"

def trafficAlerts():

  html_text = requests.get('https://nj1015.com/traffic/').text
  soup = BeautifulSoup(html_text, 'lxml') 
  
  main_body = soup.find('div', class_ = 'pod-content')
  

  garbage_tag = main_body.find('h3')
  

  for br in main_body.find_all("br"):
    br.replace_with("\n\n")

  output = []
  

  alert_body = main_body.find_all('p')  
  for alerts in range(3, 4):
    output.append(alert_body[alerts].text)
    

  h3_successor = garbage_tag.find_next_siblings('h3')
  

  for tags in range(1, len(h3_successor)):
    output.append(h3_successor[tags].text)
    
  for alerts in range(4, len(alert_body)):
    output.append(alert_body[alerts].text)

  one = output[0]
  two = output[1]
  three = output[2]
  four = output[3]

  return one + "\n\n" + two + "\n\n" + three + "\n\n" + four

client = discord.Client() #Creates connection to Discord API

gasEmbed = discord.Embed(title = "Top 3 Cheapest Gas Locations in NJ", description = "These are the three cheapest gas stations in the state along with their location, distance, and price", colour=0x87CEEB)
gasEmbed.add_field(name = "Cheapest Gas", value = gasAlerts(), inline = False )

weatherEmbed = discord.Embed(title = "NJ Weather Forecast", description = "Displays today's weather conditions as well as the weather for the upcoming three days", colour=0x87CEEB)
weatherEmbed.add_field(name = "Weather Alerts", value = weatherAlerts(), inline = False )

trafficEmbed = discord.Embed(title = "NJ Traffic Updates", description = "Displays today's ongoing traffic advisories on the roads across Jersey. Does not update on weekends", colour=0x87CEEB)
trafficEmbed.add_field(name = "Traffic Alerts", value = trafficAlerts(), inline = False )

help = discord.Embed(title = "Help", description = "These are the current commands supported by the bot", colour=0x87CEEB)
help.add_field(name = "Commands", value = "$gas: Displays gas tracker \n\n $traffic: Displays traffic updates \n\n $weather:  Displays current weather updates", inline = False )

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$gas'):
        await message.channel.send(embed = gasEmbed)

    if message.content.startswith('$weather'):
        await message.channel.send(embed = weatherEmbed)

    if message.content.startswith('$traffic'):
        await message.channel.send(embed = trafficEmbed)

    if message.content.startswith("$help"):
      await message.channel.send(embed = help)


client.run(os.getenv("DISCORD_TOKEN"))

