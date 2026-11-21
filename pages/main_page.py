import allure

from locators import MainPageLocators
from pages.base_page import BasePage


class MainPage(BasePage):
    def click_constructor(self):
        with allure.step("Перейти в раздел 'Конструктор'"):
            self.click_element(MainPageLocators.CONSTRUCTOR_BUTTON, description="кнопку 'Конструктор'")

    def click_order_feed(self):
        with allure.step("Перейти в раздел 'Лента заказов'"):
            self.click_element(MainPageLocators.ORDERS_LIST_BUTTON, description="кнопку 'Лента заказов'")

    def click_ingredient(self):
        with allure.step("Открыть детали ингредиента (булка)"):
            self.click_element(MainPageLocators.BUN_INGREDIENT, description="карточку ингредиента (булка)")

    def close_modal(self):
        with allure.step("Закрыть модальное окно"):
            self.click_element(MainPageLocators.CROSS_BUTTON, description="иконку закрытия модального окна (крестик)")

    def is_constructor_title_displayed(self):
        return self.is_element_visible(
            MainPageLocators.MAIN_LIST_TITLE,
            description="заголовка раздела 'Конструктор'"
        )

    def is_ingredient_modal_displayed(self):
        return self.is_element_visible(
            MainPageLocators.INGREDIENT_DETAILS_POPUP,
            description="всплывающего окна с деталями ингредиента"
        )

    def is_ingredient_modal_closed(self):
        with allure.step("Проверить закрытие всплывающего окна с деталями ингредиента"):
            return bool(self.wait_for_invisibility(MainPageLocators.INGREDIENT_DETAILS_POPUP))

    def get_ingredient_counter(self):
        with allure.step("Получить текущее числовое значение счетчика ингредиента"):
            try:
                return int(self.find_element(MainPageLocators.INGREDIENT_COUNTER).text)
            except Exception:
                return 0

    def wait_for_counter_increase(self, initial_count):
        with allure.step(f"Ожидать увеличения счетчика ингредиента больше {initial_count}"):
            self.wait_until(
                lambda _: self.get_ingredient_counter() > initial_count,
                description=f"увеличения счетчика ингредиента больше {initial_count}"
            )
            return self.get_ingredient_counter()

    def add_ingredient_to_order(self):
        with allure.step("Добавить ингредиент (булку) в корзину заказа"):
            self.find_element(MainPageLocators.BUN_INGREDIENT)
            self.find_element(MainPageLocators.ORDER_BASKET)
            self.drag_and_drop_js(MainPageLocators.BUN_INGREDIENT, MainPageLocators.ORDER_BASKET)

    def place_order(self):
        with allure.step("Оформить заказ и получить его идентификатор"):
            self.add_ingredient_to_order()
            self.js_click(MainPageLocators.CREATE_ORDER_BUTTON, description="кнопку отправки 'Оформить заказ'")

            with allure.step("Ожидание генерации номера заказа в открывшемся попапе"):
                order_element = self.find_element(MainPageLocators.ORDER_ID)
                self.wait_until(
                    lambda _: order_element.text.strip().isdigit() and order_element.text.strip() != "999999",
                    description="смены дефолтного номера '999999' на реальный ID заказа"
                )
                order_id = order_element.text.strip()
                allure.attach(order_id, name="Сгенерированный ID заказа", attachment_type=allure.attachment_type.TEXT)

            self.click_element(MainPageLocators.CLOSE_MODAL_ORDER, description="кнопку закрытия окна подтверждения заказа")
            return order_id
        