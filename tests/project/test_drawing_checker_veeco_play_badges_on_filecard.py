import pytest
import os
import time


@pytest.mark.regression
def test_drawing_checker_veeco_play(drawing_checker_veeco_play):

    veeco, main_window = drawing_checker_veeco_play

    download_dir = os.path.abspath("downloads")
    os.makedirs(download_dir, exist_ok=True)

    # ================= SEARCH =================
    veeco.search_issue("minor")
    veeco.clear_search()

    # ================= FILTER =================
    veeco.filter_by_severity("Major")
    veeco.filter_by_severity("All Severities")

    veeco.filter_by_source("Veeco Standards")
    veeco.filter_by_source("All Sources")

    # ================= DRILLDOWN =================
    time.sleep(2)
    veeco.click_drilldown()

    # ================= DOWNLOAD =================
    veeco.download_report(download_dir)

    # ================= CLOSE =================
    driver = veeco.driver
    driver.close()
    driver.switch_to.window(main_window)

    # Wait page fully loaded
    veeco.wait.until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )
    
    time.sleep(5) 

    screenshot_path = veeco.take_screenshot("Drawing_Checker_Veeco_Play_Badge.png")

    assert os.path.exists(screenshot_path)
    assert os.path.getsize(screenshot_path) > 0
