import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('timeclockapi.json', scope)
client = gspread.authorize(credentials)

########################################################################################################################

def newParticipant(sheetid, index):
    worksheet = sheet.get_worksheet(0)
    worksheet.update_cell(sheetid + 1, 1, sheetid)
    worksheet.update_cell(sheetid + 1, 2, index)
    worksheet.update_cell(sheetid + 1, 5, '=Sum(%i!D3:D)' % index)

def newWorksheet(index):
    worksheet = sheet.add_worksheet(str(index), 2, 4)
    sheetid = len(sheet.worksheets())-1
    newParticipant(sheetid, index)
    worksheet.update_cell(1, 1, "='Uebersicht'!C%i" % (sheetid+1))
    worksheet.update_cell(1, 2, "='Uebersicht'!D%i" % (sheetid+1))
    worksheet.update_cell(2, 1, 'Datum')
    worksheet.update_cell(2, 2, 'Ein')
    worksheet.update_cell(2, 3, 'Aus')
    worksheet.update_cell(2, 4, 'Total')
    return sheetid

########################################################################################################################

def loop():
    # get input from arduino part
    debuginput = input() # type int
    index = debuginput

    worksheet = sheet.get_worksheet(0)
    col = worksheet.col_values(2)
    sheetid = None
    for i in range(256):
        if col[i] == str(index):
            sheetid = int(worksheet.cell(i+1, 1).value)
            break
    if not sheetid:
        sheetid = newWorksheet(index)
    worksheet = sheet.get_worksheet(sheetid)

    # do stuff
    time = datetime.now()

    print worksheet


if __name__ == '__main__':
    sheet = client.open('Zeiterfassung Tueftelpark')
    while True:
        loop()
