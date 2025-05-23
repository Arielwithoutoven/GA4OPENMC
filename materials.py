import openmc

openmc.config['cross_sections'] = '/home/cir/NuclearData/mcnp_endfb71/cross_sections.xml'
UHZr_elements = {
    "U": {"percent": 0.1175, "enrichment": 19},
    "Zr": 0.86730387,
    "H": 0.01519613,
}
# TODO: OpenMC assumes the U234/U235 mass ratio is constant at 0.008, which is only valid at low enrichments. Consider setting the isotopic composition manually for enrichments over 5%.
UHZr = openmc.Material(name="UHZr")
UHZr.add_components(UHZr_elements, "wo")
UHZr.set_density("g/cm3", 6.15)
UHZr.add_s_alpha_beta(name="c_H_in_ZrH", fraction=1.0)
UHZr.add_s_alpha_beta(name="c_Zr_in_ZrH", fraction=1.0)


Zr_elements = {"Zr": 0.98233, "Cr": 1e-3, "Fe": 2.1e-3, "Ni": 7e-5, "Sn": 0.0145}
Zr = openmc.Material(name="Zr")
Zr.add_components(Zr_elements, "wo")
Zr.set_density("g/cm3", 6.44)

Graphite = openmc.Material(name="Graphite")
Graphite.add_element("C", 1.0)
Graphite.set_density("g/cm3", 1.65)
Graphite.add_s_alpha_beta(name="c_Graphite", fraction=1.0)

He = openmc.Material(name="He_gas")
He.add_element("He", 1.0)
He.set_density("g/cm3", 1.6094e-4)

SS_elements = {
    "Cr": 0.18,
    "Fe": 0.6744,
    "Ni": 0.11,
    "Ti": 6e-3,
    "C": 6e-4,
    "Si": 8e-3,
    "S": 3e-4,
    "Co": 3e-4,
    "Mn": 2e-2,
    "P": 4e-4,
}
SS = openmc.Material(name="SS")
SS.add_components(SS_elements, "wo")
SS.set_density("g/cm3", 7.9)

H2O_elements = {"H": 2.0, "O": 1.0}
H2O = openmc.Material(name="H2O")
H2O.add_components(H2O_elements, "ao")
H2O.set_density("g/cm3", 0.9982)
H2O.add_s_alpha_beta(name="c_H_in_H2O", fraction=1.0)

Al_elements = {"Al": 0.9395, "Si": 0.0525, "Fe": 8e-3}
Al = openmc.Material(name="Al")
Al.add_components(Al_elements, "wo")
Al.set_density("g/cm3", 2.707)

B4C_elements = {"B": 4.0, "C": 1.0}
B4C = openmc.Material(name="B4C")
B4C.add_components(B4C_elements, "ao")
B4C.set_density("g/cm3", 1.815)

Air_elements = {"N": 4.348e-5, "O": 1.087e-5}
Air = openmc.Material(name="Air")
Air.add_components(Air_elements, "ao")
Air.set_density("g/cm3", 0.001293)

Al_pure = openmc.Material(name="Al_pure")
Al_pure.add_element("Al", 1.0)
Al_pure.set_density("g/cm3", 2.699)

Pb = openmc.Material(name="Pb")
Pb.add_element("Pb", 1.0)
Pb.set_density("g/cm3", 11.35)

AmO2_Be_elements = {"Am241": 8.03e-2, "O16": 1.07e-2, "Be9": 0.909}  # 有无同位素？
AmO2_Be = openmc.Material(name="AmO2_Be Neutron Source")
AmO2_Be.add_components(AmO2_Be_elements, "wo")
AmO2_Be.set_density("g/cm3", 1.5)
AmO2_Be.add_s_alpha_beta(name="c_Be", fraction=1.0)

CH2_elements = {"C": 1.0, "H": 2.0}
CH2 = openmc.Material(name="CH2")
CH2.add_components(CH2_elements, "ao")
CH2.set_density("g/cm3", 0.95)
CH2.add_s_alpha_beta(name="c_H_in_CH2", fraction=1.0)

Cd = openmc.Material(name="Cd")
Cd.add_element("Cd", 1.0)
Cd.set_density("g/cm3", 8.65)

U = openmc.Material(name="Urinum")
U.add_nuclide("U235", 1.0)
U.set_density("g/cm3", 19.05)

UO2_elements = {"U": {"percent": 1.0, "enrichment": 19.75}, "O": 2.0}
UO2 = openmc.Material(name="UO2")
UO2.add_components(UO2_elements, "ao")
UO2.set_density("g/cm3", 19.5)  # TODO set correct density
UO2.add_s_alpha_beta(name="c_U_in_UO2", fraction=1.0)
UO2.add_s_alpha_beta(name="c_O_in_UO2", fraction=1.0)

H2O.color = (30, 144, 255)
U.color = (75, 75, 75)
UHZr.color = (85, 107, 47)
UO2.color = (0, 100, 0)
Al.color = (192, 192, 192)
Al_pure.color = (230, 230, 250)
Air.color = (135, 206, 235)
Zr.color = (173, 216, 230)
Graphite.color = (0, 0, 0)
He.color = (240, 248, 255)
SS.color = (128, 128, 128)
B4C.color = (0, 0, 139)
Pb.color = (47, 79, 79)
AmO2_Be.color = (255, 69, 0)
Cd.color = (70, 130, 180)

materials = openmc.Materials()
materials.append(UHZr)
materials.append(Zr)
materials.append(Graphite)
materials.append(He)
materials.append(SS)
materials.append(H2O)
materials.append(Al)
materials.append(B4C)
materials.append(Air)
materials.append(Al_pure)
materials.append(Pb)
materials.append(AmO2_Be)
materials.append(CH2)
materials.append(Cd)
materials.append(U)
materials.append(UO2)

if __name__ == "__main__":
    materials.export_to_xml()
