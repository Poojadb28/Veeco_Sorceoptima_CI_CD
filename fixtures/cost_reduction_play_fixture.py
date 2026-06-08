# import os
# import time
# import pytest
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from pages.systemadmin_login_page import LoginPage
# from pages.project_page import ProjectPage
# from pages.cost_reduction_play_page import CostReductionPage


# @pytest.fixture
# def cost_reduction_play(browser):

#     login = LoginPage(browser)
#     login.login("prekshita@sourceoptima.com", "aspl1234")

#     project = ProjectPage(browser)
#     cost = CostReductionPage(browser)

#     # Click Projects
#     project.click_projects()

#     # =========================
#     # CREATE ROOT SPACE
#     # =========================
#     project.right_click_on_canvas()
#     project.click_new_root_space()

#     root_space = f"TestSpace_{int(time.time())}"

#     project.enter_space_name(root_space)
#     project.open_icon_selector()
#     project.select_color()
#     project.click_create_space()

#     # Wait for space creation
#     project.wait.until(lambda d: root_space in d.page_source)

#     project.open_root_space(root_space)

#     # =========================
#     # CREATE PROJECT
#     # =========================
#     project_name = f"TestFile_{int(time.time())}"

#     file_path = os.path.abspath("testdata/files/0194.pdf")

#     if not os.path.exists(file_path):
#         raise Exception(f"File not found: {file_path}")

#     project.click_new_upload()
#     project.enter_project_name(project_name)
#     project.upload_file(file_path)
#     project.click_upload()

#     # Wait for project creation
#     project.wait_for_processing_complete()

#     # =========================
#     # OPEN PROJECT
#     # =========================
#     project.open_project(project_name)

#     # wait until files appear
#     project.wait.until(lambda d: len(d.find_elements(By.XPATH, "//input[@type='checkbox']")) > 0)

#     # project.select_all_files()

#     # # # Perform Cost Reduction Play
#     # cost.select_cost_reduction()

#     project.select_all_files()

#     # REAL WAIT 
#     project.wait.until(lambda d: 
#         len(d.find_elements(By.XPATH, "//button[normalize-space()='Cost Reduction']")) > 0
#     )

#     cost.select_cost_reduction()
        
#     cost.click_run()
#     cost.wait_for_processing()

#     return cost

import os
import time
import pytest
from selenium.webdriver.common.by import By
from pages.systemadmin_login_page import LoginPage
from pages.project_page import ProjectPage
from pages.cost_reduction_play_page import CostReductionPage


@pytest.fixture
def cost_reduction_play(browser):

    login = LoginPage(browser)
    login.login("prekshita@sourceoptima.com", "aspl1234")
    # login.wait_for_page_load()

    project = ProjectPage(browser)
    cost = CostReductionPage(browser)

    # =========================
    # NAVIGATE TO PROJECTS
    # =========================
    project.click_projects()
    # project.wait_for_page_load()

    # =========================
    # CREATE ROOT SPACE
    # =========================
    project.right_click_on_canvas()
    # project.wait_for_page_load()
    project.click_new_root_space()
    # project.wait_for_page_load()

    root_space = f"TestSpace_{int(time.time())}"

    project.enter_space_name(root_space)
    project.open_icon_selector()
    project.select_color()
    project.click_create_space()
    # project.wait_for_page_load()

    # Wait for space creation
    project.wait.until(lambda d: root_space in d.page_source)

    project.open_root_space(root_space)
    # project.wait_for_page_load()
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
    # project.wait_for_page_load()

    # Wait until files are visible
    project.wait.until(
        lambda d: len(d.find_elements(By.XPATH, "//input[@type='checkbox']")) > 0
    )

    # =========================
    # SELECT FILES
    # ========================= 
    # project.select_all_files()
    
    # # WAIT FOR UI TO BE READY AFTER FILE SELECTION
    # project.wait.until(lambda d: len(d.find_elements(By.XPATH, "//select")) > 0)

    # # Optional extra stability for CI
    # time.sleep(2) 

    project.select_all_files()

    # Wait dropdown/select elements loaded
    project.wait.until(
        lambda d: len(
            d.find_elements(By.XPATH, "//select")
        ) > 0
    )

    # Wait page fully stabilized
    project.wait.until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )
    # =========================
    # COST REDUCTION FLOW
    # =========================
    cost.select_cost_reduction()
    cost.click_run()
    cost.wait_for_processing()
    # cost.wait_for_page_load()

    return cost