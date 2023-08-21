import zfit
import numpy as np
import pandas as pd
import zfit.z.numpy as znp
from matplotlib import pyplot as plt
import mplhep
from zfit import z
import re

# Measuring execution time of zfit fitting
start = timer()

qcd_bin_vals = [91.9896, 77.4989, 67.9044, 58.9696, 52.7691, 46.4393, 39.324, 33.0533, 26.365, 20.5716, 16.2119, 12.0681, 9.05578, 6.15005, 4.57318, 3.08621, 2.52006]
qcd_bin_densities = [0.0161797, 0.013631, 0.0119434, 0.0103719, 0.00928135, 0.00816803, 0.00691654, 0.00581361, 0.00463723, 0.00361825, 0.00285144, 0.0021226, 0.00159279, 0.00108171, 0.000804358, 0.00054282, 0]

obs = zfit.Space("msd", limits=(50, 220))

np_data = np.array(qcd_bin_vals)

data_nobin = zfit.Data.from_numpy(obs, array=np_data)
nbins = 17
data = data_nobin.to_binned(nbins)

# Making a zfit exponential model to approximate the QCD background
lam = zfit.Parameter("Lambda", -1, -20, 0)
exp_model = zfit.pdf.Exponential(lam, obs=obs)

# Minimising loss of the fit
nll2 = zfit.loss.UnbinnedNLL(model=exp_model, data=qcd_bin_vals)

minimizer2 = zfit.minimize.Minuit()
minimum2 = minimizer2.minimize(loss=nll2)
params = minimum2.params
print(minimum2)

# Plot the exponential fit of the QCD model
bins = np.linspace(50, 220, 18)
hist_frequencies = np.array(qcd_bin_vals)
bin_edges = bins
bin_widths = np.diff(bin_edges)
bin_centers = bin_edges[:-1] + bin_widths/2
plt.bar(bin_centers, hist_frequencies, width=bin_widths, label='QCD values')
plt.xlabel('msd')
plt.ylabel('Bin value')
pdf = zfit.run(exp_model.pdf(bin_centers))
# Normalisation constant can be found in `other_workspace_elements.txt`
plt.plot(bin_centers, pdf * 568.55 * 10, color='black', label='Unnormalised fit')
plt.plot(bin_centers, np.array(qcd_bin_vals).shape[0] / 17 * (220 - 50) * pdf, color='orange', label='Exponential fit')
plt.legend()
plt.show()

# Check how good the fitting is
print(zfit.run(exp_model.pdf(bin_centers)))
print(qcd_bin_densities)
print(qcd_bin_vals)

print(f"params raw: {repr(minimum2.params)}")
errors, new_result = minimum2.errors(name="errors")
print(f"New result: {new_result}")
minuit_uncs, _ = minimum2.errors(name="minuit_unc", method="minuit_minos")
minuit_uncs, _ = minimum2.errors(name="minuit_unc_2sig", method="minuit_minos", cl=0.95)
# zfit_uncs, _ = minimum2.errors(name="zfit_unc", method="zfit_errors") - zfit error analysis method

hesse = minimum2.hesse(name="h_minuit", method="minuit_hesse") 
hesse = minimum2.hesse(name="h_minuit_2sig", method="minuit_hesse", cl=0.95) 
# hesse2 = minimum2.hesse(name="h_zfit", method="hesse_np") - zfit error analysis method
hesse3 = minimum2.hesse(name="h_approx", method="approx")

print(f"Approx gradient: {minimum2.approx.gradient()}")  # gradient approx not available in iminuit
print(f"Approx hessian (no invert): {minimum2.approx.hessian(invert=False)}")  # hessian approximation is also not available
print(f"Approx inverse hessian: {minimum2.approx.inv_hessian(invert=False)}")  # inv_hessian is available
print(f"Approx hessian (can invert): {minimum2.approx.hessian(invert=True)}")  # allowing the invert now inverts the inv_hessian

# Approx gradient: None
# Approx hessian (no invert): None
# Approx inverse hessian: [[0.0007269]]
# Approx hessian (can invert): [[1375.70332147]]

# For some reason all the zfit-specific methods aren't running
# with zfit.run.set_autograd_mode(True):
#     hesse4 = minimum2.hesse(name="h_autograd", method="hesse_np")
# print(minimum2)

minimum2.info.get("original", f"Not available for the minimizer: {minimum2.minimizer}")
minimum2.info.get("minuit", "Not available, not iminuit used in minimization?")

minimum2.message
# output: '' -- means nothing went wrong 

end = timer()
print(f'execution time: {end - start}')


# FitResult of
# <UnbinnedNLL model=[<zfit.<class 'zfit.models.basic.Exponential'>  params=[lambda2, lambda2]] data=[<zfit.core.data.Data object at 0x7defbd42e0e0>] constraints=[]> 
# with
# <Minuit Minuit tol=0.001>

# ╒═════════╤═════════════╤══════════════════╤═════════╤═════════════╕
# │ valid   │ converged   │ param at limit   │ edm     │ min value   │
# ╞═════════╪═════════════╪══════════════════╪═════════╪═════════════╡
# │ True    │ True        │ False            │ 2.6e-06 │ 9962.727    │
# ╘═════════╧═════════════╧══════════════════╧═════════╧═════════════╛

# Parameters
# name       value  (rounded)               errors           minuit_unc      minuit_unc_2sig     h_minuit     h_approx    h_minuit_2sig    at limit
# -------  ------------------  -------------------  -------------------  -------------------  -----------  -----------  ---------------  ----------
# lambda2          -0.0214455  -  0.034   +  0.027  -  0.034   +  0.027  -  0.083   +  0.027  +/-   0.027  +/-   0.027      +/-   0.053        True
