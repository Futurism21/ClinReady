from datetime import time

from playwright.sync_api import Page


from utils.logger_config import get_logger


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def navigate_to(self, url: str):
        try:
            self.logger.info(f"Navigating to URL: {url}")
            self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            self.logger.error(f"Navigation failed: {str(e)}")
            self.take_screenshot("navigation_error.png")
            raise

    def get_current_url(self):
        """
        Returns the current page URL.
        """
        try:
            current_url = self.page.url
            self.logger.info(f"Current URL: {current_url}")
            return current_url

        except Exception as e:
            self.logger.error(f"Failed to get current URL. Error: {str(e)}")
            raise Exception(f"Failed to get current URL: {str(e)}")

    def take_screenshot(self, filename: str):
        self.page.screenshot(path=filename)

    def wait_for_element(self, locator: str, timeout: int = 30000):
        try:
            self.page.wait_for_selector(locator, timeout=timeout)
            self.highlight_element(locator)
            self.logger.info(f"Element {locator} is visible on the page")
        except Exception as e:
            self.logger.error(f"Error waiting for element {locator}: {str(e)}")
            self.take_screenshot("wait_error.png")
            raise


    def click_element(self, selector: str):
        try:
            self.page.wait_for_selector(selector, timeout=5000)
            self.highlight_element(selector)
            self.page.click(selector)
            self.logger.info(f"Clicked element: {selector}")
        except Exception as e:
            self.logger.error(f"Click failed on {selector}: {str(e)}")
            self.take_screenshot("click_error.png")
            raise

    def fill_element(self, selector: str, text: str, **kwargs):
        try:
            self.page.wait_for_selector(selector, timeout=5000)
            self.highlight_element(selector)
            self.page.fill(selector, text, **kwargs)
            self.logger.info(f"Filled element {selector} with value: {text}")
        except Exception as e:
            self.logger.error(f"Fill failed on {selector}: {str(e)}")
            self.take_screenshot("fill_error.png")
            raise

    def get_text_of_element(self, locator):
        try:
            self.page.wait_for_selector(locator)
            time.sleep(2)
            self.highlight_element(locator)
            element_text = self.page.locator(locator).text_content()
            self.logger.info(f"Text for {locator}: {element_text}")
            return element_text
        except Exception as e:
            self.logger.error(f"Error getting text of element {locator}: {str(e)}")
            self.take_screenshot("gettext_error.png")
            raise

    def hover_element(self, selector: str, timeout: int = 5000):
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=timeout)
            locator.hover()
        except Exception as e:
            self.page.screenshot(path="hover_error.png")
            raise Exception(f"Failed to hover on '{selector}'. Reason: {str(e)}")

    def verify_element_is_visible(self, locator):
        try:
            visible = self.page.locator(locator).is_visible()
            self.logger.info(f"Element {locator} visibility: {visible}")
            return visible
        except Exception as e:
            self.logger.error(f"Error verifying visibility of element {locator}: {str(e)}")
            self.take_screenshot("visibility_error.png")
            return False

    def click_button(self, locator):
        try:
            self.page.wait_for_selector(locator, timeout=5000)
            self.highlight_element(locator)
            self.page.locator(locator).click()
            self.logger.info(f"Clicked button: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to click button {locator}: {str(e)}")
            self.take_screenshot("button_click_error.png")
            raise

    def get_text(self, selector: str) -> str:
        try:
            return self.page.text_content(selector)
        except Exception as e:
            self.logger.error(f"Failed to get text from {selector}: {str(e)}")
            self.take_screenshot("text_error.png")
            raise

    def check_assertion_text(self, actual: str, expected: str, context: str = ""):
        assert actual == expected, (
            f"[{context}] Expected '{expected}', but got '{actual}'"
        )

    def get_attribute(self, selector: str, attribute: str) -> str:
        try:
            return self.page.get_attribute(selector, attribute)
        except Exception as e:
            self.logger.error(f"Failed to get attribute {attribute} from {selector}: {str(e)}")
            self.take_screenshot("attribute_error.png")
            raise

    def highlight_element(self, locator):
        pass

    def select_checkbox(self, locator):
        try:
            checkbox = self.page.locator(locator)
            if not checkbox.is_checked():
                checkbox.check()
            self.logger.info(f"Checkbox selected: {locator}")
        except Exception as e:
            self.logger.error(f"Checkbox selection failed: {str(e)}")
            self.take_screenshot("checkbox_error.png")
            raise

    def select_from_dropdown(self, locator: str, value: str, by: str = "value"):
        try:
            if by == "value":
                self.page.select_option(locator, value=value)
            elif by == "label":
                self.page.select_option(locator, label=value)
            elif by == "index":
                self.page.select_option(locator, index=int(value))
            else:
                raise ValueError("Invalid selection type. Use 'value', 'label', or 'index'.")

            self.logger.info(
                f"Selected '{value}' from dropdown '{locator}' using '{by}'."
            )

        except Exception as e:
            self.logger.error(f"Dropdown selection failed: {str(e)}")
            self.take_screenshot("dropdown_error.png")
            raise

    def upload_file(self, locator: str, file_path: str):
        try:
            self.page.wait_for_selector(locator)
            self.page.set_input_files(locator, file_path)
            self.logger.info(f"Uploaded file: {file_path}")
        except Exception as e:
            self.logger.error(f"File upload failed: {str(e)}")
            self.take_screenshot("upload_error.png")
            raise

    def select_radio_button(self, locator: str):
        try:
            self.page.check(locator)
            self.logger.info(f"Radio button selected: {locator}")
        except Exception as e:
            self.logger.error(f"Error selecting radio button {locator}: {str(e)}")
            self.take_screenshot("radio_select_error.png")
            raise
