pytest_plugins = [
    "fixtures.systemadmin_login_fixture",
    "fixtures.user_creation_fixture",
    "fixtures.admin_creation_fixture",
    "fixtures.logout_fixture",
    "fixtures.project_fixture",
    "fixtures.subspace_fixture",
    "fixtures.delete_root_space_fixture",
    "fixtures.project_creation_fixture",
    "fixtures.project_upload_fixture",
    "fixtures.file_upload_fixture",
    "fixtures.edit_space_fixture",
    "fixtures.delete_project_fixture",
    "fixtures.search_file_fixture",
    "fixtures.available_plays_fixture",
    "fixtures.cost_reduction_play_fixture",
    "fixtures.design_review_fixture",
    "fixtures.drawing_checker_both_play_fixture",
    "fixtures.drawing_checker_general_play_fixture",
    "fixtures.drawing_checker_v2_play_fixture",
    "fixtures.drawing_checker_veeco_play_fixture",
    "fixtures.tariff_analysis_play_fixture",
    "fixtures.download_logs_fixture",
    "fixtures.delete_file_fixture",
    "fixtures.select_deselect_all_files_fixture",
    "fixtures.filter_labels_fixture",
    "fixtures.create_new_project_fixture",
    "fixtures.export_credit_history_fixture",
    "fixtures.export_classification_to_excel_fixture",
    "fixtures.duplicate_admin_creation_fixture",
    "fixtures.duplicate_user_creation_fixture",
    "fixtures.systemadmin_creation_fixture",
    "fixtures.duplicate_systemadmin_creation_fixture",
    "fixtures.weight_estimation_play_fixture",
    "fixtures.drawing_atlas_fixture",
    "fixtures.drawing_intelligence_fixture",
    "fixtures.organization_wide_search_fixture",
    "fixtures.play_badges_on_file_card_fixture",
    "fixtures.profile_picture_upload_fixture",
    "fixtures.project_folder_sharing_fixture",
    "fixtures.reports_builder_fixture"
]

import pytest
import sys
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# =========================
# FIX IMPORT PATH (IMPORTANT FOR JENKINS)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)


# =========================
# ADD COMMAND LINE OPTION
# =========================
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests"
    )


# =========================
# DRIVER SETUP
# =========================

@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("--browser")

    if browser_name == "chrome":
        chrome_options = Options()

        # Required for Jenkins / headless
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        # Shared download folder (no fixture changes needed)
        download_dir = os.path.abspath("downloads")
        os.makedirs(download_dir, exist_ok=True)

        # Clean folder before each test (VERY IMPORTANT)
        for f in os.listdir(download_dir):
            try:
                os.remove(os.path.join(download_dir, f))
            except:
                pass

        # Chrome download preferences
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_setting_values.automatic_downloads": 1
        }
        chrome_options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(
            executable_path="drivers/chromedriver.exe",
            options=chrome_options
        )

        # service = Service("drivers/chromedriver.exe")

        # driver = webdriver.Chrome(
        #     service=service,
        #     options=chrome_options
        # )

        # Optional: attach for future use (no need to change tests now)
        driver.download_dir = download_dir

    else:
        raise Exception(f"Browser {browser_name} not supported")


    yield driver

    driver.quit()


