import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SystemAdminPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 180)

    # ================= LOCATORS ================= #

    # Navigation
    USER_ADMIN = (By.XPATH, "//button[normalize-space()='User Admin View']")
    CREATE_USER = (By.XPATH, "//button[normalize-space()='Create User']")

    # Available Plays
    AVAILABLE_PLAYS_SECTION = (By.XPATH, "//h2[normalize-space()='Available Plays']")
    DISABLE_MSG = (By.XPATH, "//div[contains(text(),'Play disabled successfully')]")
    ENABLE_MSG = (By.XPATH, "//div[contains(text(),'Play enabled successfully')]")

    # ================= GENERIC METHODS ================= #

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text.strip()

    # ================= NAVIGATION ================= #

    def open_user_admin(self):
        self.click(self.USER_ADMIN)
        self.wait.until(EC.visibility_of_element_located(self.CREATE_USER))

    # ================= AVAILABLE PLAYS ================= #

    DISABLE_MSG = (By.XPATH, "//*[contains(text(),'disabled') and not(contains(@style,'display: none'))]")
    ENABLE_MSG = (By.XPATH, "//*[contains(text(),'enabled') and not(contains(@style,'display: none'))]")

    def go_to_available_plays(self):
        section = self.wait.until(
            EC.visibility_of_element_located(self.AVAILABLE_PLAYS_SECTION)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", section)

    def toggle_play(self, play_name):

        toggle = self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//h3[normalize-space()='{play_name}']"
                f"/ancestor::div[contains(@class,'rounded-lg')]"
                f"//button[contains(@class,'inline-flex')]"
            ))
        )

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", toggle)
        self.driver.execute_script("arguments[0].click();", toggle)

        # IMPORTANT: wait for state change
        self.wait.until(lambda d: toggle.is_displayed())

        time.sleep(2)
    

    def get_disable_message(self):
        return self.get_text(self.DISABLE_MSG)
    

    def wait_for_disable_message(self):

        element = self.wait.until(
            EC.visibility_of_element_located(self.DISABLE_MSG)
        )

        # wait until text is actually populated
        self.wait.until(lambda d: element.text.strip() != "")

        return element.text.strip()

    def wait_for_enable_message(self):

        element = self.wait.until(
            EC.visibility_of_element_located(self.ENABLE_MSG)
        )

        self.wait.until(lambda d: element.text.strip() != "")

        return element.text.strip()


    def get_enable_message(self):
        return self.get_text(self.ENABLE_MSG)
        
    
    #------------Credit History Download----------------#
    # Export
    export_credit_history_button = (By.XPATH, "//button[normalize-space()='Export Credit History']")
    
    def click_export_credit_history(self):
        self.wait.until(EC.element_to_be_clickable(self.export_credit_history_button)).click()

    def wait_for_credit_history_download(self, download_dir, timeout=60):

        end_time = time.time() + timeout

        while time.time() < end_time:
            files = os.listdir(download_dir)

            for f in files:
                file_lower = f.lower()

                if "credit_history" in file_lower and file_lower.endswith(".xlsx"):
                    return True

            time.sleep(1)

        raise Exception("Credit history file not downloaded")
