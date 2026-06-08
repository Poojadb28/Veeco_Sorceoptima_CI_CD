import pytest
import os
from datetime import datetime

from pages.systemadmin_login_page import LoginPage
from pages.system_stats_page import SystemStatsPage


@pytest.fixture
def download_logs(browser):

    login = LoginPage(browser)
    login.login("prekshita@sourceoptima.com", "aspl1234")

    system_stats = SystemStatsPage(browser)

    # SAME folder as browser
    download_dir = os.path.abspath("downloads")

    today_date = datetime.today().strftime("%Y-%m-%d")
    file_prefix = f"sourceoptima_logs_{today_date}"

    time_ranges = [
        system_stats.time_range_today,
        system_stats.time_range_2_days,
        system_stats.time_range_3_days,
        system_stats.time_range_5_days,
        system_stats.time_range_7_days
    ]

    for time_range in time_ranges:
        system_stats.select_time_range(time_range)
        system_stats.download_logs_for_range(download_dir)

    return download_dir, file_prefix