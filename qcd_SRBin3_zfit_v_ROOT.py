import numpy as np
from matplotlib import pyplot as plt

bins = np.linspace(50, 220, 18)
bin_widths = np.diff(bins)
bin_centers = bins[:-1] + bin_widths/2

print(f'zfit fitted values: {zfit.run(exp_model.pdf(bin_centers)) * 568.55 * 10}')
print(f'actual qcd values: {qcd_bin_vals}')
zfit_fit = zfit.run(exp_model.pdf(bin_centers)) * 568.55 * 10
root_fit = [ 94.77110698,  80.24260358,  67.94133396,  57.52586101,  48.70709024,
  41.24024567,  34.91807567,  29.56510051,  25.03274168,  21.1951979,
  17.94595333,  15.19482113,  12.86544019,  10.89315562,   9.22322421,
   7.80929492,   6.61212237]
print(f'root fitted values: {root_fit}')
x_axis = np.array([55., 65., 75., 85., 95., 105., 115., 125., 135., 145., 155., 165., 175., 185., 195., 205., 215.])
plt.bar(bin_centers, qcd_bin_vals, width=bin_widths, label='QCD values')
plt.plot(bin_centers, zfit_fit, label='zfit fit', color='red')
plt.plot(bin_centers, root_fit, label='ROOT fit', color='orange')
plt.legend()
plt.show()


# zfit fitted values: [112.46653816  90.75836359  73.24027837  59.10351579  47.69541647
#   38.48929664  31.06013252  25.06493795  20.22692962  16.32274864
#   13.17214863  10.62967416   8.57794548   6.92223934   5.58611588
#    4.50788958   3.63778141]
# actual qcd values: [91.9896, 77.4989, 67.9044, 58.9696, 52.7691, 46.4393, 39.324, 33.0533, 26.365, 20.5716, 16.2119, 12.0681, 9.05578, 6.15005, 4.57318, 3.08621, 2.52006]
# root fitted values: [94.77110698, 80.24260358, 67.94133396, 57.52586101, 48.70709024, 41.24024567, 34.91807567, 29.56510051, 25.03274168, 21.1951979, 17.94595333, 15.19482113, 12.86544019, 10.89315562, 9.22322421, 7.80929492, 6.61212237]
