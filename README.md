# Gym Reservation Bot
## Overview
A bot that reserves the earliest available time slot at [Fitness@MIP](https://mcmasterinnovationpark.ca/fitness) and creates an event in Google calendar. 
## Set Up
To implement this, clone this repository and follow the steps below:
1. Download the Firefox webdriver, `geckodriver`, and have it on your `PATH` 
```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/
```
2. Create environment variables
```bash
export EMAIL=<your-email@gmail.com>
export PASSWORD=<your-password>
export DRIVER=</path/to/geckodriver>
```
3. Follow [this guide](https://developers.google.com/calendar/api/quickstart/python?hl=en_GB) to access Google's Calendar API and move `credentials.json` to the root of this repository
4. Install the dependencies
```bash
python3 -m venv venv && source venv/bin/activate
pip3 install -r requirements.txt
```
5. Run the program
```bash
python3 -m bot
```
6. **(Warning)** If met with a `403` when trying to access your calendar, refer to [this thread](https://stackoverflow.com/questions/65756266/error-403-access-denied-the-developer-hasn-t-given-you-access-to-this-app-despi) 