# zfit-reimplementation
DiHiggs analysis reimplementation in zfit. 

`data_extract.C` creates a text file `out.txt` that has information from the RooWorkspace. 

`out.txt` is parsed in `create_parameters.py` to create the observable space, nuisance parameters, constraints, parameters of interest, and other objects in zfit. 

`model_combined.txt` is the datacard with the combined model created with Higgs Combine. This reflects some of the content in the RooWorkspace. 

`other_workspace_elements.txt` contains the commands and outputs that are used to create the background QCD model, and perform scans for the kappa values and branching ratios. 

`PrintSummary.C` prints a summary of the RooWorkspace contents by printing the number of events in each category.  

`SampleDataExtraction.C` has example commands that print out the contents of the RooWorkspace.

Figures plotted:
-   `Higgs_SMBR`: Branching ratios of Higgs decay channels
-   `kl_5_kt_1`, `kl_0_kt_1`, `kl_1_kt_1`: High and low Yukawa coupling constant estimations given different constant Higgs self-coupling constant.
-   `QCD_SRBin3_fit`: Exponential fitting with zfit of QCD background data in the category SRBin3.
-   `root_vs_zfit_qcd`: Comparison of execution time and Estimated Distance to Minimum (EDM) of zfit and ROOT fittings, of the QCD model from SRBin3
-   `QCD_fitting_comparison`: Plot of the zfit fit, ROOT fit and original QCD bin values
