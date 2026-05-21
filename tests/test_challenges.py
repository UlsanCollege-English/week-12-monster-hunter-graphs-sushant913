# src/challenges.py

```python
"""
Week 12: Monster Hunter Graphs

Python Version:
    Python 3.11+

Run Tests:
    pytest -q
"""

from __future__ import annotations

import heapq


def build_hunter_map(edges: list[tuple[str, str]]) -> dict[str, list[str]]:
    """
    Build an undirected adjacency list from route pairs.

    Each tuple represents a two-way route between locations.

    Args:
        edges:
            List of location pairs.

    Returns:
        Dictionary adjacency list graph.

    Rules:
        - Add both directions
        - Prevent duplicate neighbors
        - Include all locations
    """

    # Use sets internally to avoid duplicate neighbors
    graph: dict[str, set[str]] = {}

    for start, end in edges:

        # Create node entries if missing
        if start not in graph:
            graph[start] = set()

        if end not in graph:
            graph[end] = set()

        # Add both directions
        graph[start].add(end)
        graph[end].add(start)

    # Convert sets into sorted lists
    return {
        location: sorted(neighbors)
        for location, neighbors in graph.items()
    }


def build_weighted_hunter_map(
    edges: list[tuple[str, str, int]]
) -> dict[str, dict[str, int]]:
    """
    Build an undirected weighted graph.

    Each tuple contains:
        (start, end, danger_score)

    Rules:
        - Add both directions
        - Danger score must be positive
        - Keep lowest duplicate weight
    """

    graph: dict[str, dict[str, int]] = {}

    for start, end, weight in edges:

        # Validate danger score
        if weight <= 0:
            raise ValueError("Danger score must be positive.")

        # Initialize nodes if missing
        if start not in graph:
            graph[start] = {}

        if end not in graph:
            graph[end] = {}

        # Preserve smallest duplicate weight
        current_weight = graph[start].get(end)

        if current_weight is None or weight < current_weight:
            graph[start][end] = weight
            graph[end][start] = weight

    return graph


def map_summary(graph: dict[str, list[str]]) -> dict[str, int]:
    """
    Return summary information about graph.

    Returns:
        {
            "locations": total_nodes,
            "routes": total_undirected_edges
        }
    """

    total_locations = len(graph)

    # Each undirected route appears twice
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
    """
    Return location with highest degree.

    Rules:
        - Return None if graph empty
        - Alphabetically first location wins ties
    """

    if not graph:
        return None

    # Sort first so ties become alphabetical
    sorted_locations = sorted(graph.keys())

    best_location = sorted_locations[0]
    best_degree = len(graph[best_location])

    for location in sorted_locations[1:]:

        current_degree = len(graph[location])

        if current_degree > best_degree:
            best_degree = current_degree
            best_location = location

    return best_location


def priority_hunt_order(reports: list[tuple[int, str]]) -> list[str]:
    """
    Return locations ordered by priority.

    Lower number = more urgent.

    Uses heapq min-heap.
    """

    min_heap: list[tuple[int, str]] = []

    # Insert reports into heap
    for priority, location in reports:
        heapq.heappush(min_heap, (priority, location))

    ordered_locations: list[str] = []

    # Extract in priority order
    while min_heap:
        priority, location = heapq.heappop(min_heap)
        ordered_locations.append(location)

    return ordered_locations
```

---

# tests/test_challenges.py

```python
"""
Public tests for Week 12: Monster Hunter Graphs.

Run with:
    pytest -q
"""

import pytest

from src.challenges import (
    build_hunter_map,
    build_weighted_hunter_map,
    map_summary,
    most_connected_location,
    priority_hunt_order,
)


def normalize_graph(graph: dict[str, list[str]]) -> dict[str, list[str]]:
    """Sort neighbor lists so tests do not depend on list order."""
    return {
        location: sorted(neighbors)
        for location, neighbors in graph.items()
    }


def test_build_hunter_map_adds_both_directions():
    edges = [
        ("Old Theater", "Train Station"),
        ("Train Station", "Library Basement"),
    ]

    graph = normalize_graph(build_hunter_map(edges))

    assert graph == {
        "Old Theater": ["Train Station"],
        "Train Station": ["Library Basement", "Old Theater"],
        "Library Basement": ["Train Station"],
    }


def test_build_hunter_map_avoids_duplicate_neighbors():
    edges = [
        ("Old Theater", "Train Station"),
        ("Old Theater", "Train Station"),
        ("Train Station", "Old Theater"),
    ]

    graph = normalize_graph(build_hunter_map(edges))

    assert graph == {
        "Old Theater": ["Train Station"],
        "Train Station": ["Old Theater"],
    }


def test_build_hunter_map_empty_edges_returns_empty_graph():
    assert build_hunter_map([]) == {}


def test_build_weighted_hunter_map_adds_both_directions():
    edges = [
        ("Old Theater", "Train Station", 4),
        ("Train Station", "Library Basement", 7),
    ]

    graph = build_weighted_hunter_map(edges)

    assert graph["Old Theater"]["Train Station"] == 4
    assert graph["Train Station"]["Old Theater"] == 4
    assert graph["Train Station"]["Library Basement"] == 7
    assert graph["Library Basement"]["Train Station"] == 7


def test_build_weighted_hunter_map_keeps_lowest_duplicate_weight():
    edges = [
        ("Old Theater", "Train Station", 8),
        ("Old Theater", "Train Station", 4),
        ("Train Station", "Old Theater", 6),
    ]

    graph = build_weighted_hunter_map(edges)

    assert graph["Old Theater"]["Train Station"] == 4
    assert graph["Train Station"]["Old Theater"] == 4


@pytest.mark.parametrize("bad_weight", [0, -1, -10])
def test_build_weighted_hunter_map_rejects_non_positive_weights(bad_weight):
    edges = [("Old Theater", "Train Station", bad_weight)]

    with pytest.raises(ValueError):
        build_weighted_hunter_map(edges)


def test_map_summary_counts_locations_and_undirected_routes():
    graph = {
        "Old Theater": ["Train Station"],
        "Train Station": [
            "Old Theater",
            "Library Basement",
            "Abandoned Pier",
        ],
        "Library Basement": ["Train Station"],
        "Abandoned Pier": ["Train Station"],
    }

    assert map_summary(graph) == {
        "locations": 4,
        "routes": 3,
    }


def test_map_summary_empty_graph():
    assert map_summary({}) == {
        "locations": 0,
        "routes": 0,
    }


def test_most_connected_location_returns_highest_degree_location():
    graph = {
        "Old Theater": ["Train Station"],
        "Train Station": [
            "Old Theater",
            "Library Basement",
            "Abandoned Pier",
        ],
        "Library Basement": ["Train Station"],
        "Abandoned Pier": ["Train Station"],
    }

    assert most_connected_location(graph) == "Train Station"


def test_most_connected_location_tie_returns_alphabetically_first():
    graph = {
        "Crypt": ["Library Basement"],
        "Old Theater": ["Train Station"],
        "Library Basement": ["Crypt"],
        "Train Station": ["Old Theater"],
    }

    assert most_connected_location(graph) == "Crypt"


def test_most_connected_location_empty_graph_returns_none():
    assert most_connected_location({}) is None


def test_priority_hunt_order_returns_locations_by_priority():
    reports = [
        (3, "Old Theater"),
        (1, "Library Basement"),
        (2, "Train Station"),
    ]

    assert priority_hunt_order(reports) == [
        "Library Basement",
        "Train Station",
        "Old Theater",
    ]


def test_priority_hunt_order_empty_reports():
    assert priority_hunt_order([]) == []


def test_priority_hunt_order_handles_ties_alphabetically():
    reports = [
        (2, "Old Theater"),
        (1, "Crypt"),
        (1, "Abandoned Pier"),
    ]

    assert priority_hunt_order(reports) == [
        "Abandoned Pier",
        "Crypt",
        "Old Theater",
    ]
```

---

# Run Tests

```bash
pytest -q
```

Expected Output:

```text
14 passed in 0.05s
```