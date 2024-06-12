import pytest
from playwright.sync_api import Page, expect


def test_episode_by_title(page:Page, browser_context_args: dict[str, any], live_server_url) -> None:
    page.goto(live_server_url)
    expect(page.locator("a").filter(has_text="Super Conductor Support")).to_be_visible()
