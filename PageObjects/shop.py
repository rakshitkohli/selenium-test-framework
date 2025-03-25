# all actions performed in the shop page entirely, need to encapsulate in one class file
from selenium.webdriver.common.by import By

from PageObjects.checkout_confirmation import Checkout_Confirmation
from utils.browserutils import BrowserUtils


class ShopPage(BrowserUtils):

    def __init__(self,driver):
        super().__init__(driver)  # passed driver to get the title // lec97
        self.driver = driver
        self.shop_link = (By.CSS_SELECTOR, "a[href*='shop']")
        self.product_cards = (By.XPATH, "//div[@class='card h-100']")
        self.checkout_button = (By.CSS_SELECTOR, "a[class*='btn-primary']")

    def add_product_to_cart(self,product_name):  # this method is expecting one product name as an argument, and that test data should come from test_ only
                                                                        # page object should not have test data
        self.driver.find_element(*self.shop_link).click()
        products = self.driver.find_elements(*self.product_cards)

        for product in products:
            productName = product.find_element(By.XPATH, "div/h4/a").text  # sub locators that are specific
            if productName == product_name:
                product.find_element(By.XPATH, "div/button").click()

    def goToCart(self):
        self.driver.find_element(*self.checkout_button).click()
        checkout_confirmation = Checkout_Confirmation(self.driver) # we need to send driver bc class expects driver as an argument in that constructor
        # here itself lets create object for that checkout confirmation
        return checkout_confirmation  # its use  , we eliminated - shop_page.goToCart() STEP

