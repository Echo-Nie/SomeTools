from selenium import webdriver  # 导入webdriver模块，用于浏览器自动化操作
from selenium.webdriver.common.by import By  # 元素定位策略
from selenium.webdriver.support import expected_conditions as EC  # 预期条件
from selenium.webdriver.support.wait import WebDriverWait  # 显式等待
from selenium.common.exceptions import NoSuchElementException, TimeoutException  # 异常处理
import time  # 时间操作
import ast  # 抽象语法树，用于安全地解析字符串为Python对象
from selenium.webdriver.chrome.service import Service  # Chrome服务配置
import pytesseract  # OCR库，用于从图像中提取文本
from PIL import ImageGrab, Image  # 图像处理库
import cv2  # OpenCV库，用于图像处理
import numpy as np  # 数值计算库
import ddddocr  # 一个开源OCR库，用于验证码识别


class AutoLogin:
    def __init__(self, url, path, name='', pswd=''):
        """
        初始化函数，设置webdriver路径、用户名和密码。
        :param url: 登录页面URL
        :param path: ChromeDriver路径
        :param name: 用户名
        :param pswd: 密码
        """
        service = Service(path)  # 设置ChromeDriver服务
        self.driver = webdriver.Chrome(service=service)  # 创建Chrome浏览器实例
        self.name = name  # 设置用户名
        self.url = url  # 设置登录页面URL
        self.pswd = pswd  # 设置密码

    def get_params(self):
        """
        获取必要的参数并尝试登录。如果验证码不正确则重试。
        """
        while True:
            self.driver.get(self.url)  # 打开登录页面
            self.driver.implicitly_wait(3)  # 设置隐式等待时间
            # 填写用户名和密码字段
            name_ele = self.driver.find_element(By.XPATH, '//input[@id="loginName"]')
            name_ele.send_keys(self.name)
            pswd_ele = self.driver.find_element(By.XPATH, '//input[@id="loginPwd"]')
            pswd_ele.send_keys(self.pswd)
            time.sleep(1.5)

            try:
                # 尝试获取验证码图片并保存
                self.driver.find_element(By.XPATH, '//*[@id="vcodeImg"]').screenshot("img.png")
            except (NoSuchElementException, TimeoutException):
                continue  # 如果找不到元素，则重试

            # 图像预处理：读取原始图像 -> 转换为灰度图 -> 保存处理后的图像
            image = cv2.imread('img.png')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite('gray.png', gray)

            ocr = ddddocr.DdddOcr()  # 初始化ddddocr对象
            with open('img.png', 'rb') as f:
                img_bytes = f.read()
            res = ocr.classification(img_bytes)  # 使用ddddocr进行验证码识别
            print(f"识别验证码是：{res}")

            if len(res) != 4:  # 如果验证码长度不是4位数，则重试
                continue

            # 输入验证码并点击登录按钮
            self.driver.find_element(By.XPATH, '//input[@id="verifyCode"]').send_keys(res)
            submit_button = self.driver.find_element(By.ID, 'studentLoginBtn')
            submit_button.click()

            try:
                # 等待“确定”按钮出现，并点击它
                confirm_button = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@id="buttons"]//button[contains(text(), "确定")]'))
                )
                confirm_button.click()
                print("点击了确定按钮")
            except TimeoutException:
                print("Timed out waiting for the element to appear")
                continue

            # 点击“开始选课”按钮
            course_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, 'courseBtn'))
            )
            course_button.click()
            time.sleep(2)
            break

        # 自动选课逻辑
        if WebDriverWait(self.driver, 180).until(EC.presence_of_element_located((By.ID, 'aPublicCourse'))):
            time.sleep(1)  # 等待加载完成
            cookie_lis = self.driver.get_cookies()  # 获取cookie列表
            cookies = ''
            for item in cookie_lis:
                cookies += item['name'] + '=' + item['value'] + '; '
            token = self.driver.execute_script('return sessionStorage.getItem("token");')  # 获取sessionStorage中的token
            batch_str = self.driver.execute_script('return sessionStorage.getItem("currentBatch");').replace('null', 'None').replace('false', 'False').replace('true', 'True')
            batch = ast.literal_eval(batch_str)  # 安全地将字符串转换为Python对象
            self.driver.quit()  # 关闭浏览器

            return cookies, token, batch['code']
        else:
            print('page load failed')
            self.driver.quit()
            return False

    def keep_connect(self):
        """
        维持连接的函数（目前未使用）。
        """
        flag = 1
        st = time.perf_counter()
        while True:
            try:
                if flag == 1:
                    ele = self.driver.find_element(By.XPATH, '//a[@id="aPublicCourse"]')
                    ele.click()
                    flag = 2
                    time.sleep(30)
                elif flag == 2:
                    ele = self.driver.find_element(By.XPATH, '//a[@id="aProgramCourse"]')
                    ele.click()
                    flag = 1
                    time.sleep(30)

            except NoSuchElementException:
                print('连接已断开')
                print(f'运行时间：{(time.perf_counter() - st) // 60} min')
                break


if __name__ == '__main__':
    Url = 'http://xk.ynu.edu.cn/xsxkapp/sys/xsxkapp/*default/index.do'  # 目标网站的URL
    Name = ''  # 用户名
    Pswd = ''  # 密码
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }