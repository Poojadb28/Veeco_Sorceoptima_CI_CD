import pytest
import time

from pages.systemadmin_login_page import LoginPage
from selenium.webdriver.common.by import By
from pages.project_page import ProjectPage


@pytest.fixture
def edit_space(browser):

    # =========================
    # LOGIN
    # =========================
    login = LoginPage(browser)
    login.login("prekshita@sourceoptima.com", "aspl1234")

    project = ProjectPage(browser)

    # =========================
    # NAVIGATION
    # =========================
    project.click_projects()

    # =========================
    # CREATE ROOT SPACE
    # =========================
    project.right_click_on_canvas()
    project.click_new_root_space()

    old_name = f"TestSpace_{int(time.time())}"

    project.enter_space_name(old_name)
    project.open_icon_selector()
    project.select_color()
    project.click_create_space()

    # Wait for creation
    project.wait.until(lambda d: old_name in d.page_source)

    # =========================
    # EDIT SPACE
    # =========================
    new_name = f"{old_name}_Edited"

    project.right_click_root_space(old_name)

    project.click_edit_details()
    # EXTRA WAIT (this fixes Jenkins flakiness)
    project.wait.until(
        lambda d: len(d.find_elements(By.XPATH, "//input")) > 0
    )

    project.edit_space_name(new_name)
    project.change_icon()
    project.select_purple_color()
    project.save_changes()

    # wait until name updated
    project.wait.until(
        lambda d: len(d.find_elements(By.XPATH, f"//h4[normalize-space()='{new_name}']")) > 0
    )

    return project, new_name