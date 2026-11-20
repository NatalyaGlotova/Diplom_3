import allure
from pages.base_page import BasePage
from locators import MainPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage(BasePage):
    def click_constructor(self):
        self.click_element(MainPageLocators.CONSTRUCTOR_BUTTON, description="кнопку 'Конструктор'")

    def click_order_feed(self):
        self.click_element(MainPageLocators.ORDERS_LIST_BUTTON, description="кнопку 'Лента заказов'")

    def click_ingredient(self):
        self.click_element(MainPageLocators.BUN_INGREDIENT, description="карточку ингредиента (булка)")

    def close_modal(self):
        self.click_element(MainPageLocators.CROSS_BUTTON, description="иконку закрытия модального окна (крестик)")

    def get_ingredient_counter(self):
        with allure.step("Получить текущее числовое значение счетчика ингредиента"):
            try:
                return int(self.find_element(MainPageLocators.INGREDIENT_COUNTER, time=5).text)
            except:
                return 0

    def add_ingredient_to_order(self):
        # Ожидаем, что ингредиент и корзина появились в DOM и видимы на этапе выполнения действия
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(MainPageLocators.BUN_INGREDIENT))
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(MainPageLocators.ORDER_BASKET))
    
        # Только после этого выполняем JS-перетаскивание
        self.drag_and_drop_js(MainPageLocators.BUN_INGREDIENT, MainPageLocators.ORDER_BASKET)

    def place_order(self):
        self.add_ingredient_to_order()
        
        # Находим кнопку "Оформить заказ" через базовый метод
        submit_button = self.find_element(MainPageLocators.CREATE_ORDER_BUTTON)
        
        with allure.step("Кликнуть на кнопку отправки 'Оформить заказ' через JS"):
            # Клик через JavaScript защищает от ElementClickInterceptedException
            self.driver.execute_script("arguments[0].click();", submit_button)
        
        with allure.step("Ожидание генерации номера заказа в открывшемся попапе"):
            order_element = self.find_element(MainPageLocators.ORDER_ID)
            
            # Ждем, пока дефолтные "999999" сменятся на реальный ID заказа
            WebDriverWait(self.driver, 15).until(
                lambda d: order_element.text.strip().isdigit() and order_element.text.strip() != "999999"
            )
            order_id = order_element.text.strip()
            allure.attach(order_id, name="Сгенерированный ID заказа", attachment_type=allure.attachment_type.TEXT)
        
        self.click_element(MainPageLocators.CLOSE_MODAL_ORDER, description="кнопку закрытия окна подтверждения заказа")
        return order_id
    