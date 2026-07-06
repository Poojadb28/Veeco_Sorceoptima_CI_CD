import pytest
import os
import time


@pytest.mark.regression
def test_drawing_checker_general_play_badges_on_file_card(drawing_checker_general_play):

    general, main_window = drawing_checker_general_play

    download_dir = os.path.abspath("downloads")
    os.makedirs(download_dir, exist_ok=True)

    # ================= SEARCH =================
    general.search_issue("major")
    general.clear_search()

    # ================= FILTER =================
    general.filter_by_severity("Critical")
    general.filter_by_severity("All Severities")

    general.filter_by_source("General Engineering")
    general.filter_by_source("All Sources")

    # ================= DRILLDOWN =================
    time.sleep(2)
    general.click_drilldown()

    # ================= DOWNLOAD =================
    general.download_report(download_dir)

    # ================= CLOSE =================
    driver = general.driver
    driver.close()
    driver.switch_to.window(main_window)

    # Wait page fully loaded
    general.wait.until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )
    
    time.sleep(5) 

    screenshot_path = general.take_screenshot("Drawing_Checker_General_Play_Badge.png")

    assert os.path.exists(screenshot_path)
    assert os.path.getsize(screenshot_path) > 0
