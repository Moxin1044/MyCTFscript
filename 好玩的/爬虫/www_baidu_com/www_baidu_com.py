from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

# 打开百度搜索页面
driver.get("https://www.baidu.com")

# 定位搜索输入框，并输入关键词
search_box = driver.find_element(By.ID, "kw")
# search_box = driver.by_something("kw")
search_box.send_keys("测试搜索")

# 模拟键盘按下回车键
search_box.send_keys(Keys.RETURN)

# 等待搜索结果加载
time.sleep(3)

# 打印搜索结果
results = driver.find_elements(By.CSS_SELECTOR, ".t")
for result in results:
    text = result.text
    print(f"文本：{text}")

# 关闭浏览器
driver.quit()