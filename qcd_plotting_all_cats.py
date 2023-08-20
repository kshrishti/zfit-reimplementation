# The values are obtained by using a regular expression pattern matching algorithm from `other_workspace_elements.txt`
qcd_vals_SRBin1 = []
qcd_densities_SRBin1 = []
qcd_vals_SRBin2 = []
qcd_densities_SRBin2 = []
qcd_vals_SRBin3 = []
qcd_densities_SRBin3 = []

with open ("other_workspace_elements.txt") as file:
  density_match = None
  for text in file:
    density_pattern = r'RooFormulaVar::SRBin(\d+)_bbbb_boosted_ggf_qcd_datadriven_bin(\d+)_density.*?formula="(.*?)"\s*] = (\d+\.+\d+)'
    density_match = re.search(density_pattern, text)
    if density_match:
      bin_number = int(density_match.group(1))
      qcd_densities = globals()[f"qcd_densities_SRBin{bin_number}"]
      qcd_densities.append(float(density_match.group(4)))

    val_pattern = r'RooFormulaVar::SRBin(\d+)_bbbb_boosted_ggf_qcd_datadriven_bin(\d+).*?formula="(.*?)"\s*] = (\d+\.+\d+)'
    val_match = re.search(val_pattern, text)
    if val_match and (density_match is None):
      bin_number = int(val_match.group(1))
      qcd_vals = globals()[f"qcd_vals_SRBin{bin_number}"]
      qcd_vals.append(float(val_match.group(4)))

qcd_bin_sum_vals = np.array(qcd_vals_SRBin1) + np.array(qcd_vals_SRBin2) + np.array(qcd_vals_SRBin3)

print(qcd_vals_SRBin1)
print(qcd_vals_SRBin2)
print(qcd_vals_SRBin3)
print(qcd_bin_sum_vals)


# Trying an exponential fit for the sum of bin values over all 3 categories (SRBins)
lam_sum = zfit.Parameter("sum_lam", -1, -50, 0)
sum_exp_vals = zfit.pdf.Exponential(lam_sum, obs=obs)

sum_nll = zfit.loss.UnbinnedNLL(model=sum_exp_vals, data=qcd_bin_sum_vals)

sum_minimizer = zfit.minimize.Minuit()
sum_minimum = sum_minimizer.minimize(loss=sum_nll)
print(sum_minimum)

bins = np.linspace(50, 220, 18)
hist_frequencies = np.array(qcd_bin_sum_vals)
bin_edges = bins
bin_widths = np.diff(bin_edges)
bin_centers = bin_edges[:-1] + bin_widths/2
plt.bar(bin_centers, hist_frequencies, width=bin_widths, label='Data')
plt.xlabel('msd')
plt.ylabel('Bin value')
pdf = zfit.run(sum_exp_vals.pdf(bin_centers))
# here we don't have the normalisation constant because each bin has a separate coefficient
plt.plot(bin_centers, np.array(qcd_bin_sum_vals).shape[0] / 17 * (220 - 50) * pdf, color='orange', label='Exponential fit')
plt.legend()
plt.show()


# Trying to model each category as an exponential and then having a SumPDF to represent the sum of all the bin categories
lam1 = zfit.Parameter("lam1", -1, -50, 0)
lam2 = zfit.Parameter("lam2", -1, -50, 0)
lam3 = zfit.Parameter("lam3", -1, -50, 0)

exp_srbin1 = zfit.pdf.Exponential(lam1, obs=obs)
exp_srbin2 = zfit.pdf.Exponential(lam2, obs=obs)
exp_srbin3 = zfit.pdf.Exponential(lam3, obs=obs)

frac1 = zfit.Parameter("frac1", 0.3, 0, 1)
frac2 = zfit.Parameter("frac2", 0.3, 0, 1)
frac3 = zfit.Parameter("frac3", 0.3, 0, 1)

sum_exp_pdf = zfit.pdf.SumPDF(pdfs=[exp_srbin1, exp_srbin2, exp_srbin3], fracs=[frac1, frac2, frac3])

vals_sum_nll = zfit.loss.UnbinnedNLL(model=sum_exp_pdf, data=qcd_bin_sum_vals)
sum_minimizer = zfit.minimize.Minuit()
sum_minimum = sum_minimizer.minimize(loss=sum_nll)
print(sum_minimum)

bins = np.linspace(50, 220, 18)
hist_frequencies = np.array(qcd_bin_sum_vals)
bin_edges = bins
bin_widths = np.diff(bin_edges)
bin_centers = bin_edges[:-1] + bin_widths/2
plt.bar(bin_centers, hist_frequencies, width=bin_widths, label='Data')
plt.xlabel('msd')
plt.ylabel('Bin value')
pdf = zfit.run(sum_exp_pdf.pdf(bin_centers))
# here we don't have the normalisation constant because each bin has a separate coefficient
plt.plot(bin_centers, np.array(qcd_bin_sum_vals).shape[0] / 17 * (220 - 50) * pdf, color='orange', label='Exponential fit')
plt.legend()
plt.show()

