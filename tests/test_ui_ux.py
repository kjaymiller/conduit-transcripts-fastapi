import pytest
from playwright.sync_api import Page, expect

def test_home_no_ai_enabled(page: Page) -> None:
    page.goto("http://localhost:8000/")
    page.get_by_role("link", name="Home").click()
    expect(page).to_have_url("http://localhost:8000/")
    expect(page.get_by_role("link", name="Home")).to_be_visible()
    expect(page.get_by_role("link", name="Episodes")).to_be_visible()
    expect(page.get_by_role("link", name="Let's Do It!")).to_be_visible()
    expect(page.get_by_role("link", name="Disable AI")).to_be_hidden()
    expect(page.get_by_role("link", name="Enable AI")).to_be_visible()
    expect(page.get_by_role("button", name="Search")).to_be_visible()
    expect(page.get_by_role("button", name="Ask our 💫 AI Coach")).to_be_hidden()

def test_home_from_disable_ai(page: Page) -> None:
    page.goto("http://localhost:8000/disable_ai")
    page.get_by_role("link", name="Home").click()
    expect(page).to_have_url("http://localhost:8000/")
    expect(page.get_by_role("link", name="Home")).to_be_visible()
    expect(page.get_by_role("link", name="Episodes")).to_be_visible()
    expect(page.get_by_role("link", name="Let's Do It!")).to_be_visible()
    expect(page.get_by_role("link", name="Disable AI")).to_be_hidden()
    expect(page.get_by_role("link", name="Enable AI")).to_be_visible()
    expect(page.get_by_role("button", name="Search")).to_be_visible()
    expect(page.get_by_role("button", name="Ask our 💫 AI Coach")).to_be_hidden()

def test_home_ai_enabled(page: Page) -> None:
    page.goto("http://localhost:8000/enable_ai")
    expect(page).to_have_url("http://localhost:8000/")
    expect(page.get_by_role("link", name="Home")).to_be_visible()
    expect(page.get_by_role("link", name="Episodes")).to_be_visible()
    expect(page.get_by_role("link", name="Let's Do It!")).to_be_hidden()
    expect(page.get_by_role("link", name="Disable AI")).to_be_visible()
    expect(page.get_by_role("link", name="Enable AI")).to_be_hidden()
    expect(page.get_by_role("button", name="Search")).to_be_visible()
    expect(page.get_by_role("button", name="Ask our 💫 AI Coach")).to_be_visible()