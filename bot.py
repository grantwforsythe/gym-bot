# TODO: Log registered time slot into Google Calendar
from selenium import webdriver

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException

import os
import sys
import time
from pathlib import PureWindowsPath
from dotenv import load_dotenv

import logging


logging.basicConfig(
    filename="registration.log", 
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )

# TODO: make this more reproducible
PATH = PureWindowsPath("c:/Program Files (x86)/geckodriver.exe")

try: 
    load_dotenv()
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
except:
    logging.error("Create a .env file in the root of this repo with two key value pairs: EMAIL and PASSWORD.")
    sys.exit(1)

options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(
    executable_path=PATH,
    options=options
    )


def main():
    driver.get("https://my.qreserve.com/login")

    # sign in
    logging.info("Signing in...")
    driver.find_element_by_id("email-address").send_keys(EMAIL)
    driver.find_element_by_id("password").send_keys(PASSWORD)
    driver.find_element_by_id("sign-in").click()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Fitness@MIP"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-primary.btn-resource"))
        ).click()

    except TimeoutException:
        logging.error("Trouble signing in. Double check account info.")
        driver.quit()
        sys.exit(2)

    finally:
        logging.info("...Success.")

    try:
        slots = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.btn.btn-secondary.btn-slot"))
        )

        # finds the earliest available time slot
        for slot in slots:
            if slot.is_enabled():
                slot.click()
                time.sleep(5)
                reserve(driver)
                sys.exit(0)
            else:
                logging.info(f"{slot.text} unavailable.")

    except TimeoutException:
        logging.error("Unable to find available slots.")
        driver.quit()
        sys.exit(3)


def reserve(driver: webdriver.Firefox):
    """ Pass all screening questions and register """

    logging.info("Registering...")

    try:
        Select(driver.find_element_by_id("0e444062-373b-41f8-96d7-3e415856df88")).select_by_visible_text("General Use")
        Select(driver.find_element_by_id("635561e2-4bd3-47fb-996a-0a64a58832b2")).select_by_visible_text("No")
        Select(driver.find_element_by_id("61eec9a7-9409-4023-8707-d4f129e6e8ec")).select_by_visible_text("No")
        Select(driver.find_element_by_id("c9fb4519-dc23-430c-a849-0fd01eb51a33")).select_by_visible_text("No")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "reserve-next"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "book-reserve"))
        ).click()
        
    except TimeoutException:
        logging.error("Unable to register.")
        driver.quit()
        sys.exit(4)


if __name__ == "__main__":
    main()