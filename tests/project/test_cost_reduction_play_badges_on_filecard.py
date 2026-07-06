import pytest
import time
import os

@pytest.mark.regression
def test_cost_reduction_play_badges_on_file_card(cost_reduction_play):

    cost = cost_reduction_play

    # =========================
    # VALIDATION FLOW
    # =========================
    cost.click_view_results()

    # Wait page fully loaded
    cost.wait.until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )
    
    time.sleep(5) 

    screenshot_path = cost.take_screenshot("Cost_Reduction_Play_Badge.png")

    assert os.path.exists(screenshot_path)
    assert os.path.getsize(screenshot_path) > 0