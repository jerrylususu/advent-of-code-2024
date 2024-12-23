
with open("input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# list of tuple of connected computers
connections = []

for line in lines:
    computers = line.strip().split("-")
    connections.append((computers[0], computers[1]))

# print(connections)


graph = {}
for computer1, computer2 in connections:
    if computer1 not in graph:
        graph[computer1] = set()
    graph[computer1].add(computer2)
    if computer2 not in graph:
        graph[computer2] = set()
    graph[computer2].add(computer1)



# print(computer_to_connected_computers)

# https://oi-wiki.org/graph/max-clique/
# R := {}
# P := node set of G 
# X := {}

# algorithm BronKerbosch2(R, P, X) is
#     if P and X are both empty then
#         report R as a maximal clique
#     choose a pivot vertex u in P ⋃ X
#     for each vertex v in P \ N(u) do
#         BronKerbosch2(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
#         P := P \ {v}
#         X := X ⋃ {v}


def bron_kerbosch(graph, R, P, X, cliques):
    if not P and not X:
        cliques.append(R)
        return
    
    pivot = next(iter(P | X))
    for v in P - graph[pivot]:
        bron_kerbosch(graph, R | {v}, P & graph[v], X & graph[v], cliques)
        P = P - {v}
        X = X | {v}

def find_largest_clique(graph):
    cliques = []
    bron_kerbosch(graph, set(), set(graph.keys()), set(), cliques)
    return max(cliques, key=len)

print(",".join(sorted(list(find_largest_clique(graph)))))

