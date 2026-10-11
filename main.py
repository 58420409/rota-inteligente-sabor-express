from __future__ import annotations
import csv
import heapq
import math
from collections import deque
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_data():
    nodes_raw = read_csv(DATA / "nodes.csv")
    edges_raw = read_csv(DATA / "edges.csv")
    deliveries = read_csv(DATA / "deliveries.csv")
    nodes = {r["id"]: {
        "name": r["name"], "x": float(r["x_km"]), "y": float(r["y_km"]),
        "type": r["type"]
    } for r in nodes_raw}
    graph = {node_id: [] for node_id in nodes}
    edge_info = {}
    for row in edges_raw:
        a, b = row["source"], row["target"]
        distance, minutes = float(row["distance_km"]), float(row["time_min"])
        graph[a].append((b, minutes, distance))
        graph[b].append((a, minutes, distance))
        edge_info[frozenset((a,b))] = (minutes, distance)
    return nodes, graph, edge_info, deliveries

def euclidean(nodes, a, b):
    dx = nodes[a]["x"] - nodes[b]["x"]
    dy = nodes[a]["y"] - nodes[b]["y"]
    return math.hypot(dx, dy)

def heuristic(nodes, a, b):
    # Estimativa conservadora: 2 minutos por km em linha reta.
    return euclidean(nodes, a, b) * 2.0

def reconstruct_path(parent, goal):
    if goal not in parent and parent.get(goal) is None:
        return [goal]
    path, cur = [], goal
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    return list(reversed(path))

def astar(graph, nodes, start, goal):
    frontier = [(heuristic(nodes, start, goal), 0.0, start)]
    parent = {start: None}
    best_g = {start: 0.0}
    while frontier:
        _, g, current = heapq.heappop(frontier)
        if g > best_g.get(current, float("inf")):
            continue
        if current == goal:
            return reconstruct_path(parent, goal), g
        for neighbor, minutes, _ in graph[current]:
            new_g = g + minutes
            if new_g < best_g.get(neighbor, float("inf")):
                best_g[neighbor] = new_g
                parent[neighbor] = current
                heapq.heappush(frontier, (new_g + heuristic(nodes, neighbor, goal), new_g, neighbor))
    return [], float("inf")

def bfs(graph, start, goal):
    queue = deque([start])
    parent = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            return reconstruct_path(parent, goal)
        for neighbor, _, _ in graph[current]:
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)
    return []

def dfs(graph, start, goal):
    stack = [start]
    parent = {start: None}
    while stack:
        current = stack.pop()
        if current == goal:
            return reconstruct_path(parent, goal)
        for neighbor, _, _ in reversed(graph[current]):
            if neighbor not in parent:
                parent[neighbor] = current
                stack.append(neighbor)
    return []

def path_cost(path, edge_info):
    minutes, km = 0.0, 0.0
    for a, b in zip(path, path[1:]):
        m, d = edge_info[frozenset((a,b))]
        minutes += m
        km += d
    return minutes, km

def nearest_neighbor_order(graph, nodes, edge_info, depot, stop_ids):
    remaining = set(stop_ids)
    current = depot
    order = []
    total_minutes = total_km = 0.0
    while remaining:
        candidates = []
        for stop in remaining:
            path, minutes = astar(graph, nodes, current, stop)
            candidates.append((minutes, stop, path))
        minutes, stop, path = min(candidates, key=lambda x: (x[0], x[1]))
        _, km = path_cost(path, edge_info)
        total_minutes += minutes
        total_km += km
        order.append(stop)
        remaining.remove(stop)
        current = stop
    path, minutes = astar(graph, nodes, current, depot)
    _, km = path_cost(path, edge_info)
    total_minutes += minutes
    total_km += km
    return order, total_minutes, total_km

def draw_graph(nodes, graph):
    fig, ax = plt.subplots(figsize=(9, 6))
    for a, neighbors in graph.items():
        for b, minutes, _ in neighbors:
            if a < b:
                ax.plot([nodes[a]["x"], nodes[b]["x"]], [nodes[a]["y"], nodes[b]["y"]], linewidth=1.5)
                mx = (nodes[a]["x"] + nodes[b]["x"]) / 2
                my = (nodes[a]["y"] + nodes[b]["y"]) / 2
                ax.text(mx, my, f"{minutes:.0f} min", fontsize=8, bbox=dict(facecolor="white", alpha=.7, edgecolor="none"))
    for node_id, info in nodes.items():
        ax.scatter(info["x"], info["y"], s=90, marker="s" if node_id == "D" else "o")
        ax.annotate(f"{node_id}: {info['name']}", (info["x"], info["y"]), xytext=(5,5), textcoords="offset points", fontsize=8)
    ax.set_title("Grafo viário sintético — Sabor Express")
    ax.set_xlabel("Coordenada X (km, fictícia)")
    ax.set_ylabel("Coordenada Y (km, fictícia)")
    ax.grid(True, alpha=.25)
    fig.tight_layout()
    fig.savefig(OUT / "graph.png", dpi=160)
    plt.close(fig)

