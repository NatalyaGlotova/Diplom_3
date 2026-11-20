import allure
from pages.base_page import BasePage
from locators import OrderFeedLocators
from selenium.webdriver.support.ui import WebDriverWait

class OrderFeedPage(BasePage):

    def get_counter_all_time(self):
        with allure.step("Считать значение счетчика 'Выполнено за всё время'"):
            return int(self.find_element(OrderFeedLocators.TOTAL_ORDER_COUNT).text)

    def get_counter_today(self):
        with allure.step("Считать значение счетчика 'Выполнено за сегодня'"):
            return int(self.find_element(OrderFeedLocators.DAILY_ORDER_COUNT).text)

    def wait_for_order_in_progress(self, order_id):
        clean_id = order_id.lstrip('0')
        with allure.step(f"Ожидать появление идентификатора заказа {clean_id} на доске 'В работе'"):
            def check_order_in_list(d):
                # Находим элементы номеров на доске
                elements = d.find_elements(*OrderFeedLocators.NUMBER_IN_PROGRESS)
                orders = [el.text.strip().lstrip('0') for el in elements]
                return clean_id in orders

            WebDriverWait(self.driver, 15).until(check_order_in_list)
            return True
        