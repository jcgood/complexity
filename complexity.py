#!/usr/bin/env python

# A native python MySQL library
import pymysql
import rpy2.robjects as robj


def getComplexities(cur):

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
		
	return(complexities,names,types,degrees)


#Go through the WALS-like APiCS values and (i) calculate complexity averages and (ii) build up lists of values for statistical processing
def getAPiCSFeatureComps(cur,types,complexities,degrees):
	
	cur.execute("""SELECT WALSAPiCSValues.Language, APiCSFeatures.`WALS-APICS`,  WALSAPiCSValues.Wals_value_number
	FROM WALSAPiCSValues
	INNER JOIN APiCSFeatures ON WALSAPiCSValues.`APiCS_number` = APiCSFeatures.Feature_number
	WHERE APiCSFeatures.`WALS-APICS` != \"None\" AND APiCSFeatures.ComplexityType is not NULL""")

	apicsLangComp = { }	# For paradigmatic
	apicsLangCompSyn = { } # For syntagmatic
	for row in cur.fetchall():
		lang, feat, value = row
		compfeat = complexities[feat]
		compValue = compfeat[str(value)]
	
		# Get the numbers across languages
		if lang in apicsLangComp:
			if types[feat] == "Paradigmatic":
				langCompList = apicsLangComp[lang]
				langCompList.append( compValue / float(degrees[feat]) )
				apicsLangComp[lang] = langCompList
	
		else:
			if types[feat] == "Paradigmatic":
				apicsLangComp[lang] = [ compValue / float(degrees[feat])  ]


		# Now syntagmatic
		if lang in apicsLangCompSyn:
			if types[feat] == "Syntagmatic":
				langCompList = apicsLangCompSyn[lang]
				langCompList.append( compValue / float(degrees[feat]) )
				apicsLangCompSyn[lang] = langCompList
			
		else:
			if types[feat] == "Syntagmatic":
				apicsLangCompSyn[lang] = [ compValue / float(degrees[feat])  ]

	return(apicsLangComp,apicsLangCompSyn)


# # Now do the same thing across features
def getAPiCSLangComps(cur,complexities,apicsLangComp,majorFeats=False):

	cur.execute("""SELECT WALSAPiCSValues.Language, APiCSFeatures.`WALS-APICS`,  WALSAPiCSValues.Wals_value_number
	FROM WALSAPiCSValues
	INNER JOIN APiCSFeatures ON WALSAPiCSValues.`APiCS_number` = APiCSFeatures.Feature_number
	WHERE APiCSFeatures.`WALS-APICS` != \"None\" AND APiCSFeatures.ComplexityType is not NULL""")
	apicswalsFeatComp = { }
	apicswalsFeatLangCount = { }
	apicsCompList = { } # For statistical processing
	for row in cur.fetchall():
		lang, feat, value = row
		compfeat = complexities[feat]
		compValue = compfeat[str(value)]

		if feat in apicswalsFeatComp:
			apicswalsFeatComp[feat] += compValue
			apicswalsFeatLangCount[feat] += 1
			apicsCompList[feat].append( compValue )

		elif majorFeats:
			if len(apicsLangComp[lang]) >= 26:
				apicswalsFeatComp[feat] = compValue
				apicswalsFeatLangCount[feat] = 1
				apicsCompList[feat] = [ compValue ]

		else:
			apicswalsFeatComp[feat] = compValue
			apicswalsFeatLangCount[feat] = 1
			apicsCompList[feat] = [ compValue ]
			
	return(apicswalsFeatComp,apicswalsFeatLangCount,apicsCompList)






# Now do the same thing for the WALS languages


