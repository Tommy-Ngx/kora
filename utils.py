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
from tqdm import tqdm

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


def Frax(wd, id, gender, age, weight, height, prefra, nfall, parent, smoke, rheu, seosteo, drink, corti, bmd, folder, task):
    os.makedirs(folder, exist_ok=True)
    wd.refresh()
    wd.get("https://www.sheffield.ac.uk/FRAX/tool.aspx?country=57")
    # Fill data
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_nameid').clear()
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_nameid').send_keys(id)
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_toolage').clear()
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_toolage').send_keys(age)

    if gender > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_sex1').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_sex2').click()

    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_toolweight').clear()
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_toolweight').send_keys(weight)
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ht').clear()
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ht').send_keys(height)

    if prefra > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_previousfracture2').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_previousfracture1').click()

    if parent > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_pfracturehip2').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_pfracturehip1').click()

    if smoke > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_currentsmoker2').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_currentsmoker1').click()

    if corti > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_glucocorticoids2').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_glucocorticoids1').click()

    if seosteo > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_osteoporosis2').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_osteoporosis1').click()

    if rheu > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_arthritis2').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_arthritis1').click()

    if drink > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_alcohol2').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_alcohol1').click()

    countryname = str(wd.find_element(By.ID, "CountryText"))
    countryname = findkeyinfo(countryname)

    if gender > 0:
        sexF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_sex1').get_attribute("value")
    else:
        sexF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_sex2').get_attribute("value")

    sexF = sexF[0].capitalize()
    ageF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_toolage').get_attribute("value")
    weighF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_toolweight').get_attribute("value")
    heighF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ht').get_attribute("value")

    if task == "BMD":
        wd.find_element(By.XPATH, '//*[@id="dxa"]/option[3]').click()
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_bmd_input').clear()
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_bmd_input').send_keys(bmd)
        bmdF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_bmd_input').get_attribute("value")
        dxaF = wd.find_element(By.XPATH, '//*[@id="dxa"]').get_attribute("value")
    else:
        wd.find_element(By.XPATH, '//*[@id="dxa"]/option[5]').click()
        
        #browser.find_element_by_id("add_button").click()
        try:
            WebDriverWait(browser, 3).until(EC.alert_is_present(),'Timed out waiting for PA creation')
            alert = browser.switch_to.alert
            alert.accept()
        except TimeoutException:
            pass

        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_bmd_input').clear()
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_bmd_input').send_keys(bmd)
        bmdF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_bmd_input').get_attribute("value")
        #dxaF = wd.find_element(By.XPATH, '//*[@id="dxa"]').get_attribute("value")
        dxaF  = "T-Score"

    time.sleep(2)

    wd.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_btnCalculate"]').click()
    time.sleep(.31)

    wd.execute_script("window.scrollTo(0, window.scrollY + 180)")
    wd.save_screenshot('ss1.png')
    wd.save_screenshot('{}/{}.png'.format(folder, ((str(int(id))).zfill(5))))

    if task == "BMD":
        Tscore = wd.find_element(By.ID, 'score')
        Tscore = findkeyinfo(Tscore)
        Tscore = Tscore[7:]
        Majorosteo = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lbrs1')
        Majorosteo = findkeyinfo(Majorosteo)
        HipFracture = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lbrs2')
        HipFracture = findkeyinfo(HipFracture)

        outputallthing = [int(id), sexF, ageF, weighF, heighF, prefra, nfall, parent, smoke, rheu, seosteo, drink, corti, bmdF, dxaF,
                      Tscore, Majorosteo, HipFracture]
    elif task == "Tscore":
        Majorosteo = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lbrs1')
        Majorosteo = findkeyinfo(Majorosteo)
        HipFracture = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lbrs2')
        HipFracture = findkeyinfo(HipFracture)

        outputallthing = [int(id), sexF, ageF, weighF, heighF, prefra, nfall, parent, smoke, rheu, seosteo, drink, corti, bmdF, dxaF, Majorosteo, HipFracture]
    else:
        outputallthing = []

    return outputallthing



def Frax_ori(wd, id, gender, age, weight, height, prefra, nfall, parent, smoke, rheu, seosteo, drink, corti, bmd, folder):
    os.makedirs(folder, exist_ok=True)
    wd.refresh()
    wd.get("https://www.sheffield.ac.uk/FRAX/tool.aspx?country=57")
    # Fill data
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_nameid').clear()
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_nameid').send_keys(id)
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_toolage').clear()
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_toolage').send_keys(age)

    if gender > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_sex1').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_sex2').click()

    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_toolweight').clear()
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_toolweight').send_keys(weight)
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ht').clear()
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ht').send_keys(height)
    wd.find_element(By.XPATH, '//*[@id="dxa"]/option[3]').click()
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_bmd_input').clear()
    wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_bmd_input').send_keys(bmd)

    if prefra > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_previousfracture2').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_previousfracture1').click()

    if parent > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_pfracturehip2').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_pfracturehip1').click()

    if smoke > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_currentsmoker2').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_currentsmoker1').click()

    if corti > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_glucocorticoids2').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_glucocorticoids1').click()

    if seosteo > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_osteoporosis2').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_osteoporosis1').click()

    if rheu > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_arthritis2').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_arthritis1').click()

    if drink > 0:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_alcohol2').click()
    else:
        wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_alcohol1').click()

    countryname = str(wd.find_element(By.ID, "CountryText"))
    countryname = findkeyinfo(countryname)

    if gender > 0:
        sexF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_sex1').get_attribute("value")
    else:
        sexF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_sex2').get_attribute("value")

    sexF = sexF[0].capitalize()
    ageF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_toolage').get_attribute("value")
    weighF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_toolweight').get_attribute("value")
    heighF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ht').get_attribute("value")
    bmdF = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_bmd_input').get_attribute("value")
    dxaF = wd.find_element(By.XPATH, '//*[@id="dxa"]').get_attribute("value")
    time.sleep(2)

    wd.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_btnCalculate"]').click()
    time.sleep(.31)

    wd.execute_script("window.scrollTo(0, window.scrollY + 180)")
    wd.save_screenshot('ss1.png')
    wd.save_screenshot('{}/{}.png'.format(folder, ((str(int(id))).zfill(5))))
    Tscore = wd.find_element(By.ID, 'score')
    Tscore = findkeyinfo(Tscore)
    Tscore = Tscore[7:]
    Majorosteo = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lbrs1')
    Majorosteo = findkeyinfo(Majorosteo)
    HipFracture = wd.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lbrs2')
    HipFracture = findkeyinfo(HipFracture)

    #tqdm.write("{}|Age:{}|Tscore:{}|MR:{}|HR:{}".format(countryname, ((str(int(id))).zfill(5)), sexF, ageF, Tscore,
    #                                                      Majorosteo, HipFracture))

    outputallthing = [int(id), sexF, ageF, weighF, heighF, prefra, nfall, parent, smoke, rheu, seosteo, drink, corti, bmdF, dxaF,
                      Tscore, Majorosteo, HipFracture]
    return outputallthing


def click_option_by_value(wd, select_id, value):
    # Wait for the element to be present
    select = WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.ID, select_id))
    )

    # Scroll into view if needed
    wd.execute_script("arguments[0].scrollIntoView();", select)

    # Find the option using XPath
    option_xpath = f'//*[@id="{select_id}"]/option[@value="{value}"]'
    option = WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.XPATH, option_xpath))
    )

    # Click the option
    option.click()

def set_input_value(wd, input_id, value):
    wd.find_element(By.ID, input_id).clear()
    wd.find_element(By.ID, input_id).send_keys(value)

def Frax2(wd, id, gender, age, weight, height, prefra, nfall, parent, smoke, rheu, drink, corti, bmd, folder):
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