# =========================
# PYTEST HOOK (OPTIONAL - FOR LOGGING)
# =========================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("browser", None)
        if driver:
            screenshots_dir = os.path.join(BASE_DIR, "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

            file_name = os.path.join(
                screenshots_dir,
                f"{item.name}.png"
            )
            driver.save_screenshot(file_name)

##JENKINS##

# pytest_plugins = [
#     "fixtures.systemadmin_login_fixture",
#     "fixtures.user_creation_fixture",
#     "fixtures.admin_creation_fixture",
#     "fixtures.logout_fixture",
#     "fixtures.project_fixture",
#     "fixtures.subspace_fixture",
#     "fixtures.delete_root_space_fixture",
#     "fixtures.project_creation_fixture",
#     "fixtures.project_upload_fixture",
#     "fixtures.file_upload_fixture",
#     "fixtures.edit_space_fixture",
#     "fixtures.delete_project_fixture",
#     "fixtures.search_file_fixture",
#     "fixtures.available_plays_fixture",
#     "fixtures.cost_reduction_play_fixture",
#     "fixtures.design_review_fixture",
#     "fixtures.drawing_checker_both_play_fixture",
#     "fixtures.drawing_checker_v2_play_fixture",
#     "fixtures.drawing_checker_general_play_fixture",
#     "fixtures.drawing_checker_veeco_play_fixture",
#     "fixtures.tariff_analysis_play_fixture",
#     "fixtures.download_logs_fixture",
#     "fixtures.delete_file_fixture",
#     "fixtures.select_deselect_all_files_fixture",
#     "fixtures.filter_labels_fixture",
#     "fixtures.create_new_project_fixture",
#     "fixtures.export_credit_history_fixture",
#     "fixtures.export_classification_to_excel_fixture",
#     "fixtures.duplicate_admin_creation_fixture",
#     "fixtures.duplicate_user_creation_fixture",
#     "fixtures.systemadmin_creation_fixture",
#     "fixtures.duplicate_systemadmin_creation_fixture",
#     "fixtures.weight_estimation_play_fixture",
#     "fixtures.drawing_atlas_fixture",
#     "fixtures.drawing_intelligence_fixture",
#     "fixtures.organization_wide_search_fixture",
#     "fixtures.play_badges_on_file_card_fixture",
#     "fixtures.profile_picture_upload_fixture",
#     "fixtures.project_folder_sharing_fixture",
#     "fixtures.reports_builder_fixture"

# import pytest
# import sys
# import os
# from datetime import datetime

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# # Safe import for report plugin
# try:
#     import pytest_html
# except ImportError:
#     pytest_html = None


# # =========================
# # PATH SETUP
# # =========================
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, BASE_DIR)


# # =========================
# # CLI OPTIONS
# # =========================
# def pytest_addoption(parser):
#     parser.addoption("--browser", action="store", default="chrome")
#     parser.addoption("--headless", action="store_true", help="Run in headless mode")


# # =========================
# # SAFE DRIVER SETUP
# # =========================
# def get_driver_service():
#     try:
#         path = ChromeDriverManager().install()

#         # Fix for Windows chromedriver path issue
#         if "THIRD_PARTY_NOTICES" in path:
#             path = os.path.join(os.path.dirname(path), "chromedriver.exe")

#         return Service(path)

#     except Exception:
#         # Fallback (VERY IMPORTANT for Jenkins / offline)
#         local_path = os.path.join(BASE_DIR, "drivers", "chromedriver.exe")

#         if not os.path.exists(local_path):
#             raise Exception("Chromedriver not found locally or via webdriver-manager")

#         return Service(local_path)


# # =========================
# # BROWSER FIXTURE
# # =========================
# @pytest.fixture(scope="function")
# def browser(request):
#     browser_name = request.config.getoption("--browser")
#     headless = request.config.getoption("--headless")

#     if browser_name.lower() == "chrome":
#         chrome_options = Options()

#         if headless:
#             chrome_options.add_argument("--headless=new")

#         # Stability for Jenkins
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-dev-shm-usage")
#         chrome_options.add_argument("--disable-gpu")
#         chrome_options.add_argument("--window-size=1920,1080")

#         # Download directory setup
#         download_dir = os.path.join(BASE_DIR, "downloads")
#         os.makedirs(download_dir, exist_ok=True)

#         prefs = {
#             "download.default_directory": download_dir,
#             "download.prompt_for_download": False,
#             "download.directory_upgrade": True,
#             "safebrowsing.enabled": True,
#             "profile.default_content_setting_values.automatic_downloads": 1
#         }
#         chrome_options.add_experimental_option("prefs", prefs)

#         service = get_driver_service()
#         driver = webdriver.Chrome(service=service, options=chrome_options)

#     else:
#         raise Exception(f"Unsupported browser: {browser_name}")

#     driver.implicitly_wait(10)

#     yield driver

#     driver.quit()


# # =========================
# # SCREENSHOT + HTML REPORT
# # =========================
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()

#     if report.when == "call" and report.failed:
#         driver = item.funcargs.get("browser", None)

#         if driver:
#             screenshots_dir = os.path.join(BASE_DIR, "screenshots")
#             os.makedirs(screenshots_dir, exist_ok=True)

#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             file_name = f"{item.name}_{timestamp}.png"
#             file_path = os.path.join(screenshots_dir, file_name)

#             driver.save_screenshot(file_path)

#             # Attach screenshot to HTML report
#             if pytest_html:
#                 extra = getattr(report, "extra", [])
#                 extra.append(pytest_html.extras.image(file_path))
#                 report.extra = extra
