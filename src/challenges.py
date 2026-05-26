from math import inf
import heapq


HAUNTED_CITY = {
    "Crypt Kitchen": {
        "Fog Alley": 2,
        "Bone Bridge": 5,
    },
    "Fog Alley": {
        "Moon Bridge": 1,
        "Goblin Market": 6,
    },
    "Bone Bridge": {
        "Goblin Market": 2,
    },
    "Moon Bridge": {
        "Werewolf Den": 5,
        "Goblin Market": 3,
    },
    "Goblin Market": {
        "Vampire Tower": 5,
    },
    "Werewolf Den": {
        "Vampire Tower": 2,
    },
    "Vampire Tower": {},
}


def validate_haunted_map(graph: dict[str, dict[str, int]]) -> None:

    if not isinstance(graph, dict):
        raise ValueError("Graph must be a dictionary.")

    for node, neighbors in graph.items():

        if not isinstance(neighbors, dict):
            raise ValueError(
                f"Neighbors for '{node}' must be a dictionary."
            )

        for neighbor, weight in neighbors.items():

            if neighbor not in graph:
                raise ValueError(
                    f"Neighbor '{neighbor}' does not exist."
                )

            if weight <= 0:
                raise ValueError(
                    "Edge weights must be positive."
                )


def monster_delivery_costs(
    graph: dict[str, dict[str, int]],
    start: str,
) -> dict[str, float]:

    validate_haunted_map(graph)

    if start not in graph:
        raise ValueError("Start location missing.")

    distances = {
        node: inf for node in graph
    }

    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:

        current_cost, current_node = heapq.heappop(
            priority_queue
        )

        if current_cost > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():

            new_cost = current_cost + weight

            if new_cost < distances[neighbor]:

                distances[neighbor] = new_cost

                heapq.heappush(
                    priority_queue,
                    (new_cost, neighbor)
                )

    return distances


def shortest_monster_delivery(
    graph: dict[str, dict[str, int]],
    start: str,
    target: str,
) -> tuple[float, list[str]]:

    validate_haunted_map(graph)

    if start not in graph or target not in graph:
        return (inf, [])

    if start == target:
        return (0, [start])

    distances = {
        node: inf for node in graph
    }

    distances[start] = 0

    previous_nodes = {}

    priority_queue = [(0, start)]

    while priority_queue:

        current_cost, current_node = heapq.heappop(
            priority_queue
        )

        if current_cost > distances[current_node]:
            continue

        if current_node == target:
            break

        for neighbor, weight in graph[current_node].items():

            new_cost = current_cost + weight

            if new_cost < distances[neighbor]:

                distances[neighbor] = new_cost

                previous_nodes[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_cost, neighbor)
                )

    if distances[target] == inf:
        return (inf, [])

    path = []

    current = target

    while current != start:

        path.append(current)

        current = previous_nodes[current]

    path.append(start)

    path.reverse()

    return (distances[target], path)


def best_next_monster_stop(
    graph: dict[str, dict[str, int]],
    start: str,
    targets: list[str],
) -> tuple[str, float]:

    validate_haunted_map(graph)

    if start not in graph:
        return ("", inf)

    distances = monster_delivery_costs(
        graph,
        start
    )

    best_target = ""
    best_cost = inf

    for target in targets:

        if target not in distances:
            continue

        current_cost = distances[target]

        if current_cost < best_cost:

            best_cost = current_cost
            best_target = target

    return (best_target, best_cost)