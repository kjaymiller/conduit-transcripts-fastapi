import pytest
import pathlib
from playwright.sync_api import Page
from axe_playwright_python.sync_playwright import Axe

axe = Axe()
accesibility_reports = pathlib.Path("accessibility_page_results")
accesibility_reports.mkdir(exist_ok=True)
accesibility_snapshots = pathlib.Path("accessibility_page_snapshot.json")
accesibility_snapshots.touch(exist_ok=True)


def test_web_accessibility(page):
    page.goto("http://localhost:8000/")
    accessibility = axe.run(page)
    report_path = accesibility_reports / pathlib.Path("index.txt")
    
    if accessibility.violations_count > 0:
        report_path.write_text(accessibility.generate_report())
        assert False, f"Accessibility violations found. Report: {report_path}"
    
    assert True