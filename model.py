import copy
import random

from simulation import Env, State, Event
from stats import make_successive_call_distribution, duration_distribution


class SystemEnv(Env):
    pass


class SystemState(State):

    def __init__(self, connections, links):
        super().__init__()
        self.connections = connections
        self.links = links
        self.n_links = len(links)

    @classmethod
    def create(cls, n_lines: int, n_links: int):
        connections = [None for _ in range(n_lines)]
        links = list(range(n_links))
        return cls(connections, links)

    def __str__(self):
        connections = f"[{', '.join(str(c) for c in self.connections)}]"
        links = f"[{', '.join(str(l) for l in self.links)}]"
        return f"SystemState(connections={connections}, links={links})"

    def __copy__(self):
        connections = copy.deepcopy(self.connections)
        links = copy.deepcopy(self.links)
        state = SystemState(connections, links)
        state.n_links = self.n_links
        return state

    def possible_events(self):
        events = []

        for i in range(len(self.connections)):
            link_id = self.connections[i]
            if link_id is None:
                events.append(CallStarted(i))

        all_links = set(range(self.n_links))
        available_links = set(self.links)
        used_links = all_links - available_links
        for i in used_links:
            events.append(CallEnded(i))

        return events

    def start_call(self, line_id):
        other_line_ids = [
            i for i in range(len(self.connections)) if i != line_id
        ]
        other_line_id = random.choice(other_line_ids)
        if self.connections[other_line_id] is not None:
            return

        if not self.links:
            return

        min_i, min_link_id = min(enumerate(self.links), key=lambda p: p[1])
        self.links[min_i], self.links[-1] = self.links[-1], self.links[min_i]
        self.links.pop()

        self.connections[line_id] = min_link_id
        self.connections[other_line_id] = min_link_id

    def finish_call(self, link_id):
        for i in range(len(self.connections)):
            if self.connections[i] == link_id:
                self.connections[i] = None
        self.links.append(link_id)


class CallStarted(Event):
    clock_function = make_successive_call_distribution(6)

    def __init__(self, line_id):
        super().__init__()
        self.line_id = line_id
        self._id = f"CallStarted({self.line_id})"

    def __str__(self):
        return self._id

    def __repr__(self):
        return self._id

    @property
    def id(self):
        return self._id

    def modify_state(self, state: SystemState):
        state.start_call(self.line_id)


class CallEnded(Event):
    clock_function = duration_distribution

    def __init__(self, link_id: int):
        super().__init__()
        self.link_id = link_id
        self._id = f"CallEnded({self.link_id})"

    def __str__(self):
        return self._id

    def __repr__(self):
        return self._id

    @property
    def id(self):
        return self._id

    def modify_state(self, state: SystemState):
        state.finish_call(self.link_id)
