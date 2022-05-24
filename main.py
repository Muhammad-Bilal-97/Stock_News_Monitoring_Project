import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "Z0CW4JAYLRK1K67D"
NEWS_API_KEY = "9a0c194ef3984c2c8d963d95b775c213"

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

# Getting yesterday's closing stock price.
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
# print(response)
data = response.json()["Time Series (Daily)"]
# print(data)
data_list = [value for (key, value) in data.items()]
# print(data_list)
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
# print(yesterday_close_price)


# Getting the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
# print(day_before_yesterday_closing_price)


# Finding the positive difference between yesterday_closing_price and day_before_yesterday_closing_price.
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
# print(difference)
up_down = None
if difference > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"

# Working out the % difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
# print(diff_percent)


# Getting the first 3 news pieces for the COMPANY_NAME.
if abs(diff_percent) > 1:
    new_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=new_params)
    articles = news_response.json()["articles"]
    # print(articles)

    # Using the Python slice operator to create a list that contains the first 3 articles.
    three_articles = articles[:3]
    # print(three_articles)

    # to send a separate message with each article's title and description to your phone number.
    # Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\n Headline: {article['title']}. \nBrief: {article['description']}"
        for article in three_articles]
    # Send each article as a separate message via Twilio.
    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages \
            .create(
            body=article,
            from_='+16053163407',
            to='+923045678856'
        )
