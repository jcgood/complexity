from complexity import *
import pymysql

import socket

hostname = socket.gethostname()

#conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='APiCS')
conn = pymysql.connect(host='localhost', port=3307, user='root', passwd='', db='APiCS')

cur = conn.cursor()

outfile = open('/Volumes/Obang/MyDocuments/Saramaccan/Papers/WordStructure/MetricDocumentation.tex', 'w')


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



cur.execute("""SELECT WALSValueInfo.`Feature_number`, APiCSFeatures.`ShortName`, APiCSFeatures.`ComplexityType`,  WALSValueInfo.`ValShort`, WALSValueInfo.`Complexity`, WALSValueInfo.`ComplexityDocumentation`
FROM WALSValueInfo
INNER JOIN APiCSFeatures
ON WALSValueInfo.`Feature_number` = APiCSFeatures.`WALS-APiCS`
WHERE WALSValueInfo.Complexity is not NULL
ORDER BY WALSValueInfo.`PureFeatureNumber`""")


print >> outfile, "\\begin{longtable}{lllllll}"
print >> outfile, "\\Hline"
print >> outfile, "{\\sc id}\t&\t{\\sc feature name}\t&\t{\\sc p/s}\t&\t{\\sc value name}\t&\t{\\sc n}\t&\t{\\sc justification}\\\\"
print >> outfile, "\\Hline"

oldfeatname = ""
featcount = 0
for row in cur.fetchall():
	featid, featname, comptype, valuedesc, compscore, documentation = row
	
	featid = featid.replace("WALS ", "")
	featid = featid.replace("A ", "")

	documentation = documentation.replace("One ", "1 ")
	documentation = documentation.replace("Two ", "2 ")
	documentation = documentation.replace("Three ", "3 ")

	
	hline = False
	if featname == oldfeatname:
		printfeatname = ""
	else:
		printfeatname = featname
		if featcount > 0: hline = True
	
	if comptype == "Paradigmatic":
		comptype = "{\\sc p}"
	else: comptype = "{\\sc s}"

	oldfeatname = featname	
	if hline == True:
		print >> outfile, "\\hline"
	print >> outfile, featid+"\t&\t", "\\multirow{"+str(numfeatvals[featname])+"}{1in}{"+printfeatname+"}\t&\t", comptype+"\t&\t", valuedesc+"\t&\t", str(int(round(compscore,0)))+"\t&\t", documentation+"\t\\\\"
	featcount = featcount + 1

print >> outfile, "\\Hline"
print >> outfile, "\\end{longtable}"
