# This would be a continuation of the previous model-building, so we would use the same variables

sampler = exp_model.create_sampler(n=1000, fixed_params=True)
nll_sample = zfit.loss.UmbinnedNLL(model=exp_model, data=sampler)

minimizer = zfit.minimize.Minuit()

results = []
nruns = 10
for run in range(nruns):
  sampler.resample()  
  result = minimizer.minimize(nll_sample)
  results.append(result)


# If the parameters are constrained, such as the nuisance parameters that we have in the full model, we would deal with it as follows (with example values for the observation and uncertainty)
# These values come from out.txt:
  # SimpleGaussianConstraint::SRBin3_bbbb_boosted_ggf_others_mcstat_bin16_Pdf "SRBin3_bbbb_boosted_ggf_others_mcstat_bin16_Pdf"
  # RooRealVar::SRBin3_bbbb_boosted_ggf_others_mcstat_bin16 = 0 +/- 1  L(-4 - 4) 
observation = 0
uncertainty = 1

constraint = zfit.constraint.GaussianConstraing(params=[lam], observation=observation, uncertainty=uncertainty)

n_samples = 5

sampler_new = exp_model.create_sampler(n=n_samples, fixed_params=[lam])
nll = zfit.loss.UnbinnedNLL(model=exp_model, data=sampler_new, constraints=constraint)

constr_values = constraint.sample(n=n_samples)

for constr_params, constr_vals in constr_values.items():
    sampler.resample()
    with zfit.param.set_values(constr_params, constr_vals):
        minimizer.minimize(nll)  
