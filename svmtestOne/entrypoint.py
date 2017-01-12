from dbloader import *
from svmdataloader import *

rootdir = getCSVroot()
belleJSON = getCSVjsonPath()
key = "belle"

fileCnt, fileList = readFilePathList(key,rootdir,fileNamingPolicyTwo,"11_1")
if fileCnt is not None:
    dataManifold = readcsvFileList(fileList)
else:
    print " Do something else!!"

suitsizeDictLists = dataManifold.get("belle_suitsize")
scanDictLists = dataManifold.get("belle_3dmodel")
userInfoDictLists = dataManifold.get("belle_userinfo")
answerDictLists = dataManifold.get("belle_answer")
boottreeDictLists = dataManifold.get("belle_boottree")


print suitsizeDictLists[0].keys()
print suitsizeDictLists[0]
print ""

print scanDictLists[0].keys()
print scanDictLists[0]
print ""
#
print userInfoDictLists[0].keys()
print userInfoDictLists[0]
print ""
#
print answerDictLists[0].keys()
print answerDictLists[0]
print ""
#
print boottreeDictLists[0].keys()
print boottreeDictLists[0]
print ""