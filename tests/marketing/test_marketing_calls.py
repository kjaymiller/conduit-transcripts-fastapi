import pytest
from playwright.sync_api import Page, expect


def test_episode_by_title(page:Page, playwright, browser_context_args) -> None:
    page.goto("http://localhost:8000/")
    expect(page.locator("a").filter(has_text="Super Conductor Support")).to_be_visible()
