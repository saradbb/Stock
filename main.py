from datetime import timedelta, date
import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

#RETRIVING THE API KEYS FROM ENVIORNMENT VARIABLE
ALPHA_VANTAGE_API = os.environ.get("ALPHA_VINTAGE_KEY")
MESSAGE_KEY = os.environ.get("MESSAGE_KEY")
NEWS_API_KEY  = os.environ.get("NEWS_KEY")
MESSAGE_TOKEN = os.environ.get("MESSAGE_TOKEN")


STOCK = input("Insert a Stock ticker: ")


#CHECK IF STOCK MOVED CONSIDERABLY TODAY (CONSIDERABLE MEANING 5% movement)
url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + STOCK + "&apikey=" + ALPHA_VANTAGE_API
data = requests.get(url).json()["Time Series (Daily)"]   #DAILY STOCK DATA
lst = list(data.keys())
today = lst[0]    #IF CHECKED BEFORE MARKET CLOSE, TODAY REFERS TO CLOSE PRICE PREVIOUS CLOSE DAY
yesterday = lst[1]
percent =(float(data[today]["4. close"]) - float(data[yesterday]["4. close"]) ) / float(data[yesterday]["4. close"]) * 100


#IF THE STOCK MOVED 5% OR MORE
if  abs(percent) > 5:

    # Setting up client for Twillo Messaging
    account_sid = "AC146bd719b7377b7751aa78879325f8b6"
    auth_token = MESSAGE_TOKEN
    client = Client(account_sid, auth_token)

    #Getting news of company making big moves
    url = "https://newsapi.org/v2/everything?q=" + STOCK + "&apiKey=" + NEWS_API_KEY
    data = requests.get(url).json()['articles']

    #Creating the text to be sent to the user
    symbol = "🔺" if percent > 0 else "🔻"
    body = STOCK + " is " + symbol + str(percent) + " today\n"


    for i in range(0,3):
        #ONLY USING THE HEADLINES AND TITLE OF THREE MOST RECENT NEWS
        body += "Headline: " + data[i]['title'] + "\n"
        body += "Description: " + data[i]['description'] + "\n********\n"

        #SEND MESSAGE TO THE USER
    message = client.messages.create(
        body=body,
        from_='+18305417609',
        to='+15627166581'  # Not my number
    )

else:
    print("SMALL CHANGE")
