import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from webdriver_manager.utils import ChromeType
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# login Function
def login():
    print('~~Amity Scheduler~~')
    print('\n')
    print('started!!')

    site = "https://s.amizone.net/"
    browser.get(site)

    browser.implicitly_wait(5)

    print('Opened Amizone ...')
    print(f'Entering Login Credentials!')

    print(f'ENROLLMENT_NO: {ENROLLMENT_NO}')
    print(f'Password: {AMITY_PASSWORD}')

    browser.find_element_by_name(
        '_UserName').send_keys(ENROLLMENT_NO)

    browser.find_element_by_name('_Password').send_keys(AMITY_PASSWORD)

    submit_btn = browser.find_element_by_class_name("login100-form-btn")
    submit_btn.send_keys(Keys.ENTER)

    
def sendMail(image):
    print(f'Email: {EMAIL}')
    print(f'Password: {EMAIL_PASSWORD}')
    print(f"Sending Email to {EMAIL}")

    currentdatetime = str(datetime.now())
    image_name = currentdatetime[0:currentdatetime.rindex(
        ':', 0, len(currentdatetime))]

    msg = MIMEMultipart()
    msg['Subject'] = f'Today\'s {image_name} Schedule'
    msg['From'] = EMAIL
    msg['To'] = EMAIL

    text = MIMEText(image_name)
    msg.attach(text)
    image = MIMEImage(image, name=f'{image_name}.png')
    msg.attach(image)

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
    browser.close()


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
    
    # print(f'{schedule_list}')


if __name__ == "__main__":
    
    # replace os.environ.get with your enrollment number
    ENROLLMENT_NO = os.getenv('ENROLLMENT_NO')
    # replace os.environ.get with your enrollment password
    AMITY_PASSWORD = os.getenv('AMITY_PASSWORD')
    
    # replace os.environ.get with your Amity Email Address
    EMAIL = os.environ.get('EMAIL')
    # replace os.environ.get with your Amity Email Password
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=2560,1600")

    browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(),
                               options=chrome_options)
    login()
    schedule = getDaySchedule()
    # sendMail(schedule)
    