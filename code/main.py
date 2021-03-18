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

import sqlite3
from time import sleep
# import io

# Settings # Load this from config?
jobtitles = ['software engineer', '']
location = ['United States']
firstname = 'Sheldon'
lastname = 'Curtiss'
name = firstname + ' ' + lastname
phonenumber = '‪2032000399‬'
email = 'sheldoncurtiss@gmail.com'


# Stand Options
startlandingpage = ['https://www.glassdoor.com/index.htm', '']

startapplypage = ['https://www.glassdoor.com/Job/us-software-engineer-jobs-SRCH_IL.0,2_IN1_KO3,20.htm', '']

class Application:
    
    # Setups up our main shit
    def __init__(self):
        # Set Main paths
        dirpath = os.getcwd()
        self.path = dirpath + '/code/'
        self.datapath = dirpath + '/code/data/'
        self.chromepath = self.datapath + 'browser/chromedriver.exe'

        options = Options()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        # options.add_argument("user-data-dir=C:/Users/Admin/AppData/Local/Google/Chrome/User Data/Test")
        # options.add_argument("--profile-directory=test")
        self.options = options



        # create_database(self.conn)
        
    def initializedb(self):
        if self.mode == 0:
            self.conn = sqlite3.connect(self.datapath + 'database/glassdoor.sqlite3')
        if self.mode == 1:
            self.conn = sqlite3.connect(self.datapath + 'database/linkedin.sqlite3')
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                url text PRIMARY KEY
            );''')

    def dblogic(self, text):
        ignore = 1
        # cursor = self.conn.cursor()
        # cursor.execute('SELECT is_married FROM marriage WHERE user_id=?', (person.id,))
        # is_registered = cursor.fetchone()
        # if not is_registered:
        #     cursor.execute('INSERT INTO marriage(user_id, is_married, married_by) VALUES(?,?,?)', (person.id, 1, ctx.author.mention))
        #     self.conn.commit()


    def launchbrowser(self):
        self.browser = webdriver.Chrome(options=self.options, executable_path=self.chromepath)
        self.wait = WebDriverWait(self.browser, 30)


    # Startup shit
    def setmode(self):
        # Use Launch option to select mode.
        # If no launch option then ask
        # If 'glassdoor' or 1
        # If 'linkedin' or 2

        mode = ' '
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

    # Site logic
    def initalsteps(self):
        config = configparser.ConfigParser()
        config.read(self.datapath + 'config.ini')
        
        self.browser.get(startlandingpage[self.mode])
        if self.mode == 0:
            siteusername = config['LOGININFO']['GlassdoorUsername']
            sitepassword = config['LOGININFO']['GlassdoorPassword']
            
            element = self.findelement('data-ga-lbl', 'Sign In')
            self.clickelement(element)

            element = self.findelement('id', 'userEmail')
            self.fillelement(element, siteusername)
            element = self.findelement('id', 'userPassword')
            self.fillelement(element, sitepassword)

            element = self.findelement('name', 'submit')
            self.clickelement(element)            
            sleep(10)

            # Click Glassdoor sign in button
            # "//*[contains(@data-ga-lbl,'Sign In')]"
            # G email
            # "//*[contains(@id,'userEmail')]"
            # G pass
            # "//*[contains(@id,'userPassword')]"
            # G submit
            # "//*[contains(@name,'submit')]"
            

        if self.mode == 1:
            siteusername = config['LOGININFO']['LinkedinUsername']
            sitepassword = config['LOGININFO']['LinkedinPassword']

        print(siteusername)

    def corelogic(self):
        # Glass door main logic
        self.browser.get(startapplypage[self.mode])
        sleep(5)
        if self.mode == 0:
            # element = self.findelement('data-ga-lbl', 'Sign In')
            # self.clickelement(element)
            # fug = 1
            
            phase = 1
            while phase != 4:
                for job in jobtitles:
                    pageloop = 1
                    while pageloop == 1:
                        # I want to go through all the jobs then increment up

                        # Need to do this logic once for each job title
                        # Want to do Remote > Onsite after
                        # Want to do Day posting limit and increase
                        # Job title entry
                        
                        # These sleeps suck. There's gotta be a way to 

                        element = self.findelement('aria-label', 'Search Keyword')
                        self.fillelement(element, job)
                        # Location entry
                        element = self.findelement('aria-label', 'Search Location')
                        self.fillelement(element, location)

                        # Submit search
                        element = self.findelement('aria-label', 'Search Submit')
                        self.clickelement(element)

                        # More button Drop down (for easy apply)
                        element = self.findelement('data-test', 'more-filter')
                        self.clickelement(element)

                        # Toggle Easy Apply - Need to do this since we only doing easy apply for now
                        element = self.findelement('class', 'css-174kf01 e1upcuzc1')
                        self.clickelement(element)

                        # Apply to remote jobs from start
                        if phase <= 3:
                            element = self.findelement('class', 'css-1cgz916 e1upcuzc0')
                            self.clickelement(element)

                        # More button Drop down (for easy apply)
                        element = self.findelement('data-test', 'more-filter')
                        self.clickelement(element)

                        # Set date time?
                        element = self.findelement('data-test', 'DATEPOSTED')
                        self.clickelement(element)

                        if phase < 3:
                            element = self.findelement('value', '7')
                            self.clickelement(element)
                        else:
                            element = self.findelement('value', '30')
                            self.clickelement(element)


                        # So now I need to go through each result
                        for button in self.browser.find_elements_by_xpath("//*[contains(@class,'react-job-listing')]"):
                            self.clickelement(button)
                            webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                            sleep(1)
                            webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                            sleep(1)
                            # button.send_keys(Keys.ESCAPE)
                            

                            # Click easy apply
                            element = self.findelement('data-test', 'applyButton')
                            # //*[contains(@data-test,'react-job-listing')]
                            self.clickelement(element)

                            self.fill()

                            webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                            sleep(1)
                            webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                            sleep(1)



                        # # Next Page - Need to make if there is no next page then do next search.
                        try:
                            element = self.findelement('data-test', 'pagination-next')
                            self.clickelement(element)
                        except:
                            pageloop = 0


    def fill(self):
        if self.mode == 0:
            continueloop = 1
            while continueloop < 10:


                # Fill logic should be in a func?
                # First name
                element = self.findelement('aria-labelledby', 'label-input-applicant.firstName')
                self.fillelement(element, location)

                # Name
                element = self.findelement('id', 'input-applicant.name')
                self.fillelement(element, name)

                # Email
                element = self.findelement('id', 'input-applicant.email')
                self.fillelement(element, email)

                # Phone number
                element = self.findelement('id', 'input-applicant.phoneNumber')
                self.fillelement(element, phonenumber)

                # Rsume upload
                jobfolder = job
                jobfolder = jobfolder.replace(' ', '')
                element = self.findelement('name', 'applicant.fileUpload')
                element.send_keys(self.datapath + "resumes/" + jobfolder +"/SheldonCurtiss.docx")
                # name, applicant.fileUpload
                # .send_keys(os.getcwd()+"/image.png")
                

                # Attempt to find and fill based on prefered
                # Otherwise do random shit.

                # Buttons that I need to find
                # Are you authorized to work in the United States? *
                # What is the highest level of education you have completed? *
                
                # Text I need to fill
                # How many years of software design experience do you have? *
                # How many years of people management experience do you have? *

                # Er some of them want capcha

                # <input class="icl-Radio-control" aria-labelledby="label-radio-option-7" type="radio" value="1" id="radio-option-7" name="q_d89e8988be00a87ab8ead40c12367c05">

                try:
                    # Continue Button - Should keep doing this until submit button is there.
                    element = self.findelement('id', 'form-action-continue')
                    self.clickelement(element)
                except:
                    print('Continue not found breaking loop off')
                    continueloop = 10


            # Submit application
            element = self.findelement('id', 'form-action-submit')
            self.clickelement(element)





    # Utility
    def verifyint(self, text):
        try:
            text = int(text)
        except:
            text = 0

        return text


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

        # # For Clicking a button
        # dropdown = self.browser.find_element_by_xpath("//*[contains(@class,'react-job-listing')]")
        # action = webdriver.common.action_chains.ActionChains(self.browser)
        # action.move_to_element(dropdown)
        # action.click()
        # action.perform()

        # # For filling text
        # inputElement = self.browser.find_element_by_xpath("//*[contains(@data-ga-lbl,'Sign In')]")

        # inputElement = self.browser.find_element_by_xpath("//input[@id='" + idsearch[0] + "']")
        # inputElement.clear()
        # inputElement.send_keys(value)


        # # Reg ex
        # page = self.browser.page_source
        # fullchampname = re.findall(r'<h2>Best (.*?)<\/h2>', page)
        # fullchampname = str(fullchampname[0])


        # # Template
        # if mode == 1:

        temp = 0
        # Xpath
        if mode == 1:
            self.prettyprint('Please select the mode you want to use.', 1)
            self.prettyprint('1. Text Fill', 0)
            self.prettyprint('2. Button Click', 0)
            temp = input()
            temp = self.verifyint(temp)
            
            if temp == 1:
                self.prettyprint('Please enter the search you want to use.', 1)
                temp = input()
                inputElement = self.browser.find_element_by_xpath(temp)
                inputElement.clear()
                inputElement.send_keys('TestTestTestTestTestTestTestTestTest')

            if temp == 2:
                self.prettyprint('Please enter the search you want to use. Value 1', 1)
                temp = input()
                self.prettyprint('Please enter the search you want to use. Value 2', 1)
                temp2 = input()

                element = self.findelement(temp, temp2)
                self.clickelement(element)

                # button = self.browser.find_element_by_xpath(temp)
                # action = webdriver.common.action_chains.ActionChains(self.browser)
                # action.move_to_element(button)
                # action.click()
                # action.perform()


                


        # Regex
        if mode == 2:
            self.prettyprint('Please select the mode you want to use.', 1)

        if mode == 3:
            self.prettyprint('Please enter jobtitle', 1)
            temp = input()
            jobfolder = temp
            jobfolder = jobfolder.replace(' ', '')
            element = self.findelement('name', 'applicant.fileUpload')
            element.send_keys(self.datapath + "resumes/" + jobfolder +"/SheldonCurtiss.docx")


        if mode == 4:

            urls = re.findall(r'"champions=(.*?)"', self.browser.page_source)
            self.prettyprint('Please enter jobtitle', 1)
            temp = input()
            jobfolder = temp
            jobfolder = jobfolder.replace(' ', '')
            element = self.findelement('name', 'applicant.fileUpload')
            element.send_keys(self.datapath + "resumes/" + jobfolder +"/SheldonCurtiss.docx")

    def findelement(self, location, value):
        element = None
        try:
            try:
                element = self.browser.find_element_by_xpath("//*[contains(@" + location + ",'" + value + "')]")
                return element
            except:

                seq = self.browser.find_elements_by_tag_name('iframe')
                for x in range(0, len(seq)):
                    self.browser.switch_to.default_content()
                    try:
                        self.browser.switch_to.frame(int(x))
                        element = self.browser.find_element_by_xpath("//*[contains(@" + location + ",'" + value + "')]")
                        return element
                    except:
                        subframe = self.browser.find_elements_by_tag_name('iframe')
                        for y in range(0, len(subframe)):
                            try:
                                print("Sub iframe-" + str(y))
                                self.browser.switch_to.frame(int(y))
                                element = self.browser.find_element_by_xpath("//*[contains(@" + location + ",'" + value + "')]")
                                return element
                            except:
                                continue
                        continue
        except:
            print('Cant find')

    def clickelement(self, element):
        try:
            action = webdriver.common.action_chains.ActionChains(self.browser)
            action.move_to_element(element)
            action.click()
            action.perform()
            sleep(2)
        except:
            print('Cant click')

    def fillelement(self, element, text):
        try:
            action = webdriver.common.action_chains.ActionChains(self.browser)
            while element.get_attribute('value') != '':
                element.send_keys(Keys.BACK_SPACE)
            # element.send_keys(' ')
            # element.clear()
            element.send_keys(text)
            sleep(1)
        except:
            print('Cant type')

    def debugloop(self):
        loop = 1
        while loop == 1:
            self.debugoptions()
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
        self.initializedb()
        self.launchbrowser()
        # sleep(3)
        self.initalsteps()
        self.debugloop()
        self.corelogic()


        



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

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


