testStatementOne = """
    select * from
    dlo_3dscan
"""

sizeList = [250,245,240,235,230,225,220]
pDistribute = [0.98,0.97,0.96,0.95,0.94,0.93,0.92]

def generateValidResult(number):
    global sizeList
    import copy

    tmpSizeList = copy.deepcopy(sizeList)
    tmpSizeList.sort()

    vResult = {l:l>=number for l in tmpSizeList}
    return vResult

def randomResult():
    global sizeList
    import copy
    import random

    tmpSizeList = copy.deepcopy(sizeList)
    tmpSizeList.sort()

    rResult = {l:bool(random.getrandbits(1)) for l in tmpSizeList}
    return rResult

def giveResult(resultDict):
    keys = resultDict.keys()
    keys.sort()

    sortResult = [resultDict.get(k) for k in keys]

    if all(sortResult) is True: return ("valid","lower")
    if any(sortResult) is False: return ("valid","upper")

    nvlist = fakeAuxi(keys,sortResult)
    # nvlist = auxi([], sortResult, sortResult[0], [12313])
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

##no tail recursive .... fucking python
# def auxi(keys,rlist,flag,vList):
#     if len(keys) == 0:
#         print vList
#         return vList
#
#     if rlist[0] == flag:
#         auxi(keys[1:],rlist[1:],flag,vList)
#     else:
#         vList.append(keys[0])
#         print len(keys[1:])
#         print vList
#         auxi(keys[1:],rlist[1:],rlist[0],vList)

if __name__ == "__main__":

    for s in sizeList:
        print ""
        print sizeList
        print s
        print generateValidResult(s)
        print giveResult(generateValidResult(s))

    print ""
    print dict(zip(sizeList,pDistribute))

    print ""
    for i in range(10):
        print ""
        i = randomResult()
        print i
        print giveResult(i)