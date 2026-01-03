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
from sirc.simulator.device import DeviceSimulator
```

---

## 🚀 Quick Start

```python
from sirc.simulator.device import DeviceSimulator
from sirc.core.logic import LogicValue
from sirc.core.transistor import NMOS, PMOS
from sirc.core.device import VDD, GND, Input, Probe, Port

sim = DeviceSimulator()

# Create Devices and Transistors
vdd = VDD()
gnd = GND()

inp = Input()
probe = Probe()

inp_port = Port()
out_port = Port()

pmos = PMOS()
nmos = NMOS()

# Register Devices and Transistors
sim.register_devices([vdd, gnd, inp, probe, inp_port, out_port])
sim.register_transistors([pmos, nmos])

# Connect Components
sim.connect(inp.terminal, inp_port.terminal)
sim.connect(inp_port.terminal, pmos.gate)
sim.connect(inp_port.terminal, nmos.gate)
sim.connect(vdd.terminal, pmos.source)
sim.connect(gnd.terminal, nmos.source)
sim.connect(pmos.drain, out_port.terminal)
sim.connect(nmos.drain, out_port.terminal)
sim.connect(out_port.terminal, probe.terminal)

# Simulate and Sample Output
inp.set_value(LogicValue.ONE)
sim.build_topology()
sim.tick()
print(repr(probe.sample()))

# Change Input and Resimulate
inp.set_value(LogicValue.ZERO)
sim.build_topology()
sim.tick()
print(repr(probe.sample()))
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
from sirc.simulator.device import DeviceSimulator
from sirc.core.logic import LogicValue
from sirc.core.node import Node
from sirc.core.device import LogicDevice, VDD, GND, Input, Probe, Port
from sirc.core.transistor import Transistor, NMOS, PMOS
```

---

## 📂 Project Structure

```bash
src/
    sirc/
        core/
            device.py
            logic.py
            node.py
            transistor.py
        simulator/
            device.py
stats/
    main.py
tests/
    sirc/
        core/
            test_device.py
            test_logic.py
            test_node.py
            test_transistor.py
        simulator/
            test_device.py
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
