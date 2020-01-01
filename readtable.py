from datetime import datetime, timedelta, time
# import datetime
import pandas as pd

# days = []

f = open('datetime.csv', 'r')
days = f.readlines()
f.close()

begins = []; ends = []
for date in days:
    if date.startswith('Từ '):
        begins.append(date[3:13])
        ends.append(date[18:28])


# Dictionary ways
tabledict = {}
# tabledict['Lession'] = ['1-3', '4-6', '7-9', '10-12', '13-16']
lessions = ['Ngay', '1-3', '4-6', '7-9', '10-12', '13-16']

for _ in range(len(begins)):
    bday = datetime.strptime(begins[_], '%d/%m/%Y')
    aday = datetime.strptime(ends[_], '%d/%m/%Y')
    while bday <= aday:
        if bday.strftime('%A') not in tabledict.keys():
            tabledict[bday.strftime('%A')] = [bday.strftime('%d/%m')]
            # tabledict[bday.strftime('%A')].append(bday.strftime('%d/%m'))
        else:
            tabledict[bday.strftime('%A')].append(bday.strftime('%d/%m'))
        bday += timedelta(days=1)

metadata = {}
for _ in tabledict.keys():
    string = ''
    metadata[_] = []
    for value in tabledict[_]:
        string += value + ':'
    metadata[_] = string

print(metadata)

df = pd.DataFrame(metadata, index=lessions)
# df.set_index(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], inplace=False)
# print(df)


# # Tuple in list ways:
# col = []
# days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# for _ in days:
#     col.append((_, []))

# for _ in range(len(begins)):
#     bday = datetime.strptime(begins[_], '%d/%m/%Y')
#     aday = datetime.strptime(ends[_], '%d/%m/%Y')
#     while bday <= aday:
#         result = [item for item in col if item[0] == bday.strftime('%A')]
#         result[0][1].append(bday.strftime('%d/%m'))
#         bday += timedelta(days=1)

# tabledict = {title: column for (title, column) in col}