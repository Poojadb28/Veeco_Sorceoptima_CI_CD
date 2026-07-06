import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.smoke
def test_admin_invalid_login(invalid_admin_login):
    error_msg = invalid_admin_login.get_error_message()

    assert "Invalid password. Please try again." in error_msg