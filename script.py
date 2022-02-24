from datetime import datetime
from email.message import EmailMessage
import os
from typing import List
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from selenium.webdriver.chrome.options import Options
from webdriver_manager.utils import ChromeType
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from apscheduler.schedulers.blocking import BlockingScheduler

# login Function


def login(browser):
    print('Amity Schedule Sender \n')

    browser.get("https://s.amizone.net")
    browser.implicitly_wait(5)

    print('Entering Login Credentials!')

    browser\
        .find_element(by=By.NAME, value='_UserName')\
        .send_keys(os.environ.get('ENROLLMENT_NO'))

    browser\
        .find_element(by=By.NAME, value='_Password')\
        .send_keys(os.environ.get('AMITY_PASSWORD'))

    # login-btn click
    browser.find_element(by=By.CLASS_NAME, value='login100-form-btn').click()


def getHTML(schedule: List):
    start_html = "<div style='background-color:\"red\"'>"
    end_html = "</div>"

    for item in schedule:
        time = item['time']
        subject = item['subject']
        faculty = item['faculty']
        start_html += f'<h2>{time}</h2><br/><h3>{subject}</h3><br/><p>{faculty}</p>'

    return start_html + end_html


def sendMail(schedule: List):

    EMAIL = os.environ.get('EMAIL')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

    daysOfTheWeek = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    currentdatetime = datetime.now().weekday()

    email = EmailMessage()
    email['Subject'] = f'{daysOfTheWeek[currentdatetime]}\'s Schedule'
    email['From'] = EMAIL
    email['To'] = EMAIL

    email.set_content(getHTML(schedule), subtype='html')

    with smtplib.SMTP('smtp-mail.outlook.com', 587) as s:
        s.starttls()
        s.login(EMAIL, EMAIL_PASSWORD)
        s.send_message(email)
        s.quit()


def list2ListOfObjs(lst: List):
    newList = []
    for i in range(0, len(lst), 2):
        newList.append({
            "time": lst[i][0:14],
            "subject": lst[i][15:],
            "faculty": lst[i+1]
        })
    return newList


def popModal(browser):
    # closing modal
    browser.implicitly_wait(20)
    modal_close_btn = browser\
        .find_element(By.XPATH, value="/html/body/div[3]/div/div[2]/div[2]/div/div/div[1]/button")
    modal_close_btn.click()


def getDaySchedule(browser):

    # clicking on home li
    WebDriverWait(browser, 20)\
        .until(EC.element_to_be_clickable((By.CLASS_NAME, "nav-list > li:first-child > a")))\
        .click()

    # popModal()

    schedule_list = browser\
        .find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/div[2]/div/div/div/div[7]/div[1]/div/div/div/div[2]/div/div[2]/div/div/table")\
        .text\
        .split('\n')

    schedule_list.pop(0)

    return list2ListOfObjs(schedule_list)


def main(browser):
    # auth
    login(browser)

    # get schedule as an object
    schedule_list = getDaySchedule(browser)

    # send schedule
    sendMail(schedule_list)

    # browser.implicitly_wait(5)
    # browser.quit()


if __name__ == "__main__":

    options = Options()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=2560,1600")

    # browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(),
    #                            options=options)

    browser = webdriver.Chrome(executable_path=os.environ.get(
        "CHROMEDRIVER_PATH"), options=options)

    sched = BlockingScheduler()

    @sched.scheduled_job('interval', minutes=5)
    def timed_job():
        print('This job is run every five minutes.')
        main(browser)

    # @sched.scheduled_job('cron', day_of_week='mon-fri', hour=7)
    # def scheduled_job():
    #     print('This job is run every weekday at 0730.')
    #     main(browser)

    sched.start()
