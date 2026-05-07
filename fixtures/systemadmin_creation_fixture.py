import time
import pytest

from pages.systemadmin_login_page import LoginPage
from pages.user_admin_page import UserAdminPage


@pytest.fixture
def create_systemadmin(browser):

    login = LoginPage(browser)
    login.login("prekshita@sourceoptima.com", "aspl1234")

    user_page = UserAdminPage(browser)

    user_page.click_user_admin_view()

    # Cancel validation
    user_page.click_create_user()
    user_page.click_cancel()

    # Create admin
    user_page.click_create_user()

    timestamp = str(int(time.time()))

    user_page.enter_full_name(f"test_systemadmin_{timestamp}")
    user_page.enter_email(f"test_{timestamp}@aspl.ai")
    user_page.enter_password("aspl@1234")
    user_page.enter_confirm_password("aspl@1234")

    user_page.select_user_role("System Administrator")

    user_page.submit_user()

    return user_page