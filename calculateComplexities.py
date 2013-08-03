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

# Prints results to file on desktop
getFeatComplexity(walsFeatComp,walsFeatCount,walsFeatCompList,apicsFeatComp,apicsFeatCount,apicsFeatCompList,names,types,degrees)

(totalWALSPar,WALSCountPar,WALSLangCompListPar,totalAPiCSPar,APiCSCountPar,APiCSLangCompListPar) = getLangCompPar(walsLangCompPar,apicsLangCompPar)

# apicslangvector = robj.FloatVector(APiCSLangCompListPar)
# walslangvector = robj.FloatVector(WALSLangCompListPar)
# t = robj.r['t.test']
# p = t(apicslangvector,walslangvector,**{'var.equal': True}) # Do two-sample t-test assuming equal variance
# print p

(totalWALSSyn,WALSCountSyn,WALSLangCompListSyn,totalAPiCSSyn,APiCSCountSyn,APiCSLangCompListSyn) = getLangCompSyn(walsLangCompSyn,apicsLangCompSyn)

# apicslangsynvector = robj.FloatVector(APiCSLangCompListSyn)
# walslangsynvector = robj.FloatVector(WALSLangCompListSyn)
# t = robj.r['t.test']
# p = t(apicslangsynvector,walslangsynvector,**{'var.equal': True}) # Do two-sample t-test assuming equal variance
#print p


rfile = open('APiCSWALS.r', 'w')

print >> rfile, "library(ggplot2)"
print >> rfile, "library(plyr)"


print >> rfile, "alangcompPar <- c(", ",".join(map(str, APiCSLangCompListPar)), ")"
print >> rfile, "wlangcompPar <- c(", ",".join(map(str, WALSLangCompListPar)), ")"
print >> rfile, "alangcompSyn <- c(", ",".join(map(str, APiCSLangCompListSyn)), ")"
print >> rfile, "wlangcompSyn <- c(", ",".join(map(str, WALSLangCompListSyn)), ")"

print >> rfile, "alangcompParDF = as.data.frame(alangcompPar)"
print >> rfile, "wlangcompParDF = as.data.frame(wlangcompPar)"
print >> rfile, "alangcompSynDF = as.data.frame(alangcompSyn)"
print >> rfile, "wlangcompSynDF = as.data.frame(alangcompSyn)"

print >> rfile, "alangcompParDF$set = \"APiCS\""
print >> rfile, "alangcompSynDF$set = \"APiCS\""
print >> rfile, "wlangcompParDF$set = \"WALS\""
print >> rfile, "wlangcompSynDF$set = \"WALS\""

print >> rfile, "awPar = rbind(alangcompParDF,wlangcompParDF)"
print >> rfile, "awSyn = rbind(alangcompSynDF,wlangcompSynDF)"
