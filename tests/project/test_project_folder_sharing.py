import os
import pytest


@pytest.mark.regression
def test_project_folder_sharing(project_folder_sharing_fixture):

    project = project_folder_sharing_fixture

    screenshot_path = os.path.join(
        "screenshots",
        "project_shared_success.png"
    )

    # Verify screenshot captured
    assert os.path.exists(screenshot_path), \
        "Project sharing screenshot was not captured."

    assert os.path.getsize(screenshot_path) > 0, \
        "Project sharing screenshot is empty."