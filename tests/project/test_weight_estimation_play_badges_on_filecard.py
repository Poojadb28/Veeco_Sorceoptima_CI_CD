import pytest
import time
import os

@pytest.mark.regression
def test_weight_estimation_play_badges_on_filecard(weight_estimation_play):

    weight_estimation = weight_estimation_play

    weight_estimation.click_view_results()
    
    # Wait page fully loaded
    weight_estimation.wait.until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )
    
    time.sleep(5) 

    screenshot_path = weight_estimation.take_screenshot("Weight_Estimation_Play_Badge.png")

    assert os.path.exists(screenshot_path)
    assert os.path.getsize(screenshot_path) > 0