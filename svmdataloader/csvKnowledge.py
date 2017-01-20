from svmdataloader import *
from dbloader import *

def getManifold(key,rootdir,namingPolicy,suffix):
    fileCnt, fileList = readFilePathList(key,rootdir,namingPolicy,suffix)

    if fileCnt is not None:
        dataManifold = readcsvFileList(fileList)
    else:
        return (None, "Something is woring in function getManiFold")

    suitsizeDictLists = dataManifold.get("belle_suitsize")
    scanDictLists = dataManifold.get("belle_3dmodel")
    userInfoDictLists = dataManifold.get("belle_userinfo")
    answerDictLists = dataManifold.get("belle_answer")
    boottreeDictLists = dataManifold.get("belle_boottree")

    return [5,(suitsizeDictLists,scanDictLists,userInfoDictLists,answerDictLists,boottreeDictLists)]

def scan3dDatetime(g):
    import datetime

    last = datetime.datetime(1970,1,1,0,0,0)
    for r in g:
        dString = r[-1]
        dt = datetime.datetime.strptime(dString,"%Y/%m/%d %M:%S")
        if last < dt:
            last = dt
            rl = r[1:]

    return rl

def getBoottreeMapping():
    itemID_shoeID_Dict = ('32', 'TYW64N01DU1BL6', '1'), ('31', 'BYW32308DU1CM6', '1'), ('30', 'TYW63H13DU1CM6', '1'), (
        '29', 'WYW82V04DU1BM6', '1'), ('28', 'BYW38908DU1BM6', '1'), ('27', 'WYW84G02DU1CM6', '1'), (
                             '26', 'WYWA9N44DU1CM6', '1'), ('25', 'WYW82H40DU1DD5', '1'), (
                             '24', 'SZP9VN07DU1BL6', '2'), (
                             '23', 'RMDTWA18DM1BL6', '2'), ('22', 'TBL6ZA09DU1BL6', '2'), (
                             '21', 'BBLBIO15DU2CQ6', '2'), (
                             '20', 'TBL6N302DU1CQ6', '2'), ('19', 'SZP9UE24DU1CQ6', '2'), (
                             '18', 'TBL6SK19DU1CQ6', '2'), (
                             '17', 'RMDTL832DU1CQ6', '2'), ('16', 'SZP9YD01DM1AQ6', '2'), (
                             '15', 'RMDTYF21DU1CM6', '2'), (
                             '14', 'BBLBGZ25DU1CM6', '2'), ('13', 'BBLBIP23DU1CM6', '2'), (
                             '12', 'RMDTXD20DU1CM6', '2'), (
                             '11', 'BBLBJBG1DU1CM6', '2'), ('10', 'SZP9XA08DU1CM6', '2'), (
                             '9', 'BBL3C3D2DU1DZ5', '2'), (
                             '8', 'RMDTP761DU1DZ5', '2'), ('7', 'RMDTP740DU1DD5', '2'), ('6', 'TBL6D441DU1DD5', '2'), (
                             '5', 'RMDTNT47DM1DD5', '2'), ('4', 'SZP9SA04DU1DD5', '2'), ('3', 'BBL3EK59DU1DD5', '2'), (
                             '2', 'TBL6VF45DU1DD5', '2'), ('1', 'RMDTM240DU1DD5', '2')

    dl = [list(d) for d in itemID_shoeID_Dict ]
    def replaceK(d):
        d[1] = d[1][3:8]
        return d

    map(replaceK,dl)

    boottreeMapping = lists2dicts(['itemid','styleid','sex'],dl)
    return boottreeMapping

def extractScanData(eles):
    import collections
    import json

    scanList = list()

    decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
    deles = decoder.decode(eles)

    for k, dv in deles.iteritems():
        scanList.append((dv.get("left", 0)))
        scanList.append(dv.get("right", 0))

    return [scanList]

def getScanDimensionNameSides(Str):
    import collections
    import json

    decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
    deles = decoder.decode(Str)

    nameList = [k+"_"+subKey for k, dv in deles.iteritems()for subKey in dv.keys()]

    return nameList

def extractScanDataLR(eles):
    import collections
    import json

    leftList = list()
    rightList = list()
    dList = list()

    decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
    deles = decoder.decode(eles)

    for k, dv in deles.iteritems():
        leftList.append((dv.get("left",0)))
        rightList.append(dv.get("right",0))
        dList.append(k)

    return [['l']+leftList,['r']+rightList]

def getScanDimensionName(Str):
    import collections
    import json

    decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
    deles = decoder.decode(Str)

    return deles.keys()



def replaceV(d):
        d["styleid"] = d.get("styleid")[:5]


def str2num(dicts, exkeylists):
    for d in dicts:
        for k, v in d.iteritems():
            if k not in exkeylists:
                if v == u'' or v == u'\\': d[k] = float(0)
                else: d[k] = float(v)


def boottreeAve(g):
    import numpy as np
    nbt = np.array([r[2:]for r in g]).mean(0)
    return list(nbt)

