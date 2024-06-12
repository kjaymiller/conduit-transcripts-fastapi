from time import sleep
import pytest
from playwright.sync_api import Page


@pytest.mark.parametrize(
        "route",
        (
            "",
            "/episodes",
            "/episode/1"
        )
)
def test_web_get_accessibility(page: Page, route: str, live_server_url: str):
    page.goto(f"{live_server_url}{route}")


def test_search_a11y(page: Page, live_server_url: str):
    page.goto(f"{live_server_url}/enable_ai")
    page.get_by_placeholder("Ask about checking email or").fill("How do I keep my house clean", timeout=3000)
    page.get_by_role("button", name="Ask our 💫 AI Coach").click(timeout=100000)
    sleep(30)