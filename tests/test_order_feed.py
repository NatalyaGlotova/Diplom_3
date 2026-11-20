import pytest
import allure
from pages.main_page import MainPage
from pages.feed_page import OrderFeedPage
from selenium.webdriver.support.ui import WebDriverWait

@allure.suite("Проверка бизнес-логики раздела «Лента заказов»")
class TestOrderFeed:

    @allure.title("Увеличение глобального счётчика общего числа заказов «Выполнено за всё время»")
    def test_all_time_counter_increases(self, authenticated_driver):
        feed_page = OrderFeedPage(authenticated_driver)
        feed_page.open("feed")
        # Фиксируем начальное значение счетчика
        initial_counter = feed_page.get_counter_all_time()
        
        main_page = MainPage(authenticated_driver)
        main_page.open()
        main_page.place_order()
        
        feed_page.open("feed")
        # Ожидаем напрямую в тесте, пока счетчик станет строго больше начального значения
        WebDriverWait(authenticated_driver, 15).until(
            lambda d: feed_page.get_counter_all_time() > initial_counter
        )
        assert feed_page.get_counter_all_time() > initial_counter

    @allure.title("Увеличение суточного счётчика выполненных заказов «Выполнено за сегодня»")
    def test_today_counter_increases(self, authenticated_driver):
        feed_page = OrderFeedPage(authenticated_driver)
        feed_page.open("feed")
        # Фиксируем начальное значение счетчика
        initial_counter = feed_page.get_counter_today()
        
        main_page = MainPage(authenticated_driver)
        main_page.open()
        main_page.place_order()
        
        feed_page.open("feed")
        # Ожидаем напрямую в тесте, пока суточный счетчик станет строго больше начального значения
        WebDriverWait(authenticated_driver, 15).until(
            lambda d: feed_page.get_counter_today() > initial_counter
        )
        assert feed_page.get_counter_today() > initial_counter

    @allure.title("Отображение созданного идентификатора заказа на информационной доске в секции «В работе»")
    def test_order_appears_in_progress(self, authenticated_driver):
        main_page = MainPage(authenticated_driver)
        main_page.open()
        order_id = main_page.place_order()
        
        feed_page = OrderFeedPage(authenticated_driver)
        feed_page.open("feed")
        assert feed_page.wait_for_order_in_progress(order_id)
        