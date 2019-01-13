#!/usr/bin/python

import MySQLdb as mdb
from sshtunnel import SSHTunnelForwarder
import simplejson as json

MOODLE_USERNAME = ''
MOODLE_PASSWORD = ''

serverName = 'mysqlsrv1.cs.tau.ac.il'
user = 'DbMysql03'
password = 'DbMysql03'
dbName = 'DbMysql03'


def execute_query(query, *kargs):
    """
    executes DB query
    :param query:
    :param kargs:
    :return:
    """
    rows = []
    """
    # With SSH
    with SSHTunnelForwarder(('nova.cs.tau.ac.il', 22), ssh_password=MOODLE_PASSWORD, ssh_username=MOODLE_USERNAME,
                            remote_bind_address=('mysqlsrv1.cs.tau.ac.il', 3306)) as server:
        con = mdb.connect(host='127.0.0.1', port=server.local_bind_port, user='DbMysql03', passwd='DbMysql03')
        ##### end With SSH
    """
    # Without SSH
    con = mdb.connect(host='mysqlsrv1.cs.tau.ac.il', port=3306, user='DbMysql03', passwd='DbMysql03')
    ##### end Without SSH

    con.select_db('DbMysql03')
    cur = con.cursor()
    with con:
        cur = con.cursor()
        try:
            cur.execute(
                query % kargs)  # query should be something like "SELECT %S FROM %S ..." and kargs are the params
            con.commit()

        except Exception as e:
            print(e)
            print("Error: failed executing/committing query")
            con.rollback()
            return
        json_data = []
        if 'INSERT' not in query:
            try:
                row_headers = [x[0] for x in cur.description]
                rows = cur.fetchall()
            except Exception as e:
                print(e)
                print("Error: failed fetching data")

            for result in rows:
                json_data.append(dict(zip(row_headers, result)))

        cur.close()


return json.dumps(json_data)

# return rows
