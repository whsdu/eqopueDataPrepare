
from svmdataloader import *
from multiprocessing import Process,Queue
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
    nX,ny = getDataSet(key, rootdir, fileNamingPolicyTwo, suffix)

    ux = nX
    uy = ny

    paras = getRBFparas()

    paraQueue = Queue()
    paraDicts = dict()
    plist = list()
    tmplist = list()
    listSequments = seqList(tmplist, paras, 5)
    maxDict = {"para": "initial", "accu": 0}

    tmpreport = simpleSVC(ux,uy,(1000,-1),)
    for k, v in tmpreport.iteritems():
        print k
        print v

    logger.info("<<---------------------------------- svmtestOne Done ------------------------------------>")