# zfit-reimplementation
DiHiggs analysis reimplementation in zfit. 

`data_extract.C` creates a text file `out.txt` that has information from the RooWorkspace. 

`out.txt` is parsed in `create_parameters.py` to create the observable space, nuisance parameters, constraints, parameters of interest, and other objects in zfit. 

`model_combined.txt` is the datacard with the combined model created with Higgs Combine. This reflects some of the content in the RooWorkspace. 

`other_workspace_elements.txt` contains the commands and outputs that are used to create the background QCD model, and perform scans for the kappa values and branching ratios. 

`zfit_qcd_SRBin3.py` is the code to run the zfit exponential fitting of the QCD background in the category SRBin3. 
`root_fitting_qcd_SRBin3.py` runs a ROOT exponential model fitting of the QCD background in the category SRBin3. 
`qcd_SRBin3_zfit_v_ROOT.py` compares the fitting of zfit and ROOT for the QCD model in SRBin3. 

`qcd_plotting_all_cats.py` runs a fitting for the QCD background in all categories.

`PrintSummary.C` prints a summary of the RooWorkspace contents by printing the number of events in each category.  
`SampleDataExtraction.C` has example commands that print out the contents of the RooWorkspace.

`zfit_toy_model.py` details an extension which can be used when the PDFs are known but the data itself isn't, thereby using samples to generate data and minimise the loss of fitting. 

`zfit_unbinned_fit.py` does the same thing as `zfit_qcd_SRBin3.py`, but instead of using a numpy array converted to a tensor, it uses an unbinned Data object, which appears to make a worse fit and takes more time to execute. 

Figures plotted:
-   `Higgs_SMBR`: Branching ratios of Higgs decay channels
-   `kl_5_kt_1`, `kl_0_kt_1`, `kl_1_kt_1`: High and low Yukawa coupling constant estimations given different constant Higgs self-coupling constant.
-   `QCD_SRBin3_fit`: Exponential fitting with zfit of QCD background data in the category SRBin3.
-   `root_vs_zfit_qcd`: Comparison of execution time and Estimated Distance to Minimum (EDM) of zfit and ROOT fittings, of the QCD model from SRBin3
-   `QCD_fitting_comparison`: Plot of the zfit fit, ROOT fit and original QCD bin values
-   `zfit_unbinnedData_qcd_SRBin3_fit`: zfit fit using qcd values as an unbinned Data object. 
