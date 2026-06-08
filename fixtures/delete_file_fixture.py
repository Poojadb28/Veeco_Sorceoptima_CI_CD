import os
import time
import pytest

from pages.systemadmin_login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.project_page import ProjectPage


@pytest.fixture
def delete_file(browser):

    login = LoginPage(browser)
    login.login("prekshita@sourceoptima.com", "aspl1234")

    project = ProjectPage(browser)

    # ================= PROJECT =================
    project.click_projects()

    # -------- CREATE ROOT SPACE --------
    project.right_click_on_canvas()
    project.click_new_root_space()

    root_space = f"TestSpace_{int(time.time())}"

    project.enter_space_name(root_space)
    project.open_icon_selector()
    project.select_color()
    project.click_create_space()

    project.wait.until(lambda d: root_space in d.page_source)
    project.open_root_space(root_space)

    # -------- CREATE PROJECT --------
    project_name = f"TestFile_{int(time.time())}"
    file_path = os.path.abspath("testdata/files/0194.pdf")

    project.click_new_upload()
    project.enter_project_name(project_name)
    project.upload_file(file_path)
    project.click_upload()

    project.wait_for_processing_complete()

    project.open_project(project_name)

    # -------- FILE DELETE --------
    file_name = "0194.pdf"

    project.delete_file(file_name)

    return project, file_name