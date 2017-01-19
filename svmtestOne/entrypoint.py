from dbloader import *
from svmdataloader import *
import numpy as np
import sys
from sklearn import preprocessing
from multiprocessing import Process,Queue

def myCrossValidTest(x, y, num_folds,spaceFlat):
    from svmdataloader import svm_tuned_auroc
    import copy
    cx = copy.deepcopy(x)
    cy = copy.deepcopy(y)
    print y
    print len(y)
    cv_decorator = optunity.cross_validated(x=cx, y=cy, num_folds=num_folds)
    svm_tuned_auroc = cv_decorator(svm_tuned_auroc)

    optimal_svm_pars, info, _ = optunity.maximize_structured(svm_tuned_auroc, space, num_evals=150)
    print ("splace flat is" + str(spaceFlat))
    print("Optimal parameters" + str(optimal_svm_pars))
    print("AUROC of tuned SVM: %1.3f" % info.optimum)

def myCrossValid(x, y, num_folds,spaceFlat,paraDicts):
    from svmdataloader import svm_tuned_auroc
    import copy
    cx = copy.deepcopy(x)
    cy = copy.deepcopy(y)
    print y
    print len(y)
    cv_decorator = optunity.cross_validated(x=cx, y=cy, num_folds=num_folds)
    svm_tuned_auroc = cv_decorator(svm_tuned_auroc)

    optimal_svm_pars, info, _ = optunity.maximize_structured(svm_tuned_auroc, space, num_evals=150)
    print ""
    print spaceFlat
    print optimal_svm_pars
    paraDicts.put({int(spaceFlat):optimal_svm_pars})
    return optimal_svm_pars

def myPredictReport(optimal_svm_pars,yp,Xset,Yset):
    from sklearn.metrics import classification_report, confusion_matrix
    from sklearn.cross_validation import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(Xset, Yset, test_size=0.20)
    kernel = optimal_svm_pars.get("kernel")
    C = optimal_svm_pars.get("C")
    coef0 = optimal_svm_pars.get("coef0")
    degree = optimal_svm_pars.get("degree")
    logGamma = optimal_svm_pars.get("logGamma")

    model = train_model(X_train,y_train,kernel,C,logGamma,degree,coef0)
    y_pred = model.predict(X_test)

    print yp
    print classification_report(y_test, y_pred)
    print confusion_matrix(y_test, y_pred,labels=[True,False])

    print optimal_svm_pars

    return model

def testMyOneVsRest(modelDict,ux,uy):
    from sklearn.cross_validation import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(ux, uy, test_size=0.20)

    print ""
    print y_test[0]
    print getPredict([X_test[0]],modelDict)

    errorlist= list()
    elist = list()
    for i,x in enumerate(X_train):
        rlist = getPredict([x],modelDict)
        if len(rlist)>1:
            errorlist.append({y_train[i]:rlist})
        else:
            if y_train[i] != rlist[0]: elist.append({y_train[i]:rlist})
            print rlist
            print y_train[i]

    print ""
    for e in errorlist:
        print e

    for r in elist:
        print r

    print len(errorlist)
    print len(X_train)
    print len(elist)

def getPredict(x,modelDict):
    pDict = dict()
    for k,m in modelDict.iteritems():
        y_predict = m.predict(x)
        pDict[k]=y_predict

    keys = pDict.keys()
    keys.sort()

    return giveResult(pDict)

def giveResult(resultDict):
    keys = resultDict.keys()
    keys.sort()

    sortResult = [resultDict.get(k) for k in keys]

    if all(sortResult) is True: return [keys[0]]
    if any(sortResult) is False: return ("valid","upper")

    nvlist = fakeAuxi(keys,sortResult)
    return nvlist

def fakeAuxi(keys,sortResutl):
    flag = sortResutl[0]
    rlist = list()
    for i, s in enumerate(sortResutl):
        if s == flag: continue
        if s is False:
            flag = s
            continue
        flag = s
        rlist.append(keys[i])

    return rlist

def savePKL(filename,saveObj):
    import pickle

    with open(filename,"wb") as output:
        pickle.dump(saveObj,output)

def readPKL(filename):
    import pickle

    with open(filename,"rb") as input:
        loadObj = pickle.load(input)

    return loadObj

