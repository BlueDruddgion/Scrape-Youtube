import string
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import hashlib
import pandas as pd
# import openpyxl
# from openpyxl.utils.dataframe import dataframe_to_rows
# from openpyxl.styles import Alignment

url = 'http://qldt.actvn.edu.vn/CMCSoft.IU.Web.Info/Login.aspx'
table_url = 'http://qldt.actvn.edu.vn/CMCSoft.IU.Web.Info/Reports/Form/StudentTimeTable.aspx'

username = 'CT020115'
f = open('password.txt', 'r')
password = f.readline()
f.close()

# encrypted_password = hashlib.md5(password.encode())

path = os.path.dirname(os.path.realpath(__file__))

driver = webdriver.Chrome(executable_path='{}/chromedriver'.format(path))
driver.get(url)
# driver.close()
# logined to verify authentication
driver.find_element_by_id('txtUserName').send_keys(username)
driver.find_element_by_id('txtPassword').send_keys(password)
driver.find_element_by_id('btnSubmit').click()

driver.get(table_url)
# page = driver.page_source
table = driver.find_element_by_xpath('//*[@id="gridRegistered"]')
tr_elements = table.find_elements_by_xpath('.//tr')
headers = tr_elements[0].find_elements_by_xpath('.//td')
col = []

for _ in headers:
    col.append((_.text, []))

for j in range(1, len(tr_elements)):
    T = tr_elements[j].find_elements_by_xpath('.//td')

    i = 0
    for t in T:
        # text = t.text.replace('\n', '\r\n')
        col[i][1].append(t.text)
        i += 1
    
driver.close()

Dict = {title: column for (title, column) in col}
df = pd.DataFrame(Dict)
print(df)

# writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
# df.to_excel(writer, sheet_name='Sheet1', index=False)
# book = writer.book
# sheet = writer.sheets['Sheet1']
# wrap_format = book.add_format({'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})

# d = dict(zip(range(26), list(string.ascii_uppercase)))
# for col in range(df.shape[1]):
#     excel_header = d[col] + ':' + d[col]
#     sheet.set_column(excel_header, None, wrap_format)
# sheet.set_column('B:B', 35, wrap_format)
# sheet.set_column('D:D', 35, wrap_format)
# sheet.set_column('E:E', 20, wrap_format)
# sheet.set_column('F:F', 20, wrap_format)

# writer.save()

# book = openpyxl.Workbook()
# sheet = book.active

# for r_idx, row in enumerate(rows, 1):
#     for c_idx, value in enumerate(row, 1):   
#         sheet.cell(row=r_idx, column=c_idx, value=value)

# for i in range(2, df.shape[0] + 1):
#     sheet.row_dimensions[i].height = 150

# sheet.delete_rows(2)
# sheet.column_dimensions['C'].width = 35
# sheet.column_dimensions['E'].width = 50
# sheet.column_dimensions['F'].width = 25
# sheet.column_dimensions['G'].width = 20

# for col in sheet.columns:
#     for cell in col:
#         cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

# book.save('output.xlsx')