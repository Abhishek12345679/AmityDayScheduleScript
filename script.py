import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from webdriver_manager.utils import ChromeType


def sendMail(image, browser):

    # replace os.environ.get with your Amity Email Address
    # replace os.environ.get with your Amity Email Password
    EMAIL = os.environ.get('EMAIL')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

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


def scrapeSite():

    # replace os.environ.get with your enrollment number
    ENROLLMENT_NO = os.getenv('ENROLLMENT_NO')
    # replace os.environ.get with your enrollment password
    AMITY_PASSWORD = os.getenv('AMITY_PASSWORD')

    print('~~Amity Scheduler~~')
    print('\n')
    print('started!!')

    site = "https://student.amizone.net"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=2560,1600")

    browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(),
                               options=chrome_options)
    browser.get(site)

    time.sleep(5)

    print('Opened Amizone ...')
    print(f'Entering Login Credentials!')

    print(f'ENROLLMENT_NO: {ENROLLMENT_NO}')
    print(f'Password: {AMITY_PASSWORD}')

    browser.find_element_by_name(
        '_UserName').send_keys(ENROLLMENT_NO)

    browser.find_element_by_name('_Password').send_keys(AMITY_PASSWORD)

    submit_btn = browser.find_element_by_class_name("login100-form-btn")
    submit_btn.send_keys(Keys.ENTER)

    time.sleep(20)

    # close modals
    close_btn = browser.find_element_by_css_selector(
        '#MyPopup15 > div > div > div.modal-header > button')
    close_btn.send_keys(Keys.ENTER)

    currentdatetime = str(datetime.now())
    print(currentdatetime)
    image_name = currentdatetime[0:currentdatetime.rindex(
        ':', 0, len(currentdatetime))]
    print(image_name)

    time.sleep(20)

    image = browser.find_element_by_css_selector(
        '#Div_Partial > div.main-content > div > div.page-content > div > div > div > div:nth-child(7) > div:nth-child(1)').screenshot_as_png
    sendMail(image, browser)


scrapeSite()
