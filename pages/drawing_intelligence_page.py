import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DrawingIntelligencePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 280)

    # ---------------- LOCATORS ---------------- #

    drawing_intelligence_menu = (By.XPATH,"//span[normalize-space()='Drawing Intelligence']")
    all_projects_dropdown = (By.XPATH,"//span[normalize-space()='All Projects']")
    all_folders_dropdown = (By.XPATH,"//span[normalize-space()='All Folders']")
    supply_chain_analytics = (By.XPATH,"//button[normalize-space()='Supply Chain Analytics']")
    download_template_btn = (By.XPATH,"//button[normalize-space()='Download Template']")
    upload_purchase_history = (By.XPATH,"//input[@type='file']")
    network_tab = (By.XPATH,"//button[normalize-space()='network']")
    families_tab = (By.XPATH,"//button[normalize-space()='families']")
    suppliers_tab = (By.XPATH,"//button[normalize-space()='suppliers']")

    # ---------------- ACTIONS ---------------- #

    def click_drawing_intelligence(self):
        self.wait.until(EC.element_to_be_clickable(self.drawing_intelligence_menu)).click()
        time.sleep(5)  # Wait for the page to load completely

    def select_project_space(self, root_space):

        # Open All Projects dropdown
        self.wait.until(EC.element_to_be_clickable(self.all_projects_dropdown)).click()
        time.sleep(3)

        # Uncheck all selected root spaces
        checkboxes = self.driver.find_elements(By.XPATH,"//label[contains(@class,'cursor-pointer')]//input[@type='checkbox']")

        for checkbox in checkboxes:
            try:
                if checkbox.is_selected():
                    self.driver.execute_script(
                        "arguments[0].click();",
                        checkbox
                    )
            except:
                pass

        time.sleep(2)

        # Select created root space only
        root_checkbox = self.wait.until(EC.presence_of_element_located((By.XPATH,f"//label[.//span[normalize-space()='{root_space}']]//input[@type='checkbox']")))
        self.driver.execute_script("arguments[0].click();",root_checkbox)
        time.sleep(3)
        # Close dropdown
        self.driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(2)


    def select_project_folder(self, project_name):
        self.wait.until(EC.element_to_be_clickable(self.all_folders_dropdown)).click()
        time.sleep(2)
        project_checkbox = self.wait.until(EC.presence_of_element_located((By.XPATH,f"//label[.//*[contains(text(),'{project_name}')]]//input[@type='checkbox']")))

        # Only click if NOT selected
        if not project_checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();",project_checkbox)

        # Close dropdown
        self.driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(2)

    def search_part(self, value):

        search_box = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                "//input[@placeholder='Search parts, materials, drawings...']")
            )
        )

        search_box.clear()
        search_box.send_keys(value)

        time.sleep(2)

    def refresh_page(self):
        self.driver.refresh()
        time.sleep(5)


    def apply_filter(self, xpath, screenshot_name):

        checkbox = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath)
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            checkbox
        )

        time.sleep(3)

        self.take_screenshot(screenshot_name)

        self.driver.execute_script(
            "arguments[0].click();",
            checkbox
        )

        time.sleep(2)

    def click_supply_chain_analytics(self):
        self.wait.until(EC.element_to_be_clickable(self.supply_chain_analytics)).click()

    def click_download_template(self):
        self.wait.until(EC.element_to_be_clickable(self.download_template_btn)).click()

    # def upload_purchase_history_file(self, file_path):
    #     upload = self.wait.until(EC.presence_of_element_located(self.upload_purchase_history))
    #     upload.send_keys(file_path)
    #     time.sleep(5)

    def upload_purchase_history_file(self, file_path):
        file_path = os.path.abspath(file_path)

        uploads = self.driver.find_elements(
            By.XPATH,
            "//input[@type='file']"
        )

        upload = uploads[-1]

        self.driver.execute_script(
            "arguments[0].style.display='block';",
            upload
        )

        upload.send_keys(file_path)
        time.sleep(5)

    def click_network_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.network_tab)).click()

    def click_families_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.families_tab)).click()

    def click_suppliers_tab(self):
        self.wait.until(EC.element_to_be_clickable(self.suppliers_tab)).click()

    def take_screenshot(self, name):

        folder = "screenshots"
        os.makedirs(folder, exist_ok=True)

        self.driver.save_screenshot(os.path.join(folder, f"{name}.png"))