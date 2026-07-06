import os
import pytest


@pytest.mark.regression
def test_cost_reduction_play(cost_reduction_play):

    cost = cost_reduction_play

    # =========================
    # VALIDATION FLOW
    # =========================
    cost.click_view_results()
    cost.click_view_details()
    cost.open_report_tab()
    

    # Wait page fully loaded
    cost.wait.until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )

    # cost.take_screenshot()

    screenshot_path = cost.take_screenshot("Cost_Reduction_Report.png")

    assert os.path.exists(screenshot_path)
    assert os.path.getsize(screenshot_path) > 0
    
    cost.close_popup()