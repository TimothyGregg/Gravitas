import math
from Core.Vertex import Vertex


# TODO Type-hint
def vertex_distance(vertex1: Vertex, vertex2: Vertex):
    """
    Determine the 2D distance between two Vertices.

    Args:
        vertex1: The first Vertex in the pair.
        vertex2: The second Vertex in teh pair.

    Returns:
        The float, 2D distance between the two passed Vertices.
    """
    dx: int = vertex1.x - vertex2.x
    dy: int = vertex1.y - vertex2.y
    return math.sqrt(dx ** 2 + dy ** 2)


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar

    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end   - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()
