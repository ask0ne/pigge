from selenium import webdriver
from time import sleep
import pytest
URL = "http://127.0.0.1:5000/"


@pytest.fixture()
def setup():
    global driver
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.maximize_window()

def test_HOME_page(setup):
    driver.get(URL)
    assert driver.title == "Pigge Home Page"


def test_Registration_page():
    sleep(2)
    driver.find_element_by_name("Register").click()
    assert driver.title == "Parent's Registration"

def back_button():
    sleep(2)
    driver.find_element_by_name("").click()
    assert driver.title == "Pigge Home Page"

def test_LOGIN_page():
    sleep(2)
    driver.find_element_by_name("Login").click()
    assert driver.title == "Login"

def test_Parent_login():
    sleep(2)
    driver.find_element_by_name("p_email").send_keys("bob@mail.com")
    driver.find_element_by_name("password").send_keys("Bob@12345")
    driver.find_element_by_name("Log_me_in").click()
    assert driver.title == "Dashboard"

def test_PDash_AddFunds():
    sleep(2)
    driver.find_element_by_name("add_funds").send_keys("300")
    driver.find_element_by_name("FundsTransfer").click()
    assert driver.title == "Dashboard"


def test_PDash_Trans_History():
    sleep(2)
    driver.find_element_by_name("view_transactions").click()
    assert driver.title == "Transaction History"


def test_PDash_Back_fromHistory():
    sleep(2)
    driver.find_element_by_name("back_home").click()
    assert driver.title == "Dashboard"


def test_PDash_KidHistory():
    sleep(2)
    driver.find_element_by_name("kids_history").click()
    assert driver.title == "My Transactions"


def test_PDash_Back_KidHistory():
    sleep(2)
    driver.find_element_by_name("back_to_home").click()
    assert driver.title == "Dashboard"


def test_PDash_Notifications():
    sleep(2)
    driver.find_element_by_name("notify").click()
    # try this,can't find any way to test this.. else put dashboard
    assert driver.find_element_by_id("myNav")


def test_PDash_Logout():
    sleep(2)
    driver.find_element_by_name("logout").click()
    assert driver.title == "Pigge Home Page"


def test_Kid_login(setup):
    driver.get(URL + "/login")  # login url
    driver.find_element_by_name("k_email").send_keys("aditi@mail.com")
    driver.find_element_by_name("pin").send_keys("1234")
    driver.find_element_by_name("Log_me_in").click()
    assert driver.title == "My Dashboard"


def test_KDash_Pay():
    sleep(1)
    driver.find_element_by_name("pay_buddy").click()
    assert driver.title == "Payments"


def test_KDash_Pay_Back():
    sleep(1)
    driver.find_element_by_name("backhome").click()
    assert driver.title == "My Dashboard"


def test_KDash_Pay_Initiate():
    sleep(1)
    driver.find_element_by_name("pay_buddy").click()
    driver.find_element_by_name("receiver_wallet_id").send_keys(
        "W")  # fill some exsisting
    driver.find_element_by_name("amount").send_keys("250")
    driver.find_element_by_name("GO").click()
    assert driver.title == "Confirmation Required"


def test_KDash_PayConfirm():
    sleep(1)
    driver.find_element_by_id("confirm").click()
    # time lapse, sufficient ?
    time.sleep(15)
    assert driver.title == "My Dashboard"


def test_KDash_PayServices():
    sleep(1)
    driver.find_element_by_name("Services").send_keys("food")
    driver.find_element_by_id("Pay_Services").send_keys("399")
    driver.find_element_by_name("K2B").click()
    assert driver.title == "My Dashboard"


def test_KDash_RequestFunds():
    sleep(1)
    driver.find_element_by_name("message").send_keys("Hi, Dad. I need money to buy my new set of school books.")
    driver.find_element_by_name("req_amount").send_keys("2099")
    driver.find_element_by_name("Request").click()
    assert driver.title == "My Dashboard"


def test_KDash_History():
    sleep(1)
    driver.find_element_by_name("my_spends").click()
    assert driver.title == "My Transactions"


def test_KDash_Back_from_History():
    sleep(1)
    driver.find_element_by_name("back_to_home").click()
    assert driver.title == "My Dashboard"


def test_KDash_QuizModule():
    sleep(1)
    driver.find_element_by_name("my_quiz").click()
    assert driver.title == "QUIZ"


def test_KDash_Back_from_QuizModule():
    sleep(1)
    driver.find_element_by_name("backtoDash").click()
    assert driver.title == "My Dashboard"


def test_KDash_Logout():
    sleep(1)
    driver.find_element_by_name("log_me_out").click()
    assert driver.title == "Pigge Home Page"
    driver.implicitly_wait(10)
    driver.close()
