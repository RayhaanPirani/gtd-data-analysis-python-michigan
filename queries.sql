/*
 * These are some queries for analysis of the Global Terrorism Database for the project. 
 */

/*Gives the country IDs grouped by the count of terror attacks in each country sorted in descending.*/
SELECT COUNT(te.eventid),loc.country FROM Location loc, TerrorEvent te, Country c WHERE loc.id = te.eventid GROUP BY loc.country ORDER BY COUNT(te.eventid) DESC

/*Gives country IDs grouped by the casualties in each country sorted in descending.*/
SELECT SUM(te.nkill),loc.country FROM Location loc, TerrorEvent te, Country c WHERE loc.id = te.eventid GROUP BY loc.country ORDER BY SUM(te.nkill) DESC

/*Returns records of terror events that occurred before the given date. Manipulative query, can be modified and used in many ways. Use input date in place of given example.*/
SELECT * FROM TerrorEvent te, Time t WHERE te.eventid = t.id AND t.day <= '1970-04-26'

/*Obtains information to visualize all terror attacks in a map that have occurred after a given date.*/
SELECT te.eventid, c.cname, te.gname, loc.lat, loc.long, t.day FROM TerrorEvent te, Time t, Location loc, Country c WHERE te.eventid = t.id AND te.eventid = loc.id AND loc.country = c.cid AND t.day >= '1991-12-01'