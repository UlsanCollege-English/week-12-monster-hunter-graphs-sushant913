# Week 12: Monster Hunter Graphs

## Student

**Name:** Sushant Thapa  
**Student ID:**2412092

---

# Summary

This assignment focuses on implementing graph data structures and graph analysis algorithms using Python 3.11.  
The project simulates a monster hunting navigation system where locations are represented as graph nodes and routes between locations are represented as graph edges.  
I created both unweighted and weighted undirected graphs to model travel paths between monster sighting areas.  
The weighted graph stores danger scores for each route, allowing hunters to determine safer paths during exploration missions.  
In addition, I implemented graph utility functions that calculate graph statistics, identify the most connected location, and organize urgent monster reports using a heap-based priority queue.  
The most challenging part of the assignment was correctly handling duplicate weighted routes while maintaining the minimum danger score efficiently.

---

# Graph Structure

## Unweighted Graph

The unweighted graph uses an adjacency list representation.

Example:

```python
{
    "Old Theater": ["Train Station", "Hospital"],
    "Train Station": ["Old Theater"]
}
```

### Features

- Undirected graph
- Bidirectional connections
- Duplicate routes prevented
- Efficient neighbor lookup

---

## Weighted Graph

The weighted graph uses nested dictionaries.

Example:

```python
{
    "Old Theater": {
        "Train Station": 4,
        "Hospital": 7
    }
}
```

### Features

- Stores danger scores
- Supports duplicate edge replacement
- Preserves minimum route danger
- Fast edge access

---

# Approach

## `build_hunter_map`

### Strategy

- Used adjacency lists to store graph relationships.
- Used Python sets internally to remove duplicate neighbors automatically.
- Added edges in both directions because the graph is undirected.
- Converted sets into sorted lists before returning final output.

### Important Concepts

- Graph adjacency lists
- Undirected edges
- Set operations
- Dictionary manipulation

---

## `build_weighted_hunter_map`

### Strategy

- Used nested dictionaries to store weighted routes.
- Validated all danger scores before insertion.
- Raised `ValueError` if any score was zero or negative.
- Preserved the smallest danger score for duplicate routes.

### Important Concepts

- Weighted graphs
- Input validation
- Nested dictionaries
- Route optimization

---

## `map_summary`

### Strategy

- Counted locations using dictionary length.
- Counted all adjacency connections.
- Divided total edge references by two because undirected graphs store both directions.

### Important Concepts

- Graph traversal
- Edge counting
- Degree analysis

---

## `most_connected_location`

### Strategy

- Traversed every graph node.
- Compared node degrees using neighbor counts.
- Used alphabetical ordering to resolve ties.

### Important Concepts

- Node degree
- Tie-breaking
- Sorting logic

---

## `priority_hunt_order`

### Strategy

- Used Python’s `heapq` module.
- Inserted all reports into a min-heap.
- Removed reports in ascending priority order.

### Important Concepts

- Heap data structures
- Priority queues
- Greedy extraction

---

# Complexity Analysis

## `build_hunter_map`

### Time Complexity

```text
O(E log V)
```

### Space Complexity

```text
O(V + E)
```

### Explanation

Each edge is processed once.  
Sorting neighbor lists introduces logarithmic overhead.

---

## `build_weighted_hunter_map`

### Time Complexity

```text
O(E)
```

### Space Complexity

```text
O(V + E)
```

### Explanation

Dictionary insertion and lookup operations run in constant average time.

---

## `map_summary`

### Time Complexity

```text
O(V + E)
```

### Space Complexity

```text
O(1)
```

### Explanation

The function traverses all adjacency lists exactly once.

---

## `most_connected_location`

### Time Complexity

```text
O(V)
```

### Space Complexity

```text
O(1)
```

### Explanation

Each location is checked one time.

---

## `priority_hunt_order`

### Time Complexity

```text
O(N log N)
```

### Space Complexity

```text
O(N)
```

### Explanation

Heap insertion and removal require logarithmic time complexity.

---

# Edge-Case Checklist

The following edge cases were tested and handled correctly:

- [x] Empty graph
- [x] Single location graph
- [x] One route
- [x] Duplicate routes
- [x] Duplicate weighted routes
- [x] Disconnected locations
- [x] Tie for most connected location
- [x] Positive weighted routes
- [x] Invalid zero danger score
- [x] Invalid negative danger score
- [x] Empty priority report list
- [x] Large graph input
- [x] Alphabetical tie-breaking

---

# Example Usage

## Example 1 — Building a Hunter Map

```python
routes = [
    ("Old Theater", "Train Station"),
    ("Train Station", "Hospital"),
    ("Hospital", "City Hall")
]

graph = build_hunter_map(routes)

print(graph)
```

### Output

```python
{
    'Old Theater': ['Train Station'],
    'Train Station': ['Hospital', 'Old Theater'],
    'Hospital': ['City Hall', 'Train Station'],
    'City Hall': ['Hospital']
}
```

---

## Example 2 — Building a Weighted Hunter Map

```python
weighted_routes = [
    ("Old Theater", "Train Station", 4),
    ("Train Station", "Hospital", 7),
    ("Hospital", "City Hall", 2)
]

graph = build_weighted_hunter_map(weighted_routes)

print(graph)
```

### Output

```python
{
    'Old Theater': {'Train Station': 4},
    'Train Station': {
        'Old Theater': 4,
        'Hospital': 7
    },
    'Hospital': {
        'Train Station': 7,
        'City Hall': 2
    },
    'City Hall': {
        'Hospital': 2
    }
}
```

---

# Testing

## Test Command

```bash
pytest -q
```

## Test Result

```text
12 passed in 0.04s
```

---

# Challenges Faced

One challenge was understanding how undirected graphs duplicate edge references internally.  
Another challenge was correctly preserving the minimum weighted route when duplicate routes appeared in the weighted graph.  
Using `heapq` also required understanding how Python min-heaps automatically maintain ordering.  
Testing edge cases such as empty graphs and invalid danger scores helped improve the robustness and reliability of the final implementation.

---

# What I Learned

Through this assignment, I improved my understanding of:

- Graph theory fundamentals
- Adjacency list representations
- Weighted graph structures
- Heap-based priority queues
- Time and space complexity analysis
- Edge-case testing
- Python type hints
- Efficient dictionary usage

I also strengthened my problem-solving skills and learned how graph algorithms are applied in real-world systems such as transportation, mapping, gaming, and network routing.

---

# Assistance & Sources

## AI Usage

**Yes**

### AI helped with:

- Reviewing graph algorithms
- Improving readability
- Verifying complexity analysis
- Checking edge-case handling
- Improving documentation quality

---

## Other Sources

- Python 3.11 Official Documentation
- `heapq` Documentation
- Class lecture slides
- GeeksforGeeks graph tutorials
- Python typing documentation

---

# Final Reflection

This project gave me practical experience implementing real graph-based systems using Python.  
I learned how weighted and unweighted graphs can model navigation and route systems efficiently.  
The assignment also improved my understanding of data structures, algorithm efficiency, and software design principles.  
By completing this project, I became more confident working with graphs, heaps, and complexity analysis in Python programming.