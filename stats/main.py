"""SIRC Profiler"""

import cProfile
import pstats
from sirc.core import LogicValue, Node, VDD, GND
from sirc.simulator import DeviceSimulator


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
    inp_port = sim.create_port()
    out_port = sim.create_port()

    pmos = sim.create_pmos()
    nmos = sim.create_nmos()

    sim.connect(inp, inp_port.node)

    sim.connect(inp_port.node, pmos.gate)
    sim.connect(inp_port.node, nmos.gate)

    sim.connect(vdd.node, pmos.source)
    sim.connect(gnd.node, nmos.source)

    sim.connect(pmos.drain, out_port.node)
    sim.connect(nmos.drain, out_port.node)

    return out_port.node


def main(n: int = 1000):
    """SIRC Profiler"""
    sim = DeviceSimulator()

    vdd = sim.create_vdd()
    gnd = sim.create_gnd()

    inp = sim.create_input()
    probe = sim.create_probe()

    current_node: Node = inp.node

    for _ in range(n):
        current_node = build_inverter(sim, vdd, gnd, current_node)

    sim.connect(current_node, probe.node)

    sim.build_topology()

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
