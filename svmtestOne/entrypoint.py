from dbloader import *
from svmdataloader import *
import numpy as np
import sys
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

if __name__ == "__main__":
    rootdir = getCSVroot()
    # belleJSON = getCSVjsonPath()
    key = "belle"
    suffix = "11_1"

    cnt,dictLists = getManifold(key,rootdir,fileNamingPolicyTwo,suffix)

    if cnt is None:
        #logging goes here with the dictList carry error information
        sys.exit(0)

    suitsizeDictLists, scanDictLists, userInfoDictLists, answerDictLists, boottreeDictLists = dictLists

    jcnt, dJoint1 = dataJoin(userInfoDictLists, scanDictLists, left_on=['userid'], right_on=['fcode'],how='inner')
    dJoint1r = removeDimensionsOrdered(dJoint1, ['fcode'])

    ntd = groupbyDict(dJoint1r,lambda x:[x[list(dJoint1r[0].keys()).index("userid")]],scan3dDatetime)
    userinfoscan = lists2dicts(['userid','sex','height','weight','usualsize','scandata'],ntd)
    print ntd[0]
    print userinfoscan[0]


    splitLR = rowSplit(userinfoscan, 'scandata', extractScanDataLR)
    scanDimensionNames = getScanDimensionName(userinfoscan[0].get("scandata"))
    userinfoScanLR = lists2dicts(
        userinfoscan[0].keys()[:(userinfoscan[0].keys().index("usualsize")+1)]+["side"]+scanDimensionNames,
        splitLR
    )
    print ""
    print userinfoScanLR[0]
    print userinfoScanLR[1]


    split = rowSplit(userinfoscan, 'scandata', extractScanData)
    scanDimensionNamesSides = getScanDimensionNameSides(userinfoscan[0].get("scandata"))
    userinfoScan = lists2dicts(userinfoscan[0].keys()[:5] + scanDimensionNamesSides, split)
    print ""
    print userinfoScan[0]
    print userinfoScan[1]

    boottreeMapping = getBoottreeMapping()
    jcnt2, suitSizeDicts = dataJoin(suitsizeDictLists, boottreeMapping, left_on=['itemid'], right_on=['itemid'],how='inner')

    print ""
    print jcnt2
    print suitSizeDicts[0]
    # #
    jcnt3, suitUserScanInfo = dataJoin(suitSizeDicts, userinfoScan, left_on=['userid'], right_on=['userid'],how='inner')

    print ""
    print jcnt3
    print suitUserScanInfo[0]

    filter(lambda d: len(d.get("styleid","W"))>=5,boottreeDictLists)
    map(replaceV,boottreeDictLists)
    str2num(boottreeDictLists,["styleid","boottreeid",])
    str2num(suitUserScanInfo,['userid','styleid',])
    #
    print ""
    print boottreeDictLists[0]
    print suitUserScanInfo[0]

    boottreeAveList = groupbyDict(boottreeDictLists,lambda r:[r[list(boottreeDictLists[0].keys()).index("styleid")]],boottreeAve)
    boottreeDictAve = lists2dicts(["styleid"]+boottreeDictLists[0].keys()[2:],boottreeAveList)
    print boottreeDictAve[0]
    print boottreeDictAve[0].keys()
    print len(boottreeDictAve[0].keys())
    #
    jcnt4, userinfoScanBoottree = dataJoin(suitUserScanInfo, boottreeDictLists, joinKeyList=['styleid','size'],how='inner')

    print ""
    print jcnt4
    print userinfoScanBoottree[0]

    jcnt5, userinfoScanBoottreeAve = dataJoin(suitUserScanInfo, boottreeDictAve, joinKeyList=['styleid'],how='inner')
    print ""
    print jcnt5
    print userinfoScanBoottreeAve[0]
    print len(userinfoScanBoottreeAve[0].keys())


    rX = removeDimensionsOrdered(userinfoScanBoottreeAve,["userid","styleid","sex_x"])
    print rX[0]

    keys,lists = dicts2lists(rX)
    print keys
    data_set = np.asarray(lists)
    X = data_set[:,2:]
    y = data_set[:,1]
    print X.shape
    print y.shape
    print X[0]
    print y
    yB = map(lambda r: r<=230,list(y))
    print yB

    X_normalized = preprocessing.normalize(X, norm='l2')
    print X_normalized[0]

    # X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.20)
    #
    # clf = SVC()
    # clf.fit(X_train, y_train)
    #
    # y_pred = clf.predict(X_test)
    #
    # y_label = sorted(list(set(y)))
    # print confusion_matrix(y_test, y_pred, labels=y_label)



    cv_decorator = optunity.cross_validated(x=X_normalized[:1000], y=yB[:1000], num_folds=5)
    svm_tuned_auroc = cv_decorator(svm_tuned_auroc)

    optimal_svm_pars, info, _ = optunity.maximize_structured(svm_tuned_auroc, space, num_evals=150)
    print("Optimal parameters" + str(optimal_svm_pars))
    print("AUROC of tuned SVM: %1.3f" % info.optimum)

    df = optunity.call_log2dataframe(info.call_log)
    df.sort_values('value',ascending = True)
    print df

    #
    # dJoint2r = removeDimensionsOrdered(userinfoScanBoottree, ['userid'])
    # print dJoint2r[0]



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