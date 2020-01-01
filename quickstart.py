import string
import pandas as pd

f = open('TKBKMAVN-guest.html')
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