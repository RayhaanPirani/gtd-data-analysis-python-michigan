import sqlite3

dbname = raw_input("Enter the SQLite database filename to read from: ")
outdbname = dbname[:dbname.find('.')] + "_modelled.sqlite"

rconn = sqlite3.connect(dbname)
wconn = sqlite3.connect(outdbname)

rcurr = rconn.execute('SELECT country, country_txt, region, region_txt, attacktype1, attacktype1_txt, targtype1, targtype1_txt, targsubtype1, targsubtype1_txt, weaptype1, weaptype1_txt, weapsubtype1, weapsubtype1_txt, propextent, propextent_txt FROM gtd')

wconn.execute('CREATE TABLE IF NOT EXISTS Country(cid INTEGER PRIMARY KEY, cname VARCHAR)')
wconn.execute('CREATE TABLE IF NOT EXISTS Region(rid INTEGER PRIMARY KEY, rname VARCHAR)')
wconn.execute('CREATE TABLE IF NOT EXISTS AttackType(aid INTEGER PRIMARY KEY, aname VARCHAR)')
wconn.execute('CREATE TABLE IF NOT EXISTS TargType(tid INTEGER PRIMARY KEY, tname VARCHAR)')
wconn.execute('CREATE TABLE IF NOT EXISTS TargSubType(tsid INTEGER PRIMARY KEY, tsname VARCHAR)')
wconn.execute('CREATE TABLE IF NOT EXISTS WeapType(wid INTEGER PRIMARY KEY, wname VARCHAR)')
wconn.execute('CREATE TABLE IF NOT EXISTS WeapSubType(wsid INTEGER PRIMARY KEY, wsname VARCHAR)')
wconn.execute('CREATE TABLE IF NOT EXISTS PropExtent(px INTEGER PRIMARY KEY, pxtext VARCHAR)')

for row in rcurr:
    wconn.execute('INSERT OR IGNORE INTO Country (cid, cname) VALUES ( ?, ? )', (row[0], row[1]))
    wconn.execute('INSERT OR IGNORE INTO Region (rid, rname) VALUES ( ?, ? )', (row[2], row[3]))
    wconn.execute('INSERT OR IGNORE INTO AttackType (aid, aname) VALUES ( ?, ? )', (row[4], row[5]))
    wconn.execute('INSERT OR IGNORE INTO TargType (tid, tname) VALUES ( ?, ? )', (row[6], row[7]))
    wconn.execute('INSERT OR IGNORE INTO TargSubType (tsid, tsname) VALUES ( ?, ? )', (row[8], row[9]))
    wconn.execute('INSERT OR IGNORE INTO WeapType (wid, wname) VALUES ( ?, ? )', (row[10], row[11]))
    wconn.execute('INSERT OR IGNORE INTO WeapSubType (wsid, wsname) VALUES ( ?, ? )', (row[12], row[13]))
    wconn.execute('INSERT OR IGNORE INTO PropExtent (px, pxtext) VALUES ( ?, ? )', (row[14], row[15]))

wconn.commit()
print "Created and populated basic tables."

rcurr = rconn.execute('SELECT eventid, summary, attacktype1, targtype1, targsubtype1, gname, ingroup, motive, weaptype1, weapsubtype1, weapdetail, nkill, nwound, property, propextent, propvalue, propcomment, addnotes FROM gtd')
wconn.execute('CREATE TABLE IF NOT EXISTS TerrorEvent(eventid REAL PRIMARY KEY, summary VARCHAR, attacktype INTEGER references AttackType(aid), targettype INTEGER references TargType(tid), targetsubtype INTEGER references TargSubType(tsid), gname VARCHAR, ingroup REAL, motive VARCHAR, weaptype INTEGER references WeapType(wid), weapsubtype INTEGER references WeapSubType(wsid), weapdetail VARCHAR, nkill REAL, nwound REAL, property INTEGER, propextent INTEGER references PropExtent(px), propvalue REAL, propcomment VARCHAR, addnotes VARCHAR)')

for row in rcurr:
    wconn.execute('INSERT OR IGNORE INTO TerrorEvent (eventid, summary, attacktype, targettype, targetsubtype, gname, ingroup, motive, weaptype, weapsubtype, weapdetail, nkill, nwound, property, propextent, propvalue, propcomment, addnotes) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,? )', (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17]))

wconn.commit()
print "Created and populated the main table structure."

rcurr = rconn.execute('SELECT eventid, iyear, imonth, iday, country, region, provstate, city, latitude, longitude FROM gtd')
wconn.execute('CREATE TABLE IF NOT EXISTS Time(id REAL references TerrorEvent(eventid), day DATE)')
wconn.execute('CREATE TABLE IF NOT EXISTS Location(id REAL references TerrorEvent(eventid), country VARCHAR, region VARCHAR, provstate VARCHAR, city VARCHAR, lat REAL, long REAL)')

for row in rcurr:
    year = str(int(row[1]))
    if(row[2] == 0): month = '01'
    elif(row[2] < 10): month = '0' + str(int(row[2]))
    else: month = str(int(row[2]))
    if(row[3] == 0): day = '01'
    elif(row[3] < 10): day = '0' + str(int(row[3]))
    else: day = str(int(row[3]))
    date = year + '-' + month + '-' + day

    wconn.execute('INSERT OR IGNORE INTO Time (id, day) VALUES ( ?, ? )', (row[0], date))
    wconn.execute('INSERT OR IGNORE INTO Location(id, country, region, provstate, city, lat, long) VALUES ( ?, ?, ?, ?, ?, ?, ?)', (row[0], row[4], row[5], row[6], row[7], row[8], row[9]))

wconn.commit()
print "Created and populated detail tables."


print "Modelled database '" + outdbname + "' created successfully."
wconn.close()
rconn.close()