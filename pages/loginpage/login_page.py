# from playwright.sync_api import sync_playwright, Page
# from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
#
#
# from baseclass import BasePage
#
#
#
# class LoginPageClass(BasePage):
#     def __init__(self, page: Page):
#         super().__init__(page)
#         self.page = page
#
#         self.base_page_instance = BasePage(page)
#
#         self.LOGO = ""
#
#     def logoCheck(self):
#         try:
#             self.base_page_instance.wait_for_element(self.LOGO)
#             assert self.base_page_instance.verify_element_is_visible(self.LOGO), "Logo is not visible"
#         except Exception as e:
#             self.page.screenshot(path="error_logo.png")
#             print(f"❌ Logo validation failed: {str(e)}")
#             raise