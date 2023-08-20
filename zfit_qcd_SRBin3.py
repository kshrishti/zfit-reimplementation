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


end = timer()
print(f'execution time: {end - start}')


# FitResult of
# <UnbinnedNLL model=[<zfit.<class 'zfit.models.basic.Exponential'>  params=[Lambda, Lambda]] data=[<zfit.core.data.Data object at 0x7fb00ec220b0>] constraints=[]> 
# with
# <Minuit Minuit tol=0.001>

# ╒═════════╤═════════════╤══════════════════╤═════════╤═════════════╕
# │ valid   │ converged   │ param at limit   │ edm     │ min value   │
# ╞═════════╪═════════════╪══════════════════╪═════════╪═════════════╡
# │ True    │ True        │ False            │ 2.6e-06 │ 9962.727    │
# ╘═════════╧═════════════╧══════════════════╧═════════╧═════════════╛

# Parameters
# name      value  (rounded)    at limit
# ------  ------------------  ----------
# Lambda          -0.0214455       False

# zfit.run(exp_model.pdf(bin_centers)):
  # [0.01978129 0.01596313 0.01288194 0.01039548 0.00838896 0.00676973
  #  0.00546304 0.00440857 0.00355763 0.00287094 0.0023168  0.00186961
  #  0.00150874 0.00121753 0.00098252 0.00079287 0.00063983]
# qcd_bin_densities:
  # [0.0161797, 0.013631, 0.0119434, 0.0103719, 0.00928135, 0.00816803, 0.00691654, 0.00581361, 0.00463723, 0.00361825, 0.00285144, 0.0021226, 0.00159279, 0.00108171, 0.000804358, 0.00054282, 0]
# qcd_bin_vals:
  # [91.9896, 77.4989, 67.9044, 58.9696, 52.7691, 46.4393, 39.324, 33.0533, 26.365, 20.5716, 16.2119, 12.0681, 9.05578, 6.15005, 4.57318, 3.08621, 2.52006]

# execution time: 1.3615611370005354
