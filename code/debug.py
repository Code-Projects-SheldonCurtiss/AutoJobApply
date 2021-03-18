from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# Auto updates but I'm too lazy
# from webdriver_manager.chrome import ChromeDriverManager

import os
import sys

import configparser

# import io

# Settings
jobtitles = ['', '']


# Stand Options
startlandingpage = ['https://www.glassdoor.com/index.htm', '']

mode = '1'

class Application:
    
    # Setups up our main shit
    def __init__(self):
        dirpath = os.getcwd()
        self.path = dirpath + '/code/'
        self.chromepath = dirpath + '/code/assets/chromedriver.exe'

        options = Options()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        # options.add_argument("user-data-dir=C:/Users/Admin/AppData/Local/Google/Chrome/User Data/Test")
        # options.add_argument("--profile-directory=test")
        self.options = options






    # Startup shit
    def setmode(self):
        # Use Launch option to select mode.
        # If no launch option then ask
        # If 'glassdoor' or 1
        # If 'linkedin' or 2

        
        try:
            mode = sys.argv[1]
        except:
            fug = 1

        while '1' not in mode and '2' not in mode:
            self.prettyprint('Please select the mode you want to use.', 1)
            self.prettyprint('1. GlassDoor')
            self.prettyprint('2. Linkedin')
            mode = input()

        self.mode = int(mode) - 1

    def initalsteps(self):
        config = configparser.ConfigParser()
        config.read(self.path + 'config.ini')
        
        if self.mode == 0:
            siteusername = config['DEFAULT']['GlassdoorUsername']
            sitepassword = config['DEFAULT']['GlassdoorPassword']
            

        if self.mode == 1:
            siteusername = config['DEFAULT']['LinkedinUsername']
            sitepassword = config['DEFAULT']['LinkedinPassword']

        print(siteusername)

    # Utility
    def prettyprint(self, text, lines=0):
        while lines > 0:
            lines = lines - 1
            print('\n')
        print(text)

    def debugoptions(self):
        self.prettyprint('Please select the mode you want to use.', 1)
        self.prettyprint('0. Exit debug loop.', 0)
        self.prettyprint('1. Test Xpath Selection', 0)
        self.prettyprint('2. Test Regex Selection', 0)

    def debug(self, mode):

        # # Template
        # if mode == 1:

        # Xpath
        if mode == 1:
            self.prettyprint('Please select the mode you want to use.', 1)

        # Regex
        if mode == 2:
            self.prettyprint('Please select the mode you want to use.', 1)



    def debugloop(self):
        loop = 1
        While loop == 1:
            self.debugoptions
            testingmode = input()
            try:
                testingmode = int(testingmode)
                if testingmode == 0:
                    loop = 0
                else:
                    self.debug(testingmode)

            except:
                self.prettyprint('Invalid selection.', 1)
                

    def start(self):
        self.setmode()
        self.initalsteps()
        # Launches Browser
        browser = webdriver.Chrome(options=self.options, executable_path=self.chromepath)
        wait = WebDriverWait(browser, 30)
        
        browser.get(startlandingpage[self.mode])

        loop = 1
        While loop == 1:
            testingmode = input()
            if 


        # self.browser.minimize_window()


bot = Application()
bot.start()


# Notes

# cmd = 'python38 output.py ' + fullchampname + ' ' + modifiedname + ' ' + region + ' ' + str(totaloutput) + ' ' + str(games) + ' ' + str(name) + ' ' + str(champ) + ' ' + str(overallwinrate) + ' ' + str(rank)
# cmds = shlex.split(cmd)
# subprocess.Popen(cmds, start_new_session=True)

# subdelay = 5
# sleep(subdelay)

# Notes

# import time, random, os, csv, datetime
# from bs4 import BeautifulSoup
# import pandas as pd
# import pyautogui
# from tkinter import filedialog, Tk
# import tkinter.messagebox as tm
# from urllib.request import urlopen
# import re
# import io
# import bs4  # import beautifulsoup
# from time import sleep

# import asyncio

# import shlex
# import subprocess
# import time
# import shutil
# import sys


# import time, random, os, csv, datetime

# from bs4 import BeautifulSoup
# import pandas as pd
# import pyautogui
# from tkinter import filedialog, Tk

# from urllib.request import urlopen
# import re

# import bs4  # import beautifulsoup
# from time import sleep
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