def getWALSFeatureComps(cur,types,complexities,degrees):

	cur.execute("""SELECT WALSValues.LanguageName, WALSValues.Value_number, WALSValues.Feature_number
	FROM WALSValues
	INNER JOIN APiCSFeatures on  WALSValues.Feature_number = APiCSFeatures.`WALS-APICS`
	WHERE APiCSFeatures.`ComplexityType` is not NULL""")

	walsLangComp = { } # For paradigmatic
	walsLangCompSyn = { } 
	for row in cur.fetchall():
		lang, value, feat = row
		compfeat = complexities[feat]
		compValue = compfeat[str(value)]

		# Now get the numbers across languages
		if lang in walsLangComp:
			if types[feat] == "Paradigmatic":
				langCompList = walsLangComp[lang]
				langCompList.append( compValue / float(degrees[feat]) )
				walsLangComp[lang] = langCompList
			
		else:
			if types[feat] == "Paradigmatic":
				walsLangComp[lang] = [ compValue / float(degrees[feat])  ]

		# Now syntagmatic
		if lang in walsLangCompSyn:
			if types[feat] == "Syntagmatic":
				langCompList = walsLangCompSyn[lang]
				langCompList.append( compValue / float(degrees[feat]) )
				walsLangCompSyn[lang] = langCompList
			
		else:
			if types[feat] == "Syntagmatic":
				walsLangCompSyn[lang] = [ compValue / float(degrees[feat])  ]
	
	return(walsLangComp,walsLangCompSyn)



def getWALSLangComps(cur,complexities,walsLangComp,majorFeats=False):

	cur.execute("""SELECT WALSValues.LanguageName, WALSValues.Value_number, WALSValues.Feature_number
	FROM WALSValues
	INNER JOIN APiCSFeatures on  WALSValues.Feature_number = APiCSFeatures.`WALS-APICS`
	WHERE APiCSFeatures.`ComplexityType` is not NULL""")

	walsFeatComp = {}
	walsFeatLangCount = { }
	walsCompList = { } # See comments above
	for row in cur.fetchall():
		lang, value, feat = row
		compfeat = complexities[feat]
		compValue = compfeat[str(value)]

		if feat in walsFeatComp:
			walsFeatComp[feat] += compValue
			walsFeatLangCount[feat] += 1
			walsCompList[feat].append( compValue )

		# This tests to make sure the well-featured languages don't throw off calculations 
		elif majorFeats:
			if len(walsLangComp[lang]) >= 26:
				walsFeatComp[feat] = compValue
				walsFeatLangCount[feat] = 1
				walsCompList[feat] = [ compValue ]

		else:
			walsFeatComp[feat] = compValue
			walsFeatLangCount[feat] = 1
			walsCompList[feat] = [ compValue ]

	return(walsFeatComp,walsFeatLangCount,walsCompList)


 
#Get average complexity for APiCS and WALS; features should be precisely the same

def getFeatComplexity(walsFeatComp,walsFeatLangCount,walsCompList,apicswalsFeatComp,apicswalsFeatLangCount,apicsCompList,names,types,degrees):

	outfile = open('APiCSFeatureComps.txt', 'w')
	
	walsFCompAvg = [ ]
	apicsFCompAvg = [ ]
	print >> outfile, "Feature\t", "Description\t", "Types\t", "Degrees\t", "WALSscore\t", "APiCSscore\t", "WALSNorm\t", "APiCSNorm\t", "CompAvg\t", "Significance\t", "Comparison"
	for feat in walsFeatComp:
		#print feat+",", names[feat]+",", types[feat]+",", degrees[feat]
		walscompval = walsFeatComp[feat]
		walscompavg = walscompval / float(walsFeatLangCount[feat])
		apicscompval = apicswalsFeatComp[feat]
		apicscompavg = apicscompval / float(apicswalsFeatLangCount[feat])

		deg = degrees[feat]
		apicsavgnorm = apicscompavg / float(deg)
		walsavgnorm = walscompavg / float(deg)
		compavg = (apicsavgnorm + walsavgnorm) / float(2)
	
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
	
	# 	print "WALS average: ", walscompavg, "(sd:", walssd[0], ")"
	# 	print "APiCS average: ", apicscompavg, "(sd: ", apicssd[0], ")"
	#	print "p-value = ", p, "("+sig+")"
		if p <= .05 and walscompavg > apicscompavg:
	#		print "WALS more complex"
			winner = "WALS"
		elif p <= .05:
	#		print "APiCS more complex"
			winner = "APiCS"
		else:
	#		print "equal complexity"
			winner = "Same"
	# 	
	# 	print ""

		print >> outfile, feat+"\t", names[feat]+"\t", types[feat]+"\t", str(degrees[feat])+"\t", str(walscompavg)+"\t", str(apicscompavg)+"\t", str(walsavgnorm)+"\t", str(apicsavgnorm)+"\t", str(compavg)+"\t",  str(p)+"\t", winner
		
		walsFCompAvg.append(walscompavg/degrees[feat])
		apicsFCompAvg.append(apicscompavg/degrees[feat])
			
	return(walsFCompAvg,apicsFCompAvg)
	
	

