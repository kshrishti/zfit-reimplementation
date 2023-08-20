kl_dict = {}

with open("rws_data.txt") as file:
    for text in file:
        kappa_pattern = r'AsymPow::systeff_SRBin3_ggHH_kl_(\d+)_kt_(\d+)_.*?bin(\d+)\[ kappaLow=(\d+\.\d+) kappaHigh=(\d+\.\d+).*?'
        kappa_match = re.search(kappa_pattern, text)
        if kappa_match:
            kl = int(kappa_match.group(1))
            kt = int(kappa_match.group(2))
            bin_number = int(kappa_match.group(3))
            kappa_low = float(kappa_match.group(4))
            kappa_high = float(kappa_match.group(5))
            
            if kl not in kl_dict:
                kl_dict[kl] = {}
            
            kl_dict[kl][bin_number] = {'kappaLow': kappa_low, 'kappaHigh': kappa_high}

for kl_kt, bins in kl_dict.items():
    print(f'kl_{kl_kt}_kt')
    for bin_number, values in bins.items():
        print(f"bin{bin_number}: {values}")

for kl, bins in kl_dict.items():
  x_axis = []
  k_highs = []
  k_lows = []
  for bin_number, values in bins.items():
    x_axis.append(55 + 10 * bin_number)
    k_lows.append(values['kappaLow'])
    k_highs.append(values['kappaHigh'])
  fig, ax = plt.subplots()
  ax.plot(x_axis, k_lows, color='yellow', label='kappa_lows')
  ax.plot(x_axis, k_highs, color='yellow', label='kappa_highs')
  ax.axhline(y=1, color='black', label='SM_kappa')
  ax.set_title(f'kl_{kl}kt_1')
  ax.set_xlabel('msd')
  ax.set_ylabel('kappa')
  ax.legend()
  ax.fill_between(x_axis, 1, k_lows, color='yellow', alpha=.2)
  ax.fill_between(x_axis, 1, k_highs, color='yellow', alpha=.2)
  plt.show()
