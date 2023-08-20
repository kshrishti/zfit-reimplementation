with open("other_workspace_elements.txt") as file:
  smbr_dict = {}
  for text in file:
    smbr_pattern = r'RooSpline1D::SM_BR_(\w+)\[ xvar=MH \] = (\d+\.\d+)'
    smbr_match = re.search(smbr_pattern, text)
    if smbr_match:
      smbr_dict[smbr_match.group(1)] = smbr_match.group(2)

for br, val in smbr_dict.items():
  print(f'{br}: {val}')

plt.bar(list(smbr_dict.keys()), np.array(list(smbr_dict.values()), dtype=float), width=0.8, color='maroon')
plt.title("Higgs Standard Model Branching Ratios")
plt.show()
