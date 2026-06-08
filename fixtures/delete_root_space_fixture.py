import pytest
import time
from pages.project_page import ProjectPage
from pages.systemadmin_login_page import LoginPage


@pytest.fixture
def delete_root_space(browser):
    login = LoginPage(browser)
    login.login("prekshita@sourceoptima.com", "aspl1234")
    
    project = ProjectPage(browser)

    # ================= NAVIGATION =================
    project.click_projects()

    # ================= CREATE ROOT SPACE =================
    root_space_name = f"TestSpace_{int(time.time())}"

    project.right_click_on_canvas()
    project.click_new_root_space()
    project.enter_space_name(root_space_name)
    project.choose_icon()
    project.select_color()
    project.click_create_space()

    # wait for creation
    project.wait.until(lambda d: root_space_name in d.page_source)

    # ================= DELETE ROOT SPACE =================
    project.right_click_root_space(root_space_name)
    project.click_delete_space()
    project.confirm_delete_space()

    return project, root_space_name