#!/usr/bin/env python

# A native python MySQL library
import pymysql
import rpy2.robjects as robj
import operator

# Gathers reference information for other functions
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
	cur.execute("SELECT `WALS-APiCS`, `ShortName` FROM APiCSFeatures")
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
def getAPiCSLangComps(cur,types,complexities,degrees):
	
	cur.execute("""SELECT WALSAPiCSValues.TeXLang, APiCSFeatures.`WALS-APICS`,  WALSAPiCSValues.Wals_value_number
	FROM WALSAPiCSValues
	INNER JOIN APiCSFeatures ON WALSAPiCSValues.`APiCS_number` = APiCSFeatures.Feature_number
	WHERE APiCSFeatures.`WALS-APICS` != \"None\" AND APiCSFeatures.ComplexityType is not NULL""")

	apicsLangCompPar = { }	# For paradigmatic
	apicsLangCompSyn = { } # For syntagmatic
	apicsLangFeatCompPar = [ ] # For latter regression analysis on paradigmatic features
	apicsLangFeatCompSyn = [ ] # For latter regression analysis on paradigmatic features
	for row in cur.fetchall():
		lang, feat, value = row
		compfeat = complexities[feat]
		compValue = compfeat[str(value)]
	
		# Get the numbers across languages; looks like some refactoring is needed here
		if lang in apicsLangCompPar:
			if types[feat] == "Paradigmatic":
				normComp = compValue / float(degrees[feat]) 
				langCompList = apicsLangCompPar[lang]
				langCompList.append(normComp)
				apicsLangCompPar[lang] = langCompList
				apicsLangFeatCompPar.append([ lang,feat,normComp,"APiCS" ]) # For regression
		
		else:
			if types[feat] == "Paradigmatic":
				normComp = compValue / float(degrees[feat]) 
				apicsLangCompPar[lang] = [normComp]
				apicsLangFeatCompPar.append([ lang,feat,normComp,"APiCS" ])

		# Now syntagmatic
		if lang in apicsLangCompSyn:
			if types[feat] == "Syntagmatic":
				normComp = compValue / float(degrees[feat]) 
				langCompList = apicsLangCompSyn[lang]
				langCompList.append( normComp )
				apicsLangCompSyn[lang] = langCompList
				apicsLangFeatCompSyn.append([ lang,feat,normComp,"APiCS" ]) # For regression
			
		else:
			if types[feat] == "Syntagmatic":
				normComp = compValue / float(degrees[feat]) 
				apicsLangCompSyn[lang] = [ normComp ]
				apicsLangFeatCompSyn.append([ lang,feat,normComp,"APiCS" ]) # For regression

	
	return(apicsLangCompPar,apicsLangCompSyn,apicsLangFeatCompPar,apicsLangFeatCompSyn)


# Now do the same thing across features
def getAPiCSFeatureComps(cur,complexities,apicsLangComp,majorFeats=False,noMixed=True):

	cur.execute("""SELECT WALSAPiCSValues.TeXLang, APiCSFeatures.`WALS-APICS`,  WALSAPiCSValues.Wals_value_number
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

		mixedLangs = ["Michif", "Sri Lanka Portuguese"]
		if noMixed and lang in mixedLangs:
			continue
		
		if feat in apicswalsFeatComp:
			apicswalsFeatComp[feat] += compValue
			apicswalsFeatLangCount[feat] += 1
			apicsCompList[feat].append( compValue )

		# Not sure what this does anymore
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
def getWALSLangComps(cur,types,complexities,degrees,noCreoles=True):

	cur.execute("""SELECT "WALS".TeXLanguageName, WALSValues.Value_number, WALSValues.Feature_number, WALSValues.LangID
	FROM WALSValues
	INNER JOIN APiCSFeatures on  WALSValues.Feature_number = APiCSFeatures.`WALS-APICS`
	WHERE APiCSFeatures.`ComplexityType` is not NULL""")

	walsLangCompPar = { } # For paradigmatic
	walsLangCompSyn = { } 
	walsLangFeatCompPar = [ ]
	walsLangFeatCompSyn = [ ]
	for row in cur.fetchall():
		lang, value, feat, langid = row
		compfeat = complexities[feat]
		compValue = compfeat[str(value)]
		
 		creoleLangs = ["ago","bdc","bsm","bro","cvc","gdl","gfr","gbc","hcr","hwc","jcr","ktb","kfc","knq","lcr","mlc","mqc","mcr","meb","mce","npn","ndy","npi","nub","pap","pri","rcp","srm","sey","sra","tay","tpi"]
 		if noCreoles and langid in creoleLangs:
 			#print lang
 			continue

		# Now get the numbers across languages; looks like some refactoring is needed
		if lang in walsLangCompPar:
			if types[feat] == "Paradigmatic":
				normComp = compValue / float(degrees[feat]) 
				langCompList = walsLangCompPar[lang]
				langCompList.append(normComp)
				walsLangCompPar[lang] = langCompList
				walsLangFeatCompPar.append([ lang,feat,normComp,"WALS" ]) # For regression
		
		else:
			if types[feat] == "Paradigmatic":
				normComp = compValue / float(degrees[feat]) 
				walsLangCompPar[lang] = [normComp]
				walsLangFeatCompPar.append([ lang,feat,normComp,"WALS" ]) # For regression

 
		if lang in walsLangCompSyn:
			if types[feat] == "Syntagmatic":
				normComp = compValue / float(degrees[feat]) 
				langCompList = walsLangCompSyn[lang]
				langCompList.append( normComp )
				walsLangCompSyn[lang] = langCompList
				walsLangFeatCompSyn.append([ lang,feat,normComp,"WALS" ]) # For regression
		
		else:
			if types[feat] == "Syntagmatic":
				normComp = compValue / float(degrees[feat]) 
				walsLangCompSyn[lang] = [ normComp  ]
				walsLangFeatCompSyn.append([ lang,feat,normComp,"WALS" ]) # For regression
	
	return(walsLangCompPar,walsLangCompSyn,walsLangFeatCompPar,walsLangFeatCompSyn)



def getWALSFeatureComps(cur,complexities,walsLangComp,majorFeats=False,noCreoles=True):

	cur.execute("""SELECT WALSValues.TeXLanguageName, WALSValues.Value_number, WALSValues.Feature_number, WALSValues.LangID
	FROM WALSValues
	INNER JOIN APiCSFeatures on  WALSValues.Feature_number = APiCSFeatures.`WALS-APICS`
	WHERE APiCSFeatures.`ComplexityType` is not NULL""")


	walsFeatComp = {}
	walsFeatLangCount = { }
	walsCompList = { } # See comments above
	for row in cur.fetchall():
		lang, value, feat, langid = row
		compfeat = complexities[feat]
		compValue = compfeat[str(value)]

 		creoleLangs = ["ago","bdc","bsm","bro","cvc","gdl","gfr","gbc","hcr","hwc","jcr","ktb","kfc","knq","lcr","mlc","mqc","mcr","meb","mce","npn","ndy","npi","nub","pap","pri","rcp","srm","sey","sra","tay","tpi"]
 		if noCreoles and langid in creoleLangs:
 			#print lang
 			continue
 			
		if feat in walsFeatComp:
			walsFeatComp[feat] += compValue
			walsFeatLangCount[feat] += 1
			walsCompList[feat].append( compValue )

		# Not sure what this does anymore
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


 
#Get average feature complexity for APiCS and WALS; features should be precisely the same
def getFeatComplexity(walsFeatComp,walsFeatLangCount,walsCompList,apicswalsFeatComp,apicswalsFeatLangCount,apicsCompList,names,types,degrees):

	outfile = open('APiCSFeatureComps.txt', 'w')
	
	walsFCompAvg = [ ]
	apicsFCompAvg = [ ]
	walsFCompAvgPar = [ ]
	apicsFCompAvgPar = [ ]
	rowStorage = [ ] #to create a new list for a sorted output
	# NOTE DON'T JUST UNCOMMENT THIS SINCE I ALSO REARRANGED COLUMNS--see below
	#print >> outfile, "Feature\t", "Description\t", "Types\t", "Degrees\t", "WALSscore\t", "APiCSscore\t", "WALSNorm\t", "APiCSNorm\t", "CompAvg\t", "Significance\t", "Comparison"
	print >> outfile, "{\sc feature}\t&", "{\sc description}&\t", "{\sc type}&\t",   "{\sc apics}&\t", "{\sc wals}&\t", "$\sim$ {\sc p-value}&\t", "{\sc complexity}\t\\\\" # Just doing limited info for printing on paper
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
			winner = "WALS $>$ APiCS"
		elif p <= .05:
	#		print "APiCS more complex"
			winner = "APiCS $>$ WALS"
		else:
	#		print "equal complexity"
			winner = "APiCS $\\approx$ WALS"
	# 	
	# 	print ""

	# This matches with old top line (not rearranged)
	#	print >> outfile, feat+"\t"+names[feat]+"\t"+types[feat]+"\t"+str(degrees[feat])+"\t"+str(walscompavg)+"\t"+str(apicscompavg)+"\t"+str(walsavgnorm)+"\t"+str(apicsavgnorm)+"\t"+str(compavg)+"\t"+ str(p)+"\t"+winner
		print >> outfile, feat+"\t&", names[feat]+"\t&", types[feat]+"\t&",  str(round(apicsavgnorm,2))+"\t&", str(round(walsavgnorm,2))+"\t&", str(round(p,2))+"\t&", winner+"\t\\\\"
		
		# set row storage for later sorting
		shortfeat = feat
		#shortfeat = feat.replace("WALS ", "W")
		#shortfeat = shortfeat.replace("A", "")
		shorttype = "{\\sc p}"
		if types[feat] == "Syntagmatic": shorttype = "{\\sc s}"
		rowStorage.append([shortfeat, names[feat], shorttype, '%.2f' % (round(apicsavgnorm,2)), '%.2f' % (round(walsavgnorm,2)), '%.2f' % (round(p,2)), winner ])
		
		
		walsFCompAvg.append(walscompavg/degrees[feat])
		apicsFCompAvg.append(apicscompavg/degrees[feat])
		
		if types[feat] == "Paradigmatic":
			walsFCompAvgPar.append(walscompavg/degrees[feat])
			apicsFCompAvgPar.append(apicscompavg/degrees[feat])
			
			
	rowStorage = sorted(rowStorage, key=operator.itemgetter(-1,-2))
	
	# Print to proper table, file; this is for the paper
	featsfile = open('/Volumes/Obang/MyDocuments/Saramaccan/Papers/WordStructure/FeatureComps.tex', 'w')
	print >> featsfile, "\\begin{tabular}{lllrrrl}"
	print >> featsfile, "\\Hline"
	print >> featsfile, "{\sc feature}\t&", "{\sc description}&\t", "{\sc t}&\t", "{\sc apics}&\t", "{\sc wals}&\t", "$\\approx${\sc p}&\t", "{\sc comp}\t\\\\" # Just doing limited info for printing on paper
	print >> featsfile, "\\Hline"
	lastwinner = "" # for figuring out where hlines should go
	for row in rowStorage:
		currentwinner = row[-1]
		if lastwinner != "" and lastwinner != currentwinner: print >> featsfile, "\hline"
		textrow = "\t&\t".join(row)
		print >> featsfile, textrow + "\t\\\\"
		lastwinner = row[-1]
	print >> featsfile, "\\Hline"
	print >> featsfile, "\\end{tabular}"

	
	return(walsFCompAvg,apicsFCompAvg,walsFCompAvgPar,apicsFCompAvgPar)
	

# Now get average complexity for all features within a language; start with APiCS; only paradigmatic
def getLangCompPar(walsLangComp,apicsLangComp):

	outfile = open('APiCSLangComps.txt', 'w')

	totalAPiCS = 0
	APiCSCount = 0
	APiCSLangCompList = [ ]
	combinedListForSorting = [ ]
	for lang in apicsLangComp:
		# Only do languages with lots of features (paradigmatic ones only included); 26 is a semi-arbitrary choice to get a reasonable total number of language of both groups of about equal size
		if len(apicsLangComp[lang]) >= 26:
			mean = sum(apicsLangComp[lang])/len(apicsLangComp[lang])
			print >> outfile, lang, "\\>\t "+str(round(mean,2)), "\t\\> "+"APiCS\t\\\\"
			totalAPiCS += mean
			APiCSLangCompList.append(mean)
			combinedListForSorting.append([ lang, '%.2f' % mean, "APiCS" ])
			APiCSCount += 1

	# Now WALS 
	totalWALS = 0
	WALSCount = 0
	WALSLangCompList = [ ]
	for lang in walsLangComp:
		# Only do languages with lots of features (paradigmatic ones only included)
		if len(walsLangComp[lang]) >= 26:
			#print lang
			mean = sum(walsLangComp[lang])/len(walsLangComp[lang])
			print >> outfile, lang, "\\>\t "+str(round(mean,2)), "\t\\> "+"WALS \\\\"
			totalWALS += mean
			WALSLangCompList.append(mean)
			combinedListForSorting.append([ lang, '%.2f' % mean, "WALS" ])
			WALSCount += 1
	#print WALSLangCompList
				
	combinedListForSorting = sorted(combinedListForSorting, key=operator.itemgetter(1,0))

	# For paper
	langsfile = open('/Volumes/Obang/MyDocuments/Saramaccan/Papers/WordStructure/LangComps.tex', 'w')
	print >> langsfile, "\\begin{multicols}{3}"
	print >> langsfile,	"\\footnotesize"
	print >> langsfile,	"\\begin{tabbing}"
	
	firstrow = combinedListForSorting.pop(0)
	lang = firstrow[0]
	if firstrow[2] == "APiCS": lang = "\\emph{"+lang+"}"
	print >> langsfile, lang + "\\phantom{MMMMMM}\\=" + firstrow[1] + "\t\\\\"
	
	for row in combinedListForSorting:
		if row[2] == "APiCS": row[0] = "\\emph{"+row[0]+"}"
		#shortlang = row[0].replace("Creole\\b", "Cr. ")
		shortlang = row[0].replace("Cape Verdean Creole", "Cape Verd. Cr.")
		textrow = "\t\>\t".join([ shortlang, row[1] ])
		print >> langsfile, textrow + "\t\\\\"
	print >> langsfile,	"\\end{tabbing}"
	print >> langsfile, "\\end{multicols}"

	return(totalWALS,WALSCount,WALSLangCompList,totalAPiCS,APiCSCount,APiCSLangCompList)


# Now same for syntagmatic
# Now get average complexity for all features within a language; start with APiCS
def getLangCompSyn(walsLangCompSyn,apicsLangCompSyn):

	totalAPiCSSyn = 0
	APiCSCountSyn = 0
	APiCSLangCompListSyn = [ ]
	combinedListForSorting = [ ]
	for lang in apicsLangCompSyn:
		# Only do languages with lots of features (paradigmatic ones only included); 26 is a semi-arbitrary choice to get a reasonable total number of language of both groups of about equal size
		if len(apicsLangCompSyn[lang]) >= 13:
			mean = sum(apicsLangCompSyn[lang])/len(apicsLangCompSyn[lang])
			#print apicsLangCompSyn[lang]
			#print lang, mean
			totalAPiCSSyn += mean
			APiCSLangCompListSyn.append(mean)
			combinedListForSorting.append([ lang, '%.2f' % mean, "APiCS" ])
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
			combinedListForSorting.append([ lang, '%.2f' % mean, "WALS" ])
			WALSCountSyn += 1


	combinedListForSorting = sorted(combinedListForSorting, key=operator.itemgetter(1,0))

	# For paper
	langsfile = open('/Volumes/Obang/MyDocuments/Saramaccan/Papers/WordStructure/LangCompsSyn.tex', 'w')
	print >> langsfile, "\\begin{multicols}{3}"
	print >> langsfile,	"\\footnotesize"
	print >> langsfile,	"\\begin{tabbing}"
	
	firstrow = combinedListForSorting.pop(0)
	lang = firstrow[0]
	if firstrow[2] == "APiCS": lang = "\\emph{"+lang+"}"
	print >> langsfile, lang + "\\phantom{MMMMMM}\\=" + firstrow[1] + "\t\\\\"
	
	for row in combinedListForSorting:
		if row[2] == "APiCS": row[0] = "\\emph{"+row[0]+"}"
		#shortlang = row[0].replace("Creole\\b", "Cr. ")
		shortlang = row[0].replace("Cape Verdean Creole", "Cape Verd. Cr.")
		textrow = "\t\>\t".join([ shortlang, row[1] ])
		print >> langsfile, textrow + "\t\\\\"
	print >> langsfile,	"\\end{tabbing}"
	print >> langsfile, "\\end{multicols}"


	return(totalWALSSyn,WALSCountSyn,WALSLangCompListSyn,totalAPiCSSyn,APiCSCountSyn,APiCSLangCompListSyn)


def featComparison(apicsLangFeatCompPar,walsLangFeatCompPar,apicsLangComp,walsLangComp,apicsLangFeatCompSyn,walsLangFeatCompSyn,apicsLangCompSyn,walsLangCompSyn):
	
	fcfile = open('FeatComp.txt', 'w')

	print >> fcfile, "Feature\tComplexity\tSet"
	
	for featcomp in apicsLangFeatCompPar:
		lang, feat, comp, set = featcomp
		if len(apicsLangComp[lang]) >= 26:
			feat = feat.replace(" ", "")
			print >> fcfile, feat+"\t"+str(comp)+"\t"+set

	for featcomp in walsLangFeatCompPar:
		lang, feat, comp, set = featcomp
		if len(walsLangComp[lang]) >= 26:
			feat = feat.replace(" ", "")
			print >> fcfile, feat+"\t"+str(comp)+"\t"+set

	fcfilesyn = open('FeatCompSyn.txt', 'w')

	print >> fcfilesyn, "Feature\tComplexity\tSet"
	
	for featcomp in apicsLangFeatCompSyn:
		lang, feat, comp, set = featcomp
		if len(apicsLangCompSyn[lang]) >= 13:
			feat = feat.replace(" ", "")
			print >> fcfilesyn, feat+"\t"+str(comp)+"\t"+set

	for featcomp in walsLangFeatCompSyn:
		lang, feat, comp, set = featcomp
		if len(walsLangCompSyn[lang]) >= 13:
			feat = feat.replace(" ", "")
			print >> fcfilesyn, feat+"\t"+str(comp)+"\t"+set
		
		
def to_R(walsFCompAvgs,apicsFCompAvgs,WALSLangCompListPar,WALSLangCompListSyn,APiCSLangCompListPar,APiCSLangCompListSyn,walsFCompAvgsPar,apicsFCompAvgsPar):

	#print WALSLangCompListPar

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
	print >> rfile, "distPlot = ggplot(awFeat, aes(Complexity, fill=set)) + geom_density(alpha=0.2, aes(y=..scaled..)) + theme(panel.grid=element_blank(), panel.background = element_blank())"
	print >> rfile, "ggsave(\"/Users/jcgood/gitrepos/complexity/featDistr.pdf\", plot=distPlot)"
	print >> rfile, "ggsave(\"/Volumes/Obang/MyDocuments/Saramaccan/Papers/WordStructure/featDistr.pdf\", plot=distPlot)"
	print >> rfile, "distPlotBW = distPlot +  scale_fill_grey(start = 0, end = .9)"
	print >> rfile, "ggsave(\"/Users/jcgood/gitrepos/complexity/featDistrBW.pdf\", plot=distPlotBW)"

	print >> rfile, "apicsFeatCompAvgsPar <- c(", ",".join(map(str, apicsFCompAvgsPar)), ")"
	print >> rfile, "walsFeatCompAvgsPar <- c(", ",".join(map(str, walsFCompAvgsPar)), ")"

	print >> rfile, "apicsFeatCompAvgsParDF = as.data.frame(apicsFeatCompAvgsPar)"
	print >> rfile, "walsFeatCompAvgsParDF = as.data.frame(walsFeatCompAvgsPar)"

	print >> rfile, "apicsFeatCompAvgsParDF$set = \"APiCS\""
	print >> rfile, "walsFeatCompAvgsParDF$set = \"WALS\""

	print >> rfile, "apicsFeatCompAvgsParDF = rename(apicsFeatCompAvgsParDF, c(\"apicsFeatCompAvgsPar\" = \"Complexity\"))"
	print >> rfile, "walsFeatCompAvgsParDF = rename(walsFeatCompAvgsParDF, c(\"walsFeatCompAvgsPar\" = \"Complexity\"))"

	print >> rfile, "awFeatPar = rbind(apicsFeatCompAvgsParDF,walsFeatCompAvgsParDF)"
	print >> rfile, "distPlotPar = ggplot(awFeatPar, aes(Complexity, fill=set)) + geom_density(alpha=0.2, aes(y=..scaled..)) + theme(panel.grid=element_blank(), panel.background = element_blank())"
	print >> rfile, "#ggsave(\"/Users/jcgood/gitrepos/complexity/featDistrPar.pdf\", plot=distPlotPar)"
	print >> rfile, "ggsave(\"/Volumes/Obang/MyDocuments/Saramaccan/Papers/WordStructure/featDistrPar.pdf\", plot=distPlotPar)"
	print >> rfile, "distPlotParBW = distPlotPar +  scale_fill_grey(start = 0, end = .9)"
	print >> rfile, "ggsave(\"/Users/jcgood/gitrepos/complexity/featDistrParBW.pdf\", plot=distPlotParBW)"


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

	print >> rfile, "parPlot = ggplot(awPar, aes(Complexity, fill=set)) + geom_density(alpha=0.2, aes(y=..scaled..)) + theme(panel.grid=element_blank(), panel.background = element_blank())"
	print >> rfile, "parPlotBW = parPlot +  scale_fill_grey(start = 0, end = .9)"
	print >> rfile, "synPlot = ggplot(awSyn, aes(Complexity, fill=set)) + geom_density(alpha=0.2, aes(y=..scaled..)) + theme(panel.grid=element_blank(), panel.background = element_blank())"
	print >> rfile, "synPlotBW = synPlot +  scale_fill_grey(start = 0, end = .9)"
	print >> rfile, "ggsave(\"/Users/jcgood/gitrepos/complexity/parDistr.pdf\", plot=parPlot)"
	print >> rfile, "ggsave(\"/Users/jcgood/gitrepos/complexity/synDistr.pdf\", plot=synPlot)"
	print >> rfile, "ggsave(\"/Volumes/Obang/MyDocuments/Saramaccan/Papers/WordStructure/parDistr.pdf\", plot=parPlot)"
	print >> rfile, "ggsave(\"/Volumes/Obang/MyDocuments/Saramaccan/Papers/WordStructure/synDistr.pdf\", plot=synPlot)"
	print >> rfile, "ggsave(\"/Users/jcgood/gitrepos/complexity/parDistrBW.pdf\", plot=parPlotBW)"
	print >> rfile, "ggsave(\"/Users/jcgood/gitrepos/complexity/synDistrBW.pdf\", plot=synPlotBW)"
	
	print >> rfile, "aParHist = ggplot(alangcompParDF,aes(Complexity, fill=set)) + geom_histogram(alpha=0.5) + geom_density(alpha=.2) + theme(panel.grid=element_blank(), panel.background = element_blank())"
	print >> rfile, "wParHist = ggplot(wlangcompParDF,aes(Complexity, fill=set)) + geom_histogram(alpha=0.5, fill=\"#33CCCC\") + geom_density(alpha=.2, fill=\"#33CCCC\") + theme(panel.grid=element_blank(), panel.background = element_blank())"
	print >> rfile, "ggsave(\"/Users/jcgood/gitrepos/complexity/aParHist.pdf\", plot=aParHist)"
	print >> rfile, "ggsave(\"/Users/jcgood/gitrepos/complexity/wParHist.pdf\", plot=wParHist)"
	
	# For GLM par
	print >> rfile, "fc = read.table(\"/Users/jcgood/gitrepos/complexity/FeatComp.txt\", row.names=NULL, header=TRUE)"
	print >> rfile, "fcfit = glm(fc$Set ~ fc$Feature:fc$Complexity, family=\"binomial\")" # binomial default to logit function, I think; the colon means only use interacting terms, a "*" does interacting and individual
	print >> rfile, "layout(matrix(c(1,2,3,4),2,2))" #  4 graphs/page
	print >> rfile, "fcplot = plot(fcfit)"
	# Note 1 - pchisq(residualDeviance, resisdualDF) (see http://data.princeton.edu/R/glms.html) appears to be a valid "significance" test for extent to which model models the data

	# For GLM syn
	print >> rfile, "fcsyn = read.table(\"/Users/jcgood/gitrepos/complexity/FeatCompSyn.txt\", row.names=NULL, header=TRUE)"
	print >> rfile, "fcfitsyn = glm(fcsyn$Set ~ fcsyn$Feature:fcsyn$Complexity, family=\"binomial\")" # binomial default to logit function, I think; the colon means only use interacting terms, a "*" does interacting and individual
	print >> rfile, "layout(matrix(c(1,2,3,4),2,2))" #  4 graphs/page
	print >> rfile, "fcplotsyn = plot(fcfitsyn)"
	# Note 1 - pchisq(residualDeviance, resisdualDF) (see http://data.princeton.edu/R/glms.html) appears to be a valid "significance" test for extent to which model models the data



def getLangCompsTable(cur,complexities,names):
	cur.execute("SELECT `TeXLang`, `WALSFeature`, `Wals_value_Number` FROM WALSAPICSValues ORDER BY `Language`")
	langfile = open('APiCSLangCompVals.txt', 'w')
	print >> langfile, "Language\t", "Feature\t", "Feature_name\t", "Value\t", "Value_complexity"
	for row in cur.fetchall():
		lang, feat, val = row
		if feat in complexities:
			complexity = complexities[feat]
			compval = complexity[str(val)]
			print >> langfile, lang+"\t"+feat+"\t"+names[feat]+"\t"+str(val)+"\t"+str(compval)
		

def getDocumentation(cur):

	cur.execute("SELECT APiCSFeatures.`WALS-APICS`, APiCSFeatures.`Feature_name`, APiCSFeatures.`ComplexityType`, APiCSFeatures.`ComplexityDegree`, APiCSFeatures.`ComplexityDocumentation` FROM `APiCSFeatures` WHERE APiCSFeatures.`ComplexityType` IS NOT NULL ORDER BY APiCSFeatures.`WALSNumberOnly`")
	docfile = open('CompDocumentation.txt', 'w')
	print >> docfile, "Feature\tDescription\tType\tComplexityMax\tJustification"

	for row in cur.fetchall():
		feat,name,type,degree,doc = row
		print >> docfile, feat+"\t"+name+"\t"+type+"\t"+str(degree)+"\t"+doc


def getValDocumentation(cur):

	cur.execute("SELECT `WALSValueInfo`.`Feature_number`, `WALSValueInfo`.`Value_description`, `WALSValueInfo`.`Values_number`, `WALSValueInfo`.`Complexity`, `WALSValueInfo`.`ComplexityDocumentation` FROM `WALSValueInfo` WHERE `WALSValueInfo`.`Complexity` IS NOT NULL")
	docvalfile = open('ValDocumentation.txt', 'w')
	print >> docvalfile, "Feature\tValueDescription\tValueID\tComplexity\tJustification"

	for row in cur.fetchall():
		feat,val,valid,comp,doc = row
		print >> docvalfile, feat+"\t"+val+"\t"+str(valid)+"\t"+str(comp)+"\t"+doc


	

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
	