# zfit-reimplementation
DiHiggs analysis reimplementation in zfit. 

`data_extract.C` creates a text file `out.txt` that has information from the RooWorkspace. 

`out.txt` is parsed in `create_parameters.py` to create the observable space, nuisance parameters, constraints, parameters of interest, and other objects in zfit. 

`model_combined.txt` is the datacard with the combined model created with Higgs Combine. This reflects some of the content in the RooWorkspace. 

`other_workspace_elements.txt` contains the commands and outputs that are used to create the background QCD model, and perform scans for the kappa values and branching ratios. 

`PrintSummary.C` prints a summary of the RooWorkspace contents by printing the number of events in each category.  

`SampleDataExtraction.C` has example commands that print out the contents of the RooWorkspace.

There are also screenshots of all the results plotted. 
