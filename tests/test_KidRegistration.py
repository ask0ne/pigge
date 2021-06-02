from selenium import webdriver
import pytest
from time import sleep
URL = "http://127.0.0.1:5000/registration/kid"


@pytest.fixture()
def setup():
    global driver
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.maximize_window()
    yield
    driver.close()


def test_KidRegistration_valid(setup):
    driver.get(URL)
    driver.find_element_by_name("name").send_keys("John K")
    driver.find_element_by_name("birthdate").send_keys("06-06-2012")  
    driver.find_element_by_xpath("//input[@value='B']").click()
    driver.find_element_by_name("email").send_keys("jhonK@mail.com")
    driver.find_element_by_name("pin").send_keys("4110")
    assert driver.title == "Kid's Registration"  # check..


def test_KidRegistration_blankEntries(setup):
    driver.get(URL)
    driver.find_element_by_name("name").send_keys("Barry")
    driver.find_element_by_name("birthdate").send_keys("")
    driver.find_element_by_name("gender").send_keys("Male")
    driver.find_element_by_name("email").send_keys("barry@mail.com")
    driver.find_element_by_name("pin").send_keys("")
    driver.find_element_by_name("register_kid").click()
    assert driver.title == "Kid's Registration"


def test_KidRegistration_invalidEntries(setup):
    driver.get(URL)
    driver.find_element_by_name("name").send_keys("Ron14")
    driver.find_element_by_name("birthdate").send_keys("6/6/12")
    driver.find_element_by_name("gender").send_keys("Female")
    driver.find_element_by_name("email").send_keys("ron14@gmail.com")
    driver.find_element_by_name("pin").send_keys("24788")
    driver.find_element_by_name("register_kid").click()
    assert driver.title == "Kid's Registration"  # check..