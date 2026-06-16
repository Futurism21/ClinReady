from pathlib import Path
import pytest
import os
import allure
from datetime import datetime
from playwright.sync_api import sync_playwright, Page

from pages.homepage.home_page import HomePage
from pages.loginpage.login_page import LoginPageClass
from utils.constants import APPLICATION_URL, EMAIL, PASSWORD
from utils.excelimport import ExcelUtils


# -------------------------------
# CLI OPTION
# -------------------------------
def pytest_addoption(parser):
    parser.addoption(
        "--pw-browser",
        action="store",
        default="chromium",
        help="Browser: chromium/firefox/webkit"
    )


# -------------------------------
# BROWSER FIXTURES
# -------------------------------
@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--pw-browser")


@pytest.fixture(scope="function")
def page(browser_name):
    with sync_playwright() as p:
        browser = getattr(p, browser_name).launch(
            headless=False,
            args=["--window-size=1920,1080"]
        )

        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )

        page = context.new_page()
        print(f"\nRunning on browser: {browser_name}")

        yield page

        context.close()
        browser.close()


# -------------------------------
# PAGE OBJECT FIXTURES
# -------------------------------
@pytest.fixture(scope="function")
def home_page(page: Page):
    home_page_instance = HomePage(page)
    home_page_instance.navigate_to(APPLICATION_URL)
    return home_page_instance

# @pytest.fixture(scope="function")
# def login_page(page: Page):
#     login_page_instance = LoginPageClass(page)
#     login_page_instance.navigate_to(APPLICATION_URL)
#     return login_page_instance


@pytest.fixture(scope="function")
def logged_in_page(page: Page):
    login_instance = LoginPageClass(page)
    login_instance.navigate_to(APPLICATION_URL)
    login_instance.login(EMAIL, PASSWORD)
    return page


# -------------------------------
# EXCEL FIXTURES
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent
TESTDATA_FILE = BASE_DIR / "testdata" / "testdata.xlsx"


@pytest.fixture(scope="session")
def excel_utils():
    return ExcelUtils(TESTDATA_FILE)


@pytest.fixture(scope="session")
def all_test_data(excel_utils):
    return excel_utils.get_all_test_data("Sheet1")


@pytest.fixture
def test_case_data(excel_utils):
    def _get_data(test_case_id: str, sheet_name="Sheet1"):
        return excel_utils.get_test_data(sheet_name, test_case_id)
    return _get_data


# -------------------------------
# SCREENSHOT ON FAILURE
# -------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page:
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(
                screenshot_dir,
                f"{item.name}_{timestamp}.png"
            )

            page.screenshot(path=screenshot_path, full_page=True)

            allure.attach.file(
                screenshot_path,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
