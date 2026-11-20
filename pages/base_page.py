import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        return WebDriverWait(self.driver, time).until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator))

    def click_element(self, locator, description="элемент", element_name=None):
        from selenium.common.exceptions import ElementClickInterceptedException
        
        # Если в метод передали element_name вместо description, используем его для Allure
        display_name = element_name if element_name is not None else description
        
        with allure.step(f"Кликнуть на {display_name}"):
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
            try:
                # Пробуем обычный клик Selenium
                element.click()
            except ElementClickInterceptedException:
                # Если элемент перекрыт анимацией/лоадером — кликаем через JavaScript
                self.driver.execute_script("arguments[0].click();", element)

    def wait_for_invisibility(self, locator, time=10):
        with allure.step("Ожидание исчезновения элемента с экрана"):
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
