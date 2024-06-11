from playwright.sync_api import Page
from axe_playwright_python.sync_playwright import Axe
import pytest
import datetime
import pathlib

report_time = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

axe = Axe()

def pytest_addoption(parser):
    parser.addoption(
        "--a11y-count", action="store", default=0, help="Number of accessibility violations to allow"
    )


@pytest.fixture(scope="function", autouse=True)
def run_a11y_test(request, pytestconfig, page: Page):
    """Run accessibility tests on the last page and store results in a file"""
    # Create a directory to store accessibility reports
    accessibility_dir = pathlib.Path("test-results/accessibility_reports")
    accessibility_dir.mkdir(exist_ok=True, parents=True)
    _accessibility_reports = pathlib.Path(f"{report_time}_accessibility_page_results")
    accessibility_reports = accessibility_dir / _accessibility_reports
    accessibility_reports.mkdir()

    # Create a file to store accessibility snapshots
    _accessibility_snapshots = pathlib.Path(f"{report_time}_accessibility_page_snapshot.json")
    accessibility_snapshots = accessibility_dir/_accessibility_snapshots
    accessibility_snapshots.touch(exist_ok=True)

    axe_results = axe.run(page)
    report_path = accessibility_reports / pathlib.Path(f"{request.node.name}.txt")
    report_path.write_text(axe_results.generate_report())
    snapshot_path = accessibility_snapshots
    with open (snapshot_path, "a") as file:
        file.write(f"Page: {request.node.name}\n")
        file.write(axe_results.generate_snapshot())
        file.write("\n----------------\n")
    
    yield
    
    axe_results = axe.run(page)

    if axe_results.violations_count > pytestconfig.getoption("--a11y-count"):
        # fail the test if the number of violations is greater than the allowed count
        pytest.fail(f"Accessibility violations found: {axe_results.violations_count}")
    
    pytest.pass_test(f"Accessibility violations found: {axe_results.violations_count}")