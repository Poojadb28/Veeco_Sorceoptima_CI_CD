from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def wait_for_page_load(self):
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def open_url(self):
        # self.driver.get("https://testing.sourceoptima.com/")
        self.driver.get("https://testing-so.sourceoptima.com/")

    def click_login(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Login']"))).click()

    def enter_email(self, email):
        self.wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)

    def enter_password(self, password):
        self.wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)

    def click_submit(self):
        submit = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Submit']")))
        try:
            submit.click()
        except:
            self.driver.execute_script("arguments[0].click();", submit)

    def login(self, email, password):
        self.open_url()
        self.click_login()
        self.enter_email(email)
        self.enter_password(password)
        start_url = self.driver.current_url
        self.click_submit()
        WebDriverWait(self.driver, 60).until(
            lambda d: (
                "dashboard" in d.current_url.lower()
                or "orgchart" in d.current_url.lower()
                or "projects" in d.current_url.lower()
                or d.current_url != start_url
                or d.find_elements(By.XPATH, "//*[normalize-space()='Dashboard' or normalize-space()='Projects' or normalize-space()='Logout']")
                or d.find_elements(By.XPATH, "//*[contains(text(),'Error') or contains(text(),'Invalid')]")
            )
        )

    # invalid system admin login error message
    def get_error_message(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Invalid password. Please try again.')]"))).text

    
    # Logout method
    def click_logout(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Logout']"))).click()
