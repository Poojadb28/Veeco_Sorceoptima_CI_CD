import pytest


@pytest.mark.regression
def test_weight_estimation_play(weight_estimation_play):

    weight_estimation = weight_estimation_play

    weight_estimation.click_view_results()

    weight_estimation.click_view_details()

    weight_estimation.wait_for_report_tab()

    weight_estimation.open_report_tab()

    # Wait report fully loaded
    weight_estimation.wait_for_report_loaded()

    weight_estimation.take_screenshot()

    weight_estimation.close_popup()