import time
from pathlib import Path

from playwright.sync_api import Page
import pytest

from conftest import page
from pages.loginpage.login_page import LoginPageClass
from utils.constants import USER_NAME, PASSWORD, APPLICATION_URL
from utils.excelImport import ExcelUtils
from utils.logger_config import get_logger

login_page_instance = LoginPageClass(page)
logger = get_logger("Test_Login_Page")

def test_logo(login_page):
    login_page.logoCheck()
    logger.info("Logo is successfully verified and visible")
