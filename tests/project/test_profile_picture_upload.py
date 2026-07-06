# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


# def test_profile_picture_upload(profile_picture_upload_fixture):

#     browser = profile_picture_upload_fixture

#     profile_image = WebDriverWait(browser, 20).until(
#         EC.visibility_of_element_located(
#             (
#                 By.XPATH,
#                 "//img"
#             )
#         )
#     )

#     assert profile_image.is_displayed()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_profile_picture_upload(profile_picture_upload_fixture):

    browser = profile_picture_upload_fixture

    # Example: verify a success message
    success = WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//*[contains(text(),'Profile picture updated') or contains(text(),'Profile updated')]"
            )
        )
    )

    assert success.is_displayed()