from complexity import *
import pymysql
import os

import socket

hostname = socket.gethostname()

#conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='APiCS',)
conn = pymysql.connect(host='localhost', port=3307, user='root', passwd='', db='APiCS')

cur = conn.cursor()

# Get data from database
(complexities,names,types,degrees) = getComplexities(cur)
(apicsLangCompPar,apicsLangCompSyn,apicsLangFeatCompPar,apicsLangFeatCompSyn) = getAPiCSLangComps(cur,types,complexities,degrees)
(apicsFeatComp,apicsFeatCount,apicsFeatCompList) = getAPiCSFeatureComps(cur,complexities,apicsLangCompPar)
(walsLangCompPar,walsLangCompSyn,walsLangFeatCompPar,walsLangFeatCompSyn) = getWALSLangComps(cur,types,complexities,degrees)
(walsFeatComp,walsFeatCount,walsFeatCompList) = getWALSFeatureComps(cur,complexities,walsLangCompPar)

# Prints results to file among other things
(walsFCompAvgs,apicsFCompAvgs,walsFCompAvgsPar,apicsFCompAvgsPar) = getFeatComplexity(walsFeatComp,walsFeatCount,walsFeatCompList,apicsFeatComp,apicsFeatCount,apicsFeatCompList,names,types,degrees)

# Prints results to file among other things
(totalWALSPar,WALSCountPar,WALSLangCompListPar,totalAPiCSPar,APiCSCountPar,APiCSLangCompListPar) = getLangCompPar(walsLangCompPar,apicsLangCompPar)

(totalWALSSyn,WALSCountSyn,WALSLangCompListSyn,totalAPiCSSyn,APiCSCountSyn,APiCSLangCompListSyn) = getLangCompSyn(walsLangCompSyn,apicsLangCompSyn)

to_R(walsFCompAvgs,apicsFCompAvgs,WALSLangCompListPar,WALSLangCompListSyn,APiCSLangCompListPar,APiCSLangCompListSyn,walsFCompAvgsPar,apicsFCompAvgsPar)

getLangCompsTable(cur,complexities,names)

# Generates file
featComparison(apicsLangFeatCompPar,walsLangFeatCompPar,apicsLangCompPar,walsLangCompPar,apicsLangFeatCompSyn,walsLangFeatCompSyn,apicsLangCompSyn,walsLangCompSyn)

# Generates file
getDocumentation(cur)

# Generates file
getValDocumentation(cur)

# Run R script
os.system('Rscript APiCSWALS.r')