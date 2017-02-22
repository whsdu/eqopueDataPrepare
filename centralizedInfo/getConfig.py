"""
    TO BE centralized ...
"""
import logging

def getModelConf():
    path1 = 'models/11_1_C:1000_logGamma:-1.pkl'
    path2 = 'models/11_1_normalizationSet.pkl'
    return (path1,path2)

def getRDBinfo():
    queryStatement =  """
    select t1.id,t1.scan_date,t1.scan_id,t1.customer_id,t1.customer_info,t1.measurement_items from
    #select count(1) from
    dlo_3dscan as t1
    left join
    (
        select scan_id,max(scan_date) as ldate
        from
        dlo_3dscan
        group by scan_id
    ) as t2
    on t1.scan_id = t2.scan_id and t1.scan_date = t2.ldate
    where t2.scan_id is not null
    limit 100
    """
    hostname = 'dlo'
    dbname = "t_dlodb"

    return (queryStatement, hostname, dbname)

def getModelContex():
    import pickle
    modelPath, normalPath = getModelConf()

    with open(normalPath, "rb") as input:
        gap,nMin = pickle.load(input)
    input.close()

    with open(modelPath, "rb") as input:
        svcModel = pickle.load(input)
    input.close()

    return (svcModel,gap,nMin)

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


