import requests
import os 


class PrinteDiscordcopy:
    def __init__(self, data):
        self.data = {"content": data}  # Ensure data is in the correct format
        self.url = 'https://discord.com/api/webhooks/1330874159772860507/zt759H8wUIhbk_YsrgjDc3FSBm-ZDDi3z0Pj3g3etRPXt99nJEZoyxdVafi_OzYfEHdZ'
        self.send()

    def send(self):
        response = requests.post(self.url, json=self.data)
        if response.status_code != 204:
            print(f'Failed to send message to Discord: {response.status_code}, {response.text}')
