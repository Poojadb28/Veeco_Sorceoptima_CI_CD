import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException


class ProjectPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 280)

    def safe_click(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", element
        )
        self.driver.execute_script("arguments[0].click();", element)

    def wait_for_page_load(self):
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def click_projects(self):
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        projects = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space()='Projects']/ancestor::*[self::a or self::button][1]")
            )
        )
        self.safe_click(projects)
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def right_click_on_canvas(self):

        # Wait page fully loaded
        self.wait.until(
            lambda d: d.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        # Wait canvas/workspace present
        canvas = self.wait.until(
            lambda d: next(
                (
                    el for locator in [
                        (By.XPATH, "//div[contains(@class,'flex-1')]"),
                        (By.XPATH, "//main"),
                        (By.XPATH, "//div[contains(@class,'h-full') and .//*[normalize-space()='Projects']]")
                    ]
                    for el in d.find_elements(*locator)
                    if el.is_displayed()
                ),
                False
            )
        )

        # Wait canvas visible
        self.wait.until(
            EC.visibility_of(canvas)
        )

        # Wait canvas clickable/stable
        self.wait.until(lambda d: canvas.is_displayed() and canvas.size["height"] > 0)

        # Scroll to canvas
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            canvas
        )

        # Small stabilization pause
        time.sleep(1)


        # Right click
        ActionChains(self.driver)\
            .move_to_element(canvas)\
            .pause(1)\
            .context_click(canvas)\
            .perform()

        # Wait menu visible
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH,
                "//*[contains(text(),'New Root Space')]")
            )
        )


    def click_new_root_space(self):
        # Wait until context menu is visible
        menu = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//*[contains(text(),'New Root Space')]")
        ))

        for el in menu:
            if el.is_displayed():
                self.driver.execute_script("arguments[0].click();", el)
                return

        raise Exception("New Root Space option not found")


    def enter_space_name(self, name):
        field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@placeholder='e.g. Finance, Project Alpha...']")
            )
        )
        field.clear()
        field.send_keys(name)

    def open_icon_selector(self):
        icon_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//*[name()='svg' and contains(@class,'w-5')]]")))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", icon_button)
        self.driver.execute_script("arguments[0].click();", icon_button)

    def select_color(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Blue']"))).click()

    def click_create_space(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Create Space']"))).click()

    def get_success_message(self):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Space created successfully')]"))).text
    
   # ================= SUB SPACE ================= #

    def right_click_root_space(self, name):

        element = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//*[text()='{name}']")
            )
        )

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.driver).move_to_element(element).pause(1).context_click(element).perform()

        # IMPORTANT: wait for menu
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Edit')]")
            )
        )


    def click_add_sub_space(self):
        
        time.sleep(2)

        elements = self.driver.find_elements(By.XPATH, "//*[contains(text(),'Add Sub')]")

        for el in elements:
            if el.is_displayed():
                self.driver.execute_script("arguments[0].click();", el)
                return

        raise Exception("Add Sub Space option not found")


    def enter_sub_space_name(self, name):
        field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='e.g. Finance, Project Alpha...']")
        ))
        field.clear()
        field.send_keys(name)


    def choose_icon(self):
        icon = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[.//*[name()='svg']]")
        ))
        self.driver.execute_script("arguments[0].click();", icon)


    def select_color(self):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@title='Blue']")
        )).click()


    def click_create_space(self):
        btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Create Space']")
        ))
        self.driver.execute_script("arguments[0].click();", btn)


    def verify_sub_space_created(self, name):
        locator = (By.XPATH, f"//h4[normalize-space()='{name}']")
        return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
    
    # ================= DELETE ROOT SPACE ================= #
    def click_delete_space(self):
        
        time.sleep(2)

        elements = self.driver.find_elements(By.XPATH, "//*[contains(text(),'Delete')]")

        for el in elements:
            if el.is_displayed():
                self.driver.execute_script("arguments[0].click();", el)
                return

        raise Exception("Delete option not found")


    def confirm_delete_space(self):

        # wait for alert
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())

        print("Alert text:", alert.text)  

        alert.accept()  # click OK

    def verify_space_deleted(self, name):
        return self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, f"//div[contains(text(),'Space \"{name}\" deleted successfully')]")
        )).is_displayed()
    
    # ================= PROJECT ================= #

    def open_root_space(self, name):
        locator = (By.XPATH, f"//h4[normalize-space()='{name}']")
        element = self.wait.until(EC.visibility_of_element_located(locator))

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)


    def click_new_upload(self):
        btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='New Upload']")
        ))
        self.driver.execute_script("arguments[0].click();", btn)


    def enter_project_name(self, name):
        field = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Enter project name']")
        ))
        field.clear()
        field.send_keys(name)


    # def upload_file(self, file_path):

    #     file_path = os.path.abspath(file_path)

    #     upload = self.wait.until(EC.presence_of_element_located(
    #         (By.XPATH, "//input[@type='file']")
    #     ))

    #     # IMPORTANT for hidden input
    #     self.driver.execute_script("arguments[0].style.display='block';", upload)

    #     upload.send_keys(file_path)

    def upload_file(self, file_path):
        file_path = os.path.abspath(file_path)

        uploads = self.driver.find_elements(
            By.XPATH,
            "//input[@type='file']"
        )

        upload = uploads[-1]

        self.driver.execute_script(
            "arguments[0].style.display='block';",
            upload
        )

        upload.send_keys(file_path)


    def click_upload(self):
        btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Upload']")
        ))
        self.driver.execute_script("arguments[0].click();", btn)


    def create_project(self, name, file_path):
        self.click_new_upload()
        self.enter_project_name(name)
        self.upload_file(file_path)
        self.click_upload()


    def verify_project_created(self, name):
        locator = (By.XPATH, f"//h3[normalize-space()='{name}']")
        return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()

    
    
    # ================= FILE UPLOAD ================= #
    def open_project(self, project_name):

        locator = (By.XPATH, f"//h3[contains(text(),'{project_name}')]")

        # Step 1: Wait for page load
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        # Step 2: Wait until project appears in DOM
        self.wait.until(lambda d: project_name in d.page_source)

        # Step 3: Wait for visibility
        element = self.wait.until(EC.visibility_of_element_located(locator))

        # Step 4: Scroll to element
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", element
        )

        # Step 5: Wait until clickable
        self.wait.until(EC.element_to_be_clickable(locator))

        # Step 6: Try normal click first
        try:
            element.click()
        except:
            # Fallback for Jenkins/headless
            self.driver.execute_script("arguments[0].click();", element)

    def verify_file_uploaded(self, file_name):

        self.wait.until(lambda driver: len(
            driver.find_elements(By.XPATH, f"//*[contains(text(),'{file_name}')]")
        ) > 0)

        elements = self.driver.find_elements(
            By.XPATH,
            f"//*[contains(text(),'{file_name}')]"
        )

        return any(el.is_displayed() for el in elements)
    
    # ================= EDIT DETAILS ================= #
    def click_edit_details(self):

        elements = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//*[contains(text(),'Edit Details')]")
            )
        )

        for el in elements:
            if el.is_displayed():
                self.safe_click(el)
                break

        # wait for input field 
        self.wait.until(
            lambda d: len(d.find_elements(By.XPATH, "//input[@type='text']")) > 0
        )

    # def edit_space_name(self, new_name):

    #     inputs = self.wait.until(
    #         EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']"))
    #     )

    #     field = None

    #     for inp in inputs:
    #         if inp.is_displayed():
    #             field = inp
    #             break

    #     if not field:
    #         raise Exception("Edit input field not found")

    #     field.click()
    #     field.clear()
    #     field.send_keys(new_name)


    def edit_space_name(self, new_name):
        field = self.wait.until(
            lambda d: next(
                (
                    e for e in d.find_elements(
                        By.XPATH,
                        "//input[@type='text' and not(@placeholder='Search drawings...')]"
                    )
                    if e.is_displayed()
                ),
                None,
            )
        )

        field.clear()
        field.send_keys(new_name)


    def change_icon(self):
        icon = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[.//*[name()='svg']]")
        ))
        self.driver.execute_script("arguments[0].click();", icon)


    def select_purple_color(self):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@title='Purple']")
        )).click()


    def save_changes(self):
        
        # try multiple locators
        locators = [
            "//button[contains(text(),'Save')]",
            "//button[contains(text(),'Update')]",
            "//div[contains(@class,'z-50')]//button"
        ]

        for xpath in locators:
            buttons = self.driver.find_elements(By.XPATH, xpath)

            for btn in buttons:
                if btn.is_displayed():
                    self.driver.execute_script("arguments[0].click();", btn)

                    # wait for modal close
                    try:
                        self.wait.until(EC.invisibility_of_element_located(
                            (By.XPATH, "//div[contains(@class,'z-50')]")
                        ))
                    except:
                        pass

                    return

        raise Exception("Save button not found")

    def verify_space_updated(self, name):
        locator = (By.XPATH, f"//h4[normalize-space()='{name}']")
        return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
    
    #-------------------------Delete Project------------------------- #
    def wait_for_processing_complete(self):

        def processing_done(driver):
            blocking_text = driver.find_elements(
                By.XPATH,
                "//*[contains(translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'processing') "
                "or contains(translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'uploading')]"
            )

            try:
                visible_blocking_text = [
                    el for el in blocking_text
                    if el.is_displayed()
                ]
            except StaleElementReferenceException:
                return False

            if visible_blocking_text:
                return False

            upload_buttons = driver.find_elements(By.XPATH, "//button[normalize-space()='Upload']")
            try:
                visible_upload_buttons = [
                    btn for btn in upload_buttons
                    if btn.is_displayed()
                ]
            except StaleElementReferenceException:
                return False

            return len(visible_upload_buttons) == 0

        self.wait.until(processing_done)

    def click_delete_project(self):

        # try multiple locators (VERY IMPORTANT)
        locators = [
            "//button[@title='Delete project']",
            "//*[contains(@title,'Delete')]",
            "//*[contains(text(),'Delete')]"
        ]

        for xpath in locators:
            elements = self.driver.find_elements(By.XPATH, xpath)

            for el in elements:
                if el.is_displayed():
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});", el
                    )
        
                    self.driver.execute_script("arguments[0].click();", el)
                    return

        raise Exception("Delete button not found")

    def confirm_delete(self):
        confirm_input = (By.XPATH, "//input[@placeholder='Type DELETE to confirm']")
        delete_btn = (By.XPATH, "//button[normalize-space()='Delete']")

        self.wait.until(EC.visibility_of_element_located(confirm_input)).send_keys("DELETE")
        self.wait.until(EC.element_to_be_clickable(delete_btn)).click()

    def wait_for_delete_complete(self):
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//div[contains(text(),'Deleting project')]")
            )
        )
    def verify_project_deleted(self, project_name):
        elements = self.driver.find_elements(
            By.XPATH, f"//h3[contains(text(),'{project_name}')]"
        )
        return len(elements) == 0
    
