import xlrd
import csv

fname = raw_input("Enter the file name to convert: ")
wb = xlrd.open_workbook(fname)
sh = wb.sheet_by_name('Sheet1')
csvname = fname[:fname.find('.')] + '.csv'

your_csv_file = open(csvname, 'wb')
wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

for rownum in xrange(sh.nrows):
    try:
        wr.writerow(sh.row_values(rownum))
    except(UnicodeEncodeError):
        pass

your_csv_file.close()