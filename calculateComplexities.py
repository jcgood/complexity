#!/usr/bin/env python

# A native python MySQL library
import pymysql
import rpy2.robjects as robj

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='APiCS')
#conn = pymysql.connect(host='localhost', port=3307, user='root', passwd='', db='APiCS')
cur = conn.cursor()

# Make dictionary of dictionary of complexities for a given value
cur.execute("SELECT `Feature_number`, `Values_number`, Complexity FROM WALSValueInfo WHERE Complexity is not NULL")
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


# Make a dictionary for feature types and complexity degrees
cur.execute("SELECT `WALS-APICS`, `ComplexityType`, `ComplexityDegree` FROM APiCSFeatures")
types = { }
degrees = { }
for row in cur.fetchall():
	feat, type, deg = row	
	if type != None:
		types[feat] = type
		degrees[feat] = deg


# Make sure listed degrees number matches actual
for feat in degrees:
	
	degree = degrees[feat]
	upper = 0	
	
	compfeat = complexities[feat]
	for compid in compfeat:
		if compfeat[compid] > upper:
			upper = compfeat[compid]
	
	if upper == degree:
		pass
	else:
		print "Error: Upper bound on feature", feat, "does not match actual upper bound."
		


# Go through the WALS-like APiCS values and (i) calculate complexity averages and (ii) build up lists of values for statistical processing
cur.execute("""SELECT WALSAPiCSValues.Language, APiCSFeatures.`WALS-APICS`,  WALSAPiCSValues.Wals_value_number
FROM WALSAPiCSValues
INNER JOIN APiCSFeatures ON WALSAPiCSValues.`APiCS_number` = APiCSFeatures.Feature_number
WHERE APiCSFeatures.`WALS-APICS` != \"None\" AND APiCSFeatures.ComplexityType is not NULL""")

apicswalsFeatComp = { }
apicswalsFeatLangCount = { }
apicsCompList = { } # For statistical processing
apicsLangComp = { }
for row in cur.fetchall():
	lang, feat, value = row
	compfeat = complexities[feat]
	compValue = compfeat[str(value)]
	
	# Get the numbers across languages (just for paradigmatic)
	if lang in apicsLangComp:
		if types[feat] == "Paradigmatic":
			langCompList = apicsLangComp[lang]
			langCompList.append( compValue / float(degrees[feat]) )
			apicsLangComp[lang] = langCompList
	
	else:
		if types[feat] == "Paradigmatic":
			apicsLangComp[lang] = [ compValue / float(degrees[feat])  ]

	## TODO: SEPAARETE FOR LOOPS< DO ONES BELOW FIRST

	# Now do the same thing across features
	if feat in apicswalsFeatComp:
		apicswalsFeatComp[feat] += compValue
		apicswalsFeatLangCount[feat] += 1
		apicsCompList[feat].append( compValue )
	else:
		apicswalsFeatComp[feat] = compValue
		apicswalsFeatLangCount[feat] = 1
		apicsCompList[feat] = [ compValue ]




# Now do the same thing for the WALS languages
cur.execute("""SELECT WALSValues.LanguageName, WALSValues.Value_number, WALSValues.Feature_number
FROM WALSValues
INNER JOIN APiCSFeatures on  WALSValues.Feature_number = APiCSFeatures.`WALS-APICS`
WHERE APiCSFeatures.`ComplexityType` is not NULL""")

walsFeatComp = {}
walsFeatLangCount = { }
walsCompList = { } # See comments above
walsLangComp = { }
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

	# Now get the numbers across languages
	if lang in walsLangComp:
		if types[feat] == "Paradigmatic":
			langCompList = walsLangComp[lang]
			langCompList.append( compValue / float(degrees[feat]) )
			walsLangComp[lang] = langCompList
	
	else:
		if types[feat] == "Paradigmatic":
			walsLangComp[lang] = [ compValue / float(degrees[feat])  ]

walfull = 0
for lang in walsLangComp:
	if len(walsLangComp[lang]) >= 26:
		#print lang, len(walsLangComp[lang])
		walfull += 1
		

#print walsCompList


# Get average complexity for APiCS and WALS; features should be precisely the same
outfile = open('/Users/jcgood/Desktop/APiCS.txt', 'w')
print >> outfile, "Feature\t", "Description\t", "Types\t", "Degrees\t", "WALSscore\t", "APiCSscore\t", "Significance\t", "Comparison"
for feat in walsFeatComp:
	print feat+",", names[feat]+",", types[feat]+",", degrees[feat]
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
	
	sd = robj.r['sd']
	apicssd = sd(apicsvector)
	walssd = sd(walsvector)
	
	if p <= .05:
		sig = "significant"
	else: sig = "null"
	
	print "WALS average: ", walscompavg, "(sd:", walssd[0], ")"
	print "APiCS average: ", apicscompavg, "(sd: ", apicssd[0], ")"
	print "p-value = ", p, "("+sig+")"
	if p <= .05 and walscompavg > apicscompavg:
		print "WALS more complex"
		winner = "WALS"
	elif p <= .05:
		print "APiCS more complex"
		winner = "APiCS"
	else:
		print "equal complexity"
		winner = "Same"
	
	print ""

	print >> outfile, feat+"\t", names[feat]+"\t", types[feat]+"\t", str(degrees[feat])+"\t", str(walscompavg)+"\t", str(apicscompavg)+"\t", str(p)+"\t", winner


# Now get average complexity for all features within a language; start with APiCS
totalAPiCS = 0
APiCSCount = 0
APiCSLangCompList = [ ]
for lang in apicsLangComp:
	# Only do languages with lots of features (paradigmatic ones only included); 26 is a semi-arbitrary choice to get a reasonable total number of language of both groups of about equal size
	if len(apicsLangComp[lang]) >= 26:
		mean = sum(apicsLangComp[lang])/len(apicsLangComp[lang])
		#print apicsLangComp[lang]
		print lang, mean
		totalAPiCS += mean
		APiCSLangCompList.append(mean)
		APiCSCount += 1

# Now WALS 
totalWALS = 0
WALSCount = 0
WALSLangCompList = [ ]
for lang in walsLangComp:
	# Only do languages with lots of features (paradigmatic ones only included)
	if len(walsLangComp[lang]) >= 26:
		mean = sum(walsLangComp[lang])/len(walsLangComp[lang])
		#print walsLangComp[lang]
		print lang, mean
		totalWALS += mean
		WALSLangCompList.append(mean)
		WALSCount += 1

print ""
print "APiCS", totalAPiCS/APiCSCount, "WALS", totalWALS/WALSCount

#print WALSLangCompList, APiCSLangCompList

apicslangvector = robj.FloatVector(APiCSLangCompList)
walslangvector = robj.FloatVector(WALSLangCompList)
t = robj.r['t.test']
p = t(apicslangvector,walslangvector,**{'var.equal': True}) # Do two-sample t-test assuming equal variance

print "p:", p

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
	