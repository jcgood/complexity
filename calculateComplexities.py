#!/usr/bin/env python

# A native python MySQL library
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='APiCS')
cur = conn.cursor()



cur.execute("SELECT `Feature_number`, `Values_number`, Complexity FROM WALSValueInfo")

complexities = { }
for row in cur.fetchall():
	feat, value, complexity = row
	
	if feat in complexities:
		compfeat = complexities[feat]
		compfeat[str(value)] = complexity
		complexities[feat] = compfeat
		
	else:
		compfeat = {}
		compfeat[str(value)] = complexity
		complexities[feat] = compfeat

#for f in complexities:
#	print f, complexities[f]

cur.execute("""SELECT APiCSValues.Language, APiCSValues.Values, APiCSValues.Frequencies, APiCSFeatures.`WALS-APICS`
FROM APiCSValues
INNER JOIN APiCSFeatures ON APiCSValues.`Feature_number` = APiCSFeatures.`Feature_number`
WHERE APiCSFeatures.`WALS-APICS` != \"None\"""")

# A stub for getting some complexities, not primed for paradigmatic, syntagmatic, etc.
creoleFeatComp = {}
creoleFeatLangCount = {}
for row in cur.fetchall():
	lang, values, freqs, feat = row # need to work in freqs still
	compfeat = complexities[feat]
	
	#print feat, values
	values = values.split(", ")
	
	#print "v", values[0]
	# Increment counter for averaging if there's at least one value
	if values[0]:
		if feat in creoleFeatLangCount:
			creoleFeatLangCount[feat] += 1
		else:
			creoleFeatLangCount[feat] = 1


	totalValue = 0
	valCount = 0
	# Can be multiple values in APiCS
	for value in values:
		#print feat, value
		# Need this until I get mapping file for APiCS/WALS
		if value in compfeat:
			compValue = compfeat[value]
			# Placeholder for now
			if compValue is not None:
				#print feat, value
				totalValue += compValue		
				valCount += 1			
				
		
	# Conditionals because DB incomplete, remove when complete for error checking
	avgValue = 0 # Needed due to incomplete status of DB
	if valCount != 0: avgValue = totalValue/float(valCount)
	if avgValue != 0:
		#print feat, lang, avgValue
		if feat in creoleFeatComp:
			creoleFeatComp[feat] += avgValue
		else:
			creoleFeatComp[feat] = avgValue

# Get average complexity
for feat in creoleFeatComp:
	compval = creoleFeatComp[feat]
	#print "AVG: ", creoleFeatLangCount[feat]
	compavg = compval / float(creoleFeatLangCount[feat])
	print "APiCS: ", feat, compavg
	

# Now do the same thing for the WALS languages
cur.execute("""SELECT WALSValues.langid, WALSValues.Value_number, WALSValues.Feature_number
FROM WALSValues""")


walsFeatComp = {}
walsFeatLangCount = { }
for row in cur.fetchall():
	lang, value, feat = row # need to work in freqs still
	compfeat = complexities[feat]
	compValue = compfeat[str(value)]
	# Since the DB is incomplete need conditional
	if compValue != None:
		if feat in walsFeatComp:
			walsFeatComp[feat] += compValue
			walsFeatLangCount[feat] += 1
		else:
			walsFeatComp[feat] = compValue
			walsFeatLangCount[feat] = 1



# Get average complexity
for feat in walsFeatComp:
	compval = walsFeatComp[feat]
	compavg = compval / float(walsFeatLangCount[feat])
	print "WALS: ", feat, compavg



cur.close()
conn.close()