from __future__ import annotations

from pathlib import Path

import pytest
import reflex as rx
from playwright.sync_api import Page, expect
from reflex.testing import AppHarness


@pytest.fixture(scope="session")
def wac_app():
    root = Path(__file__).parent.parent
    with AppHarness.create(root=root) as harness:
        yield harness


def test_create_form(
    wac_app: AppHarness,
    page: Page,
):
    # Check that the frontend URL is set
    assert wac_app.frontend_url is not None

    page.goto(wac_app.frontend_url)
    page.set_default_timeout(3_000)
    expect(page).to_have_url(wac_app.frontend_url + "/")

    state_name = wac_app.get_state_name("State")
    full_state_name = wac_app.get_full_state_name("State")

    # driver = wac_app.frontend()
    page.goto(wac_app.frontend_url)
    expect.set_options(timeout=10_000)

    html_content = page.content()
    # breakpoint()
    # page.get_by_role("button", name="tasks").click()
    page.locator('button.rt-Button:has-text("tasks")').click()
    html_content = page.content()
    print(html_content)
    expect(page).to_have_url(wac_app.frontend_url + "/tasks")
    breakpoint()
