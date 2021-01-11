This is a repository for a dissertation project for MSc in Software System Engineering at UCL
The project is on Modification Operators Selection Strategy and Operators Efficacy for Genetic Improvement Techniques


## Prerequisites:
* [PyGGI 2.0](https://github.com/coinse/pyggi) The project uses PyGGI 2.0 as the APR GI tool
* [QuixBugs benchmark](https://github.com/jkoppel/QuixBugs) The project uses Java programs from the QuixBugs benchmark for evalutation
* [Python 3.5+](https://www.continuum.io/downloads)
* [srcML](https://www.srcml.org/#download) (needed to translate Java code to XML-based representtion

## Instructions:
* ./QuixBugs - a directory with the QuixBugs Java programs and their test suites
* logs_* - directories with log files from PyGGI runs with standard and uniform operator selection strategies

# Scripts:
* run_quixbugs.py - file to run PyGGI with QuixBugs with the standard setup
* run_quixbugs_uniform.py - file to run PyGGI with QuixBugs with the uniform sampling using Insertions before and after
* run_quixbugs_uniform_insertb4only.py - file to run PyGGI with QuixBugs with the uniform sampling using Insertions before only
* **run_quixbugs_uniform_insertb4only_fitness.py - file to run PyGGI with QuixBugs with the uniform sampling using Insertions before only and gathering all data needed for study analysis, this script was used to obtain results for the project**

# Analysis:
* operatorxnodes_analysis.ipynb - Jupiter Notebook that was used to analyse the behaviour of operators on different types of target and ingredient nodes
* Pyggi + QuixBugs Results.xlsx and Pyggi + QuixBugs Results.ods - sheets with further analysis of the data, charts, tables etc
* operatorefficacy_results.csv, operatorefficacy_results_ot.csv, operatorefficacy_results_oti.csv - csv files with raw data for the analysis
