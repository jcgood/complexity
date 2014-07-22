from complexity import *
import pymysql

import socket

hostname = socket.gethostname()

#conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='APiCS')
conn = pymysql.connect(host='localhost', port=3307, user='root', passwd='', db='APiCS')

cur = conn.cursor()

parfile = open('/Volumes/Obang/MyDocuments/Saramaccan/Papers/WordStructure/MetricDocumentationPar.tex', 'w')
synfile = open('/Volumes/Obang/MyDocuments/Saramaccan/Papers/WordStructure/MetricDocumentationSyn.tex', 'w')


cur.execute("""SELECT WALSValueInfo.`Feature_number`, APiCSFeatures.`ShortName`, APiCSFeatures.`ComplexityType`,  WALSValueInfo.`ValShort`, WALSValueInfo.`Complexity`, WALSValueInfo.`ComplexityDocumentation`
FROM WALSValueInfo
INNER JOIN APiCSFeatures
ON WALSValueInfo.`Feature_number` = APiCSFeatures.`WALS-APiCS`
WHERE WALSValueInfo.Complexity is not NULL
ORDER BY WALSValueInfo.`PureFeatureNumber`""")


# To do multirows for the feature names, collect number of values per feature
# This is inefficient, but I'm lazy
numfeatvals = { }
for row in cur.fetchall():
	featid, featname, comptype, valuedesc, compscore, documentation = row
	
	if featname in numfeatvals:
		numfeatvals[featname] += 1
	else:
		numfeatvals[featname] = 1



# Do paradigmatic documentation
cur.execute("""SELECT WALSValueInfo.`Feature_number`, APiCSFeatures.`ShortName`,  WALSValueInfo.`ValShort`, WALSValueInfo.`Complexity`, WALSValueInfo.`ShortComplexityDoc`
FROM WALSValueInfo
INNER JOIN APiCSFeatures
ON WALSValueInfo.`Feature_number` = APiCSFeatures.`WALS-APiCS`
WHERE WALSValueInfo.Complexity is not NULL AND APiCSFeatures.`ComplexityType` = 'Paradigmatic'
ORDER BY APiCSFeatures.`ComplexityType`, WALSValueInfo.`PureFeatureNumber`, WALSValueInfo.`Complexity`, WALSValueInfo.`ValShort`""")


print >> parfile, "\\begin{longtable}{lllllll}"


print >> parfile, "\\Hline"
print >> parfile, "{\\sc id}\t&\t{\\sc feature name}\t&\t{\\sc value name}\t&\t{\\sc n}\t&\t{\\sc justification}\\\\"
print >> parfile, "\\Hline"
print >> parfile, "\\endhead"
print >> parfile, "\\caption{Complexity scores assigned to values for the paradigmatic features in the WALS--APiCS data (continued)}\\\\"
print >> parfile, "\\endfoot"
print >> parfile, "\\caption{Complexity scores assigned to values for the paradigmatic features in the WALS--APiCS data \label{ParComp}}\\\\"
print >> parfile, "\\endlastfoot"


oldfeatname = ""
featcount = 0
for row in cur.fetchall():
	featid, featname, valuedesc, compscore, documentation = row
	
	featid = featid.replace("WALS ", "")
	featid = featid.replace("A", "")

# 	documentation = documentation.replace("One ", "1 ")
# 	documentation = documentation.replace("Two ", "2 ")
# 	documentation = documentation.replace("Three ", "3 ")
# 	documentation = documentation.replace("Four ", "4 ")
# 	documentation = documentation.replace("Five ", "5 ")
# 	documentation = documentation.replace("Six ", "6 ")
# 
# 	documentation = documentation.replace(" one ", " 1 ")
# 	documentation = documentation.replace(" two ", " 2 ")
# 	documentation = documentation.replace(" three ", " 3 ")
# 	documentation = documentation.replace(" four ", " 4 ")
# 	documentation = documentation.replace(" five ", " 5 ")
# 	documentation = documentation.replace(" six ", " 6 ")

 	documentation = documentation.replace("lingueme", "{\\sc lgm}")
 	documentation = documentation.replace("Lingueme", "{\\sc lgm}")
	
	hline = False
	if featname == oldfeatname:
		printfeatname = ""
	else:
		printfeatname = featname
		if featcount > 0:
			hline = True
	
	oldfeatname = featname	
	if hline == True:
		print >> parfile, "\\hline"
		
	print >> parfile, featid+"\t&\t", "\\multirow{"+str(numfeatvals[featname])+"}{1.25in}{"+printfeatname+"}\t&\t", valuedesc+"\t&\t", str(int(round(compscore,0)))+"\t&\t", documentation+"\t\\\\*"
	
	featcount = featcount + 1

