
from preprocess import *
from multiprocessing import Process,Queue
from centralizedInfo import *
from svmdataloader import *
import logging
import sys

if __name__ == "__main__":
    logger = logging.getLogger("main")

    # logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)

    loggerFH = logging.FileHandler("svmtestlog.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    loggerFH.setFormatter(formatter)

    logger.addHandler(loggerFH)
    logger.info("<----------------------------------- svmtestOne start ----------------------------------->")

    rootdir = getCSVroot()
    key = "belle"
    suffix = "11_1"
    cnt, dictLists = getManifold(key, rootdir, fileNamingPolicyTwo, suffix)



    if cnt is None:
        logger.debug(dictLists)
        sys.exit(0)

    suitsizeDictLists, scanDictLists, userInfoDictLists, answerDictLists, boottreeDictLists = dictLists

    print scanDictLists[0]

    nX, ny, gap, nMin = getDataSetCSV(key, rootdir, fileNamingPolicyTwo, suffix)
    print nX[0]
    print len(nX[0])
    print len(nX)
    print ""
    print ny[0]
    print set(ny)
    print len(ny)

    tmpIdentifier = range(len(nX[0]))
    headers = ["k"]+["d"+str(i) for i in tmpIdentifier]
    csvdata = [[ny[i]]+list(r) for i,r in enumerate(nX)]
    print headers
    print len(headers)

    print csvdata[0]
    print len(csvdata[0])
    print len(csvdata)

    finalcsv = [headers] + csvdata
    print ""
    print finalcsv[0]
    print len(finalcsv[0])
    print finalcsv[1]
    print len(finalcsv[1])
    print len(finalcsv)

    # import csv
    #
    # nrow = 10000
    # with open('testCSV_'+str(nrow)+'.csv', 'w') as fp:
    #     a = csv.writer(fp, delimiter=',')
    #     a.writerows(finalcsv[:nrow])

    logger.info("<<---------------------------------- svmtestOne Done ------------------------------------>")