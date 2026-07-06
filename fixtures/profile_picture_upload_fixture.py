# import os
# import pytest
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from pages.systemadmin_login_page import LoginPage
# from pages.project_page import ProjectPage


# @pytest.fixture
# def profile_picture_upload_fixture(browser):
#     login = LoginPage(browser)
#     login.login("prekshita@sourceoptima.com", "aspl1234")

#     project = ProjectPage(browser)

#     def upload_profile_picture(self, file_path):

#         file_path = os.path.abspath(file_path)

#         upload = self.wait.until(EC.presence_of_element_located(
#             (By.XPATH, "//input[@type='file']")
#         ))

#         # IMPORTANT for hidden input
#         self.driver.execute_script("arguments[0].style.display='block';", upload)

#         upload.send_keys(file_path)


#     # Upload image
#     image_path = os.path.abspath("testdata/files/pic2.png")

#     upload_input = WebDriverWait(browser, 20).until(
#         EC.presence_of_element_located(
#             (By.XPATH, "//input[@type='file']")
#         )
#     )

#     upload_input.send_keys(image_path)

#     return browser

import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.systemadmin_login_page import LoginPage
from pages.project_page import ProjectPage


@pytest.fixture
def profile_picture_upload_fixture(browser):

    login = LoginPage(browser)
    login.login("prekshita@sourceoptima.com", "aspl1234")

    project = ProjectPage(browser)
    project.click_projects()

    image_path = os.path.abspath("testdata/files/pic2.png")

    upload_input = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )

    # If input is hidden
    browser.execute_script(
        "arguments[0].style.display='block';", upload_input
    )

    upload_input.send_keys(image_path)

    # Verify file was selected
    assert "pic2.png" in upload_input.get_attribute("value")

    # Click Save/Update button if your application has one
    # Uncomment and adjust the XPath if applicable:
    #
    # WebDriverWait(browser, 20).until(
    #     EC.element_to_be_clickable(
    #         (By.XPATH, "//button[contains(.,'Save') or contains(.,'Update')]")
    #     )
    # ).click()

    yield browser
    