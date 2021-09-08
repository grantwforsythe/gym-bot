# TODO: set up a logger
# TODO: find avilable times
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import sys
import time
from dotenv import load_dotenv

try: 
    load_dotenv()
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
except:
    print("Create a .env file in the root with two key value pairs: EMAIL and PASSWORD.")
    sys.exit(1)

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get("https://my.qreserve.com/login")

    # sign in
    driver.find_element_by_id("email-address").send_keys(EMAIL)
    driver.find_element_by_id("password").send_keys(PASSWORD)
    driver.find_element_by_id("sign-in").click()

    # wait 10 seconds for the element to appear. If it doesn't, throw an error
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Fitness@MIP"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-primary.btn-resource"))
        ).click()
    except:
        print("Enable to sign in.")
        driver.close()
        sys.exit(2)

    print('finished')