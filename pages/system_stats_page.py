from selenium.webdriver.common.by import By
from utils.download_utils import wait_for_new_file
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


class SystemStatsPage:

    time_range_today = (By.XPATH, "//button[normalize-space()='Today']")
    time_range_2_days = (By.XPATH, "//button[normalize-space()='2 days']")
    time_range_3_days = (By.XPATH, "//button[normalize-space()='3 days']")
    time_range_5_days = (By.XPATH, "//button[normalize-space()='5 days']")
    time_range_7_days = (By.XPATH, "//button[normalize-space()='7 days']")

    download_logs_button = (By.XPATH, "//button[normalize-space()='Download Logs (.txt)']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 180)

    def safe_click(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    def select_time_range(self, locator):
        btn = self.wait.until(EC.element_to_be_clickable(locator))
        self.safe_click(btn)

        # Wait for UI to stabilize
        time.sleep(1)

    def download_logs_for_range(self, download_dir):

        before_files = set(os.listdir(download_dir))

        btn = self.wait.until(EC.element_to_be_clickable(self.download_logs_button))
        self.safe_click(btn)

        # Use reusable utility
        file_path = wait_for_new_file(download_dir, before_files, extension=".txt")

        return file_path
    
