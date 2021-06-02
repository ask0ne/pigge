from selenium import webdriver
from time import sleep
import pytest
URL = "http://127.0.0.1:5000/login"


@pytest.fixture()
def setup():
	global driver
	driver=webdriver.Chrome(executable_path="chromedriver.exe")
	driver.maximize_window()
	yield
	driver.close()

def test_ParentRegistration_valid(setup):
	driver.get(URL)
	driver.find_element_by_name("p_email").send_keys("bob@mail.com")
	driver.find_element_by_name("password").send_keys("Bob@12345")
	driver.find_element_by_name("register").click()
	sleep(2)
	assert driver.title=="Dashboard"


def test_ParentRegistration_invalid(setup):
	driver.get(URL)
	driver.find_element_by_name("p_email").send_keys("ram_s@gmail.com")		
	driver.find_element_by_name("password").send_keys("Iamram@455")
	driver.find_element_by_name("register").click()
	sleep(2)
	assert driver.title=="Dashboard"
	

def test_KidRegistration_valid(setup):
	driver.get(URL)
	driver.find_element_by_name("kid_login").click()
	sleep(3)
	driver.find_element_by_name("k_email").send_keys("aditi@mail.com")	
	driver.find_element_by_name("pin").send_keys("1234")
	driver.find_element_by_name("Log_me_in").click()
	sleep(2)
	assert driver.title=="My Dashboard"


def test_KidRegistration_invalid(setup):
	driver.get(URL)
	driver.find_element_by_name("kid_login").click()
	sleep(3)
	driver.find_element_by_name("k_email").send_keys("aditi@mail.com")		
	driver.find_element_by_name("pin").send_keys("1121")
	driver.find_element_by_name("Log_me_in").click()
	sleep(2)
	assert driver.title=="My Dashboard"