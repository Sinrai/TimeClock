import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import socket
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)
urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)

# get Google Drive API with credentials
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('timeclock/timeclockapi.json', scope)
client = gspread.authorize(credentials)

########################################################################################################################

# add new participant to worksheet #0
def new_participant(sheetid, index):
    worksheet = sheet.get_worksheet(0)
    worksheet.update_cell(sheetid + 1, 1, sheetid)
    worksheet.update_cell(sheetid + 1, 2, index)
    worksheet.update_cell(sheetid + 1, 5, '=Sum(%i!D$3:D)' % index)

# add new worksheet
def new_worksheet(index):
    worksheet = sheet.add_worksheet(str(index), 2, 4)
    sheetid = len(sheet.worksheets())-1
    worksheet.update_cell(1, 1, "='Uebersicht'!C%i" % (sheetid+1))
    worksheet.update_cell(1, 2, "='Uebersicht'!D%i" % (sheetid+1))
    worksheet.update_cell(2, 1, 'Datum')
    worksheet.update_cell(2, 2, 'Ein')
    worksheet.update_cell(2, 3, 'Aus')
    worksheet.update_cell(2, 4, 'Total')
    timestamp_in(worksheet, datetime.datetime.now(), 2)
    new_participant(sheetid, index)

########################################################################################################################

# make formats like 12:04 instead of 12:4
def format_minute(minute):
    if len(minute) < 2:
        minute = '0%s' % minute
    return minute

# timestamp when in
def timestamp_in(worksheet, time, row):
    date = str(time.date())
    hour = str(time.time().hour)
    minute = format_minute(str(time.time().minute))

    worksheet.add_rows(1)
    for i in range(row, 1, -1):
        if worksheet.cell(i, 1).value:
            if worksheet.cell(i, 1).value != date:
                worksheet.update_cell(row + 1, 1, date)
            worksheet.update_cell(row+1, 2, '%s:%s' % (hour, minute))
            break

# timestamp when out
def timestamp_out(worksheet, time, row):
    worksheet.update_cell(row, 3, '%s:%s' % (str(time.time().hour), format_minute(str(time.time().minute))))
    worksheet.update_cell(row, 4, '=C%i-B%i' % (row, row))

# actual timestamp, added directly to defined worksheet
def timestamp(worksheet):
    time = datetime.datetime.now()
    rows = worksheet.row_count
    if rows == 2 or worksheet.cell(rows, 3).value:
        timestamp_in(worksheet, time, rows)
    else:
        timestamp_out(worksheet, time, rows)

########################################################################################################################

# loop to keep script running
def loop():
    # get input from arduino part
    data = s.recv(1024)
    print(data)
    exit()
    
    index = 0

    # get informations
    worksheet = sheet.get_worksheet(0)
    col = worksheet.col_values(2)
    sheetid = None
    for i in range(len(col)):
        if col[i] == str(index):
            sheetid = int(worksheet.cell(i+1, 1).value)
            break

    # create new worksheet with timestamp or just timestamp on existing worksheet
    if not sheetid:
        new_worksheet(index)
    else:
        timestamp(sheet.get_worksheet(sheetid))

########################################################################################################################

# main
if __name__ == '__main__':
    sheet = client.open('Zeiterfassung Tueftelpark')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 5700))
    while True:
        loop()
