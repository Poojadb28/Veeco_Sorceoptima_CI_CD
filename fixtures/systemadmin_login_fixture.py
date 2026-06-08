import pytest
from pages.systemadmin_login_page import LoginPage

@pytest.fixture
def system_admin_login(browser):
    login = LoginPage(browser)
    login.login("prekshita@sourceoptima.com", "aspl1234")
    return browser

# Systemadmin Invalid Login Fixture
@pytest.fixture
def invalid_login(browser):
    login = LoginPage(browser)
    login.open_url()
    login.click_login()
    login.enter_email("pooja@gmail")  
    login.enter_password("aspl@1234")
    login.click_submit()
    return login

#  VALID ADMIN LOGIN
@pytest.fixture
def admin_login(browser):
    login = LoginPage(browser)
    login.login("poojagowda@gmail.com", "aspl@1234")
    return browser


# INVALID ADMIN LOGIN
@pytest.fixture
def invalid_admin_login(browser):
    login = LoginPage(browser)
    login.open_url()
    login.click_login()
    login.enter_email("poojagowda@gmail.com")   # valid email
    login.enter_password("aspl")       # invalid password
    login.click_submit()
    return login

# VALID USER LOGIN
@pytest.fixture
def user_login(browser):
    login = LoginPage(browser)
    login.login("poojadb1147@aspl.ai", "aspl@1234")
    # login.login("user3@gmail.com", "aspl@1234")
    return browser


# INVALID USER LOGIN
@pytest.fixture
def invalid_user_login(browser):
    login = LoginPage(browser)
    login.open_url()
    login.click_login()
    login.enter_email("poojadb1147@aspl.ai")   # valid email
    login.enter_password("aspl")       # invalid password
    login.click_submit()
    return login