def cluster_deliveries(nodes, deliveries):
    coords = [[float(d["x_km"]), float(d["y_km"])] for d in deliveries]
    k = min(3, len(deliveries))
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(coords)
    assigned = []
    for row, label in zip(deliveries, labels):
        assigned.append({**row, "cluster": int(label)})
    return assigned, model

def draw_clusters(assigned, model):
    fig, ax = plt.subplots(figsize=(8, 6))
    labels = sorted(set(int(row["cluster"]) for row in assigned))
    for label in labels:
        rows = [r for r in assigned if int(r["cluster"]) == label]
        ax.scatter([float(r["x_km"]) for r in rows],
                   [float(r["y_km"]) for r in rows], s=100, label=f"Zona {label + 1}")
        for row in rows:
            ax.annotate(row["node_id"], (float(row["x_km"]), float(row["y_km"])),
                        xytext=(4,4), textcoords="offset points")
    ax.scatter(model.cluster_centers_[:,0], model.cluster_centers_[:,1],
               marker="X", s=180, label="Centroides")
    ax.set_title("Agrupamento de entregas por K-Means (dados sintéticos)")
    ax.set_xlabel("Coordenada X (km, fictícia)")
    ax.set_ylabel("Coordenada Y (km, fictícia)")
    ax.grid(True, alpha=.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "clusters.png", dpi=160)
    plt.close(fig)

def write_csv(path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    nodes, graph, edge_info, deliveries = load_data()
    draw_graph(nodes, graph)

    # Comparação de busca para um par de referência: depósito -> Hospital.
    comparison = []
    for method, path in [
        ("A*", astar(graph, nodes, "D", "H")[0]),
        ("BFS", bfs(graph, "D", "H")),
        ("DFS", dfs(graph, "D", "H")),
    ]:
        minutes, km = path_cost(path, edge_info) if path else (float("inf"), float("inf"))
        comparison.append({
            "method": method,
            "path": " -> ".join(path),
            "estimated_time_min": round(minutes, 2),
            "estimated_distance_km": round(km, 2),
            "note": "A* minimizes weighted time; BFS/DFS are references and do not optimize weighted cost."
        })

    assigned, model = cluster_deliveries(nodes, deliveries)
    draw_clusters(assigned, model)
    write_csv(OUT / "cluster_assignments.csv", assigned,
              ["delivery_id", "node_id", "x_km", "y_km", "priority", "cluster"])

    route_summaries = []
    for cluster in sorted(set(int(r["cluster"]) for r in assigned)):
        stop_ids = [r["node_id"] for r in assigned if int(r["cluster"]) == cluster]
        order, minutes, km = nearest_neighbor_order(graph, nodes, edge_info, "D", stop_ids)
        route_summaries.append({
            "zone": cluster + 1,
            "stops": len(stop_ids),
            "delivery_order": " -> ".join(["D"] + order + ["D"]),
            "estimated_time_min": round(minutes, 2),
            "estimated_distance_km": round(km, 2),
            "estimated_time_per_stop_min": round(minutes / len(stop_ids), 2) if stop_ids else 0
        })
    write_csv(OUT / "routes_summary.csv", route_summaries,
              ["zone", "stops", "delivery_order", "estimated_time_min",
               "estimated_distance_km", "estimated_time_per_stop_min"])
    write_csv(OUT / "search_comparison.csv", comparison,
              ["method", "path", "estimated_time_min", "estimated_distance_km", "note"])

    print("Projeto executado com sucesso.")
    print(f"Entregas analisadas: {len(deliveries)}")
    print(f"Zonas K-Means: {len(set(int(r['cluster']) for r in assigned))}")
    print("\nComparação de busca: depósito (D) -> Hospital (H)")
    for row in comparison:
        print(f"- {row['method']}: {row['path']} | {row['estimated_time_min']} min | {row['estimated_distance_km']} km")
    print("\nResumo das zonas:")
    for row in route_summaries:
        print(f"- Zona {row['zone']}: {row['stops']} paradas | {row['estimated_time_min']} min | {row['estimated_distance_km']} km | ordem: {row['delivery_order']}")
    print(f"\nArquivos gerados em: {OUT}")

if __name__ == "__main__":
    main()
