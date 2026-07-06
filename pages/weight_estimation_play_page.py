import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WeightEstimationPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 600)

    # ---------------- LOCATORS ----------------

    dropdown = (By.XPATH,"//select[contains(@class,'text-sm')]")
    weight_option = (By.XPATH,"//option[normalize-space()='Weight Estimation']")
    run_btn = (By.XPATH,"//button[contains(normalize-space(),'Run Weight Estimation')]")
    view_results = (By.XPATH, "//button[normalize-space()='View Results']")
    view_details = (By.XPATH, "//button[normalize-space()='View Details']")
    report_tab = (By.XPATH,"//button[normalize-space()='Weight Estimation']")
    popup_overlay = (By.XPATH,"//div[contains(@class,'fixed inset-0')]")
    close_icon = (By.XPATH,"//button[contains(@class,'p-2')]")

    # ---------------- ACTIONS ----------------

    def select_weight_estimation(self):
        self.wait.until(EC.element_to_be_clickable(self.dropdown)).click()
        self.wait.until(EC.element_to_be_clickable(self.weight_option)).click()

    def run_weight_estimation(self):
        element = self.wait.until(EC.element_to_be_clickable(self.run_btn))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",element)
        self.driver.execute_script("arguments[0].click();",element)

    
    def wait_for_processing(self):
        self.wait.until(EC.element_to_be_clickable(self.view_results))

    def click_view_results(self):
        self.wait.until(EC.element_to_be_clickable(self.view_results)).click()

    def click_view_details(self):
        self.wait.until(EC.element_to_be_clickable(self.view_details)).click()

    def wait_for_report_tab(self):

        self.wait.until(
            EC.visibility_of_element_located(self.report_tab)
        )

    def open_report_tab(self):

        # Wait popup visible
        self.wait.until(
            EC.visibility_of_element_located(self.popup_overlay)
        )

        # Wait report tab visible
        self.wait.until(
            EC.visibility_of_element_located(self.report_tab)
        )

        # Fresh element
        element = self.driver.find_element(*self.report_tab)

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

    def wait_for_report_loaded(self):

        self.wait.until(
            lambda d: "Weight Estimation" in d.page_source
        )

    # def take_screenshot(self):

    #     os.makedirs("screenshots", exist_ok=True)

    #     self.driver.save_screenshot(
    #         "screenshots/Weight_Estimation_Report.png"
    #     )

     # ---------------- SCREENSHOT ---------------- #
    def take_screenshot(self, file_name):
        os.makedirs("screenshots", exist_ok=True)

        file_path = os.path.join("screenshots", file_name)
        self.driver.save_screenshot(file_path)

        return file_path

    def close_popup(self):

        self.wait.until(
            EC.element_to_be_clickable(self.close_icon)
        )

        element = self.driver.find_element(*self.close_icon)

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

        # Wait until page interactive again
        self.wait.until(
            EC.element_to_be_clickable(self.dropdown)
        )
        