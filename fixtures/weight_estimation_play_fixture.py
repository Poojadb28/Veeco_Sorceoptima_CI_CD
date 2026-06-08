import os
import time
import pytest
from selenium.webdriver.common.by import By

from pages.systemadmin_login_page import LoginPage
from pages.project_page import ProjectPage
from pages.weight_estimation_play_page import WeightEstimationPage


@pytest.fixture
def weight_estimation_play(browser):

    login = LoginPage(browser)
    login.login("prekshita@sourceoptima.com", "aspl1234")

    project = ProjectPage(browser)
    weight_estimation = WeightEstimationPage(browser)

    # =========================
    # NAVIGATE TO PROJECTS
    # =========================
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

    # Wait for space creation
    project.wait.until(lambda d: root_space in d.page_source)

    project.open_root_space(root_space)

    # =========================
    # CREATE PROJECT
    # =========================
    project_name = f"TestFile_{int(time.time())}"

    file_path = os.path.abspath("testdata/files/0194.pdf")

    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")

    project.click_new_upload()

    project.enter_project_name(project_name)

    project.upload_file(file_path)

    project.click_upload()

    # Wait for backend processing
    project.wait_for_processing_complete()

    # =========================
    # OPEN PROJECT
    # =========================
    project.open_project(project_name)

    # Wait until files visible
    project.wait.until(
        lambda d: len(
            d.find_elements(By.XPATH, "//input[@type='checkbox']")
        ) > 0
    )

    # =========================
    # SELECT FILES
    # =========================
    project.select_all_files()

    # Wait until dropdown ready
    project.wait.until(
        lambda d: len(d.find_elements(By.XPATH, "//select")) > 0
    )

    # =========================
    # WEIGHT ESTIMATION FLOW
    # =========================
    weight_estimation.select_weight_estimation()

    # Wait until Run button appears AFTER selecting play
    project.wait.until(lambda d: len(d.find_elements(*weight_estimation.run_btn)) > 0)

    weight_estimation.run_weight_estimation()

    weight_estimation.wait_for_processing()

    return weight_estimation