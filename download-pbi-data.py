import os, time, json, glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from sys import platform

with open('config.json', 'r') as f:
    config = json.load(f)
username = config['credentials']['username']
password = config['credentials']['password']
powerbiurl = config['links']['server']
report1url = config['links']['report1']
report2url = config['links']['report2']
filesdownloaded = 1
# set download folder path according to OS
if platform == "linux" or platform == "linux2":
    downloadpath = config['downloadfolder']['linux'] + '/download/'
elif platform == "darwin":
    downloadpath = config['downloadfolder']['mac'] + '/download/'
elif platform == "win32":
    downloadpath = config['downloadfolder']['win'] + + '\\download\\'
# set chrome options
options = webdriver.ChromeOptions() 
prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": downloadpath,
                 "directory_upgrade": True}
options.add_argument('headless')
options.add_experimental_option("prefs",prefs)      
#initiate chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

def download_wait(directory, timeout, nfiles=None):
    """
    Wait for downloads to finish with a specified timeout.

    Args
    ----
    directory : str
        The path to the folder where the files will be downloaded.
    timeout : int
        How many seconds to wait until timing out.
    nfiles : int, defaults to None
        If provided, also wait for the expected number of files.

    """
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(0.5)
        dl_wait = False
        files = os.listdir(directory)
        if nfiles and len(files) != nfiles:
            print(len(files))
            dl_wait = True
        for fname in files:
            if fname.endswith('.crdownload'):
                dl_wait = True
            seconds += 0.5
    return seconds

# download function
def download(reporturl):
    try:
        driver.get(reporturl)
        actualTitle = driver.title
        section = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/root-downgrade/mat-sidenav-container/mat-sidenav-content/div/div/report/exploration-container/exploration-container-modern/div/div/exploration-host/div/div/exploration/div/explore-canvas-modern/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-modern[3]/transform/div/div[3]/div/div/div/div")))
        hover = ActionChains(driver).move_to_element(section)
        hover.perform()
        # click on the menu
        driver.find_element_by_xpath("/html/body/div[1]/root-downgrade/mat-sidenav-container/mat-sidenav-content/div/div/report/exploration-container/exploration-container-modern/div/div/exploration-host/div/div/exploration/div/explore-canvas-modern/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-modern[3]/transform/div/visual-container-header-modern/div/div[1]/div/visual-container-options-menu/visual-header-item-container/div/button").click()
    except TimeoutException:
        print("failed to click on the ... button")
    # hover to the menu div and click export. 
    try:
        driver.find_element_by_xpath("/html/body/div[6]/drop-down-list/ng-transclude/ng-repeat[2]/drop-down-list-item/ng-transclude/ng-switch/div").click()
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'primary')))
        driver.find_elements_by_class_name("primary")[0].send_keys(Keys.RETURN)
        # wait for file download
        download_wait(downloadpath,10,filesdownloaded)
        print("report data " + actualTitle + " is downloaded")
    except TimeoutException:
        print("error download the file")
# get lastest updated file 

def rename(filename):
    list_of_files = glob.glob(downloadpath+'*') 
    latest_file = max(list_of_files, key=os.path.getctime)
    os.rename(latest_file,downloadpath+filename+'.xlsx')
# login
try:
    driver.get(powerbiurl)
    driver.find_element_by_name("loginfmt").send_keys(username)
    #driver.find_element_by_xpath("//input[@id='i0116']").send_keys(username)
    driver.find_element_by_id("idSIButton9").click()
    time.sleep(0.5)
    driver.find_element_by_name("passwd").send_keys(password)
    driver.find_element_by_id("idSIButton9").click()
    time.sleep(0.5)
    driver.find_element_by_id("idBtn_Back").click()
except TimeoutException:
    print("failed to login")
# hover to the report div to make the menu appear.
filesdownloaded += 1
download(report1url)
rename('data1')
filesdownloaded += 1
download(report2url)
rename('data2')
driver.quit()

print("Job is done, here is the file list in the folder.")
print(os.getcwd())
print(os.listdir(downloadpath))