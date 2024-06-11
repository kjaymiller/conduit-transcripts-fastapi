from time import sleep
import pytest
import pathlib
from playwright.sync_api import Page


@pytest.mark.parametrize(
        "route",
        (
            "",
            "episodes",
            "episode/1"
        )
)
def test_web_get_accessibility(page, route):
    page.goto(f"http://localhost:8000/{route}")


def test_search_a11y(page):
    page.goto("http://localhost:8000/enable_ai")
    page.get_by_placeholder("Ask about checking email or").fill("How do I keep my house clean", timeout=3000)
    page.get_by_role("button", name="Ask our 💫 AI Coach").click(timeout=100000)
    sleep(30)