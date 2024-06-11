# Script Name: setup_chromedriver.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def setup_chromedriver():
    # Chromeオプションの設定
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # GUIを表示せずに動作する
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    # ChromeDriverの自動設定
    driver_path = ChromeDriverManager().install()
    print(f"ChromeDriverは以下のパスにインストールされました: {driver_path}")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

def print_capabilities(driver):
    # driver.capabilities をすべて表示
    capabilities = driver.capabilities
    print("driver.capabilities の内容:")
    for key, value in capabilities.items():
        print(f"{key}: {value}")

def main():
    driver = setup_chromedriver()
    #check_chromedriver(driver)
    print_capabilities(driver)
    driver.quit()

if __name__ == "__main__":
    main()
