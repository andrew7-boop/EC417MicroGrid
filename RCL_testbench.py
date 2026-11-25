from pathlib import Path
import pytest
import typhoon.api.hil as hil
from typhoon.api.schematic_editor import model as mdl
from typhoon.test.capture import start_capture, get_capture_results
import matplotlib.pyplot as plt
import plotly.express as px

TSE = Path(r"C:\Users\jesse\Documents\SchoolDocs\ec417\Project\RLC_Sim.tse")
CPD = TSE.parent / f"{TSE.stem} Target files" / f"{TSE.stem}.cpd"
print("Does this work?")
#@pytest.fixture(scope="module", autouse=True)
def setup_model():  
    print("Setting up model...")
    mdl.load(str(TSE))
    rin = mdl.get_item("Rin")
    mdl.set_property_value(mdl.prop(rin, "resistance"), 50.0)
    print(mdl.get_property_value(mdl.prop(rin, "resistance")))
    ok = mdl.compile()
    assert ok is not False, "Compile failed - check the Schematic Editor messages"
    assert CPD.exists(), f"Compiled file not found: {CPD}"
    hil.load_model(file=str(CPD), offlineMode=False, vhil_device=True)
    mdl.save()
    #yield
    #hil.stop_simulation()
setup_model()
from typhoon.api.hil.exception import HILAPIException



def capture_waveform():
    hil.start_simulation()
    start_capture(duration = 0.005,rate = 10000, signals = ["Va1"])
    capture = get_capture_results(wait_capture=True)
    hil.stop_simulation()
    print(capture)
    return capture

df =capture_waveform()
#v = cap["Va1"]
##t = len(v,axis=0)
#plt.plot(t,v)
plot_df = df.reset_index()
plot_df["time_ms"] = plot_df["time"].dt.total_seconds() * 1000

fig = px.line(
    plot_df,
    x="time_ms",
    y="Va1",
    title="Va1 Waveform",
    labels={"time_ms": "Time (ms)", "Va1": "Amplitude (Va1)"},
)

