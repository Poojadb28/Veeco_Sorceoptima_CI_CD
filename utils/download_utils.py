import os
import time


def wait_for_new_file(download_dir, before_files, extension=None, timeout=60):
    
    end_time = time.time() + timeout

    while time.time() < end_time:

        after_files = set(os.listdir(download_dir))
        new_files = after_files - before_files

        # Filter completed files
        completed_files = [
            f for f in new_files
            if not f.endswith(".crdownload") and not f.endswith(".tmp")
        ]

        if extension:
            completed_files = [f for f in completed_files if f.endswith(extension)]

        if completed_files:
            file_path = os.path.join(download_dir, completed_files[0])

            # Ensure file exists (avoid FileNotFoundError)
            if not os.path.exists(file_path):
                time.sleep(1)
                continue

            # Ensure file is fully written (size stable)
            try:
                size1 = os.path.getsize(file_path)
                time.sleep(1)
                size2 = os.path.getsize(file_path)
            except FileNotFoundError:
                continue

            if size1 == size2:
                return file_path

        time.sleep(1)

    raise Exception("Download did not complete")
