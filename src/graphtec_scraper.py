from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import os

class Graphtec_Scraper():
    def __init__(self,url):
        # save url
        self.url = url

        # check if response is live
        response = os.system("ping -c 1 " + self.url)
        
        # url is valid
        if response == 0:
            # start driver
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            # options.headless = True

            self.browser = webdriver.Chrome(options=options)
            self.valid = True
        else:
            self.valid = False
            print("Graphtec URL not valid")
        # is browser open?
        self.open = False
        # was browser navigation succcessful?
        self.nav = False
    
    # Opens the browser
    def openBrowser(self):
        if not self.valid:
            print("OPEN ERROR: Graphtec URL not valid")
            return

        if not self.open:
            self.browser.get(self.url)
            self.open = True
            print('Browser successfully opened')
        else:
            print('Browser already open')
    
    # Closes the Browser
    def closeBrowser(self):
        if not self.valid:
            print("CLOSE ERROR: Graphtec URL not valid")
            return

        if self.open:
            self.browser.close()
            self.open = False
            print('Browser successfully closed')
        else:
            print('Browser not open')
    
    # navigate to the page with data
    def navigateToData(self):
        if not self.valid:
            print("NAVIGATE ERROR: Graphtec URL not valid")
            return

        if self.open:
            try:
                # go to menu settings
                self.browser.switch_to.frame("menu.cgi")

                # find the Digital Button and click on it
                table = self.browser.find_elements(By.TAG_NAME,"td")
                for row in table:
                    if "Digital" in row.find_element(By.TAG_NAME,"img").get_attribute("alt"):
                        row.find_element(By.TAG_NAME,"img").click()

                # navigate back through to change time interval to 2 sec
                self.browser.switch_to.default_content()
                self.browser.switch_to.frame('rightframe')
                self.browser.switch_to.frame('digital2')
                timeInt_dropDown = Select(self.browser.find_element(By.TAG_NAME,'select'))
                timeInt_dropDown.select_by_value('2000')
                # navigate back through to display page
                self.browser.switch_to.default_content()
                self.browser.switch_to.frame('rightframe')
                self.browser.switch_to.frame('digitalDisplay')
                self.browser.switch_to.frame('iframe0')

                # navigataion successful
                self.nav = True
                print('Browser successfully navigated')
            except Exception as e:
                self.nav = False
                print('Browser Navigation Failed?')
                print('    ',e)
                self.closeBrowser()

    def getVal(self):
        if not self.valid:
            print("GETVAL ERROR: Graphtec URL not valid")
            return

        outputVal = {'CH1':-999,'CH2':-999,'CH3':-999,'CH4':-999,'CH5':-999,'CH6':-999,'CH7':-999,'CH8':-999,'CH9':-999,'CH10':-999,
            'CH11':-999,'CH12':-999,'CH13':-999,'CH14':-999,'CH15':-999,'CH16':-999,'CH17':-999,'CH18':-999,'CH19':-999,'CH20':-999}

        # error checking
        if not self.open:
            print("Browser not open, can't getVal")
            return outputVal
        if not self.nav:
            print("Browser not navigated, can't getVal")
            return outputVal

        try:
            # get page details
            soup = BeautifulSoup(self.browser.page_source,features="lxml")

            # find all the tables
            for channel in soup.table.find_all('table'):
                # get each channel value
                values = channel.find_all('b')

                # Extract values
                ch = values[0].text.replace('\xa0','').replace(' ','')
                val = values[1].text.replace('\xa0','').replace('+','').replace(' ','').replace('-','')

                # Dump data into output variable
                if ch in outputVal and 'BURNOUT' not in val and 'Off' not in val:
                    outputVal[ch] = val
        except:
            print('Browser getVal Failed?')
        
        return outputVal