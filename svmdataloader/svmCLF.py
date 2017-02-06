
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

def seqList(initlist,inputlist,seq):
    if seq>=len(inputlist):
        initlist.append(inputlist)
        return initlist
    if seq<len(inputlist):
        initlist.append(inputlist[0:seq])
        return seqList(initlist,inputlist[seq:],seq)