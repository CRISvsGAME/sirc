# SIRC

## SIRC - Digital Logic and Circuit Simulation Engine

SIRC is a lightweight, fully typed Python library for simulating digital logic
at the transistor level. It models Nodes, Devices, and Transistors and computes
stable LogicValues through fixed-point iteration and dynamic connectivity.

---

## 📦 Installation

Install from PyPI:

```bash
pip install sirc
```

Import the device simulator:

```python
from sirc.simulator import DeviceSimulator
```

---

## 🚀 Quick Start

```python
"""
CMOS Inverter Example:

                          [VDD]
                            |
                            |
                            S
                  +--| G [PMOS] D --+
                  |                 |
[INPUT]-->[PORT]--+                 +--[PORT]-->[PROBE]
                  |                 |
                  +--| G [NMOS] D --+
                            S
                            |
                            |
                          [GND]
"""

from sirc.core import LogicValue
from sirc.simulator import DeviceSimulator

sim = DeviceSimulator()

# Create Devices and Transistors
vdd = sim.create_vdd()
gnd = sim.create_gnd()

inp = sim.create_input()
probe = sim.create_probe()

inp_port = sim.create_port()
out_port = sim.create_port()

pmos = sim.create_pmos()
nmos = sim.create_nmos()

# Connect Components
sim.connect(inp.node, inp_port.node)
sim.connect(inp_port.node, pmos.gate)
sim.connect(inp_port.node, nmos.gate)
sim.connect(vdd.node, pmos.source)
sim.connect(gnd.node, nmos.source)
sim.connect(pmos.drain, out_port.node)
sim.connect(nmos.drain, out_port.node)
sim.connect(out_port.node, probe.node)

# Build Topology
sim.build_topology()

# Simulate and Sample Output
inp.set_value(LogicValue.ONE)
sim.tick()
print(repr(probe.sample()))

# Change Input and Resimulate
inp.set_value(LogicValue.ZERO)
sim.tick()
print(repr(probe.sample()))

# Expected Output:
# LogicValue.ZERO
# LogicValue.ONE
```

---

## 🔧 Features

### Core Devices

- `VDD`
- `GND`
- `Input`
- `Probe`
- `Port`

### Transistors

- `NMOS`
- `PMOS`

### Fully Typed

```python
from sirc.core import LogicValue
from sirc.simulator import DeviceSimulator
```

---

## 📂 Project Structure

```bash
src/
    sirc/
        core/
            Logic_device.py
            logic_value.py
            node.py
            transistor.py
        simulator/
            device_dep.py
            device_sim.py
stats/
    main.py
tests/
    sirc/
        core/
            test_logic_device.py
            test_logic_value.py
            test_node.py
            test_transistor.py
        simulator/
            test_device_dep.py
            test_device_sim.py
```

---

## 🧪 Testing

Run the full test suite:

```bash
pytest
```

---

## 📝 License

MIT License

---

## 🔗 Links

- PyPI: https://pypi.org/project/sirc/
- Source Code: https://github.com/CRISvsGAME/sirc
