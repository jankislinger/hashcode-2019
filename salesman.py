from ortools.constraint_solver import pywrapcp

from inout import transition_value, read, evaluate_slideshow, write
from verticals import prepare_slides

M = 100


def create_distance_callback(photos):
    r = range(len(photos))
    weights = {(i, j): M - transition_value(photos[i], photos[j]) if i != j else 0 for i in r for j in r}

    def distance_callback(i, j):
        return weights[(i, j)]

    return distance_callback


def salesman(photos, verbose=False):
    # Cities
    tsp_size = len(photos)

    num_routes = 1
    depot = 0

    # Create routing model
    routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
    # Create the distance callback.
    dist_callback = create_distance_callback(photos)
    routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    if not assignment:
        return None

    value = tsp_size * M - assignment.ObjectiveValue()
    index = routing.Start(0)  # Index of the variable for the starting node.

    route = []
    # TODO: vybrat chytrejc, kteoru hranu vyhodit
    while not routing.IsEnd(index):
        route.append(index)
        index = assignment.Value(routing.NextVar(index))

    if verbose:
        print("Total value: " + str(value))
        print("Route:\n" + '->'.join(str(i) for i in route))

    return [photos[i] for i in route], value


def split_into_groups(length, max_len):
    return [(i, i + max_len) for i in range(0, length, max_len)]


def main(data_size, k):
    photos = prepare_slides(read(f"data/{data_size}.txt"))
    n = len(photos)
    slideshow = []
    for i, j in split_into_groups(n, k):
        subslideshow, value = salesman(photos[i:j], True)
        print(evaluate_slideshow(subslideshow))
        slideshow += subslideshow
        print(f"{j} / {n} slides done")
    print(evaluate_slideshow(slideshow))
    write(slideshow, data_size)

    print(data_size)


if __name__ == '__main__':
    main()