# Now get average complexity for all features within a language; start with APiCS; only paradigmatic
def getLangCompPar(walsLangComp,apicsLangComp):

	outfile = open('APiCSLangComps.txt', 'w')

	print >> outfile, "Language\tComplexity\tSet"

	totalAPiCS = 0
	APiCSCount = 0
	APiCSLangCompList = [ ]
	for lang in apicsLangComp:
		# Only do languages with lots of features (paradigmatic ones only included); 26 is a semi-arbitrary choice to get a reasonable total number of language of both groups of about equal size
		if len(apicsLangComp[lang]) >= 26:
			mean = sum(apicsLangComp[lang])/len(apicsLangComp[lang])
			print >> outfile, lang+"\t"+str(mean)+"\t"+"APiCS"
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
			print >> outfile, lang+"\t"+str(mean)+"\t"+"WALS"
			totalWALS += mean
			WALSLangCompList.append(mean)
			WALSCount += 1

	return(totalWALS,WALSCount,WALSLangCompList,totalAPiCS,APiCSCount,APiCSLangCompList)

# Now same for syntagmatic
# Now get average complexity for all features within a language; start with APiCS
def getLangCompSyn(walsLangCompSyn,apicsLangCompSyn):

	totalAPiCSSyn = 0
	APiCSCountSyn = 0
	APiCSLangCompListSyn = [ ]
	for lang in apicsLangCompSyn:
		# Only do languages with lots of features (paradigmatic ones only included); 26 is a semi-arbitrary choice to get a reasonable total number of language of both groups of about equal size
		if len(apicsLangCompSyn[lang]) >= 13:
			mean = sum(apicsLangCompSyn[lang])/len(apicsLangCompSyn[lang])
			#print apicsLangCompSyn[lang]
			#print lang, mean
			totalAPiCSSyn += mean
			APiCSLangCompListSyn.append(mean)
			APiCSCountSyn += 1

	# Now WALS 
	totalWALSSyn = 0
	WALSCountSyn = 0
	WALSLangCompListSyn = [ ]
	for lang in walsLangCompSyn:
		# Only do languages with lots of features (paradigmatic ones only included)
		if len(walsLangCompSyn[lang]) >= 13:
			mean = sum(walsLangCompSyn[lang])/len(walsLangCompSyn[lang])
			#print walsLangCompSyn[lang]
			#print lang, mean
			totalWALSSyn += mean
			WALSLangCompListSyn.append(mean)
			WALSCountSyn += 1

	return(totalWALSSyn,WALSCountSyn,WALSLangCompListSyn,totalAPiCSSyn,APiCSCountSyn,APiCSLangCompListSyn)



