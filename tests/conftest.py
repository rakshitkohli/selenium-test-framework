
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

driver = None  # initially the global variable is none


def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="Chrome", help="browser selection")


# we need to do above step before we can make browser step work, we need to register our options from terminal
@pytest.fixture(scope="function")  # used bc it is generic thing every test file will require
def browserInstance(request):  # request is default parameter globally available for whole framework
    global driver            # used for html reports so that driver is picked from globally
    browser_name = request.config.getoption("--browser_name")  # will help switching based on what browser name we get
    service_obj = Service()
    if browser_name == "Chrome":
        driver = webdriver.Chrome(service=service_obj)
    elif browser_name == "Firefox":
        driver = webdriver.Firefox(service=service_obj)

    driver.implicitly_wait(5)
    driver.get("https://rahulshettyacademy.com/loginpagePractise/")

    yield driver  # using yield means driver will be sent back
    # need not to put --before browser when using get option

    driver.close()  # will run post test function execution // TEARDOWN CONCEPT

    # after yield whatever step we write, fixture will execute steps before yield,
    # and then it will go inside code and execute all function code,
    # and once everything inside the code block is done, it will again revisit the fixture
    # to see if there is any code return after the yield driver


# for taking screenshots in html reports ( copied from html plugin )

@pytest.hookimpl(hookwrapper=True)  # if any of pytest fails, immediately this block will get executed
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            reports_dir = os.path.join(os.path.dirname(__file__), 'reports')  # here asking to go to that directory where project is running and from there go to reports folder
            os.makedirs(reports_dir, exist_ok=True)  # Ensure reports directory exists #CHATGPT
            file_name = os.path.join(reports_dir, report.nodeid.replace("::", "_") + ".png")
            print("file name is " + file_name)
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name

                extra.append(pytest_html.extras.html(html))
        report.extras = extra


def _capture_screenshot(file_name):
    # below code copied from CHATGPT
    if driver is None:
        print("ERROR: WebDriver instance is None, cannot take a screenshot.")
        return

    os.makedirs(os.path.dirname(file_name), exist_ok=True)  # Ensure folder exists
    success = driver.get_screenshot_as_file(file_name)

    if success:
        print(f"Screenshot successfully saved at: {file_name}")
    else:
        print(f"Failed to save screenshot at: {file_name}")


