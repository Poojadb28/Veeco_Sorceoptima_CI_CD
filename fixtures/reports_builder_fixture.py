import os
import time
import pytest

from pages.systemadmin_login_page import LoginPage
from pages.project_page import ProjectPage

@pytest.fixture
def reports_builder_fixture(browser):

    login = LoginPage(browser)
    login.login(
        "prekshita@sourceoptima.com",
        "aspl1234"
    )

    project = ProjectPage(browser)

    # ================= OPEN PROJECTS =================

    project.click_projects()

    # ================= CREATE ROOT SPACE =================

    project.right_click_on_canvas()
    project.click_new_root_space()

    root_space = f"TestSpace_{int(time.time())}"

    project.enter_space_name(root_space)
    project.open_icon_selector()
    project.select_color()
    project.click_create_space()

    project.wait.until(lambda d: root_space in d.page_source)

    project.open_root_space(root_space)

    # ================= CREATE PROJECT =================

    project_name = f"TestProject_{int(time.time())}"

    file_path = os.path.abspath("testdata/files/1212.zip")

    project.click_new_upload()
    project.enter_project_name(project_name)
    project.upload_file(file_path)
    project.click_upload()

    project.wait_for_processing_complete()

    # ================= REPORTS =================

    project.click_reports_builder()

    project.click_start_building()

    # Select created Root Space
    # project.select_root_space_for_report(root_space)
    project.select_specific_space_path()

    project.select_root_space_for_report(root_space)

    # Next
    project.click_next_preview()

    # Select required columns
    project.select_columns_for_report("Filename")
    project.select_columns_for_report("Classification Label")
    project.select_columns_for_report("Classification Confidence")
    project.select_columns_for_report("Description")
    project.select_columns_for_report("Material")
    project.select_columns_for_report("Project")
    project.select_columns_for_report("Organization Path")

    # #click on save template button
    # project.click_save_template()

    # # Enter template name and description
    # template_name = f"Template_{int(time.time())}"
    # project.enter_template_name(template_name)
    # project.enter_template_description("Automation Report Template")

    # # Click on save template button
    # project.click_save_template_button()

    return project

    