from random import randint


class Node:
    def __init__(self, value):
        self.value = value
        self.edges = []
        self.pageRank1 = 0
        self.pageRank2 = 0

    def add_edges(self, dest):
        self.edges.append(dest)


# given url , return the node of this url from nodes list .
def get_node(url, nodes):
    for n in nodes:
        if url == n.value:
            return n
    return None


# given list of pairs , build a graph according to pairs in list .
def build_graph(listOfLists):
    extracted = []  # keep detected urls
    nodes = []
    for l in listOfLists:  # create nodes
        first_url = l[0]
        second_url = l[1]
        if first_url not in extracted:
            nodes.append(Node(first_url))
            extracted.append(first_url)
        if second_url not in extracted:
            nodes.append(Node(second_url))
            extracted.append(second_url)
    for l in listOfLists:  # create edges between nodes
        src = l[0]
        dest = l[1]
        n = get_node(src, nodes)
        n.add_edges(get_node(dest, nodes))
    return nodes


# given node , return a random node from his list .
def follow_link_step(current):
    r = randint(0, len(current.edges)-1)
    return current.edges[r]


# given a graph , return random node
def random_step(nodes):
    r = randint(0, len(nodes)-1)
    return nodes[r]


def playerPageRank(listOfLists):
    graph = build_graph(listOfLists)
    current_node = graph[randint(0, len(graph)-1)]  # initial
    page_rank_flag = True  # to detrmine first or second 100,000 iterations
    for k in range(200000):
        if k == 100000:
            page_rank_flag = False
        r = randint(1, 100)
        if r < 85 and len(current_node.edges) > 0:
            current_node = follow_link_step(current_node)
        else:
            current_node = random_step(graph)
        if page_rank_flag:
            current_node.pageRank1 += 1
        else:
            current_node.pageRank2 += 1
    result_dict = {}  # keep final results
    for n in graph:
        n.pageRank1 /= 100000
        n.pageRank2 /= 100000
        result_dict[n.value] = [n.pageRank1, n.pageRank2]
    return result_dict


