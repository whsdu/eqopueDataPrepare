"""
    Package svmdataloader.
    Parsing file path, file name and suffix.

    Author: Emmett Ng (Wu Hao)
"""


####=========================================================####

# testJSON = "/home/wh/PycharmProjects/testresources/testmata.json"
# belleJSON = "/home/wh/PycharmProjects/eqopueTestData/belleconfig.json"


"""
    Type: String -> String -> Maybe (Num,[[String]])
    Applicative Paras:
        keyname: Target files' names must contain this key.
        dirname: Looking for target files in this directory.
    Return:
        dirCnt: number of sub-directories of give directory that contain target files.
        filePath: 2D array (Normally). For instance, if dirCnt is 3 and there are 4 files each sub-directory, then the filePath will be a [3,4] array.

    Description: Auxiliar Function for getting full path from a given directory.
"""
def getFilePathList(keyname,dirname):
    import os

    filePathList = list()
    dirCnt = None

    for root, dirs, files in os.walk(dirname):
        flist = [x for x in files if keyname in x]

        if len(flist) == 0: continue

        tmp = map(lambda x: root + "/" + x, flist)
        filePathList.append(tmp)
        dirCnt = len(filePathList)

    return (dirCnt,filePathList)

"""
    Type: String -> String -> (fileNaingPolicy:: string -> Num) -> Either (Maybe Int [String]) (Maybe None String)
    Appilcative Paras:
        keyname: Target files must contain this key string.
        dirname: Looking for target files in this directory.
        fileNamingPolicy: The definition of naming policy.
    Return:
        dirCnt: number of sub-directories of give directory that contain target files.
        maxFile: List of full path files. Its dimension is dirCnt.

    Description:
        To get the most recent receated files.
        Return None and error message once suffixes of most recent files from different sub-directories cannot match.
"""
def getMostRecentFiles(keyname,dirname,fileNamingPolicy):
    import os.path

    ## whether the given directory contains desired files    ##
    dirCnt,filePaths = getFilePathList(keyname,dirname)
    if dirCnt is None:
        return(None,"Cannot parse given directory successfully! Please check again!!!")

    ## get the most recent created files ##
    maxFile = list()
    for fs in filePaths:
        mtimelist = map(os.path.getmtime,[f for f in fs])
        maxFile.append(fs[mtimelist.index(max(mtimelist))])

    ## whether suffixes of most recent created files are the same ##
    epochlist = map(fileNamingPolicy,maxFile)
    if all(el == sum(epochlist)/len(epochlist) for el in epochlist):
        return (dirCnt,maxFile)
    else:
        return (None,"The most recent files of different dirs DO NOT MATCH !!!")

"""
    Type: getCertainFiles :: String -> String -> String -> (fileNaingPolicy:: string -> Int) -> Either (Maybe Int [String]) (Maybe None String)

    Applicative Paras:
        keyname: Target files must contain this key string.
        dirname: Looking for target files in this directory.
        fileNameSuffix: Target files must contain this Suffix.
        fileNamingPolicy: The definition of naming policy.

    Retrun:
        dirCnt: number of sub-directories of give directory that contain target files.
        targetFiles: List of full path files. Its dimension is dirCnt.

    Description:
        To get files with given suffix.
        Return None and error message once some sub-directorie does not contain file with given suffix.
"""
def getCertainFiles(keyname,dirname,fileNameSuffix,fileNamingPolicy):

    ## whether the given directory contains desired files ##
    dirCnt,filePaths = getFilePathList(keyname,dirname)
    if dirCnt is None:
        return(None,"Cannot parse given directory successfully! Please check again!!!")


    targetFiles = [f for fs in filePaths for f in fs if int(filter(str.isdigit,fileNameSuffix)) == fileNamingPolicy(f)]

    if len(targetFiles) == dirCnt:
        return (dirCnt,targetFiles)
    else:
        return (None,"Cannot find files with given suffix.")



"""
    Type: fileNamingPolicy :: String -> Int

    Applicative para:
        filename: the full path of a file

    Return value:
        identifier: Numerical identifies which can be used for further verification

    Description:
        File naming policies defines different possible suffix.
"""
def fileNamingPolicyOne(filename):
    identifier = int(filename.split(".")[0][-1])
    return identifier

def fileNamingPolicyTwo(filename):
    splitParts = filename.split("/")[-1].split("_")
    identifier = int(splitParts[2])*10+int(splitParts[3][0])
    return identifier


"""
    Type: [String] -> Any
    Applicative Para:
        keyList: keys of JSON config file.
    Return:
        value:
            value correspond to keylist.
            return None if no value found.
    Description:
        Extract engaged dimension of files of different categories.
"""
def getEngagedDimension(keyList):
    import json
    from filePathManager import getCSVjsonPath
    # global testJSON     ## to be centralized
    # global belleJSON    ## to be centralized

    belleJSON = getCSVjsonPath()

    def auxiliarRec(tmpvalue,keylist):
        if len(keylist) == 0 and tmpvalue is not None:
            return tmpvalue
        if tmpvalue is None:
            return None
        if tmpvalue is not None and len(keylist) != 0:
            return auxiliarRec(tmpvalue.get(keylist[0],None),keylist[1:])

    with open(belleJSON) as data_file:
        data = json.load(data_file)
        value = auxiliarRec(data,keyList)

    return value

"""
    Type: String -> String
    Applicative Para:
        filePath: full path of a file
    Return:
        filetype: correspond to

    Description:
        Extract file type which will be used to get engaged dimension from config json file.
"""
def getFileCategory(filePath):
    splitpart = filePath.split("/")[-1].split("_")
    return splitpart[0]+"_"+splitpart[1]

