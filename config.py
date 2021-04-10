import gspread

# тестовый бот:
TELEGRAM_TOKEN: str = '1391745018:AAG4cVjkrF7LAPUQst-lslEZd5Fz9r0aDuM'
gc = gspread.service_account()

SHEET_KEY = '1XPcQ6WMOQpA5M8gnAd58HuhfuJONkXOOAJPDEMWf_8c'

group_list = ["1-ТИД-3", "1-ГДА-10", "1-АДА-9"]