import os
import time
from utils.download_utils import wait_for_new_file
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TariffPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 280)

    # ---------------- LOCATORS ----------------

    dropdown = (By.XPATH, "//select[.//option[normalize-space()='Tariff Analysis']]")
    tariff_option = (By.XPATH, "//option[normalize-space()='Tariff Analysis']")
    treat_checkbox = (By.XPATH, "//input[contains(@class,'w-4 h-4')]")
    set_top = (By.XPATH, "//button[normalize-space()='Set as Top Level']")
    run_btn = (By.XPATH, "//button[contains(normalize-space(),'Run Tariff Analysis')]")

    # Separate export buttons
    bom_export_btn = (By.XPATH, "(//button[normalize-space()='Export to Excel'])[1]")
    
    tariff_export_btn = (By.XPATH, "(//button[contains(.,'Export to Excel')])[last()]")

    approve_bom_btn = (By.XPATH, "//span[normalize-space()='Approve BOM']")
    tariff_heading = (By.XPATH, "//h2[contains(text(),'Tariff Analysis')]")

    back_project = (By.XPATH, "//span[normalize-space()='Back to Project']")
    back_btn = (By.XPATH, "//span[normalize-space()='Back']")

    # ---------------- ACTIONS ----------------

    def select_tariff_analysis(self):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.dropdown))
        Select(dropdown).select_by_visible_text("Tariff Analysis")

    def treat_as_assembly(self):
        checkbox = self.wait.until(EC.presence_of_element_located(self.treat_checkbox))
        self.driver.execute_script("arguments[0].click();", checkbox)

    def set_top_level(self):
        elements = self.driver.find_elements(*self.set_top)
        if elements:
            self.driver.execute_script("arguments[0].click();", elements[0])

    def run_tariff_analysis(self):
        self.wait.until(EC.element_to_be_clickable(self.run_btn)).click()

    # ---------------- APPROVE BOM ----------------

    def approve_bom(self):

        old_buttons = self.driver.find_elements(*self.bom_export_btn)
        element = self.wait.until(EC.element_to_be_clickable(self.approve_bom_btn))
        self.driver.execute_script("arguments[0].click();", element)

        if old_buttons:
            try:
                WebDriverWait(self.driver, 15).until(EC.staleness_of(old_buttons[0]))
            except TimeoutException:
                pass

        self.wait.until(EC.invisibility_of_element_located(self.approve_bom_btn))

        self.wait.until(
            lambda d:
                d.find_elements(By.XPATH, "//button[normalize-space()='Continue']")
                or len(d.find_elements(By.XPATH, "//button[contains(.,'Export to Excel')]")) > 1
        )
   

    def export_bom(self, download_dir):

        # Step 1: Ensure page loaded
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        before_files = set(os.listdir(download_dir))

        # Step 2: Wait for button
        element = self.wait.until(EC.presence_of_element_located(self.bom_export_btn))

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.wait.until(EC.element_to_be_clickable(self.bom_export_btn))

        # Step 3: Click
        self.driver.execute_script("arguments[0].click();", element)

        # Step 4: Use utility
        file_path = wait_for_new_file(download_dir, before_files, extension=".xlsx")

        return file_path

    # ---------------- TARIFF EXPORT ----------------

    def complete_hts_wizard(self):

        

        try:
            # Loop to handle multiple steps (important)
            for _ in range(5):

                continue_buttons = [
                    btn for btn in self.driver.find_elements(By.XPATH, "//button[normalize-space()='Continue']")
                    if btn.is_displayed()
                ]

                if not continue_buttons:
                    return

                options = self.driver.find_elements(By.XPATH, "//label[.//input[@type='radio'] or .//span or .//div]")

                for opt in options:
                    if opt.is_displayed():
                        self.driver.execute_script("arguments[0].click();", opt)
                        break

                continue_btn = self.wait.until(
                    lambda d: next(
                        (
                            btn for btn in d.find_elements(By.XPATH, "//button[normalize-space()='Continue']")
                            if btn.is_displayed() and btn.is_enabled()
                        ),
                        False
                    )
                )
                self.driver.execute_script("arguments[0].click();", continue_btn)

                time.sleep(2)

        except Exception as e:
            print("Wizard handling skipped:", e)

        # time.sleep(5)

    def wait_for_processing_complete(self):
     
            # Wait until any loader disappears
        self.wait.until_not(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'animate-spin') or contains(text(),'Processing')]")
            ))
           

    def export_tariff(self, download_dir):

        # Step 1: Ensure page loaded
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        before_files = set(os.listdir(download_dir))

        # Step 2: Wait for wizard completion and export availability
        self.wait.until(
            lambda d: not any(
                btn.is_displayed()
                for btn in d.find_elements(By.XPATH, "//button[normalize-space()='Continue']")
            )
        )

        button = self.wait.until(
            lambda d: next(
                (
                    btn for btn in d.find_elements(By.XPATH, "//button[contains(.,'Export to Excel')]")
                    if btn.is_displayed() and btn.is_enabled()
                ),
                False
            )
        )

        # Step 3: Scroll
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", button
        )

        # Step 4: Wait clickable
        self.wait.until(lambda d: button.is_displayed() and button.is_enabled())

        # Step 5: Click
        try:
            button.click()
        except:
            self.driver.execute_script("arguments[0].click();", button)

        # Step 6: Use utility
        file_path = wait_for_new_file(download_dir, before_files, extension=".xlsx")

        return file_path

    # ---------------- NAVIGATION ----------------
    def go_back(self):
        self.wait.until(EC.element_to_be_clickable(self.back_project)).click()
        self.wait.until(EC.element_to_be_clickable(self.back_btn)).click()

    #click view results button
    def click_view_results(self):
        view_results = (
            By.XPATH,
            "//button[contains(.,'View Results')]"
        )

        element = self.wait.until(
            EC.element_to_be_clickable(view_results)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )
    def take_screenshot(self, file_path):
        self.driver.save_screenshot(file_path)
        
