import pytest
import allure
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data.user_data import PersonData
from data.urls import Urls 
from pages.login_page import LoginPage


@pytest.fixture(params=[
    (webdriver.Chrome, webdriver.ChromeOptions),
    (webdriver.Firefox, webdriver.FirefoxOptions)
], ids=['chrome', 'firefox'])
def driver_do(request):
    driver_class, options_class = request.param
    options = options_class()
    
    driver = driver_class(options=options)
    driver.maximize_window()  # Чистый и кроссбраузерный способ развернуть окно
    
    with allure.step('Открытие браузера'):
        driver.get(Urls.BASE_URL)
    
    yield driver
    driver.quit()


@pytest.fixture
def authenticated_driver(driver_do):
    with allure.step('Предусловие: Выполнение фонового входа пользователя в аккаунт'):
        driver_do.get(Urls.URL_LOGIN)
        login_page = LoginPage(driver_do)
        login_page.login(email=PersonData.USER_LOGIN, password=PersonData.USER_PASSWORD)
        login_page.wait_for_successful_login()
        
    return driver_do

