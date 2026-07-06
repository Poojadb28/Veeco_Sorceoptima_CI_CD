import os
import time
import pytest

from pages.systemadmin_login_page import LoginPage
from pages.project_page import ProjectPage
from pages.drawing_atlas_play_page import DrawingAtlasPage
from pages.drawing_intelligence_page import DrawingIntelligencePage


@pytest.fixture
def drawing_intelligence(browser):

    login = LoginPage(browser)
    login.login(
        "prekshita@sourceoptima.com",
        "aspl1234"
    )

    project = ProjectPage(browser)
    drawing_atlas_play = DrawingAtlasPage(browser)
    drawing_intelligence_page = DrawingIntelligencePage(browser)

    # ================= OPEN PROJECTS =================

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

    file_path = os.path.abspath("testdata/files/1212.zip")

    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")

    project.click_new_upload()
    project.enter_project_name(project_name)
    project.upload_file(file_path)
    project.click_upload()

    project.wait_for_processing_complete()

    # ================= OPEN PROJECT =================

    project.open_project(project_name)

    project.select_all_files()

    # ================= DRAWING ATLAS =================

    drawing_atlas_play.select_drawing_atlas()
    drawing_atlas_play.click_run()
    drawing_atlas_play.wait_for_processing()
    drawing_atlas_play.click_view_results()

    # ================= DRAWING INTELLIGENCE =================

    drawing_intelligence_page.click_drawing_intelligence()

    drawing_intelligence_page.select_project_space(root_space)
    drawing_intelligence_page.take_screenshot("rootspace_selected")
    drawing_intelligence_page.select_project_folder(project_name)
    drawing_intelligence_page.take_screenshot("01_project_selected")
    # Search 6001.pdf

    drawing_intelligence_page.search_part("6001.pdf")
    drawing_intelligence_page.take_screenshot("search_6001_pdf")
    drawing_intelligence_page.refresh_page()
    time.sleep(2)  # wait for page refresh

    # Drawing Type - Detail
    drawing_intelligence_page.apply_filter("//label[contains(.,'Detail')]//input[@type='checkbox']", "Detail")

    # Drawing Type - Weldment
    drawing_intelligence_page.apply_filter("//label[contains(.,'Weldment')]//input[@type='checkbox']", "Weldment")

    # Drawing Type - Sheet Metal
    drawing_intelligence_page.apply_filter("//label[contains(.,'Sheet Metal')]//input[@type='checkbox']", "Sheet Metal")

    # #Units - All DIMS In Inches
    # drawing_intelligence_page.apply_filter("//label[contains(.,'All DIMS In Inches')]//input[@type='checkbox']", "All DIMS In Inches")

    # #Units - inches
    # drawing_intelligence_page.apply_filter("//label[contains(.,'inches')]//input[@type='checkbox']", "inches")

    # #Units - INCHES [mm]
    # drawing_intelligence_page.apply_filter("//label[contains(.,'INCHES [mm]')]//input[@type='checkbox']", "INCHES_mm")

    # #RELEASE STATUS 
    # drawing_intelligence_page.apply_filter("//label[contains(.,'RELEASED')]//input[@type='checkbox']", "RELEASED")

    # #Engineering/MATERIAL

    # #Al
    # drawing_intelligence_page.apply_filter("//label[contains(.,'Al')]//input[@type='checkbox']", "Al")

    # #Cu
    # drawing_intelligence_page.apply_filter("//label[contains(.,'Cu')]//input[@type='checkbox']", "Cu")

    # #Other
    # drawing_intelligence_page.apply_filter("//label[contains(.,'Other')]//input[@type='checkbox']", "Other")

    # #Steel
    # drawing_intelligence_page.apply_filter("//label[contains(.,'Steel')]//input[@type='checkbox']", "Steel")

    # #CONDITION/TEMPER

    # #T6
    # drawing_intelligence_page.apply_filter("//label[contains(.,'T6')]//input[@type='checkbox']", "T6")

    # #COATING

    # #BLACK ANODIZE
    # drawing_intelligence_page.apply_filter("//label[contains(.,'BLACK ANODIZE')]//input[@type='checkbox']", "BLACK ANODIZE")

    # #black cathode electrocoat or CARDINAL TO02-BK08 powder coat
    # drawing_intelligence_page.apply_filter("//label[contains(.,'black cathode electrocoat') or contains(.,'CARDINAL TO02-BK08 powder coat')]//input[@type='checkbox']", "black_cathode_electrocoat")

    # #CLEAR ALODINE
    # drawing_intelligence_page.apply_filter("//label[contains(.,'CLEAR ALODINE')]//input[@type='checkbox']", "CLEAR ALODINE")

    # #clear anodize
    # drawing_intelligence_page.apply_filter("//label[contains(.,'clear anodize')]//input[@type='checkbox']", "clear anodize")

    # #CLEAR ANODIZE
    # drawing_intelligence_page.apply_filter("//label[contains(.,'CLEAR ANODIZE')]//input[@type='checkbox']", "CLEAR ANODIZE")

    # #NONE
    # drawing_intelligence_page.apply_filter("//label[contains(.,'NONE')]//input[@type='checkbox']", "NONE")


    # #PROCESS
    # #Machining
    # drawing_intelligence_page.apply_filter("//label[contains(.,'Machining')]//input[@type='checkbox']", "Machining")

    # #MACHINING ROUTE
    # #3-Axis Mill
    # drawing_intelligence_page.apply_filter("//label[contains(.,'3-Axis Mill')]//input[@type='checkbox']", "3_Axis_Mill")

    # #SECONDARY PROCESSES
  
    # #Chemical clean
    # drawing_intelligence_page.apply_filter("//label[contains(.,'Chemical clean')]//input[@type='checkbox']", "Chemical clean")

    # #cleaning
    # drawing_intelligence_page.apply_filter("//label[contains(.,'cleaning')]//input[@type='checkbox']", "cleaning")

    # #clear alodine
    # drawing_intelligence_page.apply_filter("//label[contains(.,'clear alodine')]//input[@type='checkbox']", "clear alodine")

    # #clear anodize
    # drawing_intelligence_page.apply_filter("//label[contains(.,'clear anodize')]//input[@type='checkbox']", "clear anodize")

    # #SIZE

    # #Miniature
    # drawing_intelligence_page.apply_filter("//label[contains(.,'Miniature')]//input[@type='checkbox']", "Miniature")

    # #Small
    # drawing_intelligence_page.apply_filter("//label[contains(.,'Small')]//input[@type='checkbox']", "Small")

    # #Medium
    # drawing_intelligence_page.apply_filter("//label[contains(.,'Medium')]//input[@type='checkbox']", "Medium")

    # #Large
    # drawing_intelligence_page.apply_filter("//label[contains(.,'Large')]//input[@type='checkbox']", "Large")

    # #WEIGHT

    # #Unspecified
    # drawing_intelligence_page.apply_filter("//label[contains(.,'Unspecified')]//input[@type='checkbox']", "Unspecified")

    drawing_intelligence_page.click_supply_chain_analytics()
    drawing_intelligence_page.click_download_template()
    purchase_history_file = os.path.abspath("testdata/files/purchase_history_template.csv")

    if not os.path.exists(purchase_history_file):
        raise Exception(f"File not found: {purchase_history_file}")

    drawing_intelligence_page.upload_purchase_history_file(purchase_history_file)
    drawing_intelligence_page.take_screenshot("02_file_uploaded")
    drawing_intelligence_page.click_network_tab()
    drawing_intelligence_page.take_screenshot("03_network_tab")
    drawing_intelligence_page.click_families_tab()
    drawing_intelligence_page.take_screenshot("04_families_tab")
    drawing_intelligence_page.click_suppliers_tab()
    drawing_intelligence_page.take_screenshot("05_suppliers_tab")

    return drawing_intelligence_page