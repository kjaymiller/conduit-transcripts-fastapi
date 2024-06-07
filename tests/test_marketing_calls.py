import pytest
from playwright.sync_api import Page, expect

def test_episode_by_title(page:Page):
    page.goto("http://localhost:8000/")