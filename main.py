import json

from model import SystemState
from simulation import *

from constants import *


class Collector1(Collector):

    def __init__(self, simulation_time):
        super().__init__("event_happened")
        self.simulation_time = simulation_time

        self._result = []
        self._last = IDLE

    def init(self):
        self._result.append((0, IDLE))

    def end(self):
        length = len(self._result)
        if length % 2 != 0:
            self._result.append((self.simulation_time, self._result[-1][1]))

    def reset(self):
        self._result = []

    def collect(
        self, old_state: SystemState, new_state: SystemState, event: Event
    ):
        idle = [None, None, None, None]
        if old_state.connections == idle and new_state.connections != idle:
            self._result.append((self.simulation.t, BUSY))
        elif old_state.connections != idle and new_state.connections == idle:
            self._result.append((self.simulation.t, IDLE))


class Collector2(Collector):

    def __init__(self):
        super().__init__("event_happened")

        self._result = []
        self._last = IDLE

    def init(self):
        self._result.append((0, IDLE, True))

    def end(self):
        if not self._result[-1][2]:
            self._result.append((self.simulation.t, IDLE, True))

    def reset(self):
        self._result = []

    def collect(
        self, old_state: SystemState, new_state: SystemState, event: Event
    ):
        is_regenerative = new_state.connections == [None, None, None, None]
        if (
            old_state.connections[1] is not None
            and new_state.connections[1] is None
        ):
            self._result.append((self.simulation.t, IDLE, is_regenerative))
        elif old_state.connections[1] is None and new_state.connections[
            1
        ] is not None:
            self._result.append((self.simulation.t, BUSY, is_regenerative))
        elif is_regenerative:
            self._result.append((self.simulation.t, IDLE, is_regenerative))


class CycleStopCondition(StopCondition):

    def __init__(self, total_cycles):
        self.n_total_cycles = total_cycles
        self.current_cycle = 0

    def update(self, old_state, new_state, event):
        if new_state.connections == [None, None, None, None]:
            self.current_cycle += 1

    def should_stop(self, simulation):
        return self.current_cycle >= self.n_total_cycles


def main():
    simulate_for = 100

    state = SystemState.create(n_lines=4, n_links=2)

    # Simulation 1
    n = 500
    stop_condition = TimeStopCondition(simulate_for)
    simulation = Simulation(
        state=state, stop_condition=stop_condition, progress_every=10
    )
    c1 = Collector1(simulate_for)
    simulation.add_collector(c1)
    simulation.simulate(n)

    # Simulation 2
    n = 1
    stop_condition = CycleStopCondition(500)
    simulation = Simulation(
        state=state, stop_condition=stop_condition, progress_every=10
    )
    c2 = Collector2()
    simulation.add_collector(c2)
    simulation.simulate(n)

    data = {"idle": c1.results, "link2": c2.results}

    with open("data.json", "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
