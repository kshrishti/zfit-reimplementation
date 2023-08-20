# zfit-reimplementation
DiHiggs analysis reimplementation in zfit. 

`data_extract.C` creates a text file `out.txt` that has information from the RooWorkspace. 
`out.txt` is parsed in `create_parameters.py` to create the observable space, nuisance parameters, constraints, parameters of interest, and other objects in zfit. 
