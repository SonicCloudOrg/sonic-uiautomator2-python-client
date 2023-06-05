<p align="center">
  <img width="80px" src="https://raw.githubusercontent.com/SonicCloudOrg/sonic-server/main/logo.png">
</p>
<p align="center">🎉The Python Client of appium-uiautomator2-server</p>
<p align="center">
  <span>English |</span>
  <a href="https://github.com/SonicCloudOrg/sonic-uiautomator2-python-client/blob/main/README_CN.md">  
     简体中文
  </a>
</p>
<p align="center">
  <a href="#">  
    <img src="https://img.shields.io/pypi/v/sonic-uia2-client">
  </a>
  <a href="#">  
    <img src="https://img.shields.io/pypi/dm/sonic-uia2-client">
  </a>
</p>


### Background

At present, only one project [appium-uiautomator2-client](https://github.com/xsoloking/appium-uiautomator2-client) that bypasses Appium Server and interacts with appium-uiautomator2-server alone is seen on Github for Python, but it is not compatible The baseUrl of the latest appium-uiautomator2-server v5.x API has not been published on pypi. I tried to contact the author but there was no reply, so I decided to write a maintenance. For the Java version, you can see the [sonic-driver-core](https://github.com/SonicCloudOrg/sonic-driver-core) maintained by our organization.

### How to use

➡️[More Document](https://sonic-cloud.cn/supc/re-supc.html)

1. Install uiautomator2 server

> You should install `sonic-appium-uiautomator2-server.apk` and `sonic-appium-uiautomator2-server-test.apk` in [Here](https://github.com/SonicCloudOrg/sonic-agent/tree/main/plugins).
> 
> Alternatively, you can build your own [Here](https://github.com/SonicCloudOrg/sonic-appium-uiautomator2-server)

2. Launch uiautomator2 server
```bash
adb shell am instrument -w io.appium.uiautomator2.server.test/androidx.test.runner.AndroidJUnitRunner
```

3. Forward ports

```bash
adb forward tcp:6790 tcp:6790
```

4. Install Depends
```bash
pip install -U sonic-uia2-client
```

5. Write your script
```python
from common.models import AndroidSelector
from uia2.driver import AndroidDriver
import os


class TestDriver:

    def __init__(self):
        self.uia_url = "http://localhost:6790"
        self.adb_serial_num = "DAISKnlasido"
        self.package_name = "com.android.settings"

    def test_demo(self):
        # launch App
        os.system(
            "adb -s {} shell monkey -p {} -c android.intent.category.LAUNCHER 1".format(self.adb_serial_num,
                                                                                        self.package_name))
        
        # connect remote uia2 server
        driver = AndroidDriver(self.uia_url)
        p = driver.get_page_source()
        print(p)
        e = driver.find_element(AndroidSelector.XPATH, "//*[@text='设置']")
        if e is not None:
            print(e.get_text())
            e.send_keys("Hello")
```

### Thanks

- [appium/appium-uiautomator2-server](https://github.com/appium/appium-uiautomator2-server)
- [xsoloking/appium-uiautomator2-client](https://github.com/xsoloking/appium-uiautomator2-client)

### LICENSE
[LICENSE](LICENSE)
