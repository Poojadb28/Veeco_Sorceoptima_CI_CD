import pytest
import os


@pytest.mark.regression
def test_drawing_atlas_play(drawing_atlas_play):

    drawing = drawing_atlas_play

    download_dir = os.path.abspath("downloads")
    os.makedirs(download_dir, exist_ok=True)

    drawing.click_view_results()
    drawing.click_view_details()
    drawing.open_report_tab()

    drawing.download_report(download_dir)

    drawing.close_popup()