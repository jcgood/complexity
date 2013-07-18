#!/usr/bin/env python

# A native python MySQL library
import pymysql
import rpy2.robjects as robj

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='APiCS')
#conn = pymysql.connect(host='localhost', port=3307, user='root', passwd='', db='APiCS')
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



# Make a dictionary for feature names
cur.execute("SELECT `Feature_number`, `Feature_name` FROM WALSFeatureNames")
names = { }
for row in cur.fetchall():
	feat, name = row	
	names[feat] = name


# Make a dictionary for feature types
cur.execute("SELECT `WALS-APICS`, `ComplexityType` FROM APiCSFeatures")
types = { }
for row in cur.fetchall():
	feat, type = row	
	if feat != "None":
		types[feat] = type



# Go through the WALS-like APiCS values and (i) calculate complexity averages and (ii) build up lists of values for statistical processing
cur.execute("""SELECT WALSAPiCSValues.Language, APiCSFeatures.`WALS-APICS`,  WALSAPiCSValues.Wals_value_number
FROM WALSAPiCSValues
INNER JOIN APiCSFeatures ON WALSAPiCSValues.`APiCS_number` = APiCSFeatures.Feature_number
WHERE APiCSFeatures.`WALS-APICS` != \"None\"""")

apicswalsFeatComp = { }
apicswalsFeatLangCount = { }
apicsCompList = { } # For statistical processing
for row in cur.fetchall():
	lang, feat, value = row
	compfeat = complexities[feat]
	compValue = compfeat[str(value)]
	# Since the DB is incomplete need conditional, remove when believed complete for error checking
	if compValue != None:
		if feat in apicswalsFeatComp:
			apicswalsFeatComp[feat] += compValue
			apicswalsFeatLangCount[feat] += 1
			apicsCompList[feat].append( compValue )
		else:
			apicswalsFeatComp[feat] = compValue
			apicswalsFeatLangCount[feat] = 1
			apicsCompList[feat] = [ compValue ]


# Now do the same thing for the WALS languages
cur.execute("""SELECT WALSValues.langid, WALSValues.Value_number, WALSValues.Feature_number
FROM WALSValues""")

walsFeatComp = {}
walsFeatLangCount = { }
walsCompList = { } # See comments above
for row in cur.fetchall():
	lang, value, feat = row
	compfeat = complexities[feat]
	compValue = compfeat[str(value)]
	# Since the DB is incomplete need conditional
	if compValue != None:
		if feat in walsFeatComp:
			walsFeatComp[feat] += compValue
			walsFeatLangCount[feat] += 1
			walsCompList[feat].append( compValue )

		else:
			walsFeatComp[feat] = compValue
			walsFeatLangCount[feat] = 1
			walsCompList[feat] = [ compValue ]

#print walsCompList


# Get average complexity for APiCS and WALS; features should be precisely the same
for feat in walsFeatComp:
	print feat+",", names[feat]+",", types[feat]
	walscompval = walsFeatComp[feat]
	walscompavg = walscompval / float(walsFeatLangCount[feat])
	apicscompval = apicswalsFeatComp[feat]
	apicscompavg = apicscompval / float(apicswalsFeatLangCount[feat])
	
	apicsvals = apicsCompList[feat]
	walsvals = walsCompList[feat]
	
	apicsvector = robj.IntVector(apicsvals)
	walsvector = robj.IntVector(walsvals)
	t = robj.r['t.test']
	p = t(apicsvector,walsvector,**{'var.equal': True})[2][0] # Do two-sample t-test assuming equal variance
	
	print "WALS average: ", walscompavg
	print "APiCS average: ", apicscompavg
	print "p-value = ", p
	print ""


cur.close()
conn.close()

## TO SELF: SEGMENTAL FEATURES?
## TO SELF: Prohibitive is paradigmatic and syntagmatic complexity? Can I even really test syntagmatic here?


# THIS WAS FOR WHEN I THOUGHT I COULD USE THE VARIABLE FEATURES OF APICS, BUT I HAVE NO GOOD WAY OF COMPARING THEM TO WALS
#for f in complexities:
#	print f, complexities[f]

# For real APiCS values
# cur.execute("""SELECT APiCSValues.Language, APiCSValues.Values, APiCSValues.Frequencies, APiCSFeatures.`WALS-APICS`
# FROM APiCSValues
# INNER JOIN APiCSFeatures ON APiCSValues.`Feature_number` = APiCSFeatures.`Feature_number`
# WHERE APiCSFeatures.`WALS-APICS` != \"None\"""")
# 
# # A stub for getting some complexities, not primed for paradigmatic, syntagmatic, etc.
# creoleFeatComp = {}
# creoleFeatLangCount = {}
# for row in cur.fetchall():
# 	lang, values, freqs, feat = row # need to work in freqs still
# 	compfeat = complexities[feat]
# 	
# 	#print feat, values
# 	values = values.split(", ")
# 	
# 	#print "v", values[0]
# 	# Increment counter for averaging if there's at least one value
# 	if values[0]:
# 		if feat in creoleFeatLangCount:
# 			creoleFeatLangCount[feat] += 1
# 		else:
# 			creoleFeatLangCount[feat] = 1
# 
# 
# 	totalValue = 0
# 	valCount = 0
# 	# Can be multiple values in APiCS
# 	for value in values:
# 		#print feat, value
# 		# Need this until I get mapping file for APiCS/WALS
# 		if value in compfeat:
# 			compValue = compfeat[value]
# 			# Placeholder for now
# 			if compValue is not None:
# 				#print feat, value
# 				totalValue += compValue		
# 				valCount += 1			
# 				
# 		
# 	# Conditionals because DB incomplete, remove when complete for error checking
# 	avgValue = 0 # Needed due to incomplete status of DB
# 	if valCount != 0: avgValue = totalValue/float(valCount)
# 	if avgValue != 0:
# 		#print feat, lang, avgValue
# 		if feat in creoleFeatComp:
# 			creoleFeatComp[feat] += avgValue
# 		else:
# 			creoleFeatComp[feat] = avgValue
# 
# # Get average complexity
# for feat in creoleFeatComp:
# 	compval = creoleFeatComp[feat]
# 	#print "AVG: ", creoleFeatLangCount[feat]
# 	compavg = compval / float(creoleFeatLangCount[feat])
# 	print "APiCS: ", feat, compavg
	