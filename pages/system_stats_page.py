# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import os


# class SystemStatsPage:

#     time_range_today = (By.XPATH, "//button[normalize-space()='Today']")
#     time_range_2_days = (By.XPATH, "//button[normalize-space()='2 days']")
#     time_range_3_days = (By.XPATH, "//button[normalize-space()='3 days']")
#     time_range_5_days = (By.XPATH, "//button[normalize-space()='5 days']")
#     time_range_7_days = (By.XPATH, "//button[normalize-space()='7 days']")

#     download_logs_button = (By.XPATH, "//button[normalize-space()='Download Logs (.txt)']")

#     def __init__(self, driver):
#         self.driver = driver
#         self.wait = WebDriverWait(driver, 180)

#     def safe_click(self, element):
#         self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
#         self.driver.execute_script("arguments[0].click();", element)

#     def select_time_range(self, locator):
#         btn = self.wait.until(EC.element_to_be_clickable(locator))
#         self.safe_click(btn)

    # def download_logs_for_range(self, download_dir):
    #     before = set(os.listdir(download_dir))

    #     btn = self.wait.until(EC.element_to_be_clickable(self.download_logs_button))
    #     self.safe_click(btn)

    #     # wait for new completed file
    #     self.wait.until(
    #         lambda d: len([
    #             f for f in (set(os.listdir(download_dir)) - before)
    #             if not f.endswith(".crdownload")
    #         ]) >= 1
    #     )

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

    # def download_logs_for_range(self, download_dir):

    #     before = set(os.listdir(download_dir))

    #     btn = self.wait.until(EC.element_to_be_clickable(self.download_logs_button))
    #     self.safe_click(btn)

    #     end_time = time.time() + 60

    #     while time.time() < end_time:

    #         current_files = set(os.listdir(download_dir))

    #         new_files = [
    #             f for f in (current_files - before)
    #             if not f.endswith(".crdownload")
    #         ]

    #         if new_files:
    #             file_path = os.path.join(download_dir, new_files[0])

    #             # Ensure file fully downloaded (size stable)
    #             size1 = os.path.getsize(file_path)
    #             time.sleep(1)
    #             size2 = os.path.getsize(file_path)

    #             if size1 == size2:
    #                 print("Downloaded:", new_files[0])
    #                 return

    #         time.sleep(1)

    #     raise Exception("Download failed or timed out")

    def download_logs_for_range(self, download_dir):

        before_files = set(os.listdir(download_dir))

        btn = self.wait.until(EC.element_to_be_clickable(self.download_logs_button))
        self.safe_click(btn)

        # Use reusable utility
        file_path = wait_for_new_file(download_dir, before_files, extension=".txt")

        return file_path
    
