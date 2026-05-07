import pytest


@pytest.mark.smoke
def test_create_systemadmin(create_systemadmin):

    success_msg = create_systemadmin.get_success_message()

    assert "User created successfully" in success_msg