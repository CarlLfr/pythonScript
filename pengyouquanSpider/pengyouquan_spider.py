import time

from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Wechat_Moment(object):
    def __init__(self):
        desired_caps = {}
        desired_caps['platformName'] = "Android"
        desired_caps['platformVersion'] = "5.1.1"
        desired_caps['deviceName'] = "127.0.0.1:62026"
        desired_caps['appPackage'] = "com.tencent.mm"
        desired_caps['appActivity'] = ".ui.LauncherUI"
        # desired_caps['noReset'] = "True"

        # 定义在朋友圈时候的滑动位置(根据手机像素屏幕大小合理设置)
        self.start_x = 300
        self.start_y = 800
        self.end_x = 300
        self.end_y = 300

        # 需要搜索的朋友圈名字
        # self.name = input("请输入朋友圈名字：")

        # 启动微信
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        # 设置等待
        self.wait = WebDriverWait(self.driver, 200)
        print("微信启动...")

    # 登录微信方法
    def login(self):
        # 获取到登录按钮后点击
        login_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/e80")))
        login_btn.click()

        # 获取"用微信号/QQ号/邮箱登录"按钮后点击
        change_login_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/cqb")))
        change_login_btn.click()

        # 获取用户名输入框并输入用户名
        userName_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/cq_"]/android.widget.EditText')))
        userName_btn.send_keys("lfr490635974")

        # 获取密码输入框并输入密码
        password_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/cqa"]/android.widget.EditText')))
        password_btn.send_keys("*********")

        # 获取登录按钮元素并点击
        register_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/cqc")))
        register_btn.click()

        # 获取查看手机通讯录提示的否定按钮元素后点击
        no_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/azz")))
        no_btn.click()

        print("登录成功...")

        # 等待数据加载成功
        # time.sleep(10)

    # 进入自己的朋友圈
    def go_to_pengyouquan(self):
        # 点击"我的"按钮进入
        my_xpath = '//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout[@index=2]'
        my_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, my_xpath)))
        my_btn.click()

        # 点击'朋友圈'进入朋友圈
        pyq_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.ListView/android.widget.LinearLayout[@index=0]')))
        pyq_btn.click()

        # 朋友圈点击我的头像
        my_head_btn = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/qk')))
        my_head_btn.click()

        # 再次点击朋友圈
        again_pyq_btn = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/d9u')))
        again_pyq_btn.click()

        print("进入朋友圈...")

    def get_data(self):
        while True:
            # 获取ListView
            items = self.wait.until(EC.presence_of_all_elements_located((By.ID, 'com.tencent.mm:id/m5')))

            # 滑动朋友圈
            self.driver.swipe(self.start_x, self.start_y, self.end_x, self.end_y, 2000)

            # 遍历获取每个list数据
            for item in items:
                try:
                    content_text = item.find_element_by_id('com.tencent.mm:id/o7').text
                except:
                    content_text = "无"

                day_text = item.find_element_by_id('com.tencent.mm:id/eo2').text
                mouth_text = item.find_element_by_id('com.tencent.mm:id/eo3').text
                print("%s%s发表朋友圈：%s" % (mouth_text, day_text, content_text))

if __name__ == '__main__':
    wechat_moment = Wechat_Moment()
    wechat_moment.login()
    wechat_moment.go_to_pengyouquan()
    wechat_moment.get_data()