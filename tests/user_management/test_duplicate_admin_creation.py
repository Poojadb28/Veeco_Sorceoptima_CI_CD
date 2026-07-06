import pytest


@pytest.mark.smoke
def test_duplicate_admin_creation(duplicate_admin_creation):

    user_page, email = duplicate_admin_creation

    # -------- TRY DUPLICATE --------
    user_page.click_create_user()

    user_page.enter_full_name("duplicate_user")
    user_page.enter_email(email)   
    user_page.enter_password("aspl@1234")
    user_page.enter_confirm_password("aspl@1234")
    user_page.select_user_role("Admin")
    user_page.submit_user()

    error_msg = user_page.get_duplicate_error()

    assert "user with this Email already exists." in error_msg