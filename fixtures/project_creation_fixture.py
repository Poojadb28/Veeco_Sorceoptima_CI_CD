import pytest
import time
import os

from pages.systemadmin_login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.project_page import ProjectPage


@pytest.fixture
def create_project(browser):

    # LOGIN (independent)
    login = LoginPage(browser)
    login.login("prekshita@sourceoptima.com", "aspl1234")

    project = ProjectPage(browser)

    # NAVIGATION
    project.click_projects()

    # =========================
    # CREATE ROOT SPACE
    # =========================
    project.right_click_on_canvas()
    project.click_new_root_space()

    root_space = f"TestSpace_{int(time.time())}"

    project.enter_space_name(root_space)
    project.open_icon_selector()
    project.select_color()
    project.click_create_space()

    project.wait_for_page_load()

    project.wait.until(
        EC.visibility_of_element_located((By.XPATH, f"//*[text()='{root_space}']"))
    )

    project.open_root_space(root_space)

    # Dynamic project name
    project_name = f"TestFile_{int(time.time())}"

    # File path (Jenkins safe)
    file_path = os.path.abspath("testdata/files/0254.zip")

    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")

    # Create project
    project.create_project(project_name, file_path)

    return project, project_name