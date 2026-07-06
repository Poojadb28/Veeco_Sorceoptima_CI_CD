import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.smoke
def test_system_admin_invalid_login(invalid_login):
    error_msg = invalid_login.get_error_message()

    assert "Invalid password. Please try again." in error_msg
