import json
import sys
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def sendAlertMessage(alert, channelName):
    url = os.environ.get('webhook')
    message = alert
    title = (f"REDX FFRM Alert :redx:")
    slack_data = {
        "username": "Auto Generated Alert",
        "icon_emoji": ":alert:",
        "channel" : channelName,
        "attachments": [
            {
                "color": "#EB1D36",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)