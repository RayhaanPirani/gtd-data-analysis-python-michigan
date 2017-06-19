import xlrd
import csv
import pandas
import sqlite3

fname = raw_input("Enter the file name to convert: ")
print "Initializing '" + fname + "'..."
wb = xlrd.open_workbook(fname)
sheets = wb.sheet_names()
sh = wb.sheet_by_name(str(sheets[0]))
name = fname[:fname.find('.')]
csvname = name + '.csv'

your_csv_file = open(csvname, 'wb')
wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

for rownum in xrange(sh.nrows):
    try:
        wr.writerow(sh.row_values(rownum))
    except(UnicodeEncodeError):
        pass

your_csv_file.close()

print "CSV file '" + csvname + "' created successfully."

dbfile = name + '.sqlite'
cnx = sqlite3.connect(dbfile)
print "Initializing '" + csvname + "'..."
df = pandas.read_csv(csvname)
df.to_sql('gtd', cnx)

print "SQLite database '" + dbfile + "' created successfully."