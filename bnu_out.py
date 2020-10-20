"""
Jinyi 2020.10.20

Tips for REASON
    0   实验科研
    1   校医院就医或办理报销业务
    2   实习、面试、参加考试
    3   志愿服务或社会实践
    4   办理学校（包括职能部门、学院部系或教师）交办的事务
    5   必须出校办理的其它个人事务
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import argparse

parser = argparse.ArgumentParser(description='Fast BNU Application for getting out of school')
parser.add_argument('-work', dest='work', action='store_true', help='Work mode')
parser.add_argument('-play', dest='play', action='store_true', help='Play mode')
parser.add_argument('-diy',  dest='diy', action='store', default=[], nargs=4, help='DIY your application [REASON, DOWHAT, WHERE, WHO]')
args = parser.parse_args()


# Fixed Params
URL = 'https://cas.bnu.edu.cn'
ID = 'your_student_ID'
PW = 'your_password'
PHONE = 'phone_number'
DORM = 'dorm. address'
ATTACH = '/home/bnu/Ray.png'

# Custom
assert args.work or args.play or args.diy, 'At least one argument required.'
if args.work:
    REASON = '0'
    DOWHAT = '见导师'
    WHERE = '南苑'
    WHO = '导师'
elif args.play:
    REASON = '5'
    DOWHAT = '玩耍'
    WHERE = '慕田峪'
    WHO = '帅哥靓女'
elif args.diy:
    REASON, DOWHAT, WHERE, WHO = args.diy


options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
# driver = webdriver.Firefox()
driver.get(URL)

# Login
print('Login to OneBNU.')
driver.find_element_by_id('un').send_keys(ID)
driver.find_element_by_id('pd').send_keys(PW)
driver.find_element_by_id('index_login_btn').click()
time.sleep(4)

# Enter Onehall and switch window
print('Enter Onehall.')
driver.find_element_by_id('onehall').click()
time.sleep(4)
driver.switch_to.window(driver.window_handles[-1])
driver.find_element_by_class_name('layui-laypage-next').click()
time.sleep(1)
driver.find_element_by_name('学生临时出校申请').click()
time.sleep(6)
driver.find_elements_by_id('mag_take_cancel')[1].click() # 我已阅读并确认
time.sleep(1)

# Fill
print('Fill in the Application form.')
driver.switch_to.frame(driver.find_element_by_id('formIframe'))
driver.find_element_by_name('联系电话').send_keys(PHONE)
driver.find_element_by_name('宿舍楼及宿舍号' ).send_keys(DORM)

driver.find_element_by_xpath("//*[@data-id='outarea']").click() # 出校区域
driver.find_element_by_xpath("//li[@rel='0']").click() # 本校区

driver.find_elements_by_xpath("//*[@class='van-radio van-radio--horizontal']")[0].click() # 当天返校
driver.find_elements_by_xpath("//*[@class='van-radio van-radio--horizontal']")[3].click() # 不出京

driver.find_element_by_name('出校日期').click()
driver.switch_to.default_content()
driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@hidefocus='true']"))
driver.find_element_by_id('dpTodayInput').click()
driver.switch_to.default_content()
driver.switch_to.frame(driver.find_element_by_id('formIframe'))

driver.find_element_by_name('返校日期').click()
driver.switch_to.default_content()
driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@hidefocus='true']"))
driver.find_element_by_id('dpTodayInput').click()
driver.switch_to.default_content()
driver.switch_to.frame(driver.find_element_by_id('formIframe'))

driver.find_element_by_xpath("//*[@data-id='fenlei']").click() # 出校原因
driver.find_elements_by_xpath("//li[@rel=\'%s\']" % REASON)[ 1 if int(REASON) < 3 else 0].click()

driver.find_element_by_id('CXYY').send_keys(DOWHAT) # 具体事由

driver.find_element_by_id('WCDD').send_keys(WHERE) # 外出地点

driver.find_element_by_id('JCRQ').send_keys(WHO) # 主要接触人群

driver.find_element_by_id('btn_uploader_0').send_keys(ATTACH) # 上传附件
time.sleep(2)


# Commit and Quit
print('Commit.')
driver.switch_to.default_content()
driver.find_element_by_id('commit').click()
time.sleep(1)
driver.quit()
print('Done!')
