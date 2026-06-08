import pytest
import os
import time


@pytest.mark.regression
def test_drawing_checker_v2_play(drawing_checker_v2_play):

    v2, main_window = drawing_checker_v2_play

    download_dir = os.path.abspath("downloads")
    os.makedirs(download_dir, exist_ok=True)

    # ================= SEARCH =================
    v2.search_issue("major")
    v2.clear_search()

    # ================= FILTER =================
    v2.filter_by_severity("Critical")
    v2.filter_by_severity("All Severities")

    v2.filter_by_source("General Engineering")
    v2.filter_by_source("All Sources")

    # ================= DRILLDOWN =================
    time.sleep(2)
    v2.click_drilldown()

    # ================= DOWNLOAD =================
    v2.download_report(download_dir)

    # ================= CLOSE =================
    driver = v2.driver
    driver.close()
    driver.switch_to.window(main_window)
