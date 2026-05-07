import pytest
import time

from pages.systemadmin_login_page import LoginPage
from pages.user_admin_page import UserAdminPage


@pytest.fixture
def duplicate_systemadmin_creation(browser):

    login = LoginPage(browser)
    login.login("prekshita@sourceoptima.com", "aspl1234")

    user_page = UserAdminPage(browser)

    user_page.click_user_admin_view()

    # -------- CREATE FIRST USER --------
    user_page.click_create_user()

    timestamp = str(int(time.time()))
    email = f"test_systemadmin_{timestamp}@aspl.ai"

    user_page.enter_full_name(f"systemadmin_{timestamp}")
    user_page.enter_email(email)
    user_page.enter_password("aspl@1234")
    user_page.enter_confirm_password("aspl@1234")
    user_page.select_user_role("System Administrator")
    user_page.submit_user()

    # Wait until success toast fully appears
    success_msg = user_page.get_success_message()

    assert "User created successfully" in success_msg

    return user_page, email