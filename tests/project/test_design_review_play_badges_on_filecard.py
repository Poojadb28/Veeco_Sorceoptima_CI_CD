import pytest
import os
import time

@pytest.mark.regression
def test_design_review_play_badges_on_file_card(design_review_play):

    design = design_review_play

    download_dir = os.path.abspath("downloads")
    os.makedirs(download_dir, exist_ok=True)

    design.click_view_results()

    # Wait page fully loaded
    design.wait.until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )
    
    time.sleep(5) 

    screenshot_path = design.take_screenshot("Design_Review_Play_Badge.png")

    assert os.path.exists(screenshot_path)
    assert os.path.getsize(screenshot_path) > 0