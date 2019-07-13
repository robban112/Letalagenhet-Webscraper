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


chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(executable_path=os.path.abspath("driver/chromedriver"), options=chrome_options)

def scrapePages(url, pathToNextButton):
    driver.get(url)
    htmls = []
    while True:
        try:
            htmls.append(driver.page_source)
            button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, pathToNextButton))) 
            button.click()
            print("Navigating to Next Page")
        except (TimeoutException, WebDriverException) as e:
            print(e)
            print("Last page reached")
            driver.quit()
            return htmls
            break


#scrapePages('https://hyresratt.ikanobostad.se/ledigt/sok/lagenhet', "//a[@class='btn next']")