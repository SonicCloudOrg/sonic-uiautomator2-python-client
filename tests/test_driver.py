from uia2.driver import AndroidDriver


class TestDriver:

    def test_new_session(self):
        AndroidDriver("http://localhost:6790")
