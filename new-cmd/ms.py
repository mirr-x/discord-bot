import asyncio
import requests
from bs4 import BeautifulSoup
import time
from termcolor import colored
from discordPrinte import PrinteDiscordcopy
import os

import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
import time

url = os.environ['URL']
data = os.environ['DATE']
headers = os.environ['HEADER']

max_retries = 50
retry_delay = 10  # seconds


def extract_important_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.select('tr[style="background:#fbfbfb;"]')
    important_info = []
    for row in rows:
        cells = row.find_all('td')
        subject = cells[0].text.strip()
        gbr = [cell.text.strip() for cell in cells[1:]]
        important_info.append((subject, gbr))
    return important_info


async def send_to_discord(info, channel):
    message = "Important Information:\n"
    for subject, gbr in info:
        message += f"**{subject}**: {', '.join(gbr)}\n"
    await channel.send(message)


async def check_url_status(channel):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, data=data, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            important_info = extract_important_info(response.text)
            await send_to_discord(important_info, channel)
            PrinteDiscord(f'```diff\n+ Working OK {response.status_code}✅ \n```')
            # print(colored(f"Working OK {response.status_code}", "green"))
            break  # Exit the loop if the request was successful
        except ConnectionError as e:
            PrinteDiscord(f'```diff\n- Connection error: {e}. Retrying in {retry_delay} seconds...❌ \n```')
            # print(colored(f"Connection error: {e}. Retrying in {retry_delay} seconds...", "red"))
        except Timeout as e:
            PrinteDiscord(f'```diff\n- Timeout error: {e}. Retrying in {retry_delay} seconds...❌ \n```')
            # print(colored(f"Timeout error: {e}. Retrying in {retry_delay} seconds...", "red"))
        except RequestException as e:
            PrinteDiscord(f'```diff\n- Request error: {e}. Retrying in {retry_delay} seconds...❌ \n```')
            # print(colored(f"Request error: {e}. Retrying in {retry_delay} seconds...", "red"))
        await asyncio.sleep(retry_delay)
    else:
        await channel.send("Failed to connect after several attempts.")
        print("Failed to connect after several attempts.")


async def main(channel):
    await check_url_status(channel)
