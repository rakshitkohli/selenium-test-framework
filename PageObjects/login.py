from selenium.webdriver.common.by import By

from PageObjects.shop import ShopPage
from utils.browserutils import BrowserUtils


class LoginPage(BrowserUtils):
    def __init__(self, driver):   #self is a class instance & will be assigned by default for every class method & cons.
        super().__init__(driver)  # initialized our parent class constructor with the same driver
        self.driver = driver
        self.username_input = (By.ID, "username")  # self has access to entire class and with it scope doesn't dies
        self.password = (By.NAME, "password")
        self.sign_button = (By.ID, "signInBtn")

#above we added driver as an argument to the constructor , without it no one can call this class above
# if you declare your locators in constructor, as the scope dies within the constructor,
# we can access it outside using self class instance by attaching it

    def login(self, username,password):  # U and P has to be driven from test !
        self.driver.find_element(*self.username_input).send_keys(username)
        #find element basically takes two arguments, and we are sending tuple,
        # and find element method expects arguments so we will use * before it so it breaks down and splits into two parameters
        #we can unpack tuple using * prefix
        ##### #here locators are not even present in this action methods
        #### everything is derived from constructor and we have used smart self keywords to fix this
        self.driver.find_element(*self.password).send_keys(password)
        self.driver.find_element(*self.sign_button).click()

        shop_page = ShopPage(self.driver) # we kept this here bc this login method will end up in a new page- shop one
        return shop_page    # this above login method is returning shop page object

