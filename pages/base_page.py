import allure
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data.urls import Urls


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = Urls.BASE_URL

    def open(self, url=""):
        target_url = url if url.startswith("http") else f"{self.base_url}{url}"
        with allure.step(f"Открыть URL-адрес: {target_url}"):
            self.driver.get(target_url)

    def find_element(self, locator, time=10):
        with allure.step(f"Найти и дождаться видимости элемента: {locator}"):
            return WebDriverWait(self.driver, time).until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator, time=10):
        with allure.step(f"Найти и дождаться присутствия элементов: {locator}"):
            return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator))

    def get_elements(self, locator):
        with allure.step(f"Получить список элементов без ожидания: {locator}"):
            return self.driver.find_elements(*locator)

    def is_element_visible(self, locator, description="элемента"):
        with allure.step(f"Проверить отображение {description}"):
            return self.find_element(locator).is_displayed()

    def wait_until(self, condition, time=15, description="выполнения условия"):
        with allure.step(f"Ожидать {description}"):
            return WebDriverWait(self.driver, time).until(condition)

    def click_element(self, locator, description="элемент", element_name=None):
        display_name = element_name if element_name is not None else description
        with allure.step(f"Кликнуть на {display_name}"):
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
            try:
                element.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", element)

    def js_click(self, locator, description="элемент"):
        with allure.step(f"Кликнуть на {description} через JS"):
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].click();", element)

    def wait_for_invisibility(self, locator, time=10):
        with allure.step(f"Ожидание исчезновения элемента с экрана: {locator}"):
            return WebDriverWait(self.driver, time).until(EC.invisibility_of_element_located(locator))

    def drag_and_drop_js(self, source_locator, target_locator):
        with allure.step("Выполнить Drag & Drop ингредиента в область корзины"):
            source = self.find_element(source_locator)
            target = self.find_element(target_locator)

            js_script = """
            function createEvent(typeOfEvent) {
                var event = document.createEvent("CustomEvent");
                event.initCustomEvent(typeOfEvent, true, true, null);
                event.dataTransfer = {
                    data: {},
                    setData: function (key, value) { this.data[key] = value; },
                    getData: function (key) { return this.data[key]; }
                };
                return event;
            }
            function dispatchEvent(element, event, transferData) {
                if (transferData !== undefined) { event.dataTransfer = transferData; }
                element.dispatchEvent(event);
            }
            function dragAndDrop(elementFirst, elementSecond) {
                var dragStartEvent = createEvent('dragstart');
                dispatchEvent(elementFirst, dragStartEvent);
                var dropEvent = createEvent('drop', dragStartEvent.dataTransfer);
                dispatchEvent(elementSecond, dropEvent, dragStartEvent.dataTransfer);
                var dragEndEvent = createEvent('dragend', dragStartEvent.dataTransfer);
                dispatchEvent(elementFirst, dragEndEvent);
            }
            dragAndDrop(arguments[0], arguments[1]);
            """
            self.driver.execute_script(js_script, source, target)
