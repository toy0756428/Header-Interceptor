# -*- coding: utf-8 -*-
# selenium_script.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def selenium_task():
    # Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless') 
    chrome_options.add_argument("--proxy-server=http://127.0.0.1:8088")  # Burp proxy
    chrome_options.add_argument("--ignore-certificate-errors") 

    chromedriver_path = "/path/to/chromedriver"  # chromedriver path
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://test.com")

    input = driver.find_element(By.TESTPATH, '//input[@id="test"]')
    input.send_keys("test")

    login_button = driver.find_element(By.TESTPATH, '//button[contains(@class, "test")]')
    login_button.click()
    time.sleep(1)  # load

    # close
    driver.quit()

if __name__ == "__main__":
    selenium_task()
