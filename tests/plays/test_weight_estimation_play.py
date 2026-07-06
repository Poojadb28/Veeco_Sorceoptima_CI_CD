import os
import pytest


@pytest.mark.regression
def test_weight_estimation_play(weight_estimation_play):

    weight_estimation = weight_estimation_play

    weight_estimation.click_view_results()

    weight_estimation.click_view_details()

    weight_estimation.wait_for_report_tab()

    weight_estimation.open_report_tab()

    # Wait page fully loaded
    weight_estimation.wait.until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )

    # cost.take_screenshot()

    screenshot_path = weight_estimation.take_screenshot("Weight_Estimation_Report.png")

    assert os.path.exists(screenshot_path)
    assert os.path.getsize(screenshot_path) > 0
    
    weight_estimation.close_popup()

   