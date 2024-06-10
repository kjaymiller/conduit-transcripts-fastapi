import pytest


@pytest.fixture(scope="session", params=["iPhone 12", "Pixel 5", "Desktop Chrome"])
def browser_context_args(request, browser_context_args, playwright):
    return {
        **browser_context_args,
        **playwright.devices[request.param],
    }