import zfit
import numpy as np
import pandas as pd
import zfit.z.numpy as znp
from matplotlib import pyplot as plt
import mplhep
from zfit import z
import re
from timeit import default_timer as timer

start = timer()

qcd_bin_vals = [91.9896, 77.4989, 67.9044, 58.9696, 52.7691, 46.4393, 39.324, 33.0533, 26.365, 20.5716, 16.2119, 12.0681, 9.05578, 6.15005, 4.57318, 3.08621, 2.52006]
qcd_bin_densities = [0.0161797, 0.013631, 0.0119434, 0.0103719, 0.00928135, 0.00816803, 0.00691654, 0.00581361, 0.00463723, 0.00361825, 0.00285144, 0.0021226, 0.00159279, 0.00108171, 0.000804358, 0.00054282, 0]

obs = zfit.Space("msd", limits=(50, 220))

np_data = np.array(qcd_bin_vals)

data_nobin = zfit.Data.from_numpy(obs, array=np_data)
nbins = 17
data = data_nobin.to_binned(nbins)

# Making a zfit exponential model to approximate the QCD background
lam = zfit.Parameter("lambda", -1, -20, 0)
exp_model = zfit.pdf.Exponential(lam, obs=obs)

# Minimising loss of the fit
# NOTE: Uses unbinned Data object instead of directly using numpy array which is converted to a tensor. 
nll2 = zfit.loss.UnbinnedNLL(model=exp_model, data=data_nobin)

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
# <UnbinnedNLL model=[<zfit.<class 'zfit.models.basic.Exponential'>  params=[lambda, lambda]] data=[<zfit.core.data.Data object at 0x7defc053f2e0>] constraints=[]> 
# with
# <Minuit Minuit tol=0.001>

# ╒═════════╤═════════════╤══════════════════╤═════════╤═════════════╕
# │ valid   │ converged   │ param at limit   │ edm     │ min value   │
# ╞═════════╪═════════════╪══════════════════╪═════════╪═════════════╡
# │ True    │ True        │ False            │ 9.6e-08 │ 9920.803    │
# ╘═════════╧═════════════╧══════════════════╧═════════╧═════════════╛

# Parameters
# name      value  (rounded)    at limit
# ------  ------------------  ----------
# lambda          -0.0503653       False

# fitted qcd densities:
  # [3.91604163e-02 2.36653971e-02 1.43014572e-02 8.64264726e-03
  #  5.22291892e-03 3.15631094e-03 1.90741975e-03 1.15269065e-03
  #  6.96593260e-04 4.20964782e-04 2.54397161e-04 1.53737125e-04
  #  9.29063188e-05 5.61450856e-05 3.39295613e-05 2.05042902e-05
  #  1.23911392e-05]
# actual qcd densities:
  # [0.0161797, 0.013631, 0.0119434, 0.0103719, 0.00928135, 0.00816803, 0.00691654, 0.00581361, 0.00463723, 0.00361825, 0.00285144, 0.0021226, 0.00159279, 0.00108171, 0.000804358, 0.00054282, 0]
# qcd values:
  # [91.9896, 77.4989, 67.9044, 58.9696, 52.7691, 46.4393, 39.324, 33.0533, 26.365, 20.5716, 16.2119, 12.0681, 9.05578, 6.15005, 4.57318, 3.08621, 2.52006]

# execution time: 1.4340538989999914