def to_R(walsFCompAvgs,apicsFCompAvgs,WALSLangCompListPar,WALSLangCompListSyn,APiCSLangCompListPar,APiCSLangCompListSyn):

	rfile = open('APiCSWALS.r', 'w')

	print >> rfile, "library(ggplot2)"
	print >> rfile, "library(plyr)"

	print >> rfile, "apicsFeatCompAvgs <- c(", ",".join(map(str, apicsFCompAvgs)), ")"
	print >> rfile, "walsFeatCompAvgs <- c(", ",".join(map(str, walsFCompAvgs)), ")"

	print >> rfile, "apicsFeatCompAvgsDF = as.data.frame(apicsFeatCompAvgs)"
	print >> rfile, "walsFeatCompAvgsDF = as.data.frame(walsFeatCompAvgs)"

	print >> rfile, "apicsFeatCompAvgsDF$set = \"APiCS\""
	print >> rfile, "walsFeatCompAvgsDF$set = \"WALS\""

	print >> rfile, "apicsFeatCompAvgsDF = rename(apicsFeatCompAvgsDF, c(\"apicsFeatCompAvgs\" = \"Complexity\"))"
	print >> rfile, "walsFeatCompAvgsDF = rename(walsFeatCompAvgsDF, c(\"walsFeatCompAvgs\" = \"Complexity\"))"

	print >> rfile, "awFeat = rbind(apicsFeatCompAvgsDF,walsFeatCompAvgsDF)"
	print >> rfile, "distPlot = ggplot(awFeat, aes(Complexity, fill=set)) + geom_density(alpha=0.2)"
	print >> rfile, "ggsave(\"/Users/jcgood/gitrepos/complexity/featDistr.pdf\", plot=distPlot)"

	print >> rfile, "alangcompPar <- c(", ",".join(map(str, APiCSLangCompListPar)), ")"
	print >> rfile, "wlangcompPar <- c(", ",".join(map(str, WALSLangCompListPar)), ")"
	print >> rfile, "alangcompSyn <- c(", ",".join(map(str, APiCSLangCompListSyn)), ")"
	print >> rfile, "wlangcompSyn <- c(", ",".join(map(str, WALSLangCompListSyn)), ")"

	print >> rfile, "alangcompParDF = as.data.frame(alangcompPar)"
	print >> rfile, "wlangcompParDF = as.data.frame(wlangcompPar)"
	print >> rfile, "alangcompSynDF = as.data.frame(alangcompSyn)"
	print >> rfile, "wlangcompSynDF = as.data.frame(wlangcompSyn)"

	print >> rfile, "alangcompParDF$set = \"APiCS\""
	print >> rfile, "alangcompSynDF$set = \"APiCS\""
	print >> rfile, "wlangcompParDF$set = \"WALS\""
	print >> rfile, "wlangcompSynDF$set = \"WALS\""

	print >> rfile, "alangcompParDF = rename(alangcompParDF, c(\"alangcompPar\" = \"Complexity\"))"
	print >> rfile, "alangcompSynDF = rename(alangcompSynDF, c(\"alangcompSyn\" = \"Complexity\"))"
	print >> rfile, "wlangcompParDF = rename(wlangcompParDF, c(\"wlangcompPar\" = \"Complexity\"))"
	print >> rfile, "wlangcompSynDF = rename(wlangcompSynDF, c(\"wlangcompSyn\" = \"Complexity\"))"

	print >> rfile, "awPar = rbind(alangcompParDF,wlangcompParDF)"
	print >> rfile, "awSyn = rbind(alangcompSynDF,wlangcompSynDF)"

	print >> rfile, "parPlot = ggplot(awPar, aes(Complexity, fill=set)) + geom_density(alpha=0.2)"
	print >> rfile, "synPlot = ggplot(awSyn, aes(Complexity, fill=set)) + geom_density(alpha=0.2)"

	print >> rfile, "ggsave(\"/Users/jcgood/gitrepos/complexity/parDistr.pdf\", plot=parPlot)"
	print >> rfile, "ggsave(\"/Users/jcgood/gitrepos/complexity/synDistr.pdf\", plot=synPlot)"


def getLangCompsTable(cur,complexities,names):
	cur.execute("SELECT `Language`, `WALSFeature`, `Wals_value_Number` FROM WALSAPICSValues ORDER BY `Language`")
	langfile = open('APiCSLangCompVals.txt', 'w')
	print >> langfile, "Language\t", "Feature\t", "Feature_name\t", "Value\t", "Value_complexity"
	for row in cur.fetchall():
		lang, feat, val = row
		if feat in complexities:
			complexity = complexities[feat]
			compval = complexity[str(val)]
			print >> langfile, lang+"\t", feat+"\t", names[feat]+"\t", str(val)+"\t", str(compval)
		
		

# R sample case
# apicslangsynvector = robj.FloatVector(APiCSLangCompListSyn)
# walslangsynvector = robj.FloatVector(WALSLangCompListSyn)
# t = robj.r['t.test']
# p = t(apicslangsynvector,walslangsynvector,**{'var.equal': True}) # Do two-sample t-test assuming equal variance
#print p


# apicslangvector = robj.FloatVector(APiCSLangCompListPar)
# walslangvector = robj.FloatVector(WALSLangCompListPar)
# t = robj.r['t.test']
# p = t(apicslangvector,walslangvector,**{'var.equal': True}) # Do two-sample t-test assuming equal variance
# print p


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
	