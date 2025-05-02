# -*- coding: utf-8 -*-
# selenium_script.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def selenium_task():
    # 設定 Chrome 的選項
    chrome_options = Options()
    chrome_options.add_argument('--headless') # 啟用無頭模式
    chrome_options.add_argument("--proxy-server=http://127.0.0.1:8088")  # 設定代理伺服器為 Burp 的預設值
    chrome_options.add_argument("--ignore-certificate-errors")  # 忽略 SSL 錯誤

    # 啟動 Chrome 瀏覽器
    #driver = webdriver.Chrome(executable_path="/Users/toyhsieh/Documents/chromedriver-mac-arm64/chromedriver", options=chrome_options)

    chromedriver_path = "/Users/toyhsieh/Documents/chromedriver-mac-arm64/chromedriver"  # 更換為實際的 chromedriver 路徑

    # 使用 Service 類別來指定 chromedriver 路徑
    service = Service(chromedriver_path)

    # 初始化 WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 開啟 XREX 登入頁面
    driver.get("https://exchange.xrex.io/en/auth/login")
    #time.sleep(1)  # 等待頁面載入完成

    # 找到手機號碼輸入框並輸入資料
    phone_input = driver.find_element(By.XPATH, '//input[@id="mui-2"]')
    phone_input.send_keys("0987654321")

    # 找到「Next」按鈕並點擊
    next_button = driver.find_element(By.XPATH, '//button[contains(@class, "MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge css-1lcesv")]')
    next_button.click()

    # 等待頁面反應
    time.sleep(1)

    # 關閉瀏覽器
    driver.quit()

if __name__ == "__main__":
    selenium_task()
