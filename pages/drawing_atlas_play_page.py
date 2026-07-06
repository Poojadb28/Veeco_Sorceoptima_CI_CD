import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class DrawingAtlasPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 280)


    # LOCATORS
    dropdown = (By.XPATH, "//select[contains(@class,'text-sm')]")
    option = (By.XPATH, "//option[normalize-space()='Drawing Atlas']")
    run_btn = (By.XPATH, "//button[contains(text(),'Run Drawing Atlas')]")
    view_results = (By.XPATH, "//button[normalize-space()='View Results']")
    view_details = (By.XPATH, "//button[normalize-space()='View Details']")
    popup_overlay = (By.XPATH, "//div[contains(@class,'fixed inset-0')]")
    download_btn = (By.XPATH, "//button[normalize-space()='Export Excel']")
    close_icon = (By.XPATH, "//button[contains(@class,'p-2')]")

    # ACTIONS

    def select_drawing_atlas(self):
        self.wait.until(EC.element_to_be_clickable(self.dropdown)).click()
        self.wait.until(EC.element_to_be_clickable(self.option)).click()

    def click_run(self):
        self.wait.until(EC.element_to_be_clickable(self.run_btn)).click()

    # def wait_for_processing(self):
    #     self.wait.until(EC.element_to_be_clickable(self.view_results))

    def wait_for_processing(self):

        timeout = time.time() + 1800  # 30 minutes

        while time.time() < timeout:

            elements = self.driver.find_elements(
                By.XPATH,
                "//button[contains(.,'View Results')]"
            )

            if elements and elements[0].is_displayed():
                print("Processing completed")
                return

            time.sleep(30)

        raise Exception(
            "Drawing Atlas processing did not complete within 30 minutes"
        )

    def click_view_results(self):
        self.wait.until(EC.element_to_be_clickable(self.view_results)).click()

    def click_view_details(self):
        self.wait.until(EC.element_to_be_clickable(self.view_details)).click()

    def open_report_tab(self):
        popup = self.wait.until(EC.visibility_of_element_located(self.popup_overlay))
        tab = popup.find_element(By.XPATH, ".//button[normalize-space()='Drawing Atlas']")

        self.driver.execute_script("arguments[0].scrollIntoView(true);", tab)

        try:
            tab.click()
        except:
            ActionChains(self.driver).move_to_element(tab).click().perform()

        # fallback
        try:
            self.wait.until(EC.presence_of_element_located(self.download_btn))
        except:
            self.driver.execute_script("arguments[0].click();", tab)

  

    def download_report(self, download_dir):

        before_files = set(os.listdir(download_dir))

        element = self.wait.until(EC.element_to_be_clickable(self.download_btn))
        element.click()

        import time
        timeout = 120
        end_time = time.time() + timeout

        while time.time() < end_time:

            after_files = set(os.listdir(download_dir))
            new_files = after_files - before_files

            completed_files = [f for f in new_files if not f.endswith(".crdownload")]

            if any(f.endswith(".xlsx") for f in completed_files):
                print("New downloaded file:", completed_files)
                return
            
            time.sleep(2)

        raise Exception("Download not detected")
    
    def take_screenshot(self, file_name):
        os.makedirs("screenshots", exist_ok=True)

        file_path = os.path.join("screenshots", file_name)
        self.driver.save_screenshot(file_path)

        return file_path

    def close_popup(self):
        element = self.wait.until(EC.element_to_be_clickable(self.close_icon))
        self.driver.execute_script("arguments[0].click();", element)
        self.wait.until(EC.element_to_be_clickable(self.dropdown))
