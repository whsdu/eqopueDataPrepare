

def readcsvFile(filepath):
    import csv

    csvResult = list()
    with open(filepath,'rU') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            csvResult.append(row)
    csvFile.close()

    return csvResult

def tmpParseJsonString(eles):
    import collections
    import json

    scanList = list()

    decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
    deles = decoder.decode(eles)

    return deles

def sortKeys(keys):
    less = []
    equal = []
    greater = []

    if len(keys) > 1:
        pivot = int(keys[0][1])
        for sx in keys:
            x = int(sx[1])
            if x < pivot:
                less.append(sx)
            if x == pivot:
                equal.append(sx)
            if x > pivot:
                greater.append(sx)
        # Don't forget to return something!
        return sortKeys(less)+equal+sortKeys(greater)  # Just use the + operator to join lists
    # Note that you want equal ^^^^^ not pivot
    else:  # You need to hande the part at the end of the recursion - when you only have one element in your array, just return the array.
        return keys

def processShoeTypes(typeDict,step2Dict,sid):
    sortedKyes = sortKeys(step2Dict.keys())
    #
    dictKeysString = ','.join(sortedKyes)

    tmplist = typeDict.get(dictKeysString, set())
    tmplist.add(sid)
    typeDict[dictKeysString] = tmplist

    return typeDict

def examfit(stepDictsList):
    import numpy as np
    counter = [1 for stepDict in stepDictsList if stepDict[2].get("fit",None) is True]
    step4R = [(stepDict[3].get('q1'),stepDict[3].get('q2')) for stepDict in stepDictsList if stepDict[2].get("fit",None) is True]

    count4R = dict()
    for r in step4R:
        kr = str(r[0])+","+str(r[1])
        cou = count4R.get(kr,0)
        cou +=1
        count4R[kr] = cou

    return (np.sum(counter),count4R)

def examAppro(stepDictsList):
    for stepDict in stepDictsList:
        if stepDict[2].get("fit",None) is not True:
            step1Dict = stepDict[0]
            step2Dict = stepDict[1]
            step4Dict = stepDict[3]





    return True
if __name__ == "__main__":

    # sr = sortKeys(['q1','q2','q3','q5','q7','q4'])
    # print sr

    tmpfilepath ="freetry/export_csv_file2.csv"
    csvResult = readcsvFile(tmpfilepath)

    errorTuple = (0,0)

    distinctDict = dict()
    typeDict = dict()

    for tmpRow in csvResult:
        step1JSONstring = tmpRow.get("step1",None)
        step2JSONstring = tmpRow.get("step2",None)
        step3JSONstring = tmpRow.get("step3",None)
        step4JSONstring = tmpRow.get("step4",None)

        sid = tmpRow.get("sid",None)

        stepStringList = [step1JSONstring,step2JSONstring,step3JSONstring,step4JSONstring]
        for strings in stepStringList:
            if strings is None:
                siderror,steperror = errorTuple
                errorTuple = (siderror,steperror+1)
                continue
            if sid is None:
                siderror,steperror = errorTuple
                errorTuple = (siderror+1,steperror)
                continue

        if step3JSONstring is '':
            step1Dict, step2Dict, step4Dict = [tmpParseJsonString(jsonString)
                                                for jsonString in
                                                [step1JSONstring, step2JSONstring,step4JSONstring, ]
                                             ]
            step3Dict = {"fit":True}
        else:
            step1Dict,step2Dict,step3Dict,step4Dict = [tmpParseJsonString (jsonString)
                                                   for jsonString in
                                                   [step1JSONstring,step2JSONstring,step3JSONstring,step4JSONstring,]
                                                   ]

        typeDict=processShoeTypes(typeDict,step2Dict,sid)

        sortedKyes = sortKeys(step2Dict.keys())
        dictKeysString = ','.join(sortedKyes)

        tmplist = distinctDict.get(dictKeysString,list())
        tmplist.append([step1Dict,step2Dict,step3Dict,step4Dict])
        distinctDict[dictKeysString] = tmplist
    #

    for k,v in distinctDict.iteritems():
        fitNum,step4WhenFit = examfit(v)
        print k
        print "total amount of try: " + str(len(v))
        print "total fit number: "+ str(fitNum)
        print "step4 result when total fit is: "
        print step4WhenFit
        print ""

        examAppro(v)




    ### ============ typeDict output =====================###
    # print ""
    # print "typeDict output:"
    # for k,v in typeDict.iteritems():
    #     print k
    #     print len(v)
    #     if len(v) < 10: print v
    #
    # print ""
    # print "Result of counting the error JSON: (no step2, no sid)"
    # print errorTuple
    #
    # print len(typeDict.keys())
    ### ============ typeDict output =====================###
