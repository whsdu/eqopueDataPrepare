#!/usr/bin/python
import json
import MySQLdb
import time
from svmdataloader import *


def getSQLdbinfo(datasource):

    dbinforJSONpath = getSQLjsonPath()

    hostinfor = {}
    readfrom = datasource

    with open(dbinforJSONpath) as data_file:
        data = json.load(data_file)

        inforDict = data.get(readfrom,None)

        if inforDict is None:
            return [None,"No coresponding information!"]

        hostinfor["host"] = data[readfrom]["host"]
        hostinfor["port"] = data[readfrom]["port"]
        hostinfor["usr"] = data[readfrom]["usr"]
        hostinfor["pwd"] = data[readfrom]["pwd"]

    return hostinfor

def getDBconnection(dbinfor,dbname):
    dbconnection = MySQLdb.connect(user = dbinfor['usr'],
                                  passwd = dbinfor['pwd'],
                                  host = dbinfor['host'],
                                  port = dbinfor['port'],
                                  db = dbname)
    return dbconnection

def getMysqlCon(dbhost,dbname,failCounter = 0):
    DBinfo = getSQLdbinfo(dbhost)
    DBname = dbname

    try:
        DBconnection = getDBconnection(DBinfo,DBname)
    except Exception as e:
        if failCounter == 10: return [None, e]
        time.sleep(2)
        return getMysqlCon(dbhost,dbname,failCounter +1)

    dbCur = DBconnection.cursor()

    return [DBconnection,dbCur]

def fetchsome(cursor, some=1000):
    fetch = cursor.fetchmany
    while True:
        rows = fetch(some)
        if not rows: break
        for row in rows:
            yield row


if __name__ == "__main__":
    # gtbu = sys.argv[1]
    #
    # hostinfor = getdbinfo(gtbu)
    #
    # for key, value in hostinfor.iteritems():
    #     print key + " : " + str(value)

    hostinfor = getSQLdbinfo("dlo")
    print hostinfor

    dbconnection, dbCur = getMysqlCon("dlo","t_dlodb")

    dbCur.execute("select * from dlo_3dscan")
    for i in dbCur.description:
        print i[0]

    filenames = [i[0] for i in dbCur.description]
    print filenames

