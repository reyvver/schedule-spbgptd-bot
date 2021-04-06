import gspread

# основной бот:
# TELEGRAM_TOKEN: str = '1333510013:AAFEgog3vcn_QtQWDITyrOyqlZXH-I23l68'
# gc = gspread.service_account(filename='service_account.json')

# тестовый бот:
TELEGRAM_TOKEN: str = '1391745018:AAG4cVjkrF7LAPUQst-lslEZd5Fz9r0aDuM'
gc = gspread.service_account()

SHEET_KEY = '1XPcQ6WMOQpA5M8gnAd58HuhfuJONkXOOAJPDEMWf_8c'

group_list = ["1-ТИД-3", "1-ГДА-10", "1-АДА-9"]