if __name__ == "__main__":
    rootdir = getCSVroot()
    # belleJSON = getCSVjsonPath()
    key = "belle"
    suffix = "11_1"

    (X,y) = getDataSet(key,rootdir,fileNamingPolicyTwo,suffix)

    X_normalized = preprocessing.normalize(X, norm='l2')
    print X_normalized[0]

    ux = X_normalized
    uy = y

    labels = set(list(uy))

    labelList = list()
    plist = list()
    print ""
    print labels
    for yl in sorted(list(labels))[1:-1]:
        tmpY = map(lambda r: r<=yl,list(uy))
        labelList.append((yl,tmpY))
    # labelList.append((sorted(list(labels))[0],[x == sorted(list(labels))[0] for x in list(uy)]))
    # labelList.append((sorted(list(labels))[-1], [x == sorted(list(labels))[-1] for x in list(uy)]))

    # print ""
    # print labelList

    cl = sorted(list(set(uy)))
    cntD = dict()
    for c in cl:
        for yc in uy:
            if c == yc: cntD[c] = cntD.get(c,0)+1

    print cntD

    paraQueue = Queue()
    paraDicts = dict()

    for ytuple in labelList:
        yf,tmpY = ytuple
        tmpp = Process(target=myCrossValid, args=(ux,tmpY,5,yf,paraQueue,))
        tmpp.start()
        plist.append(tmpp)


    for p in plist:
        p.join()
        print ""
        paraDicts.update(paraQueue.get())

    print ""

    for k,v in paraDicts.iteritems():
        print k
        print v


#
# ##<<=====================================================>>
#     tmpDict = dict()
#     tmpDict[245]={'kernel': 'rbf', 'C': 769.293208729815, 'coef0': None, 'degree': None, 'logGamma': -0.8214967897208845}
#     tmpDict[240]={'kernel': 'rbf', 'C': 614.6911761071799, 'coef0': None, 'degree': None, 'logGamma': -0.03274424068129187}
#     tmpDict[220]={'kernel': 'rbf', 'C': 454.42493686634856, 'coef0': None, 'degree': None, 'logGamma': -0.028190104166666424}
#     tmpDict[225]={'kernel': 'rbf', 'C': 608.0283636062602, 'coef0': None, 'degree': None, 'logGamma': -0.017444950828715444}
#     tmpDict[235]={'kernel': 'rbf', 'C': 169.51593203085275, 'coef0': None, 'degree': None, 'logGamma': -0.09701022265615394}
#     tmpDict[230]={'kernel': 'rbf', 'C': 351.8294270833336, 'coef0': None, 'degree': None, 'logGamma': -0.5033805193778467}
#
#
# ##<<======================================================>>
#
    modelDict = dict()
    for k,v in paraDicts.iteritems():
        for r in labelList:
            (yl, tmpY) = r
            if int(k) == int(yl):
                modelDict[k] = myPredictReport(v, k, ux, tmpY)
#
    savePKL("./tmpModels.pkl",modelDict)

    tmpDict = readPKL("./tmpModels.pkl")
    for k,m in modelDict.iteritems():
        print ""
        print k
        print m

    print tmpDict
    print modelDict

    testMyOneVsRest(tmpDict,ux,uy)

    # ##<<======================================================>>



    # for ytuple in labelList:
    #     yf, tmpY = ytuple
    #     print ""
    #     print yf
    #     print tmpY
    #     print list(uy)
    #     paras = myCrossValid(ux,tmpY,5,yf)
    #     myPredictReport(paras,yf,ux,tmpY)

    # X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.20)
    #
    # clf = SVC()
    # clf.fit(X_train, y_train)
    #
    # y_pred = clf.predict(X_test)
    #
    # y_label = sorted(list(set(y)))
    # print y_label
    # print confusion_matrix(y_test, y_pred, labels=y_label)

###=======================================optunity =================================================
    # cv_decorator = optunity.cross_validated(x=X_normalized, y=yB, num_folds=5)
    # cv_decorator = optunity.cross_validated(x=X_normalized[:100], y=yB[:100], num_folds=5)
    # svm_tuned_auroc = cv_decorator(svm_tuned_auroc)
    # #
    # #
    # optimal_svm_pars, info, _ = optunity.maximize_structured(svm_tuned_auroc, space, num_evals=150)
    # print("Optimal parameters" + str(optimal_svm_pars))
    # print("AUROC of tuned SVM: %1.3f" % info.optimum)
    #
    # print set(list(y))
    #
    # df = optunity.call_log2dataframe(info.call_log)
    # df.sort_values('value',ascending = True)
    # print df
###=======================================optunity =================================================



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