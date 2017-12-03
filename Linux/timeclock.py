import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('timeclockapi.json', scope)
client = gspread.authorize(credentials)

def loop():
    #get input from arduino part
    #put it in spreadsheet
    pass

if __name__ == '__main__':
    while True:
        loop()
