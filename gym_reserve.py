from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import http.client
import subprocess
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 创建一个 WebDriver 实例
driver = webdriver.Edge()

#构建一个字典，存储体育场馆和url对应关系
gym_url_dict={
    "羽毛球":"https://gym.sysu.edu.cn/product/show.html?id=161",
    "网球":"https://gym.sysu.edu.cn/product/show.html?id=101"
}
# url="https://gym.sysu.edu.cn/product/show.html?id=161"
url=gym_url_dict["网球"]
driver.get(url)

time.sleep(1)
# 找到登录按钮
login_button=driver.find_element(By.LINK_TEXT,"登录")
login_button.click()
time.sleep(1)
#找到用户名输入框
username=driver.find_element(By.ID,"username")
username.send_keys("niujh")
#找到密码输入框
password=driver.find_element(By.ID,"password")
password.send_keys("%%NJHnjh00..")
#找到验证码图片
img=driver.find_element(By.ID,"captchaImg")
img.screenshot("captcha.png")
time.sleep(0.5)
#调用云打码识别验证码
info=subprocess.getoutput("python test.py")
# print("captchainfo:",info)
#找到验证码输入框
captcha=driver.find_element(By.ID,"captcha")
captcha.send_keys(info)
#找到submit button
submit_button=driver.find_element(By.NAME,"submit")
submit_button.click()
#登录后重新跳转回最开始页面
driver.get(url)
#找到"预定"按钮
# reserve_button=driver.find_element(By.XPATH,"//*[@id="content"]/div[3]/div/a[1]")
reserve_button=driver.find_element(By.XPATH,"//*[@id='content']/div[3]/div/a[1]")
reserve_button.click()
#根据 id="places"找到对应的 ul标签，打印 "data-col","data-row"属性
places=driver.find_element(By.ID,"places")
print("data-col:",places.get_attribute("data-col"))
print("data-row:",places.get_attribute("data-row"))
lis=places.find_elements(By.TAG_NAME,"li")

available=False

for li in lis:
    #遇到可用场地后，退出循环
    if available:
        break 
    print("="*20)
    #遍历所有的span tag,打印"data-name","data-timer"属性
    spans=li.find_elements(By.TAG_NAME,"span")
    for span in spans:
        print("data-name:",span.get_attribute("data-name"))
        print("data-timer:",span.get_attribute("data-timer"))
        if span.get_attribute("data-stockid")!= "":
            print("当前场地可用")
            #找到有空位的场地，点击预定
            print("data-stockid:",span.get_attribute("data-stockid"))
            span.click()
            available=True
            break
        else:
            print("场地已经被预定")

if available:
    #找到“确认预定”button
    confirm_button=driver.find_element(By.XPATH,"//*[@id='reserve']")
    confirm_button.click()
    #再次找到“确认预定”button
    confirm_button=driver.find_element(By.XPATH,"//*[@id='reserve']")
    confirm_button.click()

    time.sleep(4)
    #找到并打印当前html页面的"title"用做debug
    print("title:",driver.title)
    #查找是否有"id=warning"的div tag
    if len(driver.find_elements(By.ID,"warning"))!=0:
        print("find warning")
    else:
        print("can not find warning")
    
    
    # driver.switch_to.frame()
    # alert=driver.switch_to.alert
    # alert.accept()
    # #更新html 的dom tree
    # driver.refresh()
    #找到"确认"button
    # confirm_button=driver.find_elements(By.CLASS_NAME,"sa-button-container")
    # print("len of confirm_button:",len(confirm_button))

    confirm_button=driver.find_element(By.XPATH,"//*[@id='warning']/div[2]/button[1]")
    confirm_button.click()
    time.sleep(0.5)
    #找到 “立即支付” button
    pay_button=driver.find_element(By.XPATH,"//*[@id='content']/div[1]/div[4]/div/button[2]")
    pay_button.click()
    time.sleep(1)
    #浏览器退出
    driver.quit()