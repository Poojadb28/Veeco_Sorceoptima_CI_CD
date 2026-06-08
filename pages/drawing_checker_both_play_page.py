import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DrawingCheckerPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 120)


    # LOCATORS
    dropdown = (By.XPATH, "//select[.//option[normalize-space()='Drawing Checker - Both']]")
    option = (By.XPATH, "//option[normalize-space()='Drawing Checker - Both']")
    run_btn = (By.XPATH, "//button[contains(text(),'Run Drawing Checker - Both')]")
    view_results = (By.XPATH, "//button[normalize-space()='View Results']")
    search_field = (By.XPATH, "//input[@id='issue-search']")
    dropdown_menu = (By.XPATH, "//select[@id='severity-filter']")
    dropdown_options = (By.XPATH, "//select[@id='source-filter']")
    drilldown_btn = (By.XPATH, "//button[contains(@class,'drill') or contains(.,'Drill')]")
    view_details = (By.XPATH, "//button[normalize-space()='View Details']")

    popup_overlay = (By.XPATH, "//div[contains(@class,'fixed inset-0')]")
    report_tab = (By.XPATH, ".//button[normalize-space()='Drawing Checker - Both']")

    download_btn = (By.XPATH, "//a[normalize-space()='Download PDF Report']")

    close_icon = (By.XPATH, "//button[contains(@class,'p-2')]")

    # ---------------- ACTIONS ----------------

    def select_drawing_checker(self):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.dropdown))
        Select(dropdown).select_by_visible_text("Drawing Checker - Both")

    def click_run(self):
        self.wait.until(EC.element_to_be_clickable(self.run_btn)).click()

    def wait_for_processing(self):
        self.wait.until(EC.element_to_be_clickable(self.view_results))

    def click_view_results(self):
        self.wait.until(EC.element_to_be_clickable(self.view_results)).click()

    def search_issue(self, issue_type):

        # wait until search field is visible in NEW TAB
        search_input = self.wait.until(
            EC.visibility_of_element_located(self.search_field)
        )

        # scroll inside page
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", search_input
        )

        # optional: small wait
        self.wait.until(EC.element_to_be_clickable(self.search_field))

        search_input.click()
        search_input.clear()
        search_input.send_keys(issue_type)

    def clear_search(self):
        search_input = self.wait.until(EC.visibility_of_element_located(self.search_field))
        search_input.clear()

    def filter_by_severity(self, severity):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.dropdown_menu))
        Select(dropdown).select_by_visible_text(severity)

    def filter_by_source(self, source):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.dropdown_options))
        Select(dropdown).select_by_visible_text(source)

    def click_drilldown(self):
        element = self.wait.until(EC.element_to_be_clickable(self.drilldown_btn))
        self.driver.execute_script("arguments[0].click();", element)

    def download_report(self, download_dir):

        # Ensure directory exists 
        if not os.path.exists(download_dir):
            raise Exception(f"Download directory not found: {download_dir}")

        # Remove old files
        before_files = set(os.listdir(download_dir))

        # Click ACTUAL BUTTON
        button = self.wait.until(EC.presence_of_element_located(self.download_btn))

        # scroll (important for hidden buttons)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )

        try:
            button.click()
        except:
            print("Normal click failed → using JS click")
            self.driver.execute_script("arguments[0].click();", button)

        # Wait for NEW file (not old ones)
        def new_file_downloaded(driver):
            after_files = set(os.listdir(download_dir))
            new_files = after_files - before_files

            for f in new_files:
                # ignore temp download files
                if f.endswith(".pdf") and not f.endswith(".crdownload"):
                    return True
            return False

        WebDriverWait(self.driver, 120).until(new_file_downloaded)

        # Get new files
        final_files = set(os.listdir(download_dir))
        downloaded_files = final_files - before_files

        print("Downloaded files:", downloaded_files)

        assert any(
            f.endswith(".pdf") for f in downloaded_files
        ), " Drawing Checker file not downloaded"

    def close_popup(self):

        element = self.wait.until(EC.element_to_be_clickable(self.close_icon))
        self.driver.execute_script("arguments[0].click();", element)

        self.wait.until(EC.element_to_be_clickable(self.dropdown))
