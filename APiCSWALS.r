library(ggplot2)
library(plyr)
apicsFeatCompAvgs <- c( 0.342465753425,0.117117117117,0.56,0.714912280702,0.315315315315,0.41095890411,0.260273972603,0.141025641026,0.666666666667,0.519736842105,0.208333333333,0.53125,0.190476190476,0.434210526316,0.554054054054,0.167808219178,1.0,0.921052631579,0.662162162162,0.147058823529,0.6,0.878378378378,0.468468468468,0.526315789474,0.164383561644,0.62,0.578431372549,0.52,0.227272727273,0.631720430108,0.48,0.357142857143,0.359375,0.571428571429,0.548051948052,0.041095890411,0.0405405405405,0.454545454545,0.353424657534,0.236486486486,0.708920187793,0.590277777778,0.297297297297,0.108108108108,0.527027027027 )
walsFeatCompAvgs <- c( 0.415282392027,0.331569664903,0.538091419407,0.701940035273,0.634272300469,0.632520325203,0.763239875389,0.245989304813,0.520732364028,0.482159624413,0.333333333333,0.551813471503,0.532536520584,0.285,0.512777777778,0.124233128834,0.943625325239,0.862645348837,0.360225140713,0.030303030303,0.563541666667,0.919413919414,0.356725146199,0.562770562771,0.535641547862,0.507345225603,0.468571428571,0.511824324324,0.260162601626,0.58064516129,0.692913385827,0.478813559322,0.443113772455,0.459317585302,0.5264604811,0.368131868132,0.286432160804,0.479541734861,0.487553648069,0.244791666667,0.669902912621,0.524734982332,0.263374485597,0.341708542714,0.470873786408 )
apicsFeatCompAvgsDF = as.data.frame(apicsFeatCompAvgs)
walsFeatCompAvgsDF = as.data.frame(walsFeatCompAvgs)
apicsFeatCompAvgsDF$set = "APiCS"
walsFeatCompAvgsDF$set = "WALS"
apicsFeatCompAvgsDF = rename(apicsFeatCompAvgsDF, c("apicsFeatCompAvgs" = "Complexity"))
walsFeatCompAvgsDF = rename(walsFeatCompAvgsDF, c("walsFeatCompAvgs" = "Complexity"))
awFeat = rbind(apicsFeatCompAvgsDF,walsFeatCompAvgsDF)
distPlot = ggplot(awFeat, aes(Complexity, fill=set)) + geom_density(alpha=0.2, aes(y=..scaled..)) + theme(panel.grid=element_blank(), panel.background = element_blank())
ggsave("/Users/jcgood/gitrepos/complexity/featDistr.pdf", plot=distPlot)
ggsave("/Volumes/Obang/MyDocuments/Saramaccan/Papers/WordStructure/featDistr.pdf", plot=distPlot)
distPlotBW = distPlot +  scale_fill_grey(start = 0, end = .9)
ggsave("/Users/jcgood/gitrepos/complexity/featDistrBW.pdf", plot=distPlotBW)
apicsFeatCompAvgsPar <- c( 0.342465753425,0.117117117117,0.714912280702,0.315315315315,0.41095890411,0.260273972603,0.141025641026,0.666666666667,0.519736842105,0.208333333333,0.190476190476,0.434210526316,0.167808219178,0.662162162162,0.147058823529,0.468468468468,0.526315789474,0.164383561644,0.578431372549,0.227272727273,0.631720430108,0.48,0.359375,0.571428571429,0.548051948052,0.041095890411,0.0405405405405,0.353424657534,0.236486486486,0.297297297297,0.108108108108 )
walsFeatCompAvgsPar <- c( 0.415282392027,0.331569664903,0.701940035273,0.634272300469,0.632520325203,0.763239875389,0.245989304813,0.520732364028,0.482159624413,0.333333333333,0.532536520584,0.285,0.124233128834,0.360225140713,0.030303030303,0.356725146199,0.562770562771,0.535641547862,0.468571428571,0.260162601626,0.58064516129,0.692913385827,0.443113772455,0.459317585302,0.5264604811,0.368131868132,0.286432160804,0.487553648069,0.244791666667,0.263374485597,0.341708542714 )
apicsFeatCompAvgsParDF = as.data.frame(apicsFeatCompAvgsPar)
walsFeatCompAvgsParDF = as.data.frame(walsFeatCompAvgsPar)
apicsFeatCompAvgsParDF$set = "APiCS"
walsFeatCompAvgsParDF$set = "WALS"
apicsFeatCompAvgsParDF = rename(apicsFeatCompAvgsParDF, c("apicsFeatCompAvgsPar" = "Complexity"))
walsFeatCompAvgsParDF = rename(walsFeatCompAvgsParDF, c("walsFeatCompAvgsPar" = "Complexity"))
awFeatPar = rbind(apicsFeatCompAvgsParDF,walsFeatCompAvgsParDF)
distPlotPar = ggplot(awFeatPar, aes(Complexity, fill=set)) + geom_density(alpha=0.2, aes(y=..scaled..)) + theme(panel.grid=element_blank(), panel.background = element_blank())
#ggsave("/Users/jcgood/gitrepos/complexity/featDistrPar.pdf", plot=distPlotPar)
ggsave("/Volumes/Obang/MyDocuments/Saramaccan/Papers/WordStructure/featDistrPar.pdf", plot=distPlotPar)
distPlotParBW = distPlotPar +  scale_fill_grey(start = 0, end = .9)
ggsave("/Users/jcgood/gitrepos/complexity/featDistrParBW.pdf", plot=distPlotParBW)
alangcompPar <- c( 0.311111111111,0.244086021505,0.327777777778,0.362068965517,0.41935483871,0.272222222222,0.389247311828,0.333333333333,0.27311827957,0.387096774194,0.358888888889,0.305555555556,0.304597701149,0.272222222222,0.343103448276,0.316091954023,0.506451612903,0.616666666667,0.380952380952,0.364516129032,0.335555555556,0.44623655914,0.4,0.33,0.44880952381,0.293103448276,0.325806451613,0.277419354839,0.4,0.285555555556,0.415555555556,0.376344086022,0.333333333333,0.216666666667,0.4,0.523333333333,0.362903225806,0.359139784946,0.427777777778,0.451612903226,0.343010752688,0.455,0.462365591398,0.202380952381,0.238095238095,0.241935483871,0.350537634409,0.384444444444,0.383333333333,0.355555555556,0.348888888889,0.334408602151,0.266666666667,0.403225806452,0.273563218391,0.474193548387,0.408602150538,0.333333333333,0.375555555556,0.240740740741,0.425925925926,0.422580645161,0.35,0.369892473118,0.33,0.379310344828,0.245977011494,0.347777777778,0.166091954023,0.638888888889,0.365591397849,0.378494623656,0.402688172043 )
wlangcompPar <- c( 0.49012345679,0.503225806452,0.366666666667,0.435802469136,0.431034482759,0.397849462366,0.432051282051,0.568888888889,0.353571428571,0.466666666667,0.471111111111,0.481111111111,0.321111111111,0.410714285714,0.47311827957,0.310752688172,0.487777777778,0.413095238095,0.444444444444,0.439743589744,0.269230769231,0.41975308642,0.385185185185,0.412820512821,0.413793103448,0.285185185185,0.50119047619,0.444444444444,0.377011494253,0.34367816092,0.583908045977,0.303571428571,0.395238095238,0.540555555556,0.418390804598,0.391397849462,0.35632183908,0.490804597701,0.426666666667,0.391954022989,0.351075268817,0.397435897436,0.421505376344,0.375268817204,0.42962962963,0.518518518519,0.405555555556,0.321428571429,0.415384615385,0.39358974359,0.412962962963,0.35119047619,0.488888888889,0.38024691358,0.534482758621,0.423333333333,0.377011494253,0.444827586207,0.476923076923,0.398717948718,0.347126436782,0.543103448276 )
alangcompSyn <- c( 0.654761904762,0.583333333333,0.75,0.628205128205,0.654761904762,0.628205128205,0.619047619048,0.654761904762,0.628205128205,0.619047619048,0.547619047619,0.619047619048,0.583333333333,0.619047619048,0.690476190476,0.619047619048,0.571428571429,0.690476190476,0.511904761905,0.619047619048,0.628205128205,0.619047619048,0.690476190476,0.589743589744,0.642857142857,0.589743589744,0.619047619048,0.690476190476,0.619047619048,0.589743589744,0.654761904762,0.653846153846,0.511904761905,0.653846153846,0.547619047619,0.583333333333,0.654761904762,0.654761904762,0.690476190476,0.678571428571,0.551282051282,0.583333333333,0.714285714286,0.628205128205,0.619047619048,0.619047619048,0.547619047619,0.690476190476,0.654761904762,0.628205128205,0.678571428571,0.619047619048,0.678571428571,0.654761904762,0.583333333333,0.619047619048,0.654761904762,0.628205128205,0.761904761905,0.547619047619,0.690476190476,0.619047619048,0.714285714286,0.619047619048,0.705128205128,0.619047619048,0.654761904762,0.654761904762,0.583333333333,0.628205128205,0.642857142857,0.619047619048,0.547619047619,0.74358974359 )
wlangcompSyn <- c( 0.628205128205,0.628205128205,0.589743589744,0.692307692308,0.628205128205,0.619047619048,0.397435897436,0.448717948718,0.589743589744,0.615384615385,0.628205128205,0.619047619048,0.5,0.619047619048,0.628205128205,0.666666666667,0.583333333333,0.619047619048,0.705128205128,0.654761904762,0.619047619048,0.589743589744,0.690476190476,0.619047619048,0.692307692308,0.678571428571,0.589743589744,0.538461538462,0.511904761905,0.52380952381,0.589743589744,0.589743589744,0.589743589744,0.547619047619,0.551282051282,0.666666666667,0.619047619048,0.628205128205,0.654761904762,0.511904761905,0.705128205128,0.619047619048,0.628205128205,0.547619047619,0.628205128205,0.628205128205,0.619047619048,0.474358974359,0.628205128205,0.628205128205,0.654761904762,0.654761904762,0.666666666667,0.654761904762,0.666666666667,0.642857142857,0.628205128205,0.630952380952,0.654761904762,0.628205128205,0.628205128205,0.628205128205,0.619047619048,0.615384615385,0.654761904762,0.628205128205,0.589743589744,0.559523809524,0.589743589744,0.583333333333,0.583333333333,0.615384615385,0.666666666667,0.666666666667,0.690476190476,0.678571428571,0.615384615385,0.628205128205,0.602564102564,0.705128205128,0.512820512821,0.615384615385,0.589743589744,0.642857142857 )
alangcompParDF = as.data.frame(alangcompPar)
wlangcompParDF = as.data.frame(wlangcompPar)
alangcompSynDF = as.data.frame(alangcompSyn)
wlangcompSynDF = as.data.frame(wlangcompSyn)
alangcompParDF$set = "APiCS"
alangcompSynDF$set = "APiCS"
wlangcompParDF$set = "WALS"
wlangcompSynDF$set = "WALS"
alangcompParDF = rename(alangcompParDF, c("alangcompPar" = "Complexity"))
alangcompSynDF = rename(alangcompSynDF, c("alangcompSyn" = "Complexity"))
wlangcompParDF = rename(wlangcompParDF, c("wlangcompPar" = "Complexity"))
wlangcompSynDF = rename(wlangcompSynDF, c("wlangcompSyn" = "Complexity"))
awPar = rbind(alangcompParDF,wlangcompParDF)
awSyn = rbind(alangcompSynDF,wlangcompSynDF)
parPlot = ggplot(awPar, aes(Complexity, fill=set)) + geom_density(alpha=0.2, aes(y=..scaled..)) + theme(panel.grid=element_blank(), panel.background = element_blank())
parPlotBW = parPlot +  scale_fill_grey(start = 0, end = .9)
synPlot = ggplot(awSyn, aes(Complexity, fill=set)) + geom_density(alpha=0.2, aes(y=..scaled..)) + theme(panel.grid=element_blank(), panel.background = element_blank())
synPlotBW = synPlot +  scale_fill_grey(start = 0, end = .9)
#ggsave("/Users/jcgood/gitrepos/complexity/parDistr.pdf", plot=parPlot)
#ggsave("/Users/jcgood/gitrepos/complexity/synDistr.pdf", plot=synPlot)
ggsave("/Volumes/Obang/MyDocuments/Saramaccan/Papers/WordStructure/parDistr.pdf", plot=parPlot)
ggsave("/Volumes/Obang/MyDocuments/Saramaccan/Papers/WordStructure/synDistr.pdf", plot=synPlot)
ggsave("/Users/jcgood/gitrepos/complexity/parDistrBW.pdf", plot=parPlotBW)
ggsave("/Users/jcgood/gitrepos/complexity/synDistrBW.pdf", plot=synPlotBW)
aParHist = ggplot(alangcompParDF,aes(Complexity, fill=set)) + geom_histogram(alpha=0.5) + geom_density(alpha=.2) + theme(panel.grid=element_blank(), panel.background = element_blank())
wParHist = ggplot(wlangcompParDF,aes(Complexity, fill=set)) + geom_histogram(alpha=0.5, fill="#33CCCC") + geom_density(alpha=.2, fill="#33CCCC") + theme(panel.grid=element_blank(), panel.background = element_blank())
ggsave("/Users/jcgood/gitrepos/complexity/aParHist.pdf", plot=aParHist)
ggsave("/Users/jcgood/gitrepos/complexity/wParHist.pdf", plot=wParHist)
fc = read.table("/Users/jcgood/gitrepos/complexity/FeatComp.txt", row.names=NULL, header=TRUE)
fcfit = glm(fc$Set ~ fc$Feature:fc$Complexity, family="binomial")
layout(matrix(c(1,2,3,4),2,2))
fcplot = plot(fcfit)
