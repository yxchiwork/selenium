import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

with open('config.json', 'r') as f:
    config = json.load(f)
username = config['credentials']['un']
password = config['credentials']['pw']
powerbiurl = config['links']['server']
report1url = config['links']['report1']
report2url = config['links']['report2']
filesdownloaded = 1
# set chrome options
downloadpath = "/Users/yxchi/Downloads/code/download/"
options = webdriver.ChromeOptions() 
prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": downloadpath,
                 "directory_upgrade": True}
options.add_argument('headless')
options.add_experimental_option("prefs",prefs)      
#initiate chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

driver.find_elements_by_class_name("itemRow pbi-focus-outline selected").get




workingfolder = '/home/vsts/work/1/s'
