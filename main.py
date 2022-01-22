import sys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
import re
import string
from webdriver_manager.chrome import ChromeDriver, ChromeDriverManager
import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image

pytesseract.pytesseract.tesseract_cmd = r'./lib/Tesseract-OCR/tesseract.exe'

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("https://dpskolkata.net/")

ADMISSION_ID = "2008/2008"
STUDENT_PASSWORD = ""

if len(ADMISSION_ID) <= 0:
    print("No addmission id was detected!")
    sys.stdout.flush()
    sys.exit(1)


def Login(state):
    wait = WebDriverWait(driver, 20);
    wait.until(ec.presence_of_element_located(
        (By.ID, "ContentPlaceHolder1_txtusername")))
    if state is True:
        driver.find_element_by_id(
            'ContentPlaceHolder1_txtusername').send_keys(f'{ADMISSION_ID}')

    driver.find_element_by_id(
        'ContentPlaceHolder1_txtpwd').send_keys(f'{STUDENT_PASSWORD}')
    
    OCRCrackCaptcha()

def OCRCrackCaptcha():
    with open('cap.png', 'wb') as file:
        file.write(driver.find_element_by_id(
            "ContentPlaceHolder1_imgCaptcha").screenshot_as_png)
    img = Image.open('cap.png')
    text = pytesseract.image_to_string(img)
    text = text.replace(" ", "")
    text = re.sub(r'\W+', '', text)
    driver.find_element_by_id(
        'ContentPlaceHolder1_txtCaptcha').send_keys(text)
    sleep(0.5)
    driver.find_element_by_id('ContentPlaceHolder1_btnLogin').click()
    wait = WebDriverWait(driver, 20);
    wait.until(ec.presence_of_element_located((By.ID, "ContentPlaceHolder1_ContentPlaceHolder2_Button2")))
    if driver.current_url is not "https://dpskolkata.net/home/home.aspx":
        Login(False)    

    return True

Login(True)
