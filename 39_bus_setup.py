from pathlib import Path
import typhoon.api.hil as hil
from typhoon.api.schematic_editor import model as mdl

TSE = Path(r"test.tse")
CPD = TSE.parent / f"{TSE.stem} Target files" / f"{TSE.stem}.cpd"
mdl.create_new_model(str(TSE))
print("Does this work?")

src = mdl.create_component("core/Voltage Source", name="V1", position=(8000, 8000))
tl  = mdl.create_component("core/Transmission Line", name="TL1", position=(8300, 8600))
rl  = mdl.create_component("core/Resistor", name="Rload", position=(8600, 8000))
gnd = mdl.create_component("core/Ground", name="GND", position=(8300, 8300))
bus1 = mdl.create_component("core/Three-phase Meter", name="Meter1", position=(9000, 8200))


mdl.set_property_value(mdl.prop(rl,"resistance"),100.0)
mdl.set_property_value(mdl.prop(tl,"model"),"PI")
print(mdl.get_property_values(tl))   # find the real property names, then set them below
# e.g. mdl.set_property_value(mdl.prop(tl, "<phases property>"), 1)

t = mdl.term
mdl.create_connection(t(src, "p_node"), t(tl, "a_in"))
mdl.create_connection(t(tl, "a_out"),  t(rl, "p_node"))
mdl.create_connection(t(rl, "n_node"), t(gnd, "node"))
mdl.create_connection(t(src, "n_node"), t(gnd, "node"))
# only if Model = PI:
mdl.create_connection(t(tl, "gnd"), t(gnd, "node"))

mdl.save_as(str(TSE))
print("Saved:", TSE, TSE.exists())

def create_bus(busNum):
    pass