#---------------------------Search File Fumctionality-------------------------#
    def search_file(self, name):
        search_input = (By.XPATH, "//input[@placeholder='Search filename...']")
        box = self.wait.until(
            EC.visibility_of_element_located(search_input)
        )
        box.clear()
        box.send_keys(name)


    def verify_file_present(self, name):

        locator = (By.XPATH, f"//*[contains(text(),'{name}')]")

        return self.wait.until(
            EC.visibility_of_element_located(locator)
        ).is_displayed()
    
  
#---------------------------Plays-------------------------#

    def select_all_files(self):

        select_all_btn = (By.XPATH, "//button[normalize-space()='Select All']")

        element = self.wait.until(EC.element_to_be_clickable(select_all_btn))

        # scroll for safety
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

        # click using JS (avoids overlay issues)
        self.driver.execute_script("arguments[0].click();", element)

# ================= DELETE FILE ================= #

# ================= DELETE CONFIRMATION LOCATORS ================= #

    confirm_delete_input = (By.XPATH, "//input[@placeholder='Type DELETE to confirm']")
    delete_button = (By.XPATH, "//button[normalize-space()='Delete']")

    def delete_file(self, file_name):

        file_locator = (By.XPATH, f"//*[contains(text(),'{file_name}')]")

        file_element = self.wait.until(
            EC.visibility_of_element_located(file_locator)
        )

        ActionChains(self.driver).move_to_element(file_element).perform()

        delete_icon = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//*[contains(text(),'{file_name}')]/ancestor::*//button[contains(@title,'Delete')]")
            )
        )

        self.driver.execute_script("arguments[0].click();", delete_icon)

        # Confirm delete
        confirm = self.wait.until(
            EC.visibility_of_element_located(self.confirm_delete_input)
        )
        confirm.clear()
        confirm.send_keys("DELETE")

        self.wait.until(
            EC.element_to_be_clickable(self.delete_button)
        ).click()

        # IMPORTANT: WAIT UNTIL FILE DISAPPEARS
        self.wait.until(
            EC.invisibility_of_element_located(file_locator)
        )


    def is_file_deleted(self, file_name):

        elements = self.driver.find_elements(
            By.XPATH, f"//*[contains(text(),'{file_name}')]"
        )

        return len(elements) == 0
    
    # ================= VERIFY BUTTONS ================= #
    def deselect_all_files(self):

        deselect_all_button = (By.XPATH, "//button[normalize-space()='Deselect All']")

        element = self.wait.until(EC.element_to_be_clickable(deselect_all_button))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", element
        )

        self.driver.execute_script("arguments[0].click();", element)

    def verify_deselect_visible(self):

        return self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[normalize-space()='Deselect All']")
            )
        ).is_displayed()


    def verify_select_visible(self):

        return self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[normalize-space()='Select All']")
            )
        ).is_displayed()
    
    # ================= FILTER ================= #

    def get_filter_dropdown(self):

        filter_dropdown = (By.XPATH, "//select[contains(@class,'text-sm')]")

        return self.wait.until(
            EC.visibility_of_element_located(filter_dropdown)
        )


    def apply_filter(self, label_text):

        dropdown = self.get_filter_dropdown()

        # wait until dropdown is enabled
        self.wait.until(lambda d: dropdown.is_enabled())

        self.driver.execute_script(
            """
            const select = arguments[0];
            const label = arguments[1];

            for (let option of select.options) {
                if (option.text.includes(label)) {
                    select.value = option.value;
                    select.dispatchEvent(new Event('change', { bubbles: true }));
                    return;
                }
            }
            """,
            dropdown,
            label_text
        )

        # IMPORTANT: wait for filter effect (UI refresh)
        self.wait.until(lambda d: dropdown.get_attribute("value") is not None)

        # small stability wait (React rendering)
        time.sleep(5)



    def clear_filter(self):

        try:
            clear_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@title='Clear filter']")
                )
            )

            self.driver.execute_script("arguments[0].click();", clear_btn)

            # wait until dropdown resets
            dropdown = self.get_filter_dropdown()

            self.wait.until(lambda d: dropdown.get_attribute("value") == "" or dropdown.get_attribute("value") is None)

            time.sleep(2)

        except:
            pass

    # ================= EXPORT CLASSIFICATION ================= #

    export_classification_btn = (By.XPATH, "//button[contains(text(),'Export Classification')]")

    def click_export_classification(self):

        btn = self.wait.until(
            EC.element_to_be_clickable(self.export_classification_btn)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", btn
        )

        
        time.sleep(1)

        self.driver.execute_script("arguments[0].click();", btn)


    def wait_for_classification_download(self, download_dir, timeout=60):

        end_time = time.time() + timeout

        while time.time() < end_time:

            files = os.listdir(download_dir)

            for f in files:
                file_lower = f.lower()

                if (
                    "classification" in file_lower
                    and file_lower.endswith(".xlsx")
                    and not file_lower.endswith((".crdownload", ".tmp"))
                ):
                    print("Downloaded:", f)
                    return True

            time.sleep(1)

        raise Exception("Classification file not downloaded")

    # ================= Organization wide search ================= #

    def take_screenshot(self, file_path):
        self.driver.save_screenshot(file_path)


    # Organization page
    def click_back_to_organization(self):
        locator = (By.XPATH, "//button[@title='Back to Organization']")

        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        self.driver.execute_script("arguments[0].click();", element)


    # Project page
    def click_back_to_projects(self):
        locator = (
            By.XPATH,
            "//button[contains(.,'Back to Projects')]"
        )

        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        self.driver.execute_script("arguments[0].click();", element)


    def search_organization(self, name):
        search = (
            By.XPATH,
            "//input[@placeholder='Search drawings...']"
        )

        box = self.wait.until(
            EC.visibility_of_element_located(search)
        )

        box.clear()
        box.send_keys(name)


    def verify_search_result(self, text):
        locator = (
            By.XPATH,
            f"//*[contains(text(),'{text}')]"
        )

        return self.wait.until(
            EC.visibility_of_element_located(locator)
        ).is_displayed()


    def click_search_result(self, text):
        locator = (
            By.XPATH,
            f"(//*[contains(text(),'{text}')])[1]"
        )

        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

    #---------------------------SHARE PROJECT-------------------------#

    # Click on 3 dots
    def click_on_3_dots(self):
        three_dots_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class,'rounded-lg') and .//*[name()='svg' and @viewBox='0 0 192 512']]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            three_dots_button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            three_dots_button
        )
        
    def click_share_project(self):
        # Wait for the share button to be clickable   
        share_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='flex items-center gap-2 w-full px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors']")
            )
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", share_button)
        self.driver.execute_script("arguments[0].click();", share_button)

    def enter_email_to_share(self, email):
        email_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@placeholder='Search by name or email...']")
            )
        )
        email_input.clear()
        email_input.send_keys(email)

    def click_share_button(self):
        share_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit' and normalize-space()='Share']")
            )
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", share_button)
        self.driver.execute_script("arguments[0].click();", share_button)

    def close_share_dialog(self):

        close_btn = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[name()='path' and contains(@d,'M242.72 256')]/ancestor::button"
                )
            )
        )

        self.driver.execute_script("arguments[0].click();", close_btn)

    # Logout method
    def click_logout(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Logout']"))).click()

    #---------------------------Reports Builder-------------------------#
    def click_reports_builder(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Reports']"))).click()

    def click_start_building(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Start Building →')]"))).click()

    #choose data which you want to include in the report
    def select_specific_space_path(self):
        radio = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[@type='radio' and @value='spaces']"
                )
            )
        )

        self.driver.execute_script("arguments[0].click();", radio)

    #click on checkbox which rootspace created now
    def select_root_space_for_report(self, root_space_name):

        checkbox_locator = (
            By.XPATH,
            f"//span[normalize-space()='{root_space_name}']/preceding-sibling::input[@type='checkbox']"
        )

        checkbox = self.wait.until(
            EC.element_to_be_clickable(checkbox_locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            checkbox
        )

        self.driver.execute_script(
            "arguments[0].click();",
            checkbox
        )

    #click on next preview button
    def click_next_preview(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next: Preview →')]"))).click()

    #Select the columns which you want to include in the report
    def select_columns_for_report(self, column_name):

        label = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//span[contains(normalize-space(),'{column_name}')]/ancestor::label"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            label
        )

        self.driver.execute_script(
            "arguments[0].click();",
            label
        )

    #click on save template button
    def click_save_template(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save Template']"))).click()

    # Enter the template name
    def enter_template_name(self, template_name):

        template_input = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[@placeholder='e.g., Monthly Tariff Summary']"
                )
            )
        )

        template_input.clear()
        template_input.send_keys(template_name)


    # Enter the template description
    def enter_template_description(self, template_description):

        description_input = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//textarea[@placeholder='What is this report for?']"
                )
            )
        )

        description_input.clear()
        description_input.send_keys(template_description)

    #click on save button to save the template
    def click_save_template_button(self):
        button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[@class='px-4 py-2 bg-teal-700 text-white text-sm font-medium rounded-lg hover:bg-teal-800 transition-colors']"
                )
            )
        )

        self.driver.execute_script("arguments[0].click();", button)

    # def wait_for_toast_to_disappear(self):

    #     self.wait.until(
    #     EC.invisibility_of_element_located(
    #         (
    #             By.XPATH,
    #             "//*[contains(@class,'Toastify__toast')]"
    #         )
    #     )
    # )
        
    def close_toast(self):
        try:
            close_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class,'Toastify__close-button')]")
                )
            )
            close_btn.click()
        except:
            pass

    #Click on export button to export the report
    def click_export_report(self):

        button = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Export']")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

    #click on excel option to export the report in excel format
    def click_export_excel(self):

        excel = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Excel (.xlsx)']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            excel
        )

    # ================= EXCEL DOWNLOAD ================= #

    # def wait_for_excel_download(self, download_dir, timeout=60):

    #     end_time = time.time() + timeout

    #     while time.time() < end_time:

    #         files = os.listdir(download_dir)

    #         for file in files:
    #             if (
    #                 file.endswith(".xlsx")
    #                 and not file.endswith(".crdownload")
    #             ):
    #                 print("Excel downloaded:", file)
    #                 return True

    #         time.sleep(1)

    #     raise Exception("Excel report was not downloaded")

    def wait_for_excel_download(self, download_dir, timeout=60):

        os.makedirs(download_dir, exist_ok=True)

        end_time = time.time() + timeout

        while time.time() < end_time:
            files = os.listdir(download_dir)

            for file in files:
                if file.endswith(".xlsx") and not file.endswith(".crdownload"):
                    return True

        raise Exception("Excel report was not downloaded")


    #click on csv option to export the report in csv format
    def click_export_csv(self):

        csv = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='CSV (.csv)']")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            csv
        )

    # ================= CSV DOWNLOAD ================= #

    # def wait_for_csv_download(self, download_dir, timeout=60):

    #     end_time = time.time() + timeout

    #     while time.time() < end_time:

    #         files = os.listdir(download_dir)

    #         for file in files:
    #             if (
    #                 file.endswith(".csv")
    #                 and not file.endswith(".crdownload")
    #             ):
    #                 print("CSV downloaded:", file)
    #                 return True

    #         time.sleep(1)

    #     raise Exception("CSV report was not downloaded")

    def wait_for_csv_download(self, download_dir, timeout=60):

        os.makedirs(download_dir, exist_ok=True)

        end_time = time.time() + timeout

        while time.time() < end_time:
            files = os.listdir(download_dir)

            for file in files:
                if file.endswith(".csv") and not file.endswith(".crdownload"):
                    return True

        raise Exception("CSV report was not downloaded")

    #assert success message after template saved successfully
    def verify_template_saved_successfully(self):
        success_message = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Template saved!')]")))
        return success_message.is_displayed()

        