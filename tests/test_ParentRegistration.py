from selenium import webdriver
import pytest
from time import sleep

URL = "http://127.0.0.1:5000/registration/parent"


@pytest.fixture()
def setup():
    global driver
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.maximize_window()
    yield
    driver.close()


def test_ParentRegistration_valid(setup):
    driver.get(URL)  # can write on top ?
    driver.find_element_by_name("pname").send_keys("Ram Sharma")
    driver.find_element_by_name("mobile").send_keys("9855656541")
    driver.find_element_by_name("email").send_keys("ram_s@gmail.com")
    driver.find_element_by_name("psw").send_keys("Iamram@45")
    driver.find_element_by_name("register").click()
    sleep(5)
    assert driver.title == "Login"  # check..

def test_ParentRegistration_blankEntries(setup):
    driver.get(URL)
    driver.find_element_by_name("pname").send_keys("Jimmy")
    driver.find_element_by_name("mobile").send_keys("")
    driver.find_element_by_name("email").send_keys("jim@hotmail.com")
    driver.find_element_by_name("psw").send_keys("Happy@2020")
    driver.find_element_by_name("register").click()
    sleep(5)
    assert driver.title == "Login"


def test_ParentRegistration_invalidEntries(setup):
    driver.get(URL)
    driver.find_element_by_name("pname").send_keys("123abc")
    driver.find_element_by_name("mobile").send_keys("abcdef")
    driver.find_element_by_name("email").send_keys("abc@small.com	")
    driver.find_element_by_name("psw").send_keys("987654321")
    driver.find_element_by_name("register").click()
    sleep(5)
    assert driver.title == "Login"
