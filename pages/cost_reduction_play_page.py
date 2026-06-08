import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CostReductionPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 120)

    # LOCATORS
    dropdown = (By.XPATH, "//select[contains(@class,'text-sm')]")
    option = (By.XPATH, "//option[normalize-space()='Cost Reduction']")
    run_button = (By.XPATH, "//button[contains(text(),'Run Cost Reduction')]")
    view_results = (By.XPATH, "//button[normalize-space()='View Results']")
    view_details = (By.XPATH, "//button[normalize-space()='View Details']")
    report_tab = (By.XPATH, "//button[normalize-space()='Cost Reduction']")
    popup_overlay = (By.XPATH, "//div[contains(@class,'fixed inset-0')]")
    close_icon = (By.XPATH, "//button[contains(@class,'p-2')]")

    # ACTIONS

    def select_cost_reduction(self):
        self.wait.until(EC.element_to_be_clickable(self.dropdown)).click()
        self.wait.until(EC.element_to_be_clickable(self.option)).click()

    def click_run(self):
        self.wait.until(EC.element_to_be_clickable(self.run_button)).click()

    def wait_for_processing(self):
        self.wait.until(EC.element_to_be_clickable(self.view_results))

    def click_view_results(self):
        self.wait.until(EC.element_to_be_clickable(self.view_results)).click()

    def click_view_details(self):
        self.wait.until(EC.element_to_be_clickable(self.view_details)).click()

    def open_report_tab(self):
        self.wait.until(EC.visibility_of_element_located(self.popup_overlay))

        element = self.wait.until(EC.element_to_be_clickable(self.report_tab))
        self.driver.execute_script("arguments[0].click();", element)

    def take_screenshot(self):
        os.makedirs("screenshots", exist_ok=True)
        self.driver.save_screenshot("screenshots/Cost_Reduction_Report.png")

    def close_popup(self):
        element = self.wait.until(EC.element_to_be_clickable(self.close_icon))
        self.driver.execute_script("arguments[0].click();", element)

        # Wait for underlying page to be clickable again
        self.wait.until(EC.element_to_be_clickable(self.dropdown))

