def attacks_by_count(con, visualize=False):
    n = raw_input("\nEnter the maximum number to display: ")
    print "Retrieving data..."
    query = "SELECT COUNT(te.eventid),loc.country FROM Location loc, TerrorEvent te, Country c WHERE loc.id = te.eventid GROUP BY loc.country ORDER BY COUNT(te.eventid) DESC LIMIT " + n
    curr = con.execute(query)
    print "Data retrieved.\n"

    if(visualize):
        words = list()
        counts = dict()

        for row in curr:
            cid = row[1]
            country = con.execute("SELECT cname FROM Country WHERE cid=" + cid)
            word = country.fetchone()[0]
            words.append(word)
            counts[word] = long(row[0])

        bigsize = 80
        smallsize = 20

        highest = None
        lowest = None
        for w in words:
            if highest is None or highest < counts[w] :
                highest = counts[w]
            if lowest is None or lowest > counts[w] :
                lowest = counts[w]

        fhand = open('gtdcountries.js','w')
        fhand.write("gword = [")
        first = True
        for k in words:
            if not first : fhand.write( ",\n")
            first = False
            size = counts[k]
            size = (size - lowest) / float(highest - lowest)
            size = int((size * bigsize) + smallsize)
            fhand.write("{text: '"+k+"', size: "+str(size)+"}")
        fhand.write( "\n];\n")

        print "Output written to gtdcountries.js"
        print "Open gtdcountries.htm in a browser to view"
        return

    print "ATTACKS\t\tCOUNTRY"
    for row in curr:
        cid = row[1]
        country = con.execute("SELECT cname FROM Country WHERE cid=" + cid)
        print  str(row[0]) + "\t\t" + country.fetchone()[0]

def attacks_by_casualties(con):
    n = raw_input("\nEnter the maximum number to display: ")
    print "Retrieving data..."
    query = "SELECT SUM(te.nkill),loc.country FROM Location loc, TerrorEvent te, Country c WHERE loc.id = te.eventid GROUP BY loc.country ORDER BY SUM(te.nkill) DESC LIMIT " + n
    curr = con.execute(query)
    print "Data retrieved.\n"

    print "CASUALTIES\t\tCOUNTRY"
    for row in curr:
        cid = row[1]
        country = con.execute("SELECT cname FROM Country WHERE cid=" + cid)
        print  str(row[0]) + "\t\t" + country.fetchone()[0]

def attacks_by_dates(con, map=False):
    print "\nDate format is YYYY-MM-DD."
    start = raw_input("Enter initial date: ")
    end = raw_input("Enter final date: ")
    print "Retrieving data..."
    query = "SELECT te.eventid, te.summary, t.day, te.nkill FROM TerrorEvent te, Time t WHERE te.eventid = t.id AND t.day >= '" + start + "' AND t.day <= '" + end + "'"
    curr = con.execute(query)
    print "Data retrieved.\n"

    strarr = ''
    if(map):
        print "Generating map..."
        strarr += "       ['Latitude', 'Longitude', 'Casualties'],\n"
        lastrow = None
        for row in curr:
            id = str(long(row[0]))
            query = "SELECT loc.lat,loc.long FROM Location loc, TerrorEvent te WHERE loc.id = " + id
            geo = con.execute(query)
            for r in geo:
                if(r[0] is None or r[1] is None): continue
                casualties = row[3]
                if(casualties is None): casualties = 0
                strarr += '       [' + str(r[0]) + ', ' + str(r[1]) + ', ' + str(int(casualties)) + '],\n'
                break
        strarr = strarr[:len(strarr)-2]

        with open('mapframe.html', 'r') as f_in:
            with open('map.html','w') as f_out:
                for line_no, line in enumerate(f_in, 1):
                    if line_no == 10:
                        f_out.write(strarr)
                    f_out.write(line)
        
        print "Map generated in 'map.html'."
        return

    for row in curr:
        print "ID: " + str(long(row[0])) + "\nDetails: " + str(row[1])
        print ""


if __name__ == "__main__":
    import sqlite3
    dbname = raw_input("Enter the SQLite database filename to read from: ")
    print "Initializing database..."
    con = sqlite3.connect(dbname)
    print "Initialization complete."

    while (True):
        print "\n1. Generate a list of all the countries that had the most number of terror attacks."
        print "2. Visualize the countries based on the number of terror attacks occurred."
        print "3. Generate a list of all the countries that had the highest casualties due to terror attacks."
        print "4. Generate a list of terror events that occurred between the specified dates."
        print "5. Locate all the terror attacks on a map that occurred between the specified dates."
        print "Enter 0 to exit."
        n = int(raw_input("Enter your choice: "))
        if(n == 0): break
        elif(n == 1): attacks_by_count(con)
        elif(n == 2): attacks_by_count(con, visualize=True)
        elif(n == 3): attacks_by_casualties(con)
        elif(n == 4): attacks_by_dates(con)
        elif(n == 5): attacks_by_dates(con,map=True)
        else: print "Invalid choice."
        