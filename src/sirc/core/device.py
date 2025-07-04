"""
SIRC Core Device Module.

Defines the LogicDevice base class and several common logic devices: VDD, GND,
Input, Probe, and Port. A LogicDevice owns exactly one terminal Node and may
drive a single LogicValue onto that Node. LogicDevices do not perform any logic
resolution. The Simulator handles all evaluation and propagation.
"""
