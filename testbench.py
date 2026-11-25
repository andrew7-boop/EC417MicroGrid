import pytest
import typhoon.api.hil as hil
from typhoon.api.schematic_editor import model
#import typhoontest.api as tt
import typhoon.test.capture as capture
import typhoon.test.signals as signals
import typhoon.test.ranges as ranges

@pytest.fixture(scope="module")
def setup_simulation():
    # 1. Load and compile the schematic for TyphoonSim (Virtual HIL)
    model.load("RLC_Sim.tse")
    model.compile()
    
    # 2. Load the compiled model into TyphoonSim
    hil.load_model(file="RLC_Sim Target files/RLC_Sim.cpd", offlineMode=True)
    hil.start_simulation()
    
    yield
    
    # 3. Teardown after all tests complete
    hil.stop_simulation()

def test_dc_bus_voltage_regulation(setup_simulation):
    # Apply stimulus
    hil.set_source_constant_value(name="V_dc", value=400.0)
    hil.wait(0.5)  # Allow transient to settle
    
    # Capture signal and assert against criteria
    capture = tt.capture.start_capture(duration=0.1, signals=["V_out"])
    df = capture.get_data()
    
    # Verify signal stays within tolerance using TyphoonTest assertions
    hil.asserts.is_within(df["V_out"], lower=395.0, upper=405.0)
