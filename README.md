WALS-APiCS complexity
==========

This repository contains code and data relevant to examining complexity of
WALS-APiCS features following proposals made in this paper:
https://benjamins.com/#catalog/journals/jpcl.27.1.01goo/ and procedures
described in this draft paper:
http://buffalo.edu/~jcgood/jcgood-ParadigmaticComplexityCreoles.pdf.
Documentation is relatively sparse since it is not clear to me how much outside
interest there will be in these materials. However, they are posted here in the
interest of transparency and replicability. Please feel free to contact Jeff
Good (jcgood@buffalo.edu) with any questions on how to use these materials.
Please note that the database posted here is mostly based on content from the
World Atlas of Language Structures (WALS; http://wals.info) and the Atlas of
Pidgin and Creole Language Structures (APiCS; http://apics-online.info). If you
choose to reuse this data, please cite these original sources as appropriate.
Citation information can be found on the websites for each of these projects.

Brief descriptions of each file are given below

- APiCSFeatureComps.txt: Tabular data summarizing complexity values across
WALS-APiCS features.

- APiCSLangComps.txt:  Tabular data summarizing complexity values across
WALS-APiCS languages for languages with values for most features.

- APiCSLangCompVals.txt: Specific complexity values for each APiCS features
across each APiCS language.

- APiCSWALS.r: Automatically generated output for loading into R for statisical
processing.

- APiCSWALSComplexity.sql: SQL dump of database used to encode complexity
scores. This database combines data from WALS (http://wals.info) and APiCS
(http://apics-online.info), and adds new information relevant to calculating
syntagmatic and paradigmatic complexity of WALS-APiCS features. Details on the
relevant methods and theoretical assumptions can be found in a draft paper
submitted for publication that is posted here:
http://buffalo.edu/~jcgood/jcgood-ParadigmaticComplexityCreoles.pdf. This paper
also contains more detailed references. The database is designed to be used
in conjunction with calculateComplexities.py to generate the complexity
scores used in the paper linked to above.

- calculateComplexities.py: A script for generating various files and complexity
scores for the study of WALS-APiCS patterns of complexity.

- CompDocumentation.txt: Documentation of criteria employed to determine maximum
complexity across features.

- complexity.py: A set of Python methods for interacting with the database to
generate complexity figures.

- FeatComp.txt: An output of all complexity scores across all features.

- README.md: This file.

- ValDocumentation.txt: Documentation of criteria employed to determine
complexity level across each value.

- calculateComplexities.pyc: Python-generated file.

- complexity.pyc: : Python-generated file.

- LICENSE: License for material on this site.

- Various pdf files for visualizations of the data:
aParHist.pdf
featDistr.pdf
featDistrBW.pdf
featDistrPar.pdf
featDistrParBW.pdf
parDistr.pdf
parDistrBW.pdf
synDistr.pdf
synDistrBW.pdf
wParHist.pdf