def excludeFailedRow(dicts,dimension):
    import collections
    import json

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

def getDataSet(key,rootdir,fileNamingPolicyTwo,suffix):
    import sys
    import numpy as np
    cnt, dictLists = getManifold(key, rootdir, fileNamingPolicyTwo, suffix)

    if cnt is None:
        # logging goes here with the dictList carry error information
        sys.exit(0)

    suitsizeDictLists, scanDictLists, userInfoDictLists, answerDictLists, boottreeDictLists = dictLists

    jcnt, dJoint1 = dataJoin(userInfoDictLists, scanDictLists, left_on=['userid'], right_on=['fcode'], how='inner')
    dJoint1r = removeDimensionsOrdered(dJoint1, ['fcode'])

    ntd = groupbyDict(dJoint1r, lambda x: [x[list(dJoint1r[0].keys()).index("userid")]], scan3dDatetime)
    userinfoscan = lists2dicts(['userid', 'sex', 'height', 'weight', 'usualsize', 'scandata'], ntd)
    # print ntd[0]
    # print userinfoscan[0]

    # mejson, mdimensionDict = dictsExamer(userinfoscan,'scandata')
    # print "mejson: " + str(mejson)
    # print "mdimensionDict: "
    # print mdimensionDict.keys()
    # print ""
    #


    fejson, userinfoscanFiltered = excludeFailedRow(userinfoscan, 'scandata')
    # print "fejson: " + str(fejson)
    # print len(userinfoscan)
    # print "fdimensionDict: "
    # print userinfoscanFiltered[0].keys()
    # print ""

    userinfoscan = userinfoscanFiltered

    splitLR = rowSplit(userinfoscan, 'scandata', extractScanDataLR)
    scanDimensionNames = getScanDimensionName(userinfoscan[0].get("scandata"))
    userinfoScanLR = lists2dicts(
        userinfoscan[0].keys()[:(userinfoscan[0].keys().index("usualsize") + 1)] + ["side"] + scanDimensionNames,
        splitLR
    )
    # print ""
    # print userinfoScanLR[0]
    # print userinfoScanLR[1]

    split = rowSplit(userinfoscan, 'scandata', extractScanData)
    scanDimensionNamesSides = getScanDimensionNameSides(userinfoscan[0].get("scandata"))
    userinfoScan = lists2dicts(userinfoscan[0].keys()[:5] + scanDimensionNamesSides, split)
    # print ""
    # print userinfoScan[0]
    # print userinfoScan[1]

    boottreeMapping = getBoottreeMapping()
    jcnt2, suitSizeDicts = dataJoin(suitsizeDictLists, boottreeMapping, left_on=['itemid'], right_on=['itemid'],
                                    how='inner')

    # print ""
    # print jcnt2
    # print suitSizeDicts[0]
    # #
    jcnt3, suitUserScanInfo = dataJoin(suitSizeDicts, userinfoScan, left_on=['userid'], right_on=['userid'],
                                       how='inner')

    # print ""
    # print jcnt3
    # print suitUserScanInfo[0]

    filter(lambda d: len(d.get("styleid", "W")) >= 5, boottreeDictLists)
    map(replaceV, boottreeDictLists)
    str2num(boottreeDictLists, ["styleid", "boottreeid", ])
    str2num(suitUserScanInfo, ['userid', 'styleid', ])
    #
    # print ""
    # print boottreeDictLists[0]
    # print suitUserScanInfo[0]

    boottreeAveList = groupbyDict(boottreeDictLists, lambda r: [r[list(boottreeDictLists[0].keys()).index("styleid")]],
                                  boottreeAve)
    boottreeDictAve = lists2dicts(["styleid"] + boottreeDictLists[0].keys()[2:], boottreeAveList)
    # print boottreeDictAve[0]
    # print boottreeDictAve[0].keys()
    # print len(boottreeDictAve[0].keys())
    #
    jcnt4, userinfoScanBoottree = dataJoin(suitUserScanInfo, boottreeDictLists, joinKeyList=['styleid', 'size'],
                                           how='inner')

    # print ""
    # print jcnt4
    # print userinfoScanBoottree[0]

    jcnt5, userinfoScanBoottreeAve = dataJoin(suitUserScanInfo, boottreeDictAve, joinKeyList=['styleid'], how='inner')
    # print ""
    # print jcnt5
    # print userinfoScanBoottreeAve[0]
    # print len(userinfoScanBoottreeAve[0].keys())

    rX = removeDimensionsOrdered(userinfoScanBoottreeAve, ["userid", "styleid", "sex_x"])
    # print rX[0]

    keys, lists = dicts2lists(rX)
    # print keys
    data_set = np.asarray(lists)
    X = data_set[:, 2:]
    y = data_set[:, 1]

    print data_set[0]
    print X[0]
    print y[0]
    return (X,y)

if __name__=="__main__":
    boottreeMapping = getBoottreeMapping()
    for d in boottreeMapping:
        print d

