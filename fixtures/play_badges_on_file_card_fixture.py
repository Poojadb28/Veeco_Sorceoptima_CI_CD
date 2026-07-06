import os
import time
import pytest

from pages.systemadmin_login_page import LoginPage
from pages.project_page import ProjectPage
from pages.tariff_analysis_play_page import TariffPage


# @pytest.fixture
# def play_badges_on_file_card(browser):

#     login = LoginPage(browser)
#     login.login("prekshita@sourceoptima.com", "aspl1234")

#     project = ProjectPage(browser)
#     tariff = TariffPage(browser)

#     project.click_projects()

#     project.right_click_on_canvas()
#     project.click_new_root_space()

#     root_space = f"TestSpace_{int(time.time())}"

#     project.enter_space_name(root_space)
#     project.open_icon_selector()
#     project.select_color()
#     project.click_create_space()

#     project.wait.until(lambda d: root_space in d.page_source)
#     project.open_root_space(root_space)

#     project_name = f"TestFile_{int(time.time())}"
#     file_path = os.path.abspath("testdata/files/0136.pdf")

#     project.click_new_upload()
#     project.enter_project_name(project_name)
#     project.upload_file(file_path)
#     project.click_upload()

#     project.wait_for_processing_complete()

#     project.open_project(project_name)
#     project.select_all_files()

#     tariff.select_tariff_analysis()
#     tariff.treat_as_assembly()
#     tariff.set_top_level()
#     tariff.run_tariff_analysis()

#     tariff.wait_for_processing_complete()

#     os.makedirs("screenshots", exist_ok=True)

#     screenshot_path = os.path.join(
#         "screenshots",
#         f"file_card_with_badges_{int(time.time())}.png"
#     )

#     tariff.take_screenshot(screenshot_path)

#     yield tariff, screenshot_path

@pytest.fixture
def play_badges_on_file_card(browser):

    login = LoginPage(browser)
    login.login("prekshita@sourceoptima.com", "aspl1234")

    project = ProjectPage(browser)
    tariff = TariffPage(browser)

    project.click_projects()

    project.right_click_on_canvas()
    project.click_new_root_space()

    root_space = f"TestSpace_{int(time.time())}"

    project.enter_space_name(root_space)
    project.open_icon_selector()
    project.select_color()
    project.click_create_space()

    project.wait.until(lambda d: root_space in d.page_source)
    project.open_root_space(root_space)

    project_name = f"TestFile_{int(time.time())}"
    file_path = os.path.abspath("testdata/files/0136.pdf")

    project.click_new_upload()
    project.enter_project_name(project_name)
    project.upload_file(file_path)
    project.click_upload()

    project.wait_for_processing_complete()

    project.open_project(project_name)
    project.select_all_files()

    tariff.select_tariff_analysis()
    tariff.treat_as_assembly()
    tariff.set_top_level()
    tariff.run_tariff_analysis()
    tariff.wait_for_processing_complete()

    yield tariff