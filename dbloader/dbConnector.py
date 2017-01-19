from dbloader import *

def sqlQuery(statement,hostname,dbname,lazySize = 1000):
    import collections

    dbconnection, dbCur = getMysqlCon(hostname,dbname)
    dbCur.execute(statement)


    filedNames = [f[0] for f in dbCur.description]
    dataGenrator = fetchsome(dbCur,lazySize)

    dicts = list()
    for row in dataGenrator:
        dicts.append(collections.OrderedDict(zip(filedNames,row)))

    return dicts

def dictsExamer(dicts,dimension):
    import collections

    errorJSON = 0
    dimensionDict = dict()

    for d in dicts:
        scanStr = d.get(dimension,None)

        if scanStr is None: return (None,"Dimension name does not exist!")

        decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
        if "nan" in scanStr: continue
        try:
            scandict = decoder.decode(scanStr)
        except:
            errorJSON += 1
            continue
        dimensionDict[len(scandict)] = scandict

    return (errorJSON,dimensionDict)

def excludeFailedRow(dicts,dimension):
    import collections

    dictList = list()
    for d in dicts:
        scanStr = d.get(dimension, None)

        if scanStr is None: return (None, "Dimension name does not exist!")

        decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
        if "nan" in scanStr: continue
        try:
            scandict = decoder.decode(scanStr)
        except:
            continue
        d[dimension] = scanStr
        dictList.append(d)

    return (len(dictList), dictList)


def str2dicts(dicts,dimension):
    import collections
    import copy

    ndictList = list()

    for d in dicts:
        scanStr = d.get(dimension,None)
        if scanStr is None: return (None,"dimension name does not exist!")
        decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
        if "nan" in scanStr:continue
        try:
            scandict = decoder.decode(scanStr)
        except:
            continue

        nd = copy.deepcopy(d)
        nd.update({dimension:scandict})
        ndictList.append(nd)

    return ndictList

if __name__ == "__main__":
    testStatementOne = """
    select * from
    dlo_3dscan
    """
    dicts = sqlQuery(testStatementOne,"dlo","t_dlodb")
    print len(dicts)
    errorjson,dimensionDict = dictsExamer(dicts,"measurement_items")
    if errorjson is not None and 49 in dimensionDict.keys():
        ndicts = str2dicts(dicts,"measurement_items")

    print ndicts[0]
    print ndicts[0].get("measurement_items")
    print len(ndicts[0].keys())
    print ""

    nndicts = str2dicts(ndicts,"customer_info")
    print nndicts[0]
    print nndicts[0].get('customer_info')
    print len(nndicts[0].keys())
    print ""

    for k,v in nndicts[0].iteritems():
        print k
        print v
