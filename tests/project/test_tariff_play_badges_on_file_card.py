import os
import time


def test_tariff_play_badges_on_file_card(play_badges_on_file_card):

    tariff = play_badges_on_file_card

    download_dir = os.path.abspath("downloads")
    os.makedirs(download_dir, exist_ok=True)

    # Export BOM
    tariff.export_bom(download_dir)

    bom_files = [
        f for f in os.listdir(download_dir)
        if f.endswith(".xlsx") and not f.endswith(".crdownload")
    ]

    assert len(bom_files) > 0, "BOM file not downloaded"

    # Approve BOM
    tariff.approve_bom()

    # Complete Wizard
    tariff.complete_hts_wizard()
    tariff.wait_for_processing_complete()

    # Export Tariff
    tariff.export_tariff(download_dir)

    tariff_files = [
        f for f in os.listdir(download_dir)
        if "tariff" in f.lower() and f.endswith(".xlsx")
    ]

    assert len(tariff_files) > 0, "Tariff file not downloaded"

    # Go back to File Card
    tariff.go_back()

    time.sleep(5)  

    # # Wait until File Card is visible (adjust locator as needed)
    # tariff.wait.until(
    #     lambda d: "Tariff" in d.page_source or "Projects" in d.page_source
    # )

    os.makedirs("screenshots", exist_ok=True)

    screenshot_path = os.path.join(
        "screenshots",
        f"file_card_with_badges_{int(time.time())}.png"
    )

    tariff.take_screenshot(screenshot_path)

    assert os.path.exists(screenshot_path), "Screenshot not captured"
    assert os.path.getsize(screenshot_path) > 0, "Screenshot is empty"