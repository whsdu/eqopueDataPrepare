
from dbloader import *


"""
    knowledge about what will be included in the CSV folders.
"""
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

def normalizeByNameSets(dicts,nameLists):
    from math import sqrt
    keys, lists = dicts2lists(dicts)

    def auxiComputeL2Normal(nlists,indexList):

        for list in nlists:
            l2acc = [0]*len(indexList)
            for bi,indexs in enumerate(indexList):
                for i in indexs:
                    l2acc[bi] += float(list[i])**2

            l2acc = map(lambda r: sqrt(r), l2acc)

            for ai,indexs in enumerate(indexList):
                for i in indexs:
                    if(l2acc[ai]==0): list[i] = 1.0
                    else:
                        list[i] = float(list[i])/l2acc[ai]
        return nlists

    try:
        indexList = [[keys.index(name) for name in names] for names in nameLists]
    except Exception as e:
        return (None,e)


    try:
        nlist = auxiComputeL2Normal(lists,indexList)
    except Exception as e:
        return (None,e)

    ndicts = lists2dicts(keys,nlist)
    return ndicts

def normalizeByAxisZero(Lists):
    import numpy as np
    X,y = list2nlist(Lists)

    nMin = X.min(axis = 0)
    gap = X.max(axis = 0) - nMin
    normalizedX = 1.0*(X-nMin)/gap

    normalizedX[np.isnan(normalizedX)] = 0

    return (normalizedX,y,gap,nMin)

def list2nlist(lists):
    import numpy as np

    data_set = np.asarray(lists)
    X = data_set[:, 2:]
    y = data_set[:, 1]

    return (X,y)


