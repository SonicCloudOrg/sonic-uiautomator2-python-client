from common.models import AndroidSelector
from uia2.driver import AndroidDriver


class TestDriver:

    def test_session(self):
        driver = AndroidDriver("http://localhost:6790")
        driver.close_driver()

    def test_page(self):
        driver = AndroidDriver("http://localhost:6790")
        p = driver.get_page_source()
        print(p)

    def test_element(self):
        driver = AndroidDriver("http://localhost:6790")
        e = driver.find_element(AndroidSelector.XPATH, "//*[@text='标题']")
        print(e.get_text())
        e.send_keys("Hello")
