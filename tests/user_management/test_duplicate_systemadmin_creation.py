import pytest


@pytest.mark.smoke
def test_duplicate_systemadmin_creation(duplicate_systemadmin_creation):

    user_page, email = duplicate_systemadmin_creation

    # -------- TRY DUPLICATE --------
    user_page.click_create_user()

    user_page.enter_full_name("duplicate_systemadmin")
    user_page.enter_email(email)   
    user_page.enter_password("aspl@1234")
    user_page.enter_confirm_password("aspl@1234")
    user_page.select_user_role("System Administrator")
    user_page.submit_user()

    error_msg = user_page.get_duplicate_error()

    assert "Failed to create user" in error_msg