

def simpleSVC(X,y,paras,paraQue=None):
    from sklearn.cross_validation import train_test_split
    from sklearn.svm import SVC
    from sklearn.metrics import classification_report
    import pickle

    C,logGamma = paras

    # X_normalized = preprocessing.normalize(X, norm='l2')
    X_normalized = X

    X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.20)

    model = SVC(kernel='rbf', C=C, gamma=10 ** logGamma)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    report = classification_report(y_test, y_pred)
    key = "C:"+str(C)+"_"+"logGamma:"+str(logGamma)

    sr = report.split()
    accu = float(sr[sr.index('total') + 1])
    if accu >= 0.75:
        modelName = key + '.pkl'
        with open('Model/' + modelName, 'wb') as f:
            pickle.dump(model, f)

    if paraQue is not None:
        paraQue.put({key: report})

    return {key: report}

def getRBFparas(logGammaStep = 1, logGammaRange = [-5,0],CStep = 100,CRange = [100,1000]):

    lowerL,upperL = logGammaRange
    lowerC,upperC = CRange


    logGammaList = range(lowerL,upperL+logGammaStep,logGammaStep)

    # Clist = range(lowerC,upperC+CStep,CStep)
    Clist = [0.1, 1, 10, 100, 1000]

    return [[C,l] for l in logGammaList for C in Clist]

"""
    >>> tl = range(0,10)
    >>> tl
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> sql = seqList([],tl,3)
    >>> sql
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
"""
def seqList(initlist,inputlist,seq):
    if seq>=len(inputlist):
        initlist.append(inputlist)
        return initlist
    if seq<len(inputlist):
        initlist.append(inputlist[0:seq])
        return seqList(initlist,inputlist[seq:],seq)


def normalizeByAxisZero(Lists):
    import numpy as np
    X,y = list2nlist(Lists)

    nMin = X.min(axis = 0)
    gap = X.max(axis = 0) - nMin
    normalizedX = 1.0*(X-nMin)/gap

    normalizedX[np.isnan(normalizedX)] = 0

    return (normalizedX,y)

def list2nlist(lists):
    import numpy as np

    data_set = np.asarray(lists)
    X = data_set[:, 2:]
    y = data_set[:, 1]

    return (X,y)