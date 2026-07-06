import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.smoke
def test_system_admin_login(system_admin_login):
    browser = system_admin_login
    wait = WebDriverWait(browser, 20)

    expected_url = "https://testing-so.sourceoptima.com/system-admin"
    wait.until(EC.url_to_be(expected_url))

    assert browser.current_url == expected_url