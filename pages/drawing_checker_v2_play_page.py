import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class DrawingCheckerV2Page:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 120)

    # def wait_for_page_load(self):
    #     self.wait.until(
    #         lambda d: d.execute_script("return document.readyState") == "complete"
    #     )

    # ---------------- LOCATORS ---------------- #

    dropdown = (By.XPATH, "//select[.//option[normalize-space()='Drawing Checker V2']]")
    option = (By.XPATH, "//option[normalize-space()='Drawing Checker V2']")
    run_btn = (By.XPATH, "//button[contains(text(),'Run Drawing Checker V2')]")
    view_results = (By.XPATH, "//button[normalize-space()='View Results']")

    search_field = (By.XPATH, "//input[@id='issue-search']")
    severity_dropdown = (By.XPATH, "//select[@id='severity-filter']")
    source_dropdown = (By.XPATH, "//select[@id='source-filter']")

    # FIXED (dynamic locator instead of absolute XPath)
    drilldown_btn = (By.XPATH, "//button[contains(@class,'drill') or contains(.,'Drill')]")

    # correct download locator
    download_btn = (By.XPATH, "//a[normalize-space()='Download PDF Report']")

    # ---------------- ACTIONS ---------------- #

    # def select_drawing_checker(self):

    #     dropdown = self.wait.until(
    #         EC.presence_of_element_located(self.dropdown)
    #     )

    #     select = Select(dropdown)
    #     select.select_by_visible_text("Drawing Checker - V2")

    def select_drawing_checker(self):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.dropdown))
        Select(dropdown).select_by_visible_text("Drawing Checker V2")


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
        self.wait.until(EC.visibility_of_element_located(self.search_field)).clear()

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
        print("Drilldown buttons:", len(buttons))

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

                

                # wait for UI update
                time.sleep(3)


                return

        raise Exception("Drilldown button not found")

    # ---------------- DOWNLOAD ---------------- #

    # def download_report(self, download_dir):

    #     if not os.path.exists(download_dir):
    #         raise Exception(f"Download directory not found: {download_dir}")

    #     print("Waiting for download button...")

    #     time.sleep(3)

    #     button = self.wait.until(
    #         EC.element_to_be_clickable(self.download_btn)
    #     )

    #     self.driver.execute_script(
    #         "arguments[0].scrollIntoView({block:'center'});", button
    #     )

    #     time.sleep(1)

    #     try:
    #         button.click()
    #     except:
    #         self.driver.execute_script("arguments[0].click();", button)

    
    def download_report(self, download_dir):

        if not os.path.exists(download_dir):
            raise Exception(f"Download directory not found: {download_dir}")

        

        before_files = set(os.listdir(download_dir))

        button = self.wait.until(
            EC.presence_of_element_located(self.download_btn)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", button
        )

        time.sleep(1)

        try:
            button.click()
        except:
            print("Normal click failed → using JS click")
            self.driver.execute_script("arguments[0].click();", button)

        

        def file_downloaded(driver):
            after_files = set(os.listdir(download_dir))
            new_files = after_files - before_files

            for f in new_files:
                if f.endswith(".pdf") and not f.endswith(".crdownload"):
                    return True
            return False

        WebDriverWait(self.driver, 120).until(file_downloaded)

        final_files = set(os.listdir(download_dir))
        downloaded_files = final_files - before_files

        print(" Downloaded files:", downloaded_files)

        assert any(f.endswith(".pdf") for f in downloaded_files), \
            "Drawing Checker V2 file NOT downloaded"
