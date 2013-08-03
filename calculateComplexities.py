from complexity import *
import pymysql


#conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='APiCS')
conn = pymysql.connect(host='localhost', port=3307, user='root', passwd='', db='APiCS')

cur = conn.cursor()

# Get data from database
(complexities,names,types,degrees) = getComplexities(cur)
(apicsLangCompPar,apicsLangCompSyn) = getAPiCSFeatureComps(cur,types,complexities,degrees)
(apicsFeatComp,apicsFeatCount,apicsFeatCompList) = getAPiCSLangComps(cur,complexities,apicsLangCompPar)
(walsLangCompPar,walsLangCompSyn) = getWALSFeatureComps(cur,types,complexities,degrees)
(walsFeatComp,walsFeatCount,walsFeatCompList) = getWALSLangComps(cur,complexities,walsLangCompPar)

# Prints results to file among other things
(walsFCompAvgs,apicsFCompAvgs) = getFeatComplexity(walsFeatComp,walsFeatCount,walsFeatCompList,apicsFeatComp,apicsFeatCount,apicsFeatCompList,names,types,degrees)

# Prints results to file among other things
(totalWALSPar,WALSCountPar,WALSLangCompListPar,totalAPiCSPar,APiCSCountPar,APiCSLangCompListPar) = getLangCompPar(walsLangCompPar,apicsLangCompPar)

(totalWALSSyn,WALSCountSyn,WALSLangCompListSyn,totalAPiCSSyn,APiCSCountSyn,APiCSLangCompListSyn) = getLangCompSyn(walsLangCompSyn,apicsLangCompSyn)

to_R(walsFCompAvgs,apicsFCompAvgs,WALSLangCompListPar,WALSLangCompListSyn,APiCSLangCompListPar,APiCSLangCompListSyn)

getLangCompsTable(cur,complexities,names)