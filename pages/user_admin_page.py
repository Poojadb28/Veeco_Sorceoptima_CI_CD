from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UserAdminPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def click_user_admin_view(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='User Admin View']"))).click()

    def click_create_user(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Create User']"))).click()

    def click_cancel(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']"))).click()

    def enter_full_name(self, name):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Enter full name (e.g., John Doe)']"))).send_keys(name)

    def enter_email(self, email):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='user@example.com']"))).send_keys(email)

    def enter_password(self, password):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Enter secure password']"))).send_keys(password)

    def enter_confirm_password(self, password):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Re-enter password']"))).send_keys(password)


    def select_user_role(self, role_name):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@class,'w-full')]"))).click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//option[contains(text(),'{role_name}')]"))).click()

    def submit_user(self):

        submit_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            submit_btn
        )

        self.driver.execute_script("arguments[0].click();", submit_btn)

    

    def get_success_message(self):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'User created successfully')]"))).text
    
    def get_duplicate_error(self):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'user with this Email already exists.')]"))).text