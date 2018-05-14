from math import ceil, sqrt

import numpy as np

from simulation import Simulation, TimeStopCondition, Collector, Event
from stats import make_successive_call_distribution
from model import SystemState, CallStarted


def compute_lambda(r):
    return 6 * (r / 0.05) ** 1.3


class FeeCollector(Collector):

    def __init__(self, simulation_time, rate):
        super().__init__("event_happened")
        self.simulation_time = simulation_time
        self.rate = rate

        self._started = {}
        self._result = 0

    def init(self):
        pass

    def end(self):
        pass

    def reset(self):
        self._started = {}
        self._result = 0

    def collect(
        self, old_state: SystemState, new_state: SystemState, event: Event
    ):
        if isinstance(event, CallStarted):
            self._started[event.line_id] = self.simulation.t

        for i in range(len(new_state.connections)):
            if i in self._started and new_state.connections[i] is None:
                now = self.simulation.t
                previous = self._started.pop(i)
                duration = now - previous
                self._result += duration * self.rate


def main():
    simulate_for = 100
    n = 40
    h = 2.786
    delta = 0.1
    rates = [0.05, 0.20, 0.60]

    result = []
    for rate in rates:
        stop_condition = TimeStopCondition(simulate_for)
        CallStarted.clock_function = make_successive_call_distribution(
            compute_lambda(rate)
        )

        fee_collector = FeeCollector(simulate_for, rate)
        state = SystemState.create(n_lines=4, n_links=2)
        simulation = Simulation(
            state=state, stop_condition=stop_condition, progress_every=10
        )
        simulation.add_collector(fee_collector)
        simulation.simulate(n)

        first_fees = fee_collector.results
        first_mu = np.mean(first_fees)
        first_s_n2 = np.var(first_fees, ddof=1)

        n_needed = max(n + 1, int(ceil(h ** 2 * first_s_n2 / delta ** 2)))
        n_remaining = n_needed - n

        fee_collector = FeeCollector(simulate_for, rate)
        state = SystemState.create(n_lines=4, n_links=2)
        simulation = Simulation(
            state=state, stop_condition=stop_condition, progress_every=1000
        )
        simulation.add_collector(fee_collector)
        simulation.simulate(n_remaining)

        second_fees = fee_collector.results
        second_mu = np.mean(second_fees)
        w = n / n_needed * (
            1
            + sqrt(
                1
                - n_needed
                / n
                * (1 - ((n_needed - n) * delta ** 2) / (h ** 2 * first_s_n2))
            )
        )

        estimate = w * first_mu + (1 - w) * second_mu
        result.append(estimate)

    print(result)


if __name__ == "__main__":
    main()
