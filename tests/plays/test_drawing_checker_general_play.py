import pytest
import os
import time


@pytest.mark.regression
def test_drawing_checker_general_play(drawing_checker_general_play):

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
