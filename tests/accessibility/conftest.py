import pytest
import datetime
import pathlib

report_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Create a directory to store accessibility reports
accessibility_dir = pathlib.Path("accessibility_reports")
accessibility_dir.mkdir(exist_ok=True)
_accessibility_reports = pathlib.Path(f"{report_time}_accessibility_page_results")
accessibility_reports = (accessibility_dir / _accessibility_reports)
accessibility_reports.mkdir()

# Create a file to store accessibility snapshots
_accessibility_snapshots = pathlib.Path(f"{report_time}_accessibility_page_snapshot.json")
accessibility_snapshots = accessibility_dir/_accessibility_snapshots
accessibility_snapshots.touch(exist_ok=True)


@pytest.fixture(scope="session")
def accessibility_reports():
    return accessibility_reports

@pytest.fixture(scope="session")
def accessibility_snapshots():
    return accessibility_snapshots