from dbloader import *
from svmdataloader import *
import sys

if __name__ == "__main__":
    rootdir = getCSVroot()
    belleJSON = getCSVjsonPath()
    key = "belle"
    suffix = "11_1"

    cnt,dictLists = getManifold(key,rootdir,fileNamingPolicyTwo,suffix)

    if cnt is None:
        #logging goes here with the dictList carry error information
        sys.exit(0)

    suitsizeDictLists, scanDictLists, userInfoDictLists, answerDictLists, boottreeDictLists = dictLists

    jcnt, dJoint1 = dataJoin(userInfoDictLists, scanDictLists, left_on=['userid'], right_on=['fcode'],how='inner')
    dJoint1r = removeDimensions(dJoint1, 'fcode')
    ntd = groupbyDict(dJoint1r,lambda x:[x[3]],scan3dDatetime)
    userinfoscan = lists2dicts(['userid','sex','weight','height','scandata'],ntd)

    splitLR = rowSplit(userinfoscan, 'scandata', extractScanDataLR)
    scanDimensionNames = getScanDimensionName(userinfoscan[0].get("scandata"))
    userinfoScanLR = lists2dicts(userinfoscan[0].keys()[:4]+["side"]+scanDimensionNames,splitLR)
    # print userinfoScanLR[0]
    # print userinfoScanLR[1]


    split = rowSplit(userinfoscan, 'scandata', extractScanData)
    scanDimensionNamesSides = getScanDimensionNameSides(userinfoscan[0].get("scandata"))
    userinfoScan = lists2dicts(userinfoscan[0].keys()[:4] + scanDimensionNamesSides, split)
    # print userinfoScan[0]
    # print userinfoScan[1]

    boottreeMapping = getBoottreeMapping()
    jcnt2, suitSizeDicts = dataJoin(suitsizeDictLists, boottreeMapping, left_on=['itemid'], right_on=['itemid'],how='inner')


    print jcnt2
    print suitSizeDicts[0]
    #
    jcnt3, suitUserScanInfo = dataJoin(suitSizeDicts, userinfoScan, left_on=['userid'], right_on=['userid'],how='inner')

    print jcnt3
    print suitUserScanInfo[0]

    filter(lambda d: len(d.get("styleid","wrong"))>=5,boottreeDictLists)
    map(replaceV,boottreeDictLists)
    str2num(boottreeDictLists,["styleid","boottreeid",])
    str2num(suitUserScanInfo,['userid','styleid',])

    print ""
    print boottreeDictLists[0]
    print suitUserScanInfo[0]


    jcnt4, userinfoScanBoottree = dataJoin(suitUserScanInfo, boottreeDictLists, joinKeyList=['styleid','size'],how='inner')

    print ""
    print jcnt4
    print userinfoScanBoottree[0]

    dJoint2r = removeDimensionsOrdered(userinfoScanBoottree, ['userid'])
    print dJoint2r[0]
    #
    # lSet = set()
    # for r in suitUserScanInfo:
    #     lSet.add(r.get("userid")+"_"+r.get("styleid"))
    #
    # print len(lSet)
    # print len(suitUserScanInfo)
    # nnlist = map(lambda r: r.get("userid")+"_"+r.get("styleid"),suitUserScanInfo)
    # print len(nnlist)
    #
    # for d in suitUserScanInfo:
    #     if d.get("userid") == "F0049375462":
    #         print d