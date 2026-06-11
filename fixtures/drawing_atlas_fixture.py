import os
import time
import pytest
from pages.drawing_atlas_play_page import DrawingAtlasPage
from pages.systemadmin_login_page import LoginPage
from pages.project_page import ProjectPage



@pytest.fixture
def drawing_atlas_play(browser):

    login = LoginPage(browser)
    login.login("prekshita@sourceoptima.com", "aspl1234")

    project = ProjectPage(browser)
    drawing_atlas_play = DrawingAtlasPage(browser)

    # Open Projects
    project.click_projects()

    # ================= ROOT SPACE =================
    project.right_click_on_canvas()
    project.click_new_root_space()

    root_space = f"TestSpace_{int(time.time())}"

    project.enter_space_name(root_space)
    project.open_icon_selector()
    project.select_color()
    project.click_create_space()

    project.wait.until(lambda d: root_space in d.page_source)
    project.open_root_space(root_space)

    # ================= PROJECT =================
    project_name = f"TestFile_{int(time.time())}"

    file_path = os.path.abspath("testdata/files/0184.pdf")

    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")

    project.click_new_upload()
    project.enter_project_name(project_name)
    project.upload_file(file_path)
    project.click_upload()

    project.wait_for_processing_complete()

    # ================= OPEN PROJECT =================
    project.open_project(project_name)

    # IMPORTANT FIX (Select All button)
    project.select_all_files()

    # ================= DRAWING ATLAS =================
    drawing_atlas_play.select_drawing_atlas()
    drawing_atlas_play.click_run()
    drawing_atlas_play.wait_for_processing()

    return drawing_atlas_play