from dbloader import *
import time
from svmdataloader import *




def testStatement():
    from sqlQueryStatement import testStatementOne
    import collections

    dicts = sqlQuery(testStatementOne, "dlo", "t_dlodb")
    print len(dicts)

    print dicts[0]
    print dicts[0].keys()
    print len(dicts)

    dimsionDict = dict()
    dSet = set()
    cnt = 1
    for d in dicts:
        scanStr = d.get("measurement_items")
        decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
        # print scanStr
        if "nan" in scanStr:continue
        try:
            scandict = decoder.decode(scanStr)
        except:
            print scanStr + " " + str(cnt)
            cnt+=1
            continue

        dimsionDict[len(scandict)] = scandict
        dSet.add(len(scandict))
    for k,v in dimsionDict.iteritems():
        print k
        print v.keys()

        print ""
    print dSet
    print cnt

    print set(dimsionDict.get(49)).issubset(set(dimsionDict.get(68)))

def unifiyDimension():
    from sqlQueryStatement import testStatementOne
    import collections
    import copy

    dicts = sqlQuery(testStatementOne, "dlo", "t_dlodb")

    errorJSON = 0
    dimsionDict = dict()
    dSet = set()
    dictLists = list()
    ndictLists = list()
    print dicts[0].keys()
    for d in dicts:
        scanStr = d.get("measurement_items")
        decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
        if "nan" in scanStr:continue
        try:
            scandict = decoder.decode(scanStr)
        except:
            errorJSON += 1
            print scanStr
            continue
        dimsionDict[len(scandict)] = scandict
        dSet.add(len(scandict))
        dictLists.append(scandict)
        nd = copy.deepcopy(d)
        nd.update({"measurement_items":scandict})
        ndictLists.append(nd)

    print len(dicts)
    print len(dictLists)
    print len(ndictLists)
    print errorJSON
    print dictLists[0]
    print ndictLists[0]
    print len(dicts[0].keys())
    print len(ndictLists[0].keys())

def getDB(queryStatement,hostname,dbname):
    dicts = sqlQuery(queryStatement, hostname, dbname)
    mejson, mdimensionDict = dictsExamer(dicts, "measurement_items")

    print "mejson: " + str(mejson)
    print "mdimensionDict: "
    print mdimensionDict
    print ""

    print dicts[0]
    print len(dicts)
    print ""

    dictCnt, filteredDicts = excludeFailedRow(dicts,"measurement_items")
    print dictCnt
    print filteredDicts[0]

    split = rowSplit(filteredDicts, 'measurement_items', extractScanData)
    scanDimensionNamesSides = getScanDimensionNameSides(filteredDicts[0].get("measurement_items"))
    userinfoScan = lists2dicts(filteredDicts[0].keys()[:5] + scanDimensionNamesSides, split)

    print ""
    print split[0]
    print scanDimensionNamesSides
    print userinfoScan[0]

    fixDicts = removeDimensionsOrdered(userinfoScan,["customer_info"])
    print fixDicts[0]

if __name__ == "__main__":
    # testStatement()
    # unifiyDimension()

    from sqlQueryStatement import testStatementOne


    queryStatement = testStatementOne
    hostname = 'dlo'
    dbname = "t_dlodb"
    dicts = sqlQuery(queryStatement,hostname,dbname)

    getDB(queryStatement, hostname, dbname)

    # errorjson,dimensionDict = dictsExamer(dicts,"customer_info")
    #
    # if errorjson is not None:
    #     ndicts = str2dicts(dicts,"customer_info")
    #
    # for k,v in ndicts[0].iteritems():
    #     print k
    #     print v
    #     print ""
    #
    # mejson,mdimensionDict = dictsExamer(dicts,"measurement_items")
    #
    # print "mejson: " + str(mejson)
    # print "mdimensionDict: "
    # print mdimensionDict
    # print ""
    #
    # if mejson is not None and 49 in mdimensionDict.keys() and set(mdimensionDict.get(49)).issubset(set(mdimensionDict.get(68))):
    #     nndicts = str2dicts(ndicts,"measurement_items")
    #
    # for k,v in nndicts[0].iteritems():
    #     print k
    #     print v
    #
    #
    # fdicts = filter(
    #     lambda d:len(d.get("measurement_items").keys())==49,
    #     nndicts
    # )
    # print len(fdicts)

    # ffdicts = filter(lambda d:len(d.get("measurement_items").keys())==68,nndicts)
    # print len(ffdicts)

