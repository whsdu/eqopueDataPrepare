import logging

"""
    TO BE CENTRALIZED
"""

def getCSVjsonPath():
    logger = logging.getLogger("main.filePathManager.getCSVjsonPath ")

    belleJSON = "/home/wh/PycharmProjects/eqopueTestData/belleconfig.json"

    logger.debug(" get CSV description from " + belleJSON)

    return belleJSON

def getSQLjsonPath():
    logger = logging.getLogger("main.filePathManager.getSQLjsonPath ")

    dbinforJSONpath = "/home/wh/PycharmProjects/eqopueDataProcess/dbloader/dbhost.json"

    logger.debug(" get RDB connection information from " + dbinforJSONpath)

    return dbinforJSONpath


def getCSVroot():
    logger = logging.getLogger("main.filePathManager.getCSVroot ")

    rootdir = "/home/wh/PycharmProjects/eqopueTestData/polling"

    logger.debug(" get CSV folder from "+rootdir)

    return rootdir


