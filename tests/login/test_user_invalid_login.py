import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.smoke
def test_user_invalid_login(invalid_user_login):
    error_msg = invalid_user_login.get_error_message()

    assert "Invalid password. Please try again." in error_msg