import os
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import json

with open('config.json', 'r') as f:
    config = json.load(f)

username = config['credentials']['un']
password = config['credentials']['pw']
url = config['server']['url']

options = webdriver.ChromeOptions() 
prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": r"/Users/yxchi/Downloads/code/",
                 "directory_upgrade": True}
options.add_experimental_option("prefs",prefs)      
driver = webdriver.Chrome(executable_path='/Users/yxchi/Downloads/chromedriver',chrome_options=options)

# login
driver.get("https://app.powerbi.com/?route=groups%2fme%2freports%2f34334ab2-7f91-477f-9e81-d62986b88d5a%2fReportSection&noSignUpCheck=1")
driver.find_element_by_xpath("//input[@id='i0116']").send_keys(username)
driver.find_element_by_id("idSIButton9").click()
time.sleep(1)
driver.find_element_by_xpath("//input[@id='i0118']").send_keys(password)
driver.find_element_by_id("idSIButton9").click()
time.sleep(0.5)
driver.find_element_by_id("idBtn_Back").click()
# hover to the report div to make the menu appear.
section = WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[1]/root-downgrade/mat-sidenav-container/mat-sidenav-content/div/div/report/exploration-container/exploration-container-modern/div/div/exploration-host/div/div/exploration/div/explore-canvas-modern/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-modern[3]/transform/div/div[3]/div/div/div/div")))
hover = ActionChains(driver).move_to_element(section)
hover.perform()
# click on the menu
driver.find_element_by_xpath("/html/body/div[1]/root-downgrade/mat-sidenav-container/mat-sidenav-content/div/div/report/exploration-container/exploration-container-modern/div/div/exploration-host/div/div/exploration/div/explore-canvas-modern/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-modern[3]/transform/div/visual-container-header-modern/div/div[1]/div/visual-container-options-menu/visual-header-item-container/div/button").click()
#driver.switch_to_frame("Microsoft_Omnichannel_LCWidget_Chat_Iframe_Window")
# hover to the menu div and click export. 
dropdown = WebDriverWait(driver,30).until(expected_conditions.presence_of_element_located((By.XPATH,"/html/body/div[6]/drop-down-list/ng-transclude/ng-repeat[2]/drop-down-list-item/ng-transclude/ng-switch/div")))

driver.find_element_by_xpath("/html/body/div[6]/drop-down-list/ng-transclude/ng-repeat[2]/drop-down-list-item/ng-transclude/ng-switch/div").click()
time.sleep(2)
driver.find_elements_by_class_name("primary")[0].send_keys(Keys.RETURN)

path = "/Users/yxchi/Downloads/code/"
if os.path.isfile(os.path.join(path, "Var Plan, Var Plan % and Actual by Business Area.xlsx")):
    print("download successfully.")
    driver.quit()
else:
    print("download failed.")
    
