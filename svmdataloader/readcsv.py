
from svmfileIO import *
import logging

"""
    Type: String -> String -> (String -> Int) -> String -> Either (Maybe Int [String]) (Maybe None String)
    Applicative Paras:
        keyname: Target files' names must contain this key.
        dirname: Looking for target files in this directory.
        fileNamingPolicy: The definition of naming policy.
        readlast: OPTIONAL !!! The Suffix of target files.
    Return:
        dirCnt: number of sub-directories of give directory that contain target files.
        targetFiles: List of full path files. Its dimension is dirCnt.

    Description:
        wrap both file extraction functions (files with certain suffix and most recent files)
        When file Cnt is None, fileList would contain error message.
"""

def readFilePathList(keyname,dirname,fileNamingPolicy,readlast = True):
    if readlast==True:
        print "last"
        fileCnt, fileList = getMostRecentFiles(keyname,dirname,fileNamingPolicy=fileNamingPolicy)
    else:
        fileCnt, fileList = getCertainFiles(keyname,dirname,readlast,fileNamingPolicy=fileNamingPolicy)

    return (fileCnt,fileList)


"""
    type Dimension = String
    type InfoType = String

    Type: [String] -> String -> [{InfoType:[{Dimension:Float}]}]
    Applicative Paras:
        filePathList: Full Path of all target files
        suffix: When skipped, the default engaged dimension will be implemented.
    Return:
        Data structure :: [{InfoType:[{Dimension:Float}]}]
"""
def readcsvFileList(filePathList,suffix=None):

    if suffix == None:
        filterList ={ele[0]:list(ele) for ele in
                     zip(
                         map(getFileCategory,filePathList),
                        ["engagedDimension"]*len(filePathList)
                        )
                     }
    else:
        filterList ={ele[0]:list(ele) for ele in
                    zip(
                        map(getFileCategory, filePathList),
                        [suffix] * len(filePathList),
                        ["engagedDimension"] * len(filePathList)
                        )
                     }
    print filterList

    csvResult = {
        getFileCategory(filePath):
            readcsvFileOrdered(
                filePath,
                getEngagedDimension(
                    filterList.get(
                        getFileCategory(filePath)
                    )
                )
            )
        for filePath in filePathList
        }

    return csvResult

"""
    Type: String -> [String] -> [{Dimension:Float}]
    Applicative Paras:
        filePath: The full path of a target file.
        filterList: The desired engaged dimensions.
    Return:
        csvResult::[{Dimension:Float}]
            List of dictionaries. Keys are engaged dimensions.
"""
def readcsvFile(filepath,filterList):
    import csv

    if filterList is None:
        return (None,"engaged dimension not match!")

    with open(filepath,'rU') as csvFile:
        reader = csv.reader(csvFile)
        headers = reader.next()

    if set(filterList).issubset(set(headers)):
        csvFile.close()
    else:
        csvFile.close()
        return (None,filepath+" does not contain all engaged dimensions, please check the name of corresponding file")

    csvResult = list()
    with open(filepath,'rU') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            csvResult.append(
                {k:row[k] for k in filterList}
            )
    csvFile.close()

    return csvResult

"""
    Type: String -> [String] -> [{Dimension:Float}]
    Applicative Paras:
        filePath: The full path of a target file.
        filterList: The desired engaged dimensions.
    Return:
        csvResult::[{Dimension:Float}]
            List of dictionaries. Keys are engaged dimensions.
"""
def readcsvFileOrdered(filepath,filterList):
    import csv
    import collections

    if filterList is None:
        return (None,"engaged dimension not match!")

    with open(filepath,'rU') as csvFile:
        reader = csv.reader(csvFile)
        headers = reader.next()

    if set(filterList).issubset(set(headers)):
        csvFile.close()
    else:
        csvFile.close()
        return (None,filepath+" does not contain all engaged dimensions, please check the name of corresponding file")

    csvResult = list()
    with open(filepath,'rU') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            od = collections.OrderedDict()
            for k in filterList:
                od[k]=row[k]
            csvResult.append(od)
    csvFile.close()

    return csvResult

"""
    Type: [{Dimension:Float}] -> [{Dimension:Float}] -> [String]  -> Any -> String -> [{Dimension:Float}]
    Applicative Paras:
        leftCSVDicts: A list of dictionaries
        rightCSVDicts: A list of dictionaries
        joinKeyList: The key dimensions for join action
        nan: value for NaN value
        how: 'left','right',etc
    Return:
        leftjoinDicts:: [{Dimension:Float}]
            Dataset after join action
"""
def dataJoin(leftCSVDicts,rightCSVDicts,joinKeyList=None,left_on = None,right_on= None,fnan = 0,how = 'left'):
    from pandas import merge
    if any(len(dictList) == 0 for dictList in [leftCSVDicts,rightCSVDicts]):
        return (None, "Please do not use empty dataSet")

    if all(joinSet is None for joinSet in[joinKeyList,left_on,right_on]):
        return (None, "Please provide information about join keys!")

    leftKeys,leftlists = dicts2lists(leftCSVDicts)
    rightKeys,rightlists = dicts2lists(rightCSVDicts)

    leftframe = getDataFrame(leftKeys,leftlists)
    rightframe = getDataFrame(rightKeys,rightlists)

    if joinKeyList is not None \
            and \
            not all(set(joinKeyList).issubset(set(dataFrame.keys())) for dataFrame in [leftframe,rightframe]):
        return (None,"At least one dataset doesn't contain one of these common join keys!" )

    if left_on is not None and \
                    right_on is not None and \
                        not all(
                            [
                                set(left_on).issubset(set(leftframe.keys())),
                                set(right_on).issubset(set(rightframe.keys()))
                            ]
                        ):
        return (None, "At leaset one joint key is not match!!")

    if any(joinOn is None for joinOn in [left_on,right_on]):
        left_on = joinKeyList
        right_on = joinKeyList

    leftjoin = merge(leftframe,rightframe,how=how,left_on=left_on,right_on=right_on)
    leftjoin.fillna(fnan,inplace = True)
    leftjoinDicts = lists2dicts(leftjoin.columns.values,leftjoin.as_matrix()[1:])
    return (len(leftjoinDicts),leftjoinDicts)


