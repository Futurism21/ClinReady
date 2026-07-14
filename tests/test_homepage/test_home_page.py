from conftest import page
from pages.homepage.home_page import HomePage
from utils.logger_config import get_logger

home_page_instance = HomePage(page)
logger = get_logger("Test_HomePage")

def test_logo(home_page):
    home_page.logoCheck()
    logger.info("Logo is successfully verified and visible")

def test_search_job(home_page):
    home_page.verify_search_job()
    logger.info("Search Job link navigation verified successfully.")

def test_enroll_now(home_page):
    home_page.verify_enroll_now()
    logger.info("Enroll Now link navigation verified successfully.")