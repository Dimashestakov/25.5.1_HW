import time
from datetime import datetime
import pytest
from selenium import webdriver as selenium_webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# Webdriver fixture

@pytest.fixture(scope='session')
def selenium_driver(request):
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = selenium_webdriver.Chrome(executable_path=r"C:/projects/chromedriver_win32/chromedriver.exe",
                                       options=chrome_options)
    driver.set_window_size(1920, 1080)
    driver.maximize_window()
    driver.implicitly_wait(5)

    # Login
    driver.get('http://petfriends.skillfactory.ru/login')
    driver.find_element(By.ID, "email").send_keys("ddimakosmos1991@gmail.com")
    driver.find_element(By.ID, "pass").send_keys("ddimakosmos1991@gmail.com")
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    yield driver

    driver.quit()


# Создайте хук, который позволит вам проверять, прошел ли тест успешно или нет
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Для получения объекта отчета необходимо выполнить все оставшиеся перехватчики.
    outcome = yield
    rep = outcome.get_result()

    # Установите атрибут отчета для каждой фазы вызова, если это возможно
    # "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


# Проверка работоспособности теста
@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
    yield
    # request.node является "item", потому что мы используем значение по умолчанию
    # "function" scope
    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            driver = request.node.funcargs['selenium_driver']
            take_screenshot(driver, request.node.nodeid)
            print("executing test failed", request.node.nodeid)


# Скриншот теста
def take_screenshot(driver, nodeid):
    time.sleep(1)
    file_name = f'{nodeid}_{datetime.today().strftime("%Y-%m-%d_%H:%M")}.png'.replace("/", "_").replace("::", "__")
    driver.save_screenshot(file_name)