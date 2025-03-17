from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import ast
from selenium.webdriver.chrome.service import Service
import pytesseract
from PIL import ImageGrab, Image
import cv2
import numpy as np
import ddddocr


class AutoLogin:
    def __init__(self, url, path, name='', pswd=''):
        service = Service(path)
        self.driver = webdriver.Chrome(service=service)
        self.name = name
        self.url = url
        self.pswd = pswd

    def get_params(self):
        # 获得必要参数
        while (True):
            # 打开网页
            self.driver.get(self.url)
            self.driver.implicitly_wait(3)
            # 填入字段
            name_ele = self.driver.find_element(By.XPATH, '//input[@id="loginName"]')
            name_ele.send_keys(self.name)
            pswd_ele = self.driver.find_element(By.XPATH, '//input[@id="loginPwd"]')
            pswd_ele.send_keys(self.pswd)
            time.sleep(1.5)
            # 等待vcodeImg加载
            try:
                # 保存验证码图像
                self.driver.find_element(By.XPATH, '//*[@id="vcodeImg"]').screenshot("img.png")
            except NoSuchElementException or TimeoutException:
                continue

            # 读取彩色图像
            image = cv2.imread('img.png')
            # 灰度图像
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # 保存处理后的图像为新文件
            cv2.imwrite('gray.png', gray)
            ocr = ddddocr.DdddOcr()
            with open('img.png', 'rb') as f:
                img_bytes = f.read()
            res = ocr.classification(img_bytes)
            print(f"识别验证码是：{res}")
            # 如果验证码长度不为4位，直接重开
            if len(res) != 4:
                continue
            # 填入验证码
            self.driver.find_element(By.XPATH, '//input[@id="verifyCode"]').send_keys(res)
            # 点击登录
            submit_button = self.driver.find_element(By.ID, 'studentLoginBtn')
            submit_button.click()
            # time.sleep(2)
            try:
                # 等待“确定”按钮出现，最多等待12秒
                confirm_button = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@id="buttons"]//button[contains(text(), "确定")]'))
                )
                # 点击“确定”按钮
                confirm_button.click()
                print("点击了确定按钮")
            except TimeoutException:
                print("Timed out waiting for the element to appear")
                continue

            # “开始选课”按钮
            # courseBtn
            course_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, 'courseBtn'))
            )
            # 点击“开始选课”按钮
            course_button.click()
            time.sleep(2)
            break

        #自动选课逻辑
        if WebDriverWait(self.driver, 180).until(EC.presence_of_element_located((By.ID, 'aPublicCourse'))):
            time.sleep(1)  # waiting for loading
            cookie_lis = self.driver.get_cookies()
            cookies = ''
            for item in cookie_lis:
                cookies += item['name'] + '=' + item['value'] + '; '
            token = self.driver.execute_script('return sessionStorage.getItem("token");')
            batch_str = self.driver. \
                execute_script('return sessionStorage.getItem("currentBatch");').replace('null', 'None').replace(
                'false', 'False').replace('true', 'True')
            batch = ast.literal_eval(batch_str)
            self.driver.quit()

            return cookies, token, batch['code']

        else:
            print('page load failed')
            self.driver.quit()
            return False

    # 暂时无用
    def keep_connect(self):
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
                # self.driver.quit()
                break


if __name__ == '__main__':
    Url = 'http://xk.ynu.edu.cn/xsxkapp/sys/xsxkapp/*default/index.do'
    Name = ''
    Pswd = ''
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.116 Safari/537.36'
    }
