import pytest
import os


@pytest.mark.smoke
def test_download_logs(download_logs):

    download_dir, file_prefix = download_logs

    files = sorted([
        f for f in os.listdir(download_dir)
        if f.startswith(file_prefix) and not f.endswith((".crdownload", ".tmp"))
    ])

    # Flexible assertion (handles real scenarios)
    assert len(files) >= 4, f"Expected logs missing. Found {len(files)}"

    # Validate file integrity
    for file in files:
        file_path = os.path.join(download_dir, file)

        assert os.path.exists(file_path), f"{file} not found"
        assert os.path.getsize(file_path) > 0, f"{file} is empty"