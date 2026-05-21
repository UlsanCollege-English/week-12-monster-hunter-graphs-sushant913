import heapq


def build_hunter_map(edges: list[tuple[str, str]]) -> dict[str, list[str]]:
    graph: dict[str, set[str]] = {}

    for start, end in edges:
        if start not in graph:
            graph[start] = set()

        if end not in graph:
            graph[end] = set()

        graph[start].add(end)
        graph[end].add(start)

    return {
        location: sorted(neighbors)
        for location, neighbors in graph.items()
    }


def build_weighted_hunter_map(
    edges: list[tuple[str, str, int]]
) -> dict[str, dict[str, int]]:

    graph: dict[str, dict[str, int]] = {}

    for start, end, weight in edges:

        if weight <= 0:
            raise ValueError

        if start not in graph:
            graph[start] = {}

        if end not in graph:
            graph[end] = {}

        current = graph[start].get(end)

        if current is None or weight < current:
            graph[start][end] = weight
            graph[end][start] = weight

    return graph


def map_summary(graph: dict[str, list[str]]) -> dict[str, int]:

    total_locations = len(graph)

    total_connections = sum(
        len(neighbors)
        for neighbors in graph.values()
    )

    total_routes = total_connections // 2

    return {
        "locations": total_locations,
        "routes": total_routes,
    }


def most_connected_location(graph: dict[str, list[str]]) -> str | None:

    if not graph:
        return None

    return min(
        graph,
        key=lambda location: (-len(graph[location]), location)
    )


def priority_hunt_order(
    reports: list[tuple[int, str]]
) -> list[str]:

    heap: list[tuple[int, str]] = []

    for priority, location in reports:
        heapq.heappush(heap, (priority, location))

    ordered: list[str] = []

    while heap:
        _, location = heapq.heappop(heap)
        ordered.append(location)

    return ordered