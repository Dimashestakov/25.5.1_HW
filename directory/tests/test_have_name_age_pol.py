import pytest
from selenium import webdriver as selenium_webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_have_name_age_and_gender(selenium_driver):
    ''' Данный тест выполняет проверку списка питомцев по следующим критериям:
    1)Проверяется, что пользователь находится на странице с питомцами.
    2)Проверяется, что у всех питомцев на странице есть указанные характеристики: имя, возраст и порода.  '''

    driver = selenium_driver
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.nav-link[href='/my_pets']")))
    # Нажимаем на кнопку входа в пункт меню Мои питомцы
    driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/my_pets']").click()
    # time.sleep(3)
    # Чтобы перейти к списку "Мои питомцы", необходимо нажать на кнопку входа в соответствующий пункт меню.
    assert driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr')))
    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    # time.sleep(3)
    # Для выполнения теста необходимо:
    # Перебрать данные из pet_data.
    # Для каждого питомца оставить только имя, возраст и породу, остальные данные заменить на пустую строку.
    # Разделить полученную строку по пробелам и сохранить каждый элемент в список.
    # Подсчитать количество элементов в списке и сравнить его с ожидаемым результатом.
    for i in range(len(pets_count)):
        data_pet = pets_count[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        result = len(split_data_pet)
        assert result == 3
        # print(result) 