"""
    Type: [{Dimension:Float}] -> lambda x: (x[0],x[1]...) -> ( []->[] ) ->[[]]
    Applicative Paras:
        csvByModuleDicts: The list of dictionaries
        lambda4keys: lambda function with the form ( lambda x: (x[0],x[1]...) indexes in the function body are keys of group operation.
        groupOpeartionF: the function which handle list of records of a same key.
    Return:
        outputlists::[[]]
            Due to this groupby operation, the original name of each dimension cannot be preserved, therefore
        please construct a list of new names, and by calling lists2dicts, you could get the type [{Dimension:Float}]  back.
"""
def groupbyDict(csvByModuleDicts,lambda4keys,groupOpeartionF):
    from itertools import groupby

    keys,lists = dicts2lists(csvByModuleDicts)

    sortedlist = sorted(lists,key = lambda4keys)

    outputlists = list()
    for k, g in groupby(sortedlist,lambda4keys):
        outputlists.append(list(k)+[groupOpeartionF(g)])

    return outputlists

"""
    Type: [{Dimension:Float}] -> String -> ( a -> [[a]] ) ->[[]]

    Applicative Paras:
        csvByModuleDicts: The list of dictionaries
        splitkey: The dimension that will be splitted
        splitOperationF: split operation which will convert an instance of a data type to a list of several data types.
    Return:
        newlists::[[]]
            This is the operation which usually being used to seperate information of left and right foot,
        since these information is being recorded as a tuple currently. Due to the split operation, the original name of
        each dimension cannot be preserved, therefore please construct a list of new names, and by calling lists2dicts,
        you could get the type [{Dimension:Float}]  back.
"""
def rowSplit(csvByModuleDicts,splitkey,splitOperationF):
    import copy

    keys, lists = dicts2lists(csvByModuleDicts)
    if splitkey not in keys: return (None, "Please provide correct dimenson name!")

    dIndex = keys.index(splitkey)

    newlists = []
    for tl in lists:
        splitResult = splitOperationF(tl[dIndex])
        for r in splitResult:
            if not (isinstance(r, list)): r = [r]
            r.reverse()
            tmpCopy = copy.deepcopy(tl)
            del tmpCopy[dIndex]
            [tmpCopy.insert(dIndex, i) for i in r]

            newlists.append(tmpCopy)

    return newlists

"""
    Type: [{Dimension:Float}] -> [String] -> [{Dimension:Float}]
    Applicative Paras:
        csvByModuleDicts: The list of dictionaries
        removeKey: Dimensions that yet to be removed.
    Return:
        amended::[{Dimension:Float}]
"""
def removeDimensions(csvByModuleDicts,removeKey):
    amended =[
        {
            k:v for k,v in d.iteritems() if k not in removeKey
            }
        for d in csvByModuleDicts
        ]
    return amended


"""
    Type: [{Dimension:Float}] -> ( Hashable::a ==> a -> b -> c ) -> [{Dimension:Float}]
    Applicative Paras:
        csvByModuleDicts: The list of dictionaries
        replaceF :: Could be a filter or any other functions which took two parameters
    Return:
        amended::[{Dimension:Float}]
"""
def replace(csvByModuleDicts,replaceF):
    amended = [
        {
            k:replaceF(k,v) for k, v in d.iteritems()
            }
        for d in csvByModuleDicts
    ]
    return amended

def removeRows(csvByModuleDicts,filterF):
    rList = list()
    for d in csvByModuleDicts:
        if filterF(d): rList.append(d)
    return rList

"""
    Type: [{Dimension:Float}] ->([String],[[]])
    Applicative Paras:
        dicts:The list of dictionaries
    Return:
        Keys: list of keys of the original list of dictionaries.
        lists: list of lists which store the values of original list of dictionaries.

    Description:
        Convert a list of dictionaries to a tuple( keys , list of values).
        inverse function of lists2dicts
"""
def dicts2lists(dicts):
    lists = [
                [v for v in d.values()]
            for d in dicts
            ]
    keys = dicts[0].keys()

    return (keys,lists)


"""
    Type: ([String],[[]]) -> [{Dimension:Float}]
    Applicative Paras:
        Keys: list of keys of the original list of dictionaries.
        lists: list of lists which store the values of original list of dictionaries.
    Return:
        dicts:The list of dictionaries
    Description:
        Convert a tuple( keys , list of values) to a list of dictionaries.
        inverse function of dicts2lists.
"""
def lists2dicts(keys,lists):
    import collections
    dicts = [collections.OrderedDict(zip(keys,list)) for list in lists]
    return dicts

"""
    Type :: ([String],[[]]) -> Panads.DataFrame
    Applicative Paras:
        Keys: list of keys of the original list of dictionaries.
        lists: list of lists which store the values of original list of dictionaries.
    Return:
        Panads.DataFrame , being used to do Pandas Merge operation.
"""
def getDataFrame(keys,lists):
    from pandas import DataFrame
    return DataFrame([keys]+lists,columns = keys)