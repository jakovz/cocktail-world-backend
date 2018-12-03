#!/usr/bin/python

import MySQLdb as mdb

serverName = 'test623'
user = 'testuser'
password = 'localhost'
dbName = 'testdb'

con = mdb.connect(serverName, user, password, dbName);

with con:

	cur = con.cursor(mdb.cursors.DictCursor)
	
	try:
		cur.execute("SELECT * FROM %s LIMIT %s", "Writers", "4")
		cur.commit()

	except:
		cur.rollback()

	rows = cur.fetchall()

	for row in rows:
		print row["Id"], row["Name"]

	for i in range(cur.rowcount):
		row = cur.fetchone()
		print row[0] row[1]

	cur.close()
