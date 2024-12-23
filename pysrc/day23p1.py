
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
        graph[computer1] = []
    graph[computer1].append(computer2)
    if computer2 not in graph:
        graph[computer2] = []
    graph[computer2].append(computer1)

# print(computer_to_connected_computers)

set_of_3s = set()
for a in graph:
    for b in graph[a]:
        if b > a:
            for c in graph[b]:
                if c > b and c in graph[a]:
                    set_of_3s.add(tuple(sorted([a, b, c])))

# print(set_of_3s)
print("len of set of 3", len(set_of_3s))

begin_with_t = 0
for s in set_of_3s:
    if any([i[0] == "t" for i in s]):
        begin_with_t += 1
    

print(begin_with_t)