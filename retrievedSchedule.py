import os
import string
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import hashlib

retrieve_url = 'http://tkbkmavnteam.tk'
path = os.path.dirname(os.path.realpath(__file__))
download_path = path + '/downloads'

before = os.listdir(download_path)

options = Options()
options.add_experimental_option('prefs', {
    'download.default_directory': download_path,
    'download.prompt_for_download': False,
    'safebrowsing.enabled': False,
    'download.directory_upgrade': True,
    'safebrowsing_for_trusted_sources_enabled': False
})

# username = 'CT020115'
# f = open('password.txt', 'r')
# password = f.readline()
# f.close()

username = str(input('Enter your studentID: '))
password = str(input('Enter your password: '))

driver = webdriver.Chrome(executable_path='{}/chromedriver'.format(path), options=options)
driver.get(retrieve_url)

driver.find_element_by_xpath('/html/body/div[2]/app-root/div[3]/app-login/div/div/div[2]/div[4]').click()
driver.find_element_by_xpath('/html/body/div[2]/app-root/div[3]/app-app-privacy-policy/div/div/div/p/input').click()
driver.find_element_by_xpath('//*[@id="RoomBoxChat"]/div[1]/div[1]/div[3]').click()
driver.find_element_by_tag_name('html').send_keys(Keys.END)

time.sleep(10)

driver.find_element_by_xpath('/html/body/div[2]/app-root/div[3]/app-app-privacy-policy/div/div/div/div').click()
driver.find_element_by_xpath('/html/body/div[2]/app-root/div[2]/ul/li[4]/a/img').click()

driver.find_element_by_xpath('/html/body/div[2]/app-root/div[3]/app-setting-app/div/div/div/div[2]/form/div[2]/div/input').send_keys(username)
driver.find_element_by_xpath('/html/body/div[2]/app-root/div[3]/app-setting-app/div/div/div/div[2]/form/div[3]/div/input').send_keys(password)
driver.find_element_by_xpath('/html/body/div[2]/app-root/div[3]/app-setting-app/div/div/div/div[2]/form/div[4]/button[2]').click()

time.sleep(3)
# headers = driver.find_elements_by_xpath('/html/body/div[2]/app-root/div[3]/app-mainapp/div/div/div[2]/table/tr/td[1]/table/thead/tr/th')
# subjects = driver.find_elements_by_xpath('/html/body/div[2]/app-root/div[3]/app-mainapp/div/div/div[2]/table/tr/td[1]/table/tbody/tr/td')
# print(subjects[1].text, subjects[2].text)

# sub_table = []
# for _ in headers:
#     sub_table.append((_.text, []))

# for i in range(len(subjects)):
#     if i % 3 == 0:
#         sub_table[0][1].append(subjects[i].text)
#     elif i % 3 == 1:
#         sub_table[1][1].append(subjects[i].text)
#     else:
#         sub_table[2][1].append(subjects[i].text)

# driver.quit()

# Dict = {title: column for (title, column) in sub_table}
# print(Dict)
# df = pd.DataFrame(Dict)
# df.to_excel('schedule.xlsx', sheet_name='Sheet_name_1')

download_btn = driver.find_element_by_xpath('/html/body/div[2]/app-root/div[2]/ul/li[1]/a/img')
download_btn.click()
time.sleep(2)
file_download_formatter = driver.find_element_by_xpath('/html/body/div[2]/app-root/div[4]/div/div[2]/div[1]/div/img')
file_download_formatter.click()

driver.close()

after = os.listdir(download_path)
change = set(after) - set(before)
filename = None
if len(change) == 1:
    filename = change.pop()

# convert HTML file to Dictionary
html_file = download_path + '/' + filename
f = open(html_file, 'r')
content = f.read()
f.close()

df = pd.read_html(content)
dfsubpart1 = df[1]
dfsubpart2 = df[2]
dfschedule = df[3]

writer = pd.ExcelWriter('outp.xlsx', engine='xlsxwriter')
dfsubpart1.to_excel(writer, sheet_name='Sheet1', startcol=3)
dfsubpart2.to_excel(writer, sheet_name='Sheet1', startcol=8)
dfschedule.to_excel(writer, sheet_name='Sheet1', startrow=8)

book = writer.book
sheet = writer.sheets['Sheet1']
wrap_format = book.add_format({'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})

d = dict(zip(range(26), list(string.ascii_uppercase)))
for col in range(dfschedule.shape[1] + 1):
    excel_header = d[col] + ':' + d[col]
    sheet.set_column(excel_header, None, wrap_format)

for col in range(dfschedule.shape[1] + 1):
    if col > 2:
        excel_header = d[col] + ':' + d[col]
        sheet.set_column(excel_header, 25, wrap_format)

writer.save()