print >> parfile, "\\Hline"
print >> parfile, "\\end{longtable}"


# Do syntagmatic documentation
cur.execute("""SELECT WALSValueInfo.`Feature_number`, APiCSFeatures.`ShortName`,  WALSValueInfo.`ValShort`, WALSValueInfo.`Complexity`, WALSValueInfo.`ShortComplexityDoc`
FROM WALSValueInfo
INNER JOIN APiCSFeatures
ON WALSValueInfo.`Feature_number` = APiCSFeatures.`WALS-APiCS`
WHERE WALSValueInfo.Complexity is not NULL AND APiCSFeatures.`ComplexityType` = 'Syntagmatic'
ORDER BY APiCSFeatures.`ComplexityType`, WALSValueInfo.`PureFeatureNumber`, WALSValueInfo.`Complexity`, WALSValueInfo.`ValShort`""")


print >> synfile, "\\begin{longtable}{lllllll}"
print >> synfile, "\\Hline"
print >> synfile, "{\\sc id}\t&\t{\\sc feature name}\t&\t{\\sc value name}\t&\t{\\sc n}\t&\t{\\sc justification}\\\\"
print >> synfile, "\\Hline"
print >> synfile, "\\endhead"
print >> synfile, "\\caption{Complexity scores assigned to values for the syntagmatic features in the WALS--APiCS data (continued)}\\\\"
print >> synfile, "\\endfoot"
print >> synfile, "\\caption{Complexity scores assigned to values for the syntagmatic features in the WALS--APiCS data \label{SynComp}}\\\\"
print >> synfile, "\\endlastfoot"


oldfeatname = ""
featcount = 0
for row in cur.fetchall():
	featid, featname, valuedesc, compscore, documentation = row
	
	featid = featid.replace("WALS ", "")
	featid = featid.replace("A", "")

# 	documentation = documentation.replace("One ", "1 ")
# 	documentation = documentation.replace("Two ", "2 ")
# 	documentation = documentation.replace("Three ", "3 ")
# 	documentation = documentation.replace("Four ", "4 ")
# 	documentation = documentation.replace("Five ", "5 ")
# 	documentation = documentation.replace("Six ", "6 ")
# 
# 	documentation = documentation.replace(" one ", " 1 ")
# 	documentation = documentation.replace(" two ", " 2 ")
# 	documentation = documentation.replace(" three ", " 3 ")
# 	documentation = documentation.replace(" four ", " 4 ")
# 	documentation = documentation.replace(" five ", " 5 ")
# 	documentation = documentation.replace(" six ", " 6 ")

 	documentation = documentation.replace("lingueme", "{\\sc lgm}")
 	documentation = documentation.replace("Lingueme", "{\\sc lgm}")
	
	hline = False
	if featname == oldfeatname:
		printfeatname = ""
	else:
		printfeatname = featname
		if featcount > 0:
			hline = True
	
	oldfeatname = featname	
	if hline == True:
		print >> synfile, "\\hline"
		
	print >> synfile, featid+"\t&\t", "\\multirow{"+str(numfeatvals[featname])+"}{1.25in}{"+printfeatname+"}\t&\t", valuedesc+"\t&\t", str(int(round(compscore,0)))+"\t&\t", documentation+"\t\\\\*"
	
	featcount = featcount + 1

print >> synfile, "\\Hline"
print >> synfile, "\\end{longtable}"
