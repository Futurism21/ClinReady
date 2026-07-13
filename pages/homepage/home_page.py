import pytest
from playwright.sync_api import sync_playwright, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


from baseclass import BasePage

class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.base_page_instance = BasePage(page)

        self.LOGO = "//img[@alt = 'logo']"
        self.SEARCH_JOB= "//p[normalize-space()='Professional Journey']/following::a[@href='/findjobs'][1]"

    def logoCheck(self):
        try:
            self.base_page_instance.wait_for_element(self.LOGO)
            assert self.base_page_instance.verify_element_is_visible(self.LOGO), "Logo is not visible"
        except Exception as e:
            self.page.screenshot(path="error_logo.png")
            print(f"❌ Logo validation failed: {str(e)}")
            raise

    def verify_search_job(self):
        try:
            self.base_page_instance.click_element(self.SEARCH_JOB)

            current_url = self.base_page_instance.get_current_url()

            assert "/findjobs" in current_url, \
                f"Expected '/findjobs' in URL but got {current_url}"

        except Exception as e:
            raise Exception(f"Failed to verify Search Job page: {e}")

