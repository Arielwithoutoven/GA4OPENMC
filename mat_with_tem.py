import openmc

CROSS_SECTIONS_LIST = ["/home/openmc/cross_sections/mcnp_endfb70/cross_sections.xml",
  "/home/cardinal/cross_sections/mcnp_endfb70/cross_sections.xml",
  "/home/cardinal/cross_sections/mcnp_endfb71/cross_sections.xml",
  "/home/cardinal/cross_sections/lib80x_hdf5/cross_sections.xml"]

OPENMC_CROSS_SECTIONS = CROSS_SECTIONS_LIST[3]
mats = openmc.Materials()
mats.cross_sections = OPENMC_CROSS_SECTIONS

UHZr_elements = {"U":0.12, "Zr":0.864, "H":0.016}
UHZr= openmc.Material(name="UHZr")
UHZr.add_components(UHZr_elements, "wo")
UHZr.set_density("g/cc", 6.15)
UHZr.add_s_alpha_beta(name="c_H_in_ZrH", fraction=1.0)
UHZr.add_s_alpha_beta(name="c_Zr_in_ZrH", fraction=1.0)

UHZr_30815 = UHZr.clone()
UHZr_30815._temperature=308.15

UHZr_30817 = UHZr.clone()
UHZr_30817._temperature=308.17

UHZr_30818 = UHZr.clone()
UHZr_30818._temperature=308.18

mats.append(UHZr_30815)
mats.append(UHZr_30817)
mats.append(UHZr_30818)

mats.export_to_xml()
print(UHZr_30815)
#print(help(UHZr_30815))
