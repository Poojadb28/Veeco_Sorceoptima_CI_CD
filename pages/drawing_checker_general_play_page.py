import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DrawingCheckerGeneralPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 120)

    # ---------------- LOCATORS ---------------- #

    dropdown = (By.XPATH, "//select[.//option[normalize-space()='Drawing Checker - General']]")
    option = (By.XPATH, "//option[normalize-space()='Drawing Checker - General']")
    run_btn = (By.XPATH, "//button[contains(text(),'Run Drawing Checker - General')]")
    view_results = (By.XPATH, "//button[normalize-space()='View Results']")

    search_field = (By.XPATH, "//input[@id='issue-search']")

    severity_dropdown = (By.XPATH, "//select[@id='severity-filter']")
    source_dropdown = (By.XPATH, "//select[@id='source-filter']")

    drilldown_btn = (By.XPATH, "//button[contains(@class,'drill') or contains(.,'Drill')]")

    download_btn = (By.XPATH, "//a[normalize-space()='Download PDF Report']")

    # ---------------- ACTIONS ---------------- #

    def select_drawing_checker_general(self):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.dropdown))
        Select(dropdown).select_by_visible_text("Drawing Checker - General")

    def click_run(self):
        self.wait.until(EC.element_to_be_clickable(self.run_btn)).click()

    def wait_for_processing(self):
        self.wait.until(EC.element_to_be_clickable(self.view_results))

    def click_view_results(self):
        self.wait.until(EC.element_to_be_clickable(self.view_results)).click()

    # ---------------- SEARCH ---------------- #

    def search_issue(self, text):

        field = self.wait.until(EC.visibility_of_element_located(self.search_field))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", field
        )

        field.clear()
        field.send_keys(text)

    def clear_search(self):

        field = self.wait.until(EC.visibility_of_element_located(self.search_field))
        field.clear()

    # ---------------- FILTERS ---------------- #

    def filter_by_severity(self, value):

        dropdown = self.wait.until(EC.element_to_be_clickable(self.severity_dropdown))
        Select(dropdown).select_by_visible_text(value)

    def filter_by_source(self, value):

        dropdown = self.wait.until(EC.element_to_be_clickable(self.source_dropdown))
        Select(dropdown).select_by_visible_text(value)

    # ---------------- DRILLDOWN ---------------- #

    def click_drilldown(self):

        time.sleep(2)

        buttons = self.driver.find_elements(*self.drilldown_btn)
        print("Drilldown buttons found:", len(buttons))

        for btn in buttons:
            if btn.is_displayed():

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", btn
                )

                time.sleep(1)

                try:
                    btn.click()
                except:
                    self.driver.execute_script("arguments[0].click();", btn)

        

                # IMPORTANT wait for UI load
                time.sleep(3)

                return

        raise Exception("Drilldown button not found")

    # ---------------- DOWNLOAD ---------------- #

    def download_report(self, download_dir):

        if not os.path.exists(download_dir):
            raise Exception(f"Download directory not found: {download_dir}")

        before_files = set(os.listdir(download_dir))

        button = self.wait.until(EC.element_to_be_clickable(self.download_btn))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", button
        )

        try:
            button.click()
        except:
            self.driver.execute_script("arguments[0].click();", button)

        
        timeout = 120
        end_time = time.time() + timeout

        while time.time() < end_time:

            after_files = set(os.listdir(download_dir))
            new_files = after_files - before_files

            completed = [f for f in new_files if not f.endswith(".crdownload")]

            if any(f.endswith(".pdf") for f in completed):
                print("Downloaded:", completed)
                return

            time.sleep(2)

        raise Exception("Download not detected")

       
