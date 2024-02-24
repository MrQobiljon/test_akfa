# import re
#
# # a = "Дата начисления: 21/04/2022"
# # res = re.sub(r"[/\\.]", "-", re.search(r"(\d+.*?\d+.*?\d+)", a).group(1))
# #
# # print(res)
#
# # print(re.fullmatch(r'\d\d\.\d\d\.\d{4}',
# #                  r'Эта строка написана 19.01.2018, а могла бы и 01.09.2017'))
#
# a = re.fullmatch(r'\d\d\.\d\d\.\d{4}', r'19.01.2018')
# # if a:
# #     print('salom')
# # else:
# #     print('no')

# a = {
#     'l': []
# }
#
# print(a)
# del a['l']
# print(a)



# from data.loader import db
#
# db.insert_user(12345678910, "Jaloliddin", '+998991234567', 1)
# db.insert_user(12345678911, "Sobirjon", '+998991234568', 1)
# db.insert_user(12345678912, "Toxirjon", '+998991234569', 1)
# db.insert_user(12345678913, "KAmol", '+998991234570', 1)
# db.insert_user(12345678914, "Bakir", '+998991234571', 1)
# db.insert_user(12345678915, "Davron", '+998991234572', 1)
# db.insert_user(12345678916, "Suhrob", '+998991234573', 1)
# db.insert_user(12345678917, "DIyor", '+998991234574', 1)
# db.insert_user(12345678918, "Javohir", '+998991234575', 1)
# db.insert_user(12345678919, "Kim", '+998991234576', 1)
# db.insert_user(12345678920, "Doon Li", '+998991234577', 1)

# from openpyxl import Workbook
# wb = Workbook()
#
# # grab the active worksheet
# ws = wb.active
#
# # Data can be assigned directly to cells
# ws['A1'] = 42
#
# # Rows can also be appended
# ws.append([1, 2, 3])
#
# # Python types will automatically be converted
# import datetime
# ws['A2'] = datetime.datetime.now()
#
# # Save the file
# wb.save("sample.xlsx")

