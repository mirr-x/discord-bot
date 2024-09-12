#!/usr/bin/python3
""" github force codespace to be open 24/7 """

import time
import json
from selenium.webdriver.common.by import By
from module.discordPrinte import PrinteDiscord
import os


class KeepSpaceOpen:
    def __init__(self, browser):
        self.browser = browser

    def login_github_with_cookies(self):
        browser = self.browser
        browser.get('https://github.com/')
        time.sleep(10)

        # ? Load cookies from the JSON file
        
        cookies = os.environ['GITHUB_COOKIE']
        for cookie in cookies:
            if 'sameSite' in cookie and cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                del cookie['sameSite']
            browser.add_cookie(cookie)

        # ? Refresh the page to log in with cookies
        browser.refresh()
        time.sleep(10)

    def open_codeSpace(self):
        browser = self.browser
        browser.get('https://github.com/codespaces')
        time.sleep(10)

        # ? Enter the codespace
        browser.find_element(By.XPATH, '/html/body/div[1]/div[5]/main/div/div[2]/div[3]/div/div[2]/div/div/div[1]/div[2]/div/a/span').click()
        time.sleep(60)

        # @Switch to the codespace tab
        codespace_tab = browser.window_handles[1]
        browser.switch_to.window(codespace_tab)
        time.sleep(50)

        # ? Check if this Button is available
        try:
            browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/button').click()
        except:
            print('Button RESTART not found')
        time.sleep(60)


        # @Close all other tabs
        for handle in browser.window_handles:
            if handle != codespace_tab:
                browser.switch_to.window(handle)
                browser.close()

        # @Switch back to the codespace tab
        browser.switch_to.window(codespace_tab)

        # @smulate user activity
        time.sleep(10)
   
        # ? Keep the codespace open (refresh the page every 120 seconds)
        PrinteDiscord('```diff\n+ codespace is ✅ \n```')
        time.sleep(1800) # 30 minutes
        # ?Close the codespace
        browser.get('https://github.com/codespaces')
        time.sleep(6)

        # # ? close button
        # browser.find_element(By.XPATH, '//button[@id and @aria-controls and @aria-haspopup="true"]').click()
        # time.sleep(4)
        # browser.find_element(By.XPATH, '//button[.//span[text()="Stop codespace"]]').click()
        # time.sleep(6)
        # PrinteDiscord('```diff\n- codespace is ❌ \n```')
        # time.sleep(6)
