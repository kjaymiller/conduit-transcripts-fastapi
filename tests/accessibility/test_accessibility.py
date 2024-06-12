import pytest

import time
import datetime
import pathlib

from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page
from slugify import slugify

report_time = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

axe = Axe()
    
@pytest.fixture()
def run_a11y_test(request):
    """Run accessibility tests on the last page and store results in a file"""
    # Create a directory to store accessibility reports
    accessibility_dir = pathlib.Path("test-results/accessibility_reports")
    accessibility_dir.mkdir(exist_ok=True, parents=True)
    _accessibility_reports = pathlib.Path(f"{report_time}_accessibility_page_results")
    accessibility_reports = accessibility_dir / _accessibility_reports
    accessibility_reports.mkdir(exist_ok=True, parents=True)

    # Create a file to store accessibility snapshots
    _accessibility_snapshots = pathlib.Path(f"{report_time}_accessibility_page_snapshot.txt")
    accessibility_snapshots = accessibility_dir/_accessibility_snapshots
    accessibility_snapshots.touch(exist_ok=True)

    report_path = accessibility_reports / pathlib.Path(f"{slugify(request.node.name)}.txt")
    report_path.touch(exist_ok=True)

    return report_path, accessibility_snapshots


@pytest.mark.parametrize(
        "route",
        (
            "",
            "episodes/",
            "episode/1/"
        )
)
def test_web_get_accessibility(request, pytestconfig, page: Page, route: str, live_server_url: str, run_a11y_test: tuple[pathlib.Path, pathlib.Path]):
    report_path, accessibility_snapshots = run_a11y_test

    page.goto(f"{live_server_url}{route}")
    axe_results = axe.run(page)

    report_path.write_text(axe_results.generate_report())
    snapshot_path = accessibility_snapshots
    with open (snapshot_path, "a") as file:
        file.write(f"Page: {request.node.name}\n")
        file.write(axe_results.generate_snapshot())
        file.write("\n----------------\n")
    
    if axe_results.violations_count > pytestconfig.getoption("--a11y-count"):
        # fail the test if the number of violations is greater than the allowed count
        pytest.fail(f"Accessibility violations found: {axe_results.violations_count}")
    
    pytest.pass_test(f"Accessibility violations found: {axe_results.violations_count}")


def test_search_a11y(request, pytestconfig, page: Page, live_server_url: str, run_a11y_test: tuple[Axe, pathlib.Path, pathlib.Path]):
    report_path, accessibility_snapshots = run_a11y_test
    page.goto(f"{live_server_url}enable_ai/")
    page.get_by_placeholder("Ask about checking email or").click()
    page.get_by_placeholder("Ask about checking email or").fill("How do I clean my house regularly?")
    page.get_by_placeholder("Ask about checking email or").press("Enter")
    page.wait_for_url(f"{live_server_url}ai_search/")
    axe_results = axe.run(page)

    report_path.write_text(axe_results.generate_report())
    snapshot_path = accessibility_snapshots

    with open (snapshot_path, "a") as file:
        file.write(f"Page: {request.node.name}\n")
        file.write(axe_results.generate_snapshot())
        file.write("\n----------------\n")
    
    if axe_results.violations_count > pytestconfig.getoption("--a11y-count"):
        # fail the test if the number of violations is greater than the allowed count
        pytest.fail(f"Accessibility violations found: {axe_results.violations_count}")
    
    pytest.pass_test(f"Accessibility violations found: {axe_results.violations_count}")