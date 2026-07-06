# import pytest
# import time
# import os
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from pages.systemadmin_login_page import LoginPage
# from pages.project_page import ProjectPage


# @pytest.fixture
# def project_folder_sharing_fixture(browser):
#     login = LoginPage(browser)
#     login.login("poojagowda@gmail.com", "aspl@1234")

#     project = ProjectPage(browser)

#     # Navigate to Projects
#     project.click_projects()

#     # ---------------- Create Root Space ----------------
#     project.right_click_on_canvas()
#     project.click_new_root_space()

#     root_space = f"TestSpace_{int(time.time())}"

#     project.enter_space_name(root_space)
#     project.open_icon_selector()
#     project.select_color()
#     project.click_create_space()

#     project.wait_for_page_load()

#     project.wait.until(
#         EC.visibility_of_element_located(
#             (By.XPATH, f"//*[text()='{root_space}']")
#         )
#     )

#     project.open_root_space(root_space)

#     # ---------------- Create Project ----------------
#     project_name = f"TestFile_{int(time.time())}"

#     file_name = "0136.pdf"
#     file_path = os.path.abspath("testdata/files/0136.pdf")

#     if not os.path.exists(file_path):
#         raise Exception(f"File not found: {file_path}")

#     project.create_project(project_name, file_path)

#     project.wait_for_page_load()
#     time.sleep(5)

#     # ---------------- Open Project and Share ----------------
#     project.open_project(project_name)

#     #click on 3 dots
#     project.click_on_3_dots()

#     #---------------- Share Project ----------------
#     project.click_share_project()

#     #---------------- Share Project with User ----------------
#     user_email = "poojadb1147@aspl.ai"
#     project.enter_email_to_share(user_email)

#     #click on email suggestion
#     project.click_on_email_suggestion()

#     #---------------- Click Share Button ----------------
#     project.click_share_button()

#     #---------------- Verify Sharing Success by taking screenshot ----------------
#     project.take_screenshot("screenshots/project_shared_success.png")

#     return project

import os
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.systemadmin_login_page import LoginPage
from pages.project_page import ProjectPage


@pytest.fixture
def project_folder_sharing_fixture(browser):

    login = LoginPage(browser)
    project = ProjectPage(browser)

    # ==========================================================
    # SYSTEM ADMIN
    # ==========================================================

    login.login("prekshita@sourceoptima.com", "aspl1234")

    project.click_projects()

    project.right_click_on_canvas()
    project.click_new_root_space()

    root_space = f"TestSpace_{int(time.time())}"

    project.enter_space_name(root_space)
    project.open_icon_selector()
    project.select_color()
    project.click_create_space()

    project.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//*[text()='{root_space}']")
        )
    )

    # Logout
    login.click_logout()

    # ==========================================================
    # ADMIN
    # ==========================================================

    login.login("poojagowda@gmail.com", "aspl@1234")

    project.click_projects()

    project.open_root_space(root_space)

    project_name = f"Project_{int(time.time())}"

    file_path = os.path.abspath("testdata/files/0136.pdf")

    project.create_project(project_name, file_path)

    project.wait_for_processing_complete()

    # project.open_project(project_name)

    project.click_on_3_dots()

    project.click_share_project()

    user_email = "poojadb1147@aspl.ai"

    project.enter_email_to_share(user_email)

    # project.click_on_email_suggestion(user_email)

    project.click_share_button()

    time.sleep(5)  

    project.take_screenshot("screenshots/project_shared_success.png")

    project.close_share_dialog()

    # Logout
    login.click_logout()


    # ==========================================================
    # USER
    # ==========================================================

    login.login("poojadb1147@aspl.ai", "aspl@1234")

    project.click_projects()

    project.open_root_space(root_space)

    project.open_project(project_name)

    time.sleep(5)  # Wait for the project to appear

    project.take_screenshot("screenshots/user_access_to_shared_project.png")

    yield project, project_name