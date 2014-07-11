from complexity import *
import pymysql

import socket

hostname = socket.gethostname()

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='APiCS')
#conn = pymysql.connect(host='localhost', port=3307, user='root', passwd='', db='APiCS')

cur = conn.cursor()

outfile = open('/Volumes/Obang/MyDocuments/Saramaccan/Papers/WordStructure/MetricDocumentation.tex', 'w')


cur.execute("""SELECT WALSValueInfo.`Feature_number`, APiCSFeatures.`ShortName`, APiCSFeatures.`ComplexityType`,  WALSValueInfo.`Value_description`, WALSValueInfo.`Complexity`, WALSValueInfo.`ComplexityDocumentation`
FROM WALSValueInfo
INNER JOIN APiCSFeatures
ON WALSValueInfo.`Feature_number` = APiCSFeatures.`WALS-APiCS`
WHERE WALSValueInfo.Complexity is not NULL
ORDER BY WALSValueInfo.`PureFeatureNumber`""")

print >> outfile, "\\begin{longtable}{lllllll}"

for row in cur.fetchall():
	featid, featname, comptype, valuedesc, compscore, documentation = row
	
	featid = featid.replace("WALS ", "")
	featid = featid.replace("A ", "")
	
	if comptype == "Paradigmatic":
		comptype = "{\\sc p}"
	else: comptype = "{\\sc s}"
	
	print >> outfile, featid+"\t&\t", featname+"\t&\t", comptype+"\t&\t", valuedesc+"\t&\t", str(compscore)+"\t&\t", documentation+"\t\\\\"
	
print >> outfile, "\\end{longtable}"
