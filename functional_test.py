# coding = utf-8

# 第一个TDD测试的脚本

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://localhost:8000/")
assert "Django" in driver.title
driver.close()

# driver.close()关闭当前窗口
# driver.quit()退出驱动关闭所有窗口
