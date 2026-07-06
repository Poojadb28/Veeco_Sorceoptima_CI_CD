import pytest

def test_organization_wide_search(organization_wide_search_fixture):
    (
        project,
        project_name,
        file_name,
        project_screenshot,
        file_screenshot,
    ) = organization_wide_search_fixture

    assert project_screenshot is not None
    assert file_screenshot is not None