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
    
    
def getHTML(schedule:List):
    start_html = "<div style='background-color:\"red\"'>"
    end_html = "</div>"
    
    
    for item in schedule:
        time = item['time']
        subject = item['subject']
        faculty = item['faculty']
        start_html += f'<h2>{time}</h2><br/><h3>{subject}</h3><br/><p>{faculty}</p>'
        
    return start_html + end_html
    
     
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
    
    currentdatetime = datetime.now().weekday()

    email = EmailMessage()
    email['Subject'] = f'{daysOfTheWeek[currentdatetime]}\'s Schedule'
    email['From'] = EMAIL
    email['To'] = EMAIL

    email.set_content(getHTML(schedule),subtype='html')
    
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as s:
        s.starttls()
        s.login(EMAIL, EMAIL_PASSWORD)
        s.send_message(email)
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
    
    browser.implicitly_wait(5)
    browser.quit()
    
    