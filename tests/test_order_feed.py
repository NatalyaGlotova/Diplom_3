import allure

from pages.feed_page import OrderFeedPage
from pages.main_page import MainPage


@allure.suite("Проверка бизнес-логики раздела «Лента заказов»")
class TestOrderFeed:

    @allure.title("Увеличение глобального счётчика общего числа заказов «Выполнено за всё время»")
    def test_all_time_counter_increases(self, authenticated_driver):
        feed_page = OrderFeedPage(authenticated_driver)
        feed_page.open("feed")
        initial_counter = feed_page.get_counter_all_time()

        main_page = MainPage(authenticated_driver)
        main_page.open()
        main_page.place_order()

        feed_page.open("feed")
        assert feed_page.is_counter_all_time_increased(initial_counter)

    @allure.title("Увеличение суточного счётчика выполненных заказов «Выполнено за сегодня»")
    def test_today_counter_increases(self, authenticated_driver):
        feed_page = OrderFeedPage(authenticated_driver)
        feed_page.open("feed")
        initial_counter = feed_page.get_counter_today()

        main_page = MainPage(authenticated_driver)
        main_page.open()
        main_page.place_order()

        feed_page.open("feed")
        assert feed_page.is_counter_today_increased(initial_counter)

    @allure.title("Отображение созданного идентификатора заказа на информационной доске в секции «В работе»")
    def test_order_appears_in_progress(self, authenticated_driver):
        main_page = MainPage(authenticated_driver)
        main_page.open()
        order_id = main_page.place_order()

        feed_page = OrderFeedPage(authenticated_driver)
        feed_page.open("feed")
        assert feed_page.wait_for_order_in_progress(order_id)
        