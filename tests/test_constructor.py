import allure

from pages.feed_page import OrderFeedPage
from pages.main_page import MainPage


@allure.suite("Проверка основной функциональности конструктора бургеров")
class TestMainFunctionality:

    @allure.title("Переход по клику на «Конструктор»")
    def test_navigate_to_constructor(self, driver_do):
        main_page = MainPage(driver_do)
        main_page.open("feed")
        main_page.click_constructor()

        assert main_page.is_constructor_title_displayed()

    @allure.title("Переход по клику на раздел «Лента заказов»")
    def test_navigate_to_feed(self, driver_do):
        main_page = MainPage(driver_do)
        main_page.open()
        main_page.click_order_feed()
        feed_page = OrderFeedPage(driver_do)

        assert feed_page.is_feed_title_displayed()

    @allure.title("Появление всплывающего окна при клике на ингредиент")
    def test_ingredient_modal_open(self, driver_do):
        main_page = MainPage(driver_do)
        main_page.open()
        main_page.click_ingredient()

        assert main_page.is_ingredient_modal_displayed()

    @allure.title("Закрытие всплывающего окна кликом по крестику")
    def test_ingredient_modal_close(self, driver_do):
        main_page = MainPage(driver_do)
        main_page.open()
        main_page.click_ingredient()
        main_page.close_modal()

        assert main_page.is_ingredient_modal_closed()

    @allure.title("Увеличение счетчика при добавлении ингредиента")
    def test_ingredient_counter_increase(self, authenticated_driver):
        main_page = MainPage(authenticated_driver)
        main_page.open()

        initial_count = main_page.get_ingredient_counter()
        main_page.add_ingredient_to_order()
        final_count = main_page.wait_for_counter_increase(initial_count)

        assert final_count > initial_count
        