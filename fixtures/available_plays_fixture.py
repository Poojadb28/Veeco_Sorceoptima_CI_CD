import pytest
from pages.systemadmin_login_page import LoginPage
from pages.systemadmin_page import SystemAdminPage



@pytest.fixture
def available_plays(browser):
    login = LoginPage(browser)
    login.login("prekshita@sourceoptima.com", "aspl1234")

    admin = SystemAdminPage(browser)

    admin.open_user_admin()
    admin.go_to_available_plays()

    play_name = [
        "Tariff Analysis",
        "Cost Reduction Analysis",
        "Design Review",
        "Drawing Checker - Both",
        "Drawing Checker - Veeco",
        "Drawing Checker - General",
        "Drawing Checker V2",
        "Weight Estimation",
        "Drawing Atlas"
    ]

    return admin, play_name

