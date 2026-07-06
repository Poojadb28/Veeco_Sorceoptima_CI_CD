import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.systemadmin_login_page import LoginPage
from pages.project_page import ProjectPage


@pytest.fixture
def organization_wide_search_fixture(browser):
    login = LoginPage(browser)
    login.login("prekshita@sourceoptima.com", "aspl1234")

    project = ProjectPage(browser)

    # Navigate to Projects
    project.click_projects()

    # ---------------- Create Root Space ----------------
    project.right_click_on_canvas()
    project.click_new_root_space()

    root_space = f"TestSpace_{int(time.time())}"

    project.enter_space_name(root_space)
    project.open_icon_selector()
    project.select_color()
    project.click_create_space()

    project.wait_for_page_load()

    project.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//*[text()='{root_space}']")
        )
    )

    project.open_root_space(root_space)

    # ---------------- Create Project ----------------
    project_name = f"TestFile_{int(time.time())}"

    file_name = "0194.pdf"
    file_path = os.path.abspath("testdata/files/0194.pdf")

    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")

    project.create_project(project_name, file_path)

    project.wait_for_page_load()
    time.sleep(5)

    # Back to Organization
    project.click_back_to_organization()
    project.wait_for_page_load()
    time.sleep(2)

    # =====================================================
    # Search Project
    # =====================================================

    project.search_organization(project_name)

    assert project.verify_search_result(project_name)

    project.click_search_result(project_name)

    project.wait_for_page_load()
    time.sleep(2)

    project_screenshot = os.path.join(
    "screenshots",
    f"project_search_{int(time.time())}.png")

    # =====================================================
    # Back to Projects
    # =====================================================

    project.click_back_to_projects()

    project.wait_for_page_load()
    time.sleep(2)

   

    # =====================================================
    # Search File
    # =====================================================

    project.search_organization(file_name)

    assert project.verify_search_result(file_name)

    project.click_search_result(file_name)

    project.wait_for_page_load()
    time.sleep(2)

    file_screenshot = os.path.join(
    "screenshots",
    f"file_search_{int(time.time())}.png")

    return (
        project,
        project_name,
        file_name,
        project_screenshot,
        file_screenshot,
    )