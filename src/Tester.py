from Display.DisplayHandler import *

antgraph_window(size_x=1920, size_y=1080, vertex_radius=25, fullscreen=False, sparcity=1.0)
test = AntGraph(200, 200, 5, 1.0).get_voronoi_regions()
# incremental_graph_window(size_x=1920, size_y=1080, vertex_radius=25, fullscreen=False, sparcity=1.0)
# 5 is too small
# 10 is neat
# 2560 x 1440, node radius = 30 --> ~500 Nodes
# pyinstaller --onefile Tester.py
