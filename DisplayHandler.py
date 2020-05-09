from AntGraph import *
import pygame
from pygame import gfxdraw


class DisplayHandler:
	def __init__(self):
		self.window = None
		self.font = None
		self.board = None

	def give_window(self, window):
		self.window = window

	def give_font(self, font):
		self.font = font


def display_test(display_x: int, display_y: int, node_radius: int, fullscreen: int = True):
	# Initialize pygame
	pygame.init()

	# Name the pygame window
	pygame.display.set_caption("display_test")

	# Create the DisplayHandler for passing pygame objects through functions
	display = DisplayHandler()

	# Create/get(?) the surface and font object, then pass them to a DisplayHandler
	if fullscreen:
		info = pygame.display.Info()
		display_x = info.current_w
		display_y = info.current_h
		window = pygame.display.set_mode((display_x, display_y), pygame.FULLSCREEN)
	else:
		window = pygame.display.set_mode((display_x, display_y))
	display.give_window(window)
	# font = pygame.font.Font("Fonts/FontomType - SkyhookMono.ttf", 18)
	font = pygame.font.SysFont("couriernew", 18)
	display.give_font(font)

	# Create the first AntGraph and hand it to the DisplayHandler
	display.board = AntGraph(display_x, display_y, node_radius)

	# Run the loop
	run(display)

	# Kill pygame
	pygame.quit()


def run(display: DisplayHandler):
	show_board(display)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
				else:
					# TODO Throw a "Generating..." splash here
					show_new_board(display)


def show_new_board(display):
	display.board = AntGraph(display.board.size_x, display.board.size_y, display.board.node_radius)
	show_board(display)


def show_board(display: DisplayHandler):
	print("Nodes: " + str(len(display.board.nodes)))
	display.window.fill((0, 43, 54))
	for edge_uid in display.board.edges:
		edge = display.board.edges[edge_uid]
		pygame.gfxdraw.line(display.window, edge.n1.x, edge.n1.y, edge.n2.x, edge.n2.y, (88, 110, 117))
	for node_uid in display.board.nodes:
		node = display.board.nodes[node_uid]
		pygame.gfxdraw.circle(display.window, node.x, node.y, display.board.node_radius, (88, 110, 117))
		pygame.gfxdraw.circle(display.window, node.x, node.y, 5, (131, 148, 150))
		text_surface = display.font.render(str(node_uid), True, (203, 75, 22))  # string, antialias, then color
		display.window.blit(text_surface, dest=(node.x, node.y))
	pygame.display.flip()  # Update the whole window
