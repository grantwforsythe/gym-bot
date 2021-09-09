from selenium import webdriver

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException

import os
import sys
import time
import argparse

from utils.google import create_service, create_event

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler('registration.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

DRIVER = os.getenv("DRIVER")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

GYM_HOME_URL = 'https://my.qreserve.com/login'
CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'primary'


def run(driver: webdriver, add_event: bool):
    """ 
    :param driver: Instance of a Firefox webdriver
    :param add_event: Add event to Google Calendar
    """
    try:
        login(driver)
    except Exception as e:
        logger.exception('Failed to login: ' + str(e))
        driver.quit()
        sys.exit(1)

    try:
        navigate(driver)
    except Exception as e:
        logger.exception('Failed to navigate: ' + str(e))
        driver.quit()
        sys.exit(2)

    try:
        find_time_slot(driver)
    except TimeoutException:
        logger.error('Unable to find available slots.')
        driver.quit()
        sys.exit(3)
    
    if add_event:
        add_to_calendar(driver)


def login(driver):
    """ Login to webpage """
    try:
        logger.info('Requesting page: ' + GYM_HOME_URL)
        driver.get(GYM_HOME_URL)
    except TimeoutException:
        logger.info('Page load timed out but continuing anyway')
    
    logger.info('Entering username and password')
    email_input = driver.find_element_by_id('email-address')
    email_input.clear()
    email_input.send_keys(EMAIL)

    password_input = driver.find_element_by_id('password')
    password_input.clear()
    password_input.send_keys(PASSWORD)
    
    logger.info('Logging in')
    driver.find_element_by_id('sign-in').click()
    
    logger.info('Successfully logged in')


def navigate(driver):
    """ Navigate the webpage """
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Fitness@MIP'))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn.btn-primary.btn-resource'))
    ).click()


def find_time_slot(driver):
    """ Find the earliest available time slot """
    slots = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button.btn.btn-secondary.btn-slot'))
    )

    for slot in slots:
        if slot.is_enabled():
            logger.info(f'{slot.text} available.')
            slot.click()
            reserve(driver)
        else:
            logger.info(f'{slot.text} unavailable.')


def reserve(driver):
    """ Pass all screening questions and register """
    logger.info('Registering for first available timeslot.')
    time.sleep(10)  # wait for contents to load

    try:
        Select(driver.find_element_by_id('0e444062-373b-41f8-96d7-3e415856df88')).select_by_visible_text('General Use')
        Select(driver.find_element_by_id('635561e2-4bd3-47fb-996a-0a64a58832b2')).select_by_visible_text('No')
        Select(driver.find_element_by_id('61eec9a7-9409-4023-8707-d4f129e6e8ec')).select_by_visible_text('No')
        Select(driver.find_element_by_id('c9fb4519-dc23-430c-a849-0fd01eb51a33')).select_by_visible_text('No')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'reserve-next'))
        ).click()

        confirm = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'book-reserve'))
        )
    except TimeoutException:
        logger.error('Timed out while registering.')
        driver.quit()
        sys.exit(4)

    if confirm.is_enabled():
        confirm.click()
        logger.info('Successfully registered for the gym.')
    else:
       logger.error('Conflict Resolution Required.')
       driver.quit()
       sys.exit(5)


def add_to_calendar(driver):
    """ Create event on Google calendar """
    service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # TODO: convert AM/PM into 24 hours
    start_hour = int(driver.find_elements_by_id('timepicker-date-time-picker-start6b7fc49d-4f95-4dfb-9252-a191debbe40a-day-mode').get_attribute("value"))
    stop_hour = start_hour + 1  # at present, you are only given an hour to workout
    response = service.events().insert(
        calendarId=CALENDAR_ID,
        body=create_event(start_hour, stop_hour)
    ).execute()

    logger.info(f"Event created: {response.get('htmlLink')}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--headless',  default=True)
    parser.add_argument('--add-event', default=False)
    args = parser.parse_args()

    driver = None
    options = None

    if args.headless:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(executable_path=DRIVER, options=options)
    else:
        driver = webdriver.Firefox(executable_path=DRIVER)

    run(driver, args.add_event)