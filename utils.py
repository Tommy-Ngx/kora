#
# selenium 
# Kora 
# Update 30 Nov 2023
# Tommy bugs
# Miscellaneous utilities.
#
import os, pytz, time, shutil, requests, glob, re,sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from kora.selenium import wd as wd2


def download_file_from_google_drive(file_id, destination):
    url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(url, stream=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def findkeyinfo(countryname):
  countryname = re.findall(r'>(.*?)\<', str(countryname))
  countryname = re.sub('[^A-Za-z0-9.-]+','', str(countryname))
  return countryname


def click_option_by_value(wd, option_id, value):
    option_xpath = f'//*[@id="{option_id}"]/option[{value}]'
    wd.find_element(By.XPATH, option_xpath).click()

def set_input_value(wd, input_id, value):
    wd.find_element(By.ID, input_id).clear()
    wd.find_element(By.ID, input_id).send_keys(value)

def Frax(wd, id, gender, age, weight, height, prefra, nfall, parent, smoke, rheu, drink, corti, bmd, folder):
    os.makedirs(folder, exist_ok=True)
    wd.refresh()
    wd.get("https://www.sheffield.ac.uk/FRAX/tool.aspx?country=57")

    # Fill data
    set_input_value(wd, 'ctl00_ContentPlaceHolder1_nameid', id)
    set_input_value(wd, 'ctl00_ContentPlaceHolder1_toolage', age)

    if gender > 0:
        click_option_by_value(wd, 'ctl00_ContentPlaceHolder1_sex', 1)
    else:
        click_option_by_value(wd, 'ctl00_ContentPlaceHolder1_sex', 2)

    set_input_value(wd, 'ctl00_ContentPlaceHolder1_toolweight', weight)
    set_input_value(wd, 'ctl00_ContentPlaceHolder1_ht', height)
    click_option_by_value(wd, 'dxa', 3)
    set_input_value(wd, 'ctl00_ContentPlaceHolder1_bmd_input', bmd)

    options = [
        ('previousfracture', prefra),
        ('pfracturehip', parent),
        ('currentsmoker', smoke),
        ('glucocorticoids', corti),
        ('arthritis', rheu),
        ('alcohol', drink),
    ]

    for option_id, value in options:
        if value > 0:
            click_option_by_value(wd, f'ctl00_ContentPlaceHolder1_{option_id}2', 1)
        else:
            click_option_by_value(wd, f'ctl00_ContentPlaceHolder1_{option_id}1', 1)

    countryname = findkeyinfo(str(wd.find_element(By.ID, "CountryText")))
    countryname = countryname[7:]

    sexF = wd.find_element(By.ID, f'ctl00_ContentPlaceHolder1_sex{1 if gender > 0 else 2}').get_attribute("value")
    sexF = sexF[0].capitalize()

    ageF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_toolage').get_attribute("value")
    weighF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_toolweight').get_attribute("value")
    heighF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ht').get_attribute("value")
    bmdF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_bmd_input').get_attribute("value")
    dxaF = wd.find_element(By.XPATH, '//*[@id="dxa"]').get_attribute("value")

    time.sleep(2)

    wd.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_btnCalculate"]').click()
    time.sleep(0.31)

    wd.execute_script("window.scrollTo(0, window.scrollY + 180)")
    wd.save_screenshot('ss1.png')
    wd.save_screenshot('{}/{}.png'.format(folder, ((str(int(id))).zfill(5))))
    Tscore = findkeyinfo(wd.find_element(By.ID, 'score'))
    Majorosteo = findkeyinfo(wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lbrs1'))
    HipFracture = findkeyinfo(wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lbrs2'))

    tqdm.write("{}|Age:{}|Tscore:{}|MR:{}|HR:{}".format(sexF, ageF, Tscore, Majorosteo, HipFracture))

    outputallthing = [int(id), sexF, ageF, weighF, heighF, prefra, nfall, parent, smoke, rheu, drink, corti, bmdF, dxaF, Tscore, Majorosteo, HipFracture]
    return outputallthing


