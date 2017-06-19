import pandas
import sqlite3

csvfile = raw_input('Enter the name of the CSV file: ')
dbfile = csvfile[:csvfile.find('.')] + '.sqlite'
print "File to be saved to: " + dbfile
cnx = sqlite3.connect(dbfile)
df = pandas.read_csv(csvfile)
df.to_sql('table_name', cnx)