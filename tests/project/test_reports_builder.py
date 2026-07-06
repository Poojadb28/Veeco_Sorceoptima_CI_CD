import os
import time


def test_reports_builder(reports_builder_fixture):

    project = reports_builder_fixture

    download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    # Save Template
    template_name = f"Template_{int(time.time())}"

    project.click_save_template()
    project.enter_template_name(template_name)
    project.enter_template_description("Automation Report Template")
    project.click_save_template_button()

    #assert that the template is saved successfully
    assert project.verify_template_saved_successfully(), "Template saved!"

    # # Wait until the toast disappears
    # project.wait_for_toast_to_disappear()

    project.close_toast()

    # Export Excel
    project.click_export_report()
    project.click_export_excel()
    project.wait_for_excel_download(download_dir)

    # Verify that the Excel file is downloaded
    excel_files = [
        f for f in os.listdir(download_dir)
        if f.endswith(".xlsx")
    ]
    assert excel_files, "Excel file not found"

    # Export CSV
    project.click_export_report()
    project.click_export_csv()
    project.wait_for_csv_download(download_dir)

    # Verify that the CSV file is downloaded
    csv_files = [
        f for f in os.listdir(download_dir)
        if f.endswith(".csv")
    ]
    assert csv_files, "CSV file not found"