from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time, os

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
        time.sleep(1)
        dl_wait = False
        files = os.listdir(directory)
        if nfiles and len(files) != nfiles:
            dl_wait = True
        for fname in files:
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
    return seconds
downloadpath = r"/Users/yxchi/Downloads/code/download/"
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": downloadpath,
                 "directory_upgrade": True}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.get('http://the-internet.herokuapp.com/download')
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/a[1]')))
    driver.find_element(By.XPATH, '//*[@id="content"]/div/a[1]').click()
    download_wait(downloadpath,20,3)
    # print("program flow comes here")
except TimeoutException:
    print("Failed to load page")
finally:
    if os.path.isfile(os.path.join(downloadpath, "not_empty.txt")):
        print("download successfully.")
        driver.quit()