import pytest
import os


@pytest.mark.regression
def test_drawing_checker_both_play(drawing_checker_both_play):

    drawing, main_window = drawing_checker_both_play

    download_dir = os.path.abspath("downloads")
    os.makedirs(download_dir, exist_ok=True)

    # ================= SEARCH =================
    drawing.search_issue("minor")
    drawing.clear_search()

    # ================= FILTER =================
    drawing.filter_by_severity("Critical")
    drawing.filter_by_severity("All Severities")

    drawing.filter_by_source("Veeco Standards")
    drawing.filter_by_source("All Sources")

    # ================= DRILLDOWN =================
    drawing.click_drilldown()

    # ================= DOWNLOAD =================
    drawing.download_report(download_dir)

    # ================= CLOSE TAB =================
    driver = drawing.driver
    driver.close()
    driver.switch_to.window(main_window)