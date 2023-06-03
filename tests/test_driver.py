from uia2.driver import AndroidDriver


class TestDriver:

    def test_new_session(self):
        driver = AndroidDriver("http://localhost:6790")
        p = driver.get_page_source()
        print(p)
