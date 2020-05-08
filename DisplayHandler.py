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
	window.fill((43, 43, 43))
	for node in board.nodes:
		pygame.gfxdraw.circle(window, node.x, node.y, node_radius, (187, 187, 187))
		pygame.gfxdraw.circle(window, node.x, node.y, 5, (187, 187, 187))
	pygame.display.flip()  # Update the whole window
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
				else:
					# TODO Throw a "Generating..." splash here
					board = AntGraph(size_x, size_y, node_radius)
					window.fill((43, 43, 43))
					for node in board.nodes:
						pygame.gfxdraw.circle(window, node.x, node.y, node_radius, (187, 187, 187))
						pygame.gfxdraw.circle(window, node.x, node.y, 5, (187, 187, 187))
					pygame.display.flip()  # Update the whole window


display_test(display_x=1920, display_y=1080, node_radius=20)