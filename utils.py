#
# selenium 
# Kora 
# Update 30 Nov 2023
#
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

def Frax(wd,id, age, weight, height,  prefra, nfall, parent, smoke, rheu,  drink, corti, bmd, folder):
  os.makedirs(folder, exist_ok=True)
  wd.refresh()
  wd.get("https://www.sheffield.ac.uk/FRAX/tool.aspx?country=57")
  # Fill data
  wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_nameid').clear()
  wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_nameid').send_keys(id)
  wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_toolage').clear()
  wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_toolage').send_keys(age)
  wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_sex2').click()
  wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_toolweight').clear()
  wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_toolweight').send_keys(weight)
  wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_ht').clear()
  wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_ht').send_keys(height)
  wd.find_element(By.XPATH,'//*[@id="dxa"]/option[3]').click()
  wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_bmd_input').clear
  wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_bmd_input').send_keys(bmd)
  if (prefra>0): wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_previousfracture2').click()
  else:          wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_previousfracture1').click()

  if (parent>0): wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_pfracturehip2').click()
  else:          wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_pfracturehip1').click()

  if (smoke>1): wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_currentsmoker2').click()
  else:          wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_currentsmoker1').click()

  if (corti>0): wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_glucocorticoids2').click()
  else:          wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_glucocorticoids1').click()
  if (rheu>0): wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_arthritis2').click()
  else:          wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_arthritis1').click()
  if (drink>=3): wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_alcohol2').click()
  else:          wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_alcohol1').click()

  countryname = str(wd.find_element(By.ID,"CountryText"))
  countryname = findkeyinfo(countryname)
  sexF = wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_sex2').get_attribute("value")
  ageF = wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_toolage').get_attribute("value")
  weighF = wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_toolweight').get_attribute("value")
  heighF = wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_ht').get_attribute("value")
  bmdF = wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_bmd_input').get_attribute("value")
  dxaF = wd.find_element(By.XPATH,'//*[@id="dxa"]').get_attribute("value")
  time.sleep(2)

  wd.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_btnCalculate"]').click()
  time.sleep(.31)

  wd.execute_script("window.scrollTo(0, window.scrollY + 180)")
  wd.save_screenshot('ss1.png')
  wd.save_screenshot('{}/{}.png'.format(folder,((str(int(id))).zfill(5))))
  Tscore =  wd.find_element(By.ID,'score')
  Tscore = findkeyinfo(Tscore)
  Tscore = Tscore[7:]
  Majorosteo  = wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_lbrs1')
  Majorosteo = findkeyinfo(Majorosteo)
  HipFracture = wd.find_element(By.ID,'ctl00_ContentPlaceHolder1_lbrs2')
  HipFracture = findkeyinfo(HipFracture)

  print(countryname,((str(int(id))).zfill(5)),"{}|Age:{}|Tscore:{}|MR:{}|HR:{}".format(sexF,ageF,Tscore,Majorosteo, HipFracture ) )
  outputallthing= [int(id), sexF,ageF,weighF, heighF,prefra, nfall ,parent,smoke,rheu,drink,corti,bmdF,dxaF,Tscore,Majorosteo, HipFracture]
  return outputallthing