def getDataSet(key,rootdir,fileNamingPolicyTwo,suffix):
    import logging
    logger = logging.getLogger("main.getDataSet")

    import sys
    import numpy as np

    cnt, dictLists = getManifold(key, rootdir, fileNamingPolicyTwo, suffix)

    if cnt is None:
        logger.debug(dictLists)
        sys.exit(0)

    suitsizeDictLists, scanDictLists, userInfoDictLists, answerDictLists, boottreeDictLists = dictLists

    ### Merge Userinfor and scan3D infor
    jcnt, dJoint1 = dataJoin(userInfoDictLists, scanDictLists, left_on=['userid'], right_on=['fcode'], how='inner')
    if jcnt is None: return (jcnt,dJoint1)
    dJoint1r = removeDimensionsOrdered(dJoint1, ['fcode'])
    ntd = groupbyDict(dJoint1r, lambda x: [x[list(dJoint1r[0].keys()).index("userid")]], scan3dDatetime)
    userinfoscan = lists2dicts(['userid', 'sex', 'height', 'weight', 'usualsize', 'scandata'], ntd)
    logger.debug("Join userinfor(hight,weight,age) with 3Dscan data")
    logger.debug(ntd[0])
    logger.debug(userinfoscan[0])

    # mejson, mdimensionDict = dictsExamer(userinfoscan,'scandata')
    # print "mejson: " + str(mejson)
    # print "mdimensionDict: "
    # print mdimensionDict.keys()
    # print ""

    ### Clean failed scandata ( Such as unfinished JSON object )
    fejson, userinfoscanFiltered = excludeFailedRow(userinfoscan, 'scandata')
    logger.debug("remove incomplete json")
    logger.debug("fejson: " + str(fejson))
    logger.debug(len(userinfoscan))
    logger.debug("fdimensionDict: ")
    logger.debug(userinfoscanFiltered[0].keys())

    userinfoscan = userinfoscanFiltered

    ### Extract scanData by foot position (Left and Right)
    splitLR = rowSplit(userinfoscan, 'scandata', extractScanDataLR)
    scanDimensionNames = getScanDimensionName(userinfoscan[0].get("scandata"))
    userinfoScanLR = lists2dicts(
        userinfoscan[0].keys()[:(userinfoscan[0].keys().index("usualsize") + 1)] + ["side"] + scanDimensionNames,
        splitLR
    )
    logger.debug("parse the json part, the result is: ")
    logger.debug(userinfoScanLR[0])
    logger.debug(userinfoScanLR[1])

    ### Extract scanData, concatenate left and right.
    split = rowSplit(userinfoscan, 'scandata', extractScanData)
    scanDimensionNamesSides = getScanDimensionNameSides(userinfoscan[0].get("scandata"))
    userinfoScan = lists2dicts(userinfoscan[0].keys()[:5] + scanDimensionNamesSides, split)
    logger.debug("parse the json part and concatenate left and rith, the result is: ")
    logger.debug(userinfoScan[0])
    logger.debug(userinfoScan[1])

    ### Get the mapping relation between shoes' itemID and styleid.
    ### Merge the fitSize record with shoes' Info
    boottreeMapping = getBoottreeMapping()
    jcnt2, suitSizeDicts = dataJoin(suitsizeDictLists, boottreeMapping, left_on=['itemid'], right_on=['itemid'],
                                    how='inner')
    logger.debug("Combine suitsize information with the shoes' style and id mapping relations. The result is : ")
    logger.debug(jcnt2)
    logger.debug(suitSizeDicts[0])

    ### Merge suitsize, userinfo with shoes infor ==> Userinfo, suitsize, User3DScan, shoesID, shoesStyleid
    jcnt3, suitUserScanInfo = dataJoin(suitSizeDicts, userinfoScan, left_on=['userid'], right_on=['userid'],
                                       how='inner')
    logger.debug("Contain 'Userinfo', 'suitsize', 'User3DScan', 'shoesID', 'shoesStyleid'. The result is : ")
    logger.debug(jcnt3)
    logger.debug(suitUserScanInfo[0])

    ### Clearn Boottree infor
    filter(lambda d: len(d.get("styleid", "W")) >= 5, boottreeDictLists)
    map(replaceV, boottreeDictLists)
    str2num(boottreeDictLists, ["styleid", "boottreeid", ])
    str2num(suitUserScanInfo, ['userid', 'styleid', ])

    logger.debug("Convert string to Num of boottree and userscan info. The result is: ")
    logger.debug(boottreeDictLists[0])
    logger.debug(suitUserScanInfo[0])

    ### Generate boottreeinfor for a given Shooe style
    boottreeAveList = groupbyDict(boottreeDictLists, lambda r: [r[list(boottreeDictLists[0].keys()).index("styleid")]],
                                  boottreeAve)
    boottreeDictAve = lists2dicts(["styleid"] + boottreeDictLists[0].keys()[2:], boottreeAveList)
    logger.debug("Get average boottree to represent a unique style. The result is: ")
    logger.debug(boottreeDictAve[0])
    logger.debug(len(boottreeDictAve[0].keys()))
    logger.debug(boottreeDictAve[0].keys())
    #
    # jcnt4, userinfoScanBoottree = dataJoin(suitUserScanInfo, boottreeDictLists, joinKeyList=['styleid', 'size'],
    #                                        how='inner')
    # print ""
    # print jcnt4
    # print userinfoScanBoottree[0]

    jcnt5, userinfoScanBoottreeAve = dataJoin(suitUserScanInfo, boottreeDictAve, joinKeyList=['styleid'], how='inner')
    logger.debug("Get the training dataset: ")
    logger.debug(jcnt5)
    logger.debug(len(userinfoScanBoottreeAve[0].keys()))
    logger.debug(userinfoScanBoottreeAve[0])

    rX = removeDimensionsOrdered(userinfoScanBoottreeAve, ["userid", "styleid", "sex_x","size_y"])
    print rX[0]
    keys, lists = dicts2lists(rX)
    print keys
    normalizedX,hehey,gap,nMin = normalizeByAxisZero(lists)
    print normalizedX[0]
    print hehey
    print len(normalizedX[0])
    return (normalizedX,hehey,gap,nMin)

    #
    # nrX = normalizeByNameSets(rX,[
    #     ['height','weight','usualsize'],
    #     [k for i, k in enumerate(keys) if (i >= keys.index("foot_length_original_left") and i <= keys.index("below_knee_girth_right"))],
    #     ["bathickness","bbthickness"],
    #     [k for i, k in enumerate(keys) if (i >= keys.index("d1") and i <= keys.index("d19"))],
    # ])
    #
    # print rX[0]
    # print rX[1]
    # print len(rX[1])
    # print ""
    # print nrX[0]
    # print nrX[1]
    # print len(nrX[1])
    #
    # nkeys, nlists = dicts2lists(nrX)
    # ndata_set = np.asarray(nlists)
    # nX = ndata_set[:,2:]
    # ny = ndata_set[:,1]
    #
    # print keys
    # print len(nX[1])
    # data_set = np.asarray(lists)
    # X = data_set[:, 2:]
    # y = data_set[:, 1]
    #
    # print rX[0].keys()
    # print data_set[0]
    # print len(X[1])
    # # print X[0]
    # # print y[0]
    # return [(X,y),(nX,ny),rX,nrX]

if __name__=="__main__":
    # boottreeMapping = getBoottreeMapping()
    # for d in boottreeMapping:
    #     print d

    import collections

    dict1 = collections.OrderedDict([('a','1'),  ('b','2'),  ('c',"stringC"),('d',5),('e',"string_E"),('f','10.3')])
    dict2 = collections.OrderedDict([('a','2'),  ('b','4'),  ('c',"stringC"),('d',15),('e',"string_E"),('f',11.3)])
    dict3 = collections.OrderedDict([('a','3'),  ('b','6'),  ('c',"stringC"),('d',25),('e',"string_E"),('f',12.3)])
    dict4 = collections.OrderedDict([('a','4'),  ('b','7'),  ('c',"stringC"),('d',35),('e',"string_E"),('f',13.3)])
    dict5 = collections.OrderedDict([('a','5'),  ('b','10'),  ('c',"stringC"),('d',45),('e',"string_E"),('f',14.3)])
    dicts = [dict1,dict2,dict3,dict4,dict5]

    namelist = [['a','b'],['d'],['f']]
    for d in dicts:
        print d

    for d in normalizeByNameSets(dicts,namelist):
        print d