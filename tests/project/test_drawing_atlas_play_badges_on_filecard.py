import pytest
import time
import os


@pytest.mark.regression
def test_drawing_atlas_play_badges_on_file_card(drawing_atlas_play):

    drawing = drawing_atlas_play

    download_dir = os.path.abspath("downloads")
    os.makedirs(download_dir, exist_ok=True)

    drawing.click_view_results()

    # Wait page fully loaded
    drawing.wait.until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )
    
    time.sleep(5) 

    screenshot_path = drawing.take_screenshot("Drawing_Atlas_Play_Badge.png")

    assert os.path.exists(screenshot_path)
    assert os.path.getsize(screenshot_path) > 0