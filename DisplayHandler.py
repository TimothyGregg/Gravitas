from AntGraph import *
import pygame
from pygame import gfxdraw


def display_test(display_x: int, display_y: int, node_radius: int):
	# Initialize pygame
	pygame.init()
	# Name the pygame window
	pygame.display.set_caption("display_test")
	# Create/get(?) the surface
	window = pygame.display.set_mode((display_x, display_y))
	# Run the loop
	run(window, node_radius)
	# Kill pygame
	pygame.quit()


def run(window: pygame.Surface, node_radius: int):
	size_x = window.get_width()
	size_y = window.get_height()
	board = AntGraph(size_x, size_y, node_radius)
	display(window, board)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
				else:
					# TODO Throw a "Generating..." splash here
					show_new_board(window, board)


def show_new_board(window, board: AntGraph):
	board = AntGraph(board.size_x, board.size_y, board.node_radius)
	display(window, board)


def display(window: pygame.Surface, board: AntGraph):
	window.fill((43, 43, 43))
	for node_uid in board.nodes:
		node = board.nodes[node_uid]
		pygame.gfxdraw.circle(window, node.x, node.y, board.node_radius, (187, 187, 187))
		pygame.gfxdraw.circle(window, node.x, node.y, 5, (187, 187, 187))
	for edge_uid in board.edges:
		edge = board.edges[edge_uid]
		pygame.gfxdraw.line(window, edge.n1.x, edge.n1.y, edge.n2.x, edge.n2.y, (187, 187, 0))
	pygame.display.flip()  # Update the whole window


display_test(display_x=1920, display_y=1080, node_radius=10)
