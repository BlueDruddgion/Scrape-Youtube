# import string
# import pandas as pd

# f = open('TKBKMAVN-guest.html')
# content = f.read()
# f.close()

# df = pd.read_html(content)
# dfsubpart1 = df[1]
# dfsubpart2 = df[2]
# dfschedule = df[3]

# writer = pd.ExcelWriter('outp.xlsx', engine='xlsxwriter')
# dfsubpart1.to_excel(writer, sheet_name='Sheet1', startcol=3)
# dfsubpart2.to_excel(writer, sheet_name='Sheet1', startcol=8)
# dfschedule.to_excel(writer, sheet_name='Sheet1', startrow=8)

# book = writer.book
# sheet = writer.sheets['Sheet1']
# wrap_format = book.add_format({'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})

# d = dict(zip(range(26), list(string.ascii_uppercase)))
# for col in range(dfschedule.shape[1] + 1):
#     excel_header = d[col] + ':' + d[col]
#     sheet.set_column(excel_header, None, wrap_format)

# for col in range(dfschedule.shape[1] + 1):
#     if col > 2:
#         excel_header = d[col] + ':' + d[col]
#         sheet.set_column(excel_header, 25, wrap_format)

# writer.save()


import os
import pandas as pd
import string
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

retrieve_url = 'http://tkbkmavnteam.tk'
path = os.path.dirname(os.path.realpath(__file__))
download_path = path + '/image'
options = Options()
options.add_experimental_option('prefs', {
    'download.default_directory': download_path,
    'download.prompt_for_download': False,
    'safebrowsing.enabled': False,
    'download.directory_upgrade': False,
    'safebrowsing_for_trusted_sources_enabled': False
})

before = os.listdir(download_path)

# username = input('Enter your ID: ')
# password = input('Enter your password: ')
username = 'CT020115'
password = 'falcon99'

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

time.sleep(5)
driver.find_element_by_xpath('/html/body/div[2]/app-root/div[2]/ul/li[1]/a/img').click()
driver.find_element_by_xpath('/html/body/div[2]/app-root/div[4]/div/div[2]/div[2]/div/img').click()
time.sleep(5)
driver.close()

print(download_path)
after = os.listdir(download_path)
change = set(after) - set(before)
filename = None
if len(change) == 1:
    filename = change.pop()
print('--- Saved into image named {}'.format(filename))