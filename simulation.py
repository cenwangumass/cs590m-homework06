from heapq import heappush, heappop
from typing import Iterable, Optional, TypeVar, ClassVar, List, Set
import copy

ENV = TypeVar("ENV", bound="Env")
STATE = TypeVar("STATE", bound="State")
EVENT = TypeVar("EVENT", bound="Event")


class Env(object):
    pass


class Event(object):
    clock_function = None
    env = ClassVar[Optional[ENV]]

    def __init__(self, t=0) -> None:
        self._t = t
        self._cancelled = False

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, t):
        self._t = t

    def __lt__(self, other):
        return self.t < other.t

    @property
    def id(self):
        raise NotImplementedError()

    def countdown(self):
        return self.__class__.clock_function()

    def modify_state(self, state: STATE):
        raise NotImplementedError()

    def cancel(self):
        self._cancelled = True

    @property
    def cancelled(self):
        return self._cancelled


class State(object):
    env = ClassVar[Optional[ENV]]

    def __copy__(self):
        raise NotImplementedError()

    def possible_events(self) -> Iterable[Event]:
        raise NotImplementedError()


class EventQueue(object):

    def __init__(self) -> None:
        self._events = []

    def schedule(self, t, event: EVENT):
        event.t = t
        heappush(self._events, event)

    def next(self) -> EVENT:
        while True:
            event = heappop(self._events)
            if not event.cancelled:
                return event

    def cancel(self, event: EVENT):
        for e in self._events:
            if e.id == event.id:
                e.cancel()


def get_new_events(old_possible_events, new_possible_events, trigger_event):
    new_events = []
    old_possible_event_ids = {
        event.id
        for event in old_possible_events
        if event.id != trigger_event.id
    }
    for event in new_possible_events:
        if event.id not in old_possible_event_ids:
            new_events.append(event)
    return new_events


def get_cancelled_events(
    old_state: "State", new_state: "State", trigger_event: Event
):
    old_possible_events = old_state.possible_events()
    new_possible_events = new_state.possible_events()

    new_possible_event_ids = {event.id for event in new_possible_events}

    cancelled_events = []
    for event in old_possible_events:
        if (
            event.id not in new_possible_event_ids
            and event.id != trigger_event.id
        ):
            cancelled_events.append(event)

    return cancelled_events


def stop_after(desired_time):

    def f(current_time):
        return current_time > desired_time

    return f


class StopCondition(object):

    def should_stop(self, simulation) -> bool:
        raise NotImplementedError()

    def update(self, old_state, new_state, event):
        raise NotImplementedError()


class TimeStopCondition(StopCondition):

    def __init__(self, duration) -> None:
        self.duration = duration

    def should_stop(self, simulation):
        return simulation.t > self.duration

    def update(self, old_state, new_state, event):
        pass


class Collector(object):

    def __init__(self, trigger_on=None) -> None:
        self.simulation = None
        self.trigger_on = trigger_on

        self._result = None
        self._results = []

    def init(self):
        raise NotImplementedError()

    def end(self):
        raise NotImplementedError()

    def set_simulation(self, simulation):
        self.simulation = simulation

    def reset(self):
        raise NotImplementedError()

    def save_result(self):
        self._results.append(self._result)

    @property
    def results(self):
        return self._results

    def collect(self, old_state: STATE, new_state: STATE, event: EVENT):
        raise NotImplementedError()


class Simulation(object):

    def __init__(
        self, state: STATE, stop_condition: StopCondition, progress_every=1000
    ) -> None:
        self.state = state
        self.stop_condition = stop_condition
        self.progress_every = progress_every

        self.t = 0

        self.collectors = {}

        self.results = []

    def _reset_time(self):
        self.t = 0

    def _simulate(self):
        self.t = 0
        state = copy.copy(self.state)

        result = {}
        events = EventQueue()

        for event in state.possible_events():
            future_at = self.t + event.countdown()
            events.schedule(future_at, event)
        # print(
        #     f'T: {self.t}, '
        #     f'event scheduled: {event}, '
        #     f'will happen at T: {future_at}'
        # )

        while True:
            old_state = copy.copy(state)

            event = events.next()
            self.t = event.t

            if self.stop_condition.should_stop(self):
                break

            event.modify_state(state)

            for collector in self.collectors["event_happened"]:
                collector.collect(old_state, state, event)

            # print(f'T: {self.t}, '
            #       f'event happened: {event}, '
            #       f'old state: {old_state}, '
            #       f'new state: {state}')

            self.stop_condition.update(old_state, state, event)

            new_events = get_new_events(
                old_state.possible_events(), state.possible_events(), event
            )
            for event in new_events:
                future_at = self.t + event.countdown()
                events.schedule(future_at, event)
                # print(f'T: {self.t}, '
                #       f'event scheduled: {event}, '
                #       f'will happen at T: {future_at}')

            cancelled_events = get_cancelled_events(old_state, state, event)
            for event in cancelled_events:
                events.cancel(event)

        return result

    def add_collector(self, collector):
        collector.set_simulation(self)

        if collector.trigger_on not in self.collectors:
            self.collectors[collector.trigger_on] = []
        self.collectors[collector.trigger_on].append(collector)

    def _before_simulation(self):
        for trigger in self.collectors:
            for collector in self.collectors[trigger]:
                collector.reset()
                collector.init()

    def _after_simulation(self):
        for trigger in self.collectors:
            for collector in self.collectors[trigger]:
                collector.end()
                collector.save_result()

    def simulate(self, n=1):
        for i in range(n):
            if i % self.progress_every == 0:
                print(f"{i / n * 100:.2f}%")

            self._reset_time()
            self._before_simulation()
            result = self._simulate()
            self._after_simulation()
        # self.results.append(result)

        print(f"{100:.2f}%")

        return self.results
