###############################################################################
##            To run the code in a terminal, type "python main.py"           ##
##                        Using an IDE press play/run                        ##
###############################################################################
## The Boruvka function accepts valid connected, undirected, weighted graphs ##
###############################################################################

from Graph import Graph

def plotMST(graph: Graph, mst: Graph):
    """Plots the Graph and MST using Pyplot and Networkx
    
    Code modelled from Workshop 05 model solution

    Args:
        graph (Graph): Graph to be plotted
        mst (Graph): MST of the Graph
    """
    try:
        import matplotlib.pyplot as plt
        import networkx as nx
    except:
        print("Required libraries are not installed to plot graphs.")
        return 

    # opens environments
    plt.clf()
    G = nx.Graph()

    # adding all edges to the nx Graph
    edges_all = []
    for a, b, w in graph.get_edges():
        G.add_node(a)
        G.add_node(b)
        G.add_edge(a, b, weight=w)
        edges_all.append((a, b))

    edges_route = []
    for e in mst.get_edges():
        a, b, _ = e
        edges_route.append((a, b))

    # plotting the Graph and MST
    pos = nx.spring_layout(G, k=2)
    edge_labels = dict([((u,v,), d['weight']) for u,v,d in G.edges(data=True)])
    nx.draw_networkx_nodes(G, pos, node_size=300)
    nx.draw_networkx_edges(G, pos, edgelist=edges_all, width=2, alpha=0.5, style='dashed')
    nx.draw_networkx_edges(G, pos, edgelist=edges_route, width=3, edge_color='b')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # ensuring full screen plot
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()

    plt.axis('off')
    plt.show()

def merge_sublists(lst: list, a: int, b: int) -> list:
    """Merges the sublists of lst that contain a and b
    e.g. [[1,2,3], [4,5], [6,7,8]] on 2 and 7 -> [[1,2,3,6,7,8], [4,5]]

    Args:
        lst (list): list of sublists
        a (int): value in a sublist to be merged
        b (int): value in the other sublist to be merged

    Returns:
        list: the new list of lists
    """
    merged_list = []
    temp = []
    for sublist in lst:
        if a in sublist or b in sublist:
            temp.extend(sublist)
        else:
            merged_list.append(sublist)
    if temp:
        merged_list.append(list(set(temp)))
    
    return merged_list

def edge_tiebreak(edge1: tuple, edge2: tuple) -> tuple:
    """Resolves ties where two edges have the same weight
    This avoids cycles in the resulting graph

    Args:
        edge1 (tuple): tuple of form (a,b,w) representing edge of the graph
        edge2 (tuple): tuple of form (a,b,w) representing edge of the graph

    Returns:
        tuple: either edge1 or edge2 depending on which is favoured
    """
    # unpacking the values
    v11, v12, w1 = edge1
    v21, v22, w2 = edge2
    sum1 = [v11, v12, w1]
    sum2 = [v21, v22, w2]
    # favour the edge with the highest sum 
    if sum1 >= sum2:
        return edge2
    elif sum2 > sum1:
        return edge1

