from __future__ import print_function, division
import os
import numpy as np
import logging
import sys
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import zfit
import zfit.z.numpy as znp
import zfit_physics as zphysics
from zfit import z
import re    

filename = "/out.txt"      # this is the file that has all the contents of the RooWorkspace

obs_pattern = r'(\w+)\s*=\s*([\d.]+)\s+L\((\d+)\s*-\s*(\d+)\)\s+B\((\d+)\)'
# msd =  215.00 L(50 - 220) B(17)

weight_pattern = r'(\w+)\s*=\s*([\d.]+)\s+L\((-?[\d.eE+-]+)\s*-\s*(-?[\d.eE+-]+)\)'
# weight =  0.0000 L(-1e+09 - 1e+09)

param_pattern = r'(\w+)\s*=\s*([\d.]+)\s*\+/-\s*([\d.]+)\s+L\(([-\d]+)\s*-\s*([-\d]+)\)'
# ps_fsr =  0.0000 +/- 1.0000 L(-4 - 4)

poi_floating_pattern = r'(\w+)\s*=\s*([\d.]+)\s+L\(([-\d]+)\s*-\s*(\d+)\)'
# r =  1.0000 L(-20 - 20)

poi_const_pattern = r'(\w+)\s*=\s*([\d.]+)\s+C\s+L\(([-\d]+)\s*-\s*(\d+)\)'
# r_gghh =  1.0000 C L(-20 - 20)

channel_pattern = r'Index:\s*(\d+), Pdf:\s*(\w+), Data:\s*(\w+), SumEntries:\s*(\d+), NumEntries:\s*(\d+)'
# Index: 0, Pdf: pdf_binfitfail, Data: SRBin1, SumEntries: 50, NumEntries: 17

channels = {}   # name : sum_entries --> acts almost like a binning
obs = []

data = []
bins = []
range = []
weights = []
# numpy.histogram(a, bins=10, range=None, density=None, weights=None)

with open(filename) as f:
  for text in f:
    obs_match = re.search(obs_pattern, text)
    param_match = re.search(param_pattern, text)
    poi_floating_match = re.search(poi_floating_pattern, text)
    poi_const_match = re.search(poi_const_pattern, text)
    channel_match = re.search(channel_pattern, text)

    # only to take the first one of this, becuase this appears multiple times in the data
    if obs_match and obs == []:
      obs_name = obs_match.group(1)
      obs_value = float(obs_match.group(2))
      obs_lo_lim = int(obs_match.group(3))
      obs_hi_lim = int(obs_match.group(4))
      num_bins = int(obs_match.group(5))

      bins.append(num_bins)
      range.append((int(obs_match.group(3)), int(obs_match.group(4))))
      globals()[obs_name] = zfit.Space(obs_name, (obs_lo_lim, obs_hi_lim))

      obs.append(globals()[obs_name])

    elif obs_match:
      hist_x_val = float(obs_match.group(2))
      next_line = next(f)
      weight_match = re.search(weight_pattern, next_line)
      if weight_match:
        weight = float(weight_match.group(2))
        weights.append(weight)
      # need to figure out how to get hist_y_val and then data.append(hist_y_val)

    elif param_match:
      param_name = param_match.group(1)
      param_val = float(param_match.group(2))
      param_unc_val = float(param_match.group(3))
      param_lo_val = int(param_match.group(4))
      param_hi_val = int(param_match.group(5))

      globals()[param_name] = zfit.Parameter(param_name, param_val, param_lo_val, param_hi_val)
      # all of these have shape/prior lnN - need to add constraints
      # if a nuisance parameter, has lnN constraint from datacard
      zfit.constraint.LogNormalConstraint(globals()[param_name], param_val, param_unc_val)
      # OR if a syst, has gaussian constraint of 1 sigma `shape`
      zfit.constraint.GaussianConstraint(globals()[param_name], param_val, param_unc_val)


    elif poi_floating_match:
      poi_name = poi_floating_match.group(1)
      poi_val = float(poi_floating_match.group(2))
      poi_lo_val = int(poi_floating_match.group(3))
      poi_hi_val = int(poi_floating_match.group(4))

      globals()[poi_name] = zfit.Parameter(poi_name, poi_val, poi_lo_val, poi_hi_val)

    elif poi_const_match:
      poi_name = poi_const_match.group(1)
      poi_val = float(poi_const_match.group(2))
      poi_lo_val = int(poi_const_match.group(3))
      poi_hi_val = int(poi_const_match.group(4))

      globals()[poi_name] = zfit.Parameter(poi_name, poi_val, poi_lo_val, poi_hi_val, floating=False)

    elif channel_match:
      channel_num = channel_match.group(1)
      channel_pdf_name = channel_match.group(2)
      channel_name = channel_match.group(3)
      channel_sum_entries = channel_match.group(4)
      channel_num_entries = channel_match.group(5)
      channels[channel_name] = channel_sum_entries
