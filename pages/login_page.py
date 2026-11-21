import allure
from pages.base_page import BasePage
from locators import LoginPageLocators, MainPageLocators

class LoginPage(BasePage):
    def login(self, email, password):
        with allure.step(f"Заполнить форму авторизации учетными данными"):
            email_input = self.find_element(LoginPageLocators.EMAIL_INPUT)
            email_input.send_keys(email)
            password_input = self.find_element(LoginPageLocators.PASSWORD_INPUT)
            password_input.send_keys(password)
        self.click_element(LoginPageLocators.LOGIN_BUTTON, element_name="кнопку подтверждения 'Войти'")

    def wait_for_successful_login(self):
        with allure.step("Проверить успешность входа по отображению кнопки создания заказа"):
            self.find_element(MainPageLocators.CREATE_ORDER_BUTTON, time=15)
