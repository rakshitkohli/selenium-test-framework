import json
import os.path
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# if we are getting no module named "pageobjects" error in terminal
# with above LOC, we can go to directory name, from there to absolute path, & it will append to my system path


from PageObjects.login import LoginPage

# with below loc we can traverse relatively from test to data path
test_data_path = "C:/Users/HP/Downloads/test_framework/data/test_e2ePOP.json"  # to come out of folder and come at project level ../
# to read the json file we will use below LOC
with open(test_data_path) as f:
    test_data = json.load(f)  # the load method will convert json file into python object
    test_list = test_data["data"]  # all the value present in the 'data' will be retrieved and we will store that list in one variable


# SO NOW WE WILL SEND THAT TEST LIST BELOW FOR PARAMETRIZATION, Used TLI variable to store list
# @pytest.mark.smoke   # used to run only some particular pytest
@pytest.mark.parametrize("test_list_item",test_list)  # with this annotation we are clearly telling that this test is going to get parametrized
# from param. annotation, it has to go as an argument, so added test_list_item below
def test_e2e(browserInstance, test_list_item):  # we passed the fix name inside this as an argument
    driver = browserInstance
    # driver.get("https://rahulshettyacademy.com/loginpagePractise/")
    # this driver has to be sent to the page object, from our TEST
    loginPage = LoginPage(driver)  # the real driver that we created in the test , we are sending as an argument
    print(loginPage.getTitle())  # automatically came cos of inheritance
    # loginPage.login()   #removed bc we will only create a page object class in the beginning of login page
    # shop_page = ShopPage(driver)                 # create first object for that page
    shop_page = loginPage.login(test_list_item["userEmail"], test_list_item[
        "userPassword"])  # now coming from login.py, we will send those username and passwrd as an arguments
    shop_page.add_product_to_cart(test_list_item["productName"])
    print(shop_page.getTitle())
    # shop_page.goToCart()
    checkout_confirmation = shop_page.goToCart()
    # above step can directly catch object here instead of creating another object creation step,
    # we encapsulated that in the method itself

    checkout_confirmation.checkout()
    checkout_confirmation.enter_delivery_address("Ind")  # test data should be sent from your test
    checkout_confirmation.validate_order()
