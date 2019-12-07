#Importing packages
from selenium import webdriver
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import os 
from time import sleep


chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


def scrapePages(url, pathToNextButton):
    driver = webdriver.Chrome(executable_path=os.path.abspath("driver/chromedriver"), options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(url)
    htmls = []
    while True:
        try:
            htmls.append(driver.page_source)
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, pathToNextButton))
            ) 
            button.click()
            print("Navigating to Next Page")
        except (TimeoutException, WebDriverException) as e:
            print(e)
            print("Last page reached")
            driver.close()
            driver.quit()
            return htmls
            break

def getHTML(url):
    driver = webdriver.Chrome(executable_path=os.path.abspath("driver/chromedriver"), options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(url)
    return driver.page_source


#scrapePages('https://hyresratt.ikanobostad.se/ledigt/sok/lagenhet', "//a[@class='btn next']")