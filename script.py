from datetime import datetime
import os
from typing import List
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.chrome.options import Options
from webdriver_manager.utils import ChromeType
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# login Function
def login(site):
    print('Amity Schedule Sender \n')
    
    browser.get(site)
    browser.implicitly_wait(5)

    print('Entering Login Credentials!')
    print(f'ENROLLMENT_NO: {ENROLLMENT_NO}')
    print(f'PASSWORD: {AMITY_PASSWORD}')

    browser.find_element_by_name(
        '_UserName').send_keys(ENROLLMENT_NO)

    browser.find_element_by_name('_Password').send_keys(AMITY_PASSWORD)

    #login-btn click
    browser.find_element_by_class_name("login100-form-btn").click()
     
def sendMail(schedule:List):
    
    daysOfTheWeek = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
    ];
    
    currentdatetime = datetime.now().weekday

    msg = MIMEMultipart()
    msg['Subject'] = f'{daysOfTheWeek[currentdatetime]}\'s Schedule'
    msg['From'] = EMAIL
    msg['To'] = EMAIL

    text = MIMEText(str(schedule))
    msg.attach(text)
    
    s = smtplib.SMTP('smtp-mail.outlook.com', 587)

    # start TLS for security
    s.ehlo()
    s.starttls()
    s.ehlo()

    # Authentication
    s.login(EMAIL, EMAIL_PASSWORD)

    # sending the mail
    s.sendmail(EMAIL,
               EMAIL,  msg.as_string())

    # terminating the session
    s.quit()


def list2ListOfObjs(lst:List):
    newList = []
    for i in range(0,len(lst),2):
        newList.append({
            "time":lst[i][0:14],
            "subject":lst[i][15:],
            "faculty":lst[i+1]
        })
    return newList

def getDaySchedule():
    
    # clicking on home li
    WebDriverWait(browser, 20)\
        .until(EC.element_to_be_clickable((By.CLASS_NAME,"nav-list > li:first-child > a")))\
        .click()
        
    # closing the students welfare department modal   
    browser.implicitly_wait(20)
    modal_close_btn = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[2]/div/div/div[1]/button")
    modal_close_btn.click()
    
    schedule_list = browser\
                .find_element_by_xpath("/html/body/div[3]/div/div[2]/div[1]/div/div[2]/div/div/div/div[7]/div[1]/div/div/div/div[2]/div/div[2]/div/div/table")\
                .text\
                .split('\n')
    
    schedule_list.pop(0)
    
    return list2ListOfObjs(schedule_list)


if __name__ == "__main__":
    
    # replace os.environ.get with your enrollment number
    ENROLLMENT_NO = os.getenv('ENROLLMENT_NO')
    # replace os.environ.get with your enrollment password
    AMITY_PASSWORD = os.getenv('AMITY_PASSWORD')
    
    # replace os.environ.get with your Amity Email Address
    EMAIL = os.environ.get('EMAIL')
    # replace os.environ.get with your Amity Email Password
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    
    SITE_URL = "https://s.amizone.net"
    
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=2560,1600")

    browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(),
                               options=chrome_options)
    
    # auth
    login(SITE_URL)
    
    # get schedule as an object
    schedule_list = getDaySchedule()
    
    #send schedule
    sendMail(schedule_list)
    
    