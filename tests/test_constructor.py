import pytest
import allure
from pages.main_page import MainPage
from pages.feed_page import OrderFeedPage
from locators import MainPageLocators, OrderFeedLocators
from selenium.webdriver.support.ui import WebDriverWait

@allure.suite("Проверка основной функциональности конструктора бургеров")
class TestMainFunctionality:

    @allure.title("Переход по клику на «Конструктор»")
    def test_navigate_to_constructor(self, driver_do): # Заменено на driver_do
        main_page = MainPage(driver_do)
        main_page.open("feed")
        main_page.click_constructor()
        assert main_page.find_element(MainPageLocators.MAIN_LIST_TITLE).is_displayed()

    @allure.title("Переход по клику на раздел «Лента заказов»")
    def test_navigate_to_feed(self, driver_do): # Заменено на driver_do
        main_page = MainPage(driver_do)
        main_page.open()
        main_page.click_order_feed()
        feed_page = OrderFeedPage(driver_do)
        assert feed_page.find_element(OrderFeedLocators.ORDERS_LIST_TITLE).is_displayed()

    @allure.title("Появление всплывающего окна при клике на ингредиент")
    def test_ingredient_modal_open(self, driver_do): # Заменено на driver_do
        main_page = MainPage(driver_do)
        main_page.open()
        main_page.click_ingredient()
        assert main_page.find_element(MainPageLocators.INGREDIENT_DETAILS_POPUP).is_displayed()

    @allure.title("Закрытие всплывающего окна кликом по крестику")
    def test_ingredient_modal_close(self, driver_do): # Заменено на driver_do
        main_page = MainPage(driver_do)
        main_page.open()
        main_page.click_ingredient()
        
        assert main_page.find_element(MainPageLocators.INGREDIENT_DETAILS_POPUP).is_displayed()
        main_page.close_modal()
        assert main_page.wait_for_invisibility(MainPageLocators.INGREDIENT_DETAILS_POPUP)

    @allure.title("Увеличение счетчика при добавлении ингредиента")
    def test_ingredient_counter_increase(self, authenticated_driver):
        main_page = MainPage(authenticated_driver)
        main_page.open()
    
        # 1. Запоминаем начальное значение
        initial_count = main_page.get_ingredient_counter()
    
        # 2. Перетаскиваем булку в конструктор
        main_page.add_ingredient_to_order()
    
        # 3. Ждем, пока метод получения счетчика вернет значение больше начального
        # (Если изначально было 0, то метод get_ingredient_counter вернет 0, а после добавления — 2)
        WebDriverWait(authenticated_driver, 10).until(
            lambda d: main_page.get_ingredient_counter() > initial_count
        )
    
        final_count = main_page.get_ingredient_counter()
    
        assert final_count > initial_count
