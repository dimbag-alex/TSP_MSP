import itertools
from collections import namedtuple, defaultdict
from typing import Any, List, Tuple, Dict

import matplotlib.pyplot as plt

# Define custom types
City = Tuple[float, float]
Tour = List[City]
Result = namedtuple('Result', 'tsp, tour, cities, secs')

all_results = defaultdict(list)  # {cities: [tour, ...]}


def length(result: Result):
    return tour_length(result.tour)


def distance(A: City, B: City) -> float:
    """Distance between two cities A and B"""
    return ((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2) ** 0.5


def tour_length(tour: Tour) -> float:
    """The total distances of each link in the tour, including the link from last back to first."""
    return sum(distance(tour[i], tour[i - 1]) for i in range(len(tour)))


def shortest_links_first(cities: List[City]):
    """Return all links between cities, sorted shortest first."""
    return sorted(itertools.combinations(cities, 2), key=lambda link: distance(*link))


def mst(vertexes: List[City]) -> Dict[City, List[City]]:
    """Given a set of vertexes, build a minimum spanning tree: a dict of the form {parent: [child...]}, spanning all
    vertexes."""
    tree = {vertexes[0]: []}  # the first city is the root of the tree.
    links = shortest_links_first(vertexes)
    while len(tree) < len(vertexes):
        (A, B) = next((A, B) for (A, B) in links if (A in tree) ^ (B in tree))
        if A not in tree:
            A, B = B, A
        tree[A].append(B)
        tree[B] = []
    return tree


def preorder_traversal(tree: Dict[City, List[City]], root: City):
    """Traverse tree in pre-order, starting at root of tree."""
    yield root
    for child in tree.get(root, ()):
        yield from preorder_traversal(tree, child)


def mst_tsp(cities_coords: List[Tuple[Any, Any]], cities_names: Dict[Tuple[float, float], str]):
    """Create a minimum spanning tree and walk it in pre-order."""
    cities = list(cities_coords)
    ans = list(preorder_traversal(mst(cities), cities[0]))

    order_of_travelling_coords = [(i[0], i[1]) for i in ans]

    order_of_travelling_names = [cities_names[elem] for elem in order_of_travelling_coords]
    # plot_tour(ans, 'tour2.png')
    return order_of_travelling_coords, tour_length(ans), order_of_travelling_names, ans


def plot_tour(tour: Tour, img: str, style='bo-', hilite='rs', title=''):
    "Plot every city and link in the tour, and highlight the start city."
    scale = 1 + len(tour) ** 0.5 // 10
    plt.figure(figsize=((3 * scale, 2 * scale)))
    start = tour[0]
    plot_segment([*tour, start], style)
    plot_segment([start], hilite)
    plt.title(title)
    plt.savefig(img, format='png')
    plt.close()


def plot_segment(segment: Tour, style='bo:'):
    "Plot every city and link in the segment."
    plt.plot([c[1] for c in segment], [c[0] for c in segment], style, linewidth=2 / 3, markersize=4, clip_on=False)
    plt.axis('scaled')
    plt.axis('off')


# # Example usage
# cities_coords = [(55.75222, 37.61556), (54.5293, 36.2754), (56.1446, 40.41787), (54.9158, 37.4111)]
# cities_names = {(56.1446, 40.41787): "Vladimir", (54.5293, 36.2754): "Kaluga", (54.9158, 37.4111): "Serpukhov",
#                 (55.75222,  37.61556): "Moscow", }

# order_of_travelling_coords, total_distance, order_of_travelling_names, ans = mst_tsp(cities_coords, cities_names)
# print("Compelteon time: ")
# print("Order of travelling (coordinates):", order_of_travelling_coords)
# print("Total distance:", total_distance)
# print("Order of travelling (names):", order_of_travelling_names)

# # Plot the tour
# plot_tour(ans, 'tour.png')

# """
# "Moscow"	55.75222	37.61556
# "Vladimir"	56.1446	ч
# "Kaluga"	54.5293	36.2754
# "Serpukhov"	54.9158	37.4111
# "Tula"	54.20484	37.61849
# "Tveyr"	56.85872	35.9176
# "Ryazan"	54.60954	39.71259
# "Nizhny Novgorod"	56.2965	43.93606
# """
# {
#   "name": "Moscow",
#   "latitude": "55.75222",
#   "longitude": "37.61556"
# }
