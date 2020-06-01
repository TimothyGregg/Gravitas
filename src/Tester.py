from Display.DisplayHandler import *

antgraph_window(size_x=1920, size_y=1080, vertex_radius=50, fullscreen=False, sparcity=0.7)
# for _ in range(100):
# 	test = AntBoard(200, 200, 5, 1.0)
	# test.get_voronoi_regions()
# print(AntBoard(1920, 1080, 50, 1.0))

incremental_graph_window(size_x=1080, size_y=720, vertex_radius=25, fullscreen=True, sparcity=1.0)

# 5 is too small
# 10 is neat
# 2560 x 1440, node radius = 30 --> ~500 Nodes
# pyinstaller --onefile Tester.py
