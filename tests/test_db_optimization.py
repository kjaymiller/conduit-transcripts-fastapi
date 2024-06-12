import pytest
from playwright.sync_api import Page
import dotenv
from db.redis import redis_connection as redis

import uuid

dotenv.load_dotenv()

def test_checks_redis_cache_when_search_is_called(page:Page, live_server_url: str):
    """Checks if when an AI Search is called twice, only one redis cache is created"""
    redis.flushall()
    page.goto(f"{live_server_url}/enable_ai")

    query = f"{uuid.uuid4()} - How do I check to see if I'm doing the things on my list"

    page.get_by_placeholder("Ask about checking email or").fill(query)
    page.get_by_role("button", name="Ask our 💫 AI Coach").click(timeout=100000)
    
    page.get_by_placeholder("Ask about checking email or").fill(query)
    page.get_by_role("button", name="Ask our 💫 AI Coach").click(timeout=100000)
    
    redis_scan = redis.scan()
    assert len(redis_scan[1]) == 1 # And not 2

