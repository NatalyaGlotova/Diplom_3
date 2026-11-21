import allure
from selenium.common.exceptions import TimeoutException

from locators import OrderFeedLocators
from pages.base_page import BasePage


class OrderFeedPage(BasePage):
    def is_feed_title_displayed(self):
        return self.is_element_visible(
            OrderFeedLocators.ORDERS_LIST_TITLE,
            description="заголовка раздела 'Лента заказов'"
        )

    def get_counter_all_time(self):
        with allure.step("Считать значение счетчика «Выполнено за всё время»"):
            text = self.find_element(OrderFeedLocators.TOTAL_ORDER_COUNT).text.strip()
            return int(text.replace(" ", ""))

    def get_counter_today(self):
        with allure.step("Считать значение счетчика «Выполнено за сегодня»"):
            text = self.find_element(OrderFeedLocators.DAILY_ORDER_COUNT).text.strip()
            return int(text.replace(" ", ""))

    def is_counter_all_time_increased(self, initial_counter):
        step_description = f"увеличения счетчика «Выполнено за всё время» больше {initial_counter}"
        with allure.step(f"Проверить факт {step_description}"):
            try:
                self.wait_until(
                    lambda _: self.get_counter_all_time() > initial_counter,
                    description=step_description
                )
                return True
            except TimeoutException:
                return False

    def is_counter_today_increased(self, initial_counter):
        step_description = f"увеличения счетчика «Выполнено за сегодня» больше {initial_counter}"
        with allure.step(f"Проверить факт {step_description}"):
            try:
                self.wait_until(
                    lambda _: self.get_counter_today() > initial_counter,
                    description=step_description
                )
                return True
            except TimeoutException:
                return False

    def wait_for_order_in_progress(self, order_id):
        clean_id = str(order_id).strip().lstrip("0")
        step_description = f"появления идентификатора заказа {clean_id} на доске «В работе»"
        with allure.step(f"Проверить факт {step_description}"):
            def check_order_in_list(_):
                elements = self.get_elements(OrderFeedLocators.NUMBER_IN_PROGRESS)
                orders = [el.text.strip().lstrip("0") for el in elements if el.text.strip()]
                return clean_id in orders

            try:
                self.wait_until(check_order_in_list, description=step_description)
                return True
            except TimeoutException:
                return False
        