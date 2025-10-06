"""SIRC Profiler"""

import cProfile
import pstats
from sirc.core.logic import LogicValue
from sirc.core.node import Node
from sirc.core.device import VDD, GND, Input, Probe, Port
from sirc.core.transistor import NMOS, PMOS
from sirc.simulator.device import DeviceSimulator


def build_inverter(
    sim: DeviceSimulator,
    vdd: VDD,
    gnd: GND,
    inp: Node,
) -> Node:
    """
    Build one CMOS inverter.

    Args:
        sim: DeviceSimulator
        vdd: Shared VDD rail
        gnd: Shared GND rail
        inp: Node driving this inverter

    Returns:
        out: Node driven by this inverter
    """
    inp_port = Port()
    out_port = Port()

    pmos = PMOS()
    nmos = NMOS()

    sim.register_devices([inp_port, out_port])
    sim.register_transistors([pmos, nmos])

    sim.connect(inp, inp_port.terminal)

    sim.connect(inp_port.terminal, pmos.gate)
    sim.connect(inp_port.terminal, nmos.gate)

    sim.connect(vdd.terminal, pmos.source)
    sim.connect(gnd.terminal, nmos.source)

    sim.connect(pmos.drain, out_port.terminal)
    sim.connect(nmos.drain, out_port.terminal)

    return out_port.terminal


def main(n: int = 1000):
    """SIRC Profiler"""
    sim = DeviceSimulator()

    vdd = VDD()
    gnd = GND()

    inp = Input()
    probe = Probe()

    sim.register_devices([vdd, gnd, inp, probe])

    current_node: Node = inp.terminal

    for _ in range(n):
        current_node = build_inverter(sim, vdd, gnd, current_node)

    sim.connect(current_node, probe.terminal)

    inp.set_value(LogicValue.ONE)
    sim.tick()
    print("Input = 1 → Output =", probe.sample())

    inp.set_value(LogicValue.ZERO)
    sim.tick()
    print("Input = 0 → Output =", probe.sample())


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()
    pstats.Stats(profiler).sort_stats("cumtime").print_stats()