def boruvka(graph: Graph) -> Graph:
    """Runs Boruvkas algorithm on the graph given, returning its MST

    Args:
        graph (Graph): the input graph, assumed to be connected, undirected and weighted

    Returns:
        Graph: the MST of the input graph
    """
    # initialising an empty MST
    mst = Graph(graph.get_vertices(), [])
    # initialising components containing just one vertex
    components = [[x] for x in graph.get_vertices()]
    iteration = 0
    print("Components on iteration {}: {}".format(iteration, components))
    while len(components) > 1:
        updated_components = components
        for i in range(len(components)):
            new_edges = []
            # looping vertices in each component to find the shortest links
            for vertex in components[i]:
                remaining_components = components[:i] + components[i+1:]
                others = [item for sublist in remaining_components for item in sublist]
                try:
                    edge = graph.get_min_edge_from_to(vertex, others)
                    new_edges += [edge]
                    v1, v2, _ = edge
                except:
                    # if no edges link from the vertex
                    pass
            
            # getting the cheapest link from this component to any other
            min_v1, min_v2, min_w = new_edges[0]
            for v1,v2,w in new_edges[1:]:
                if min_w == w:
                    # resolving in the case of a tie
                    min_v1, min_v2, min_w = edge_tiebreak((min_v1, min_v2, min_w), (v1,v2,w))
                elif w < min_w:
                    min_v1, min_v2, min_w = v1, v2, w
                else:
                    pass

            # adds the best edge to the MST
            mst.add_edge((min_v1, min_v2, min_w))
            # merge the sublists
            updated_components = merge_sublists(updated_components, min_v1, min_v2)

        # updates the components after any merges
        components = updated_components
        iteration += 1
        print("Components on iteration {}: {}".format(iteration, components))

    # printing the final MST
    print("MST edges: {}".format(mst.get_edges()))
    print("MST weight: {}".format(mst.get_total_weight()))

    return mst

def test1():
    # Arbitrary test 1
    g = Graph([1,2,3,4,5,6,7], [])
    edges = [(1,2,7), (1,4,4), (2,3,11), (2,5,10), (2,4,9), (3,5,5), (5,4,15), (5,6,12), (5,7,8), (6,4,6), (6,7,13)]
    for edge in edges:
        g.add_edge(edge)
    mst = boruvka(g)
    
    if mst.get_total_weight()==40:
        print("Weight Test Passed")
    else:
        print("Weight Test Failed")

    if mst.get_edges()==[(1, 4, 4), (2, 1, 7), (3, 5, 5), (6, 4, 6), (7, 5, 8), (2, 5, 10)]:
        print("Edge Test Passed")
    else:
        print("Edge Test Failed") 

    plotMST(g, mst)

def test2():
    # Arbitrary test 2
    # Tests the case which would cause a cycle if the tiebreaker is incorrectly applied
    g2 = Graph([1,2,3,4], [])
    edges = [(1,2,1), (2,3,1), (3,4,1), (4,1,1)]
    for edge in edges:
        g2.add_edge(edge)
    mst2 = boruvka(g2)

    if mst2.get_total_weight()==3:
        print("Weight Test Passed")
    else:
        print("Weight Test Failed")

    if mst2.get_edges()==[(1, 2, 1), (3, 2, 1), (4, 1, 1)]:
        print("Edge Test Passed")
    else:
        print("Edge Test Failed") 

    plotMST(g2, mst2)

def test3():
    # Arbitrary test 3
    g3 = Graph([0,1,2,3,4,5,6,7,8], [])
    edges = [(0,1,4),(0,7,8), (1,2,8), (1,7,11), (2,3,7), (2,8,2), (2,5,4), (3,4,9), (3,5,14), (4,5,10), (5,6,2), (6,7,1), (6,8,6), (7,8,7)]
    for edge in edges:
        g3.add_edge(edge)
    mst3 = boruvka(g3)

    if mst3.get_total_weight()==37:
        print("Weight Test Passed")
    else:
        print("Weight Test Failed")

    if mst3.get_edges()==[(0, 1, 4), (2, 8, 2), (3, 2, 7), (4, 3, 9), (5, 6, 2), (6, 7, 1), (0, 7, 8), (5, 2, 4)]:
        print("Edge Test Passed")
    else:
        print("Edge Test Failed") 

    plotMST(g3, mst3)

def main():
    # Each test function plots the Graph and MST
    # The next test will not run until the plot for the current test is closed

    print("Running Test 1")
    test1()
    print("Test 1 Complete \n")

    print("Running Test 2")
    test2()
    print("Test 2 Complete \n")

    print("Running Test 3")
    test3()
    print("Test 3 Complete \n")

if __name__=="__main__":
    main()