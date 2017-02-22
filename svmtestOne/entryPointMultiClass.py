
from preprocess import *
from multiprocessing import Process,Queue
from centralizedInfo import *
from svmdataloader import *
import logging


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
    nX,ny,gap,nMin = getDataSetCSV(key, rootdir, fileNamingPolicyTwo, suffix)

    normalizationSetName = suffix+"_"+"normalizationSet.pkl"
    savePKL('Model/'+normalizationSetName,(gap,nMin))
    ux = nX
    uy = ny

    paras = getRBFparas()
    print len(paras)

    paraQueue = Queue()
    paraDicts = dict()
    plist = list()
    tmplist = list()
    listSequments = seqList(tmplist, paras, 5)
    maxDict = {"para": "initial", "accu": 0}

    tmpreport = simpleSVC(ux,uy,(1000,-1),suffix,)

    savePKL('Model/tmpreport.pkl', tmpreport)

    for k, v in tmpreport.iteritems():
        print k
        print v


    # for subParas in listSequments:
    #     for para in subParas:
    #         # tmpp = Process(target=simpleSVC, args=(ux,uy,para,paraQueue))
    #         # tmpp.start()
    #         tmpp = simpleSVC(ux,uy,para,)
    #         plist.append(tmpp)
    #
    #         for k,v in tmpp.iteritems():
    #             print""
    #             print k
    #             print v
    #
    # for p in plist:
    #     paraDicts.update(p)
    #
    # for k,v in paraDicts.iteritems():
    #     sr = v.split()
    #     accu = float(sr[sr.index('total')+1])
    #     if (accu>=maxDict.get("accu")):
    #         maxDict["para"] = k
    #         maxDict["accu"] = accu
    # #
    # print maxDict

    logger.info("<<---------------------------------- svmtestOne Done ------------------------------------>")