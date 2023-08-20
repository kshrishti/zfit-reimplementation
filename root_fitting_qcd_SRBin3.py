import ROOT
import numpy as np

from timeit import default_timer as timer

start = timer()

x_axis = np.array([55., 65., 75., 85., 95., 105., 115., 125., 135., 145., 155., 165., 175., 185., 195., 205., 215.])
y_axis = np.array([91.9896, 77.4989, 67.9044, 58.9696, 52.7691, 46.4393, 39.324, 33.0533, 26.365, 20.5716, 16.2119, 12.0681, 9.05578, 6.15005, 4.57318, 3.08621, 2.52006])

graph = ROOT.TGraph(len(x_axis), x_axis, y_axis)

# Create the exponential fit and set the initial guesses
exponential_fit = ROOT.TF1("exponential_fit", "[0] * exp([1] * x)", x_axis[0], x_axis[-1])
exponential_fit.SetParameters(100, -0.03)  

graph.Fit("exponential_fit", "R")  # "R" for range fit within x-axis range

# Get the values of the parameters and y-values after they have been fitted
parameters = [exponential_fit.GetParameter(i) for i in range(2)]
print("Fit parameters:", parameters)

fitted_y_values = np.array([exponential_fit.Eval(x) for x in x_axis])
print("Fitted y-axis values:", fitted_y_values)

canvas = ROOT.TCanvas("canvas", "Exponential Fit", 800, 600)
graph.Draw("AP")  # "AP" for points and connecting lines
exponential_fit.Draw("same")
canvas.Draw()

# Measure execution time
end = timer()
print(f'execution time: {end - start}')


# ****************************************
# Minimizer is Minuit / Migrad
# Chi2                      =      205.093
# NDf                       =           15
# Edm                       =  5.11604e-10
# NCalls                    =           81
# p0                        =      236.682   +/-   14.1239     
# p1                        =    -0.016641   +/-   0.000701485 
# Fit parameters: [236.68249248635354, -0.016640999358609236]
# Fitted y-axis values: [ 94.77110698  80.24260358  67.94133396  57.52586101  48.70709024
#   41.24024567  34.91807567  29.56510051  25.03274168  21.1951979
#   17.94595333  15.19482113  12.86544019  10.89315562   9.22322421
#    7.80929492   6.61212237]
# Fontconfig warning: ignoring UTF-8: not a valid region tag
# execution time: 0.22956785303540528
