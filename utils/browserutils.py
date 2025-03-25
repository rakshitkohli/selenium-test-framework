# To apply inheritance concept in python,
# all you need to do is open brackets on child classes.. i.e class loginpage(browserutils):

class BrowserUtils:

    def __init__(self, driver):
        self.driver = driver

    def getTitle(self):
        return self.driver.title
