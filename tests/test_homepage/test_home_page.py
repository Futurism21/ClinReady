import time
from pathlib import Path

from playwright.sync_api import Page
import pytest

from conftest import page
from pages.homepage.home_page import HomePage
from pages.loginpage.login_page import LoginPageClass
from utils.constants import EMAIL, PASSWORD, APPLICATION_URL
from utils.excelimport import ExcelUtils
from utils.logger_config import get_logger

home_page_instance = HomePage(page)
logger = get_logger("Test_HomePage")

def test_logo(home_page):
    home_page.logoCheck()
    logger.info("Logo is successfully verified and visible")