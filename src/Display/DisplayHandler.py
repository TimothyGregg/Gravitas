from GraphTypes.AntGraph import *
from GraphTypes.IncrementalGraph import *
import pygame
from pygame import gfxdraw
from typing import Tuple


BASE03 = (0, 43, 54)
BASE01 = (88, 110, 117)
BASE0 = (131, 148, 150)
BASE3 = (253, 246, 227)
ORANGE = (203, 75, 22)
RED = (220, 50, 47)
BLUE = (38, 139, 210)


class DisplayHandler:
	def __init__(self):
		self.window = None
		self.font = None
		self.board = None
		self.fullscreen = None

	def give_window(self, window):
		self.window = window

	def give_font(self, font):
		self.font = font


def pygame_wrapper(screen_size: Tuple[int, int], board: Graph, fullscreen: bool = True):
	# Initialize pygame
	pygame.init()

	# Name the pygame window
	pygame.display.set_caption("antgraph_display_test")

	# Create the DisplayHandler for passing pygame objects through functions
	display = DisplayHandler()

	# Create/get(?) the surface and font object, then pass them to a DisplayHandler
	display.fullscreen = fullscreen
	if display.fullscreen:
		info = pygame.display.Info()
		window = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN | pygame.RESIZABLE)
	else:
		window = pygame.display.set_mode((screen_size[0], screen_size[1]), pygame.RESIZABLE)

	display.give_window(window)
	# font = pygame.font.Font("Fonts/FontomType - SkyhookMono.ttf", 18)
	font = pygame.font.SysFont("couriernew", 18)
	display.give_font(font)

	# Add the board
	display.board = board

	# Run the loop
	run(display)

	# Kill pygame
	pygame.quit()


def antgraph_window(size_x: int, size_y: int, vertex_radius: int, fullscreen: bool = False, sparcity: float = 1.0):

	# Create the first GraphTypes and hand it to the pygame_wrapper
	board = AntGraph(size_x, size_y, vertex_radius, sparcity)
	pygame_wrapper((size_x, size_y), board, fullscreen)


def incremental_graph_window(size_x: int, size_y: int, vertex_radius: int, fullscreen: bool = False, sparcity: float =
1.0):

	# Create the first GraphTypes and hand it to the pygame_wrapper
	board = IncrementalGraph(size_x, size_y, vertex_radius, sparcity)
	pygame_wrapper((size_x, size_y), board, fullscreen)


def run(display: DisplayHandler):
	show_board(display)
	update_clock = 0
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
			elif event.type == pygame.VIDEORESIZE:
				# This handles resizing the graph to fit the window. Currently it stretches to fill. I think I want
				# to keep it proportional and just fit it inside the window. TODO: <-- That
				if display.fullscreen:
					display.window = pygame.display.set_mode(event.dict['size'], pygame.FULLSCREEN | pygame.RESIZABLE)
				else:
					display.window = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
				show_board(display)
		# This is where we put the update code
		if update_clock == 0:
			display.board.update()
		update_clock = (update_clock + 1) % 10
		show_board(display)


def show_new_board(display):
	if type(display.board) == AntGraph:
		display.board = AntGraph(display.window.get_width(), display.window.get_height(),
								 display.board.vertex_radius, display.board.sparcity)
	elif type(display.board) == IncrementalGraph:
		display.board = IncrementalGraph(display.window.get_width(), display.window.get_height(),
										 display.board.vertex_radius, display.board.sparcity)
	show_board(display)


def show_board(display: DisplayHandler):
	board_surface = pygame.Surface((display.board.size_x, display.board.size_y))  # Make a new surface to draw
	# everything on (to aid in resizing)
	board_surface.fill(BASE03)
	for vertex_uid in display.board.vertices:
		vertex = display.board.vertices[vertex_uid]
		# This is 2 * vertex_radius as seen by the Poisson Generator. This is the maximum spawn radius.
		pygame.gfxdraw.circle(board_surface, vertex.x, vertex.y, 4 * display.board.vertex_radius, BLUE)  # 4x radius
		# This is vertex_radius as seen by the Poisson Generator. This is the exclusion radius.
		# pygame.gfxdraw.circle(board_surface, vertex.x, vertex.y, 2 * display.board.vertex_radius, RED)  # 2x radius
		pygame.gfxdraw.circle(board_surface, vertex.x, vertex.y, display.board.vertex_radius, BASE01)  # True radius
		pygame.gfxdraw.circle(board_surface, vertex.x, vertex.y, 5, BASE0)  # Center circle
		if len(display.board.vertices) < 500:
			text_surface = display.font.render(str(vertex_uid), True, ORANGE)  # string, antialias, then color
			board_surface.blit(text_surface, dest=(vertex.x, vertex.y))  # Vertex number
	for edge_uid in display.board.edges:
		edge = display.board.edges[edge_uid]
		pygame.gfxdraw.line(board_surface, edge.v1.x, edge.v1.y, edge.v2.x, edge.v2.y, BASE3)
	display.window.blit(pygame.transform.scale(board_surface,
		(display.window.get_width(), display.window.get_height())), (0, 0))  # Add the new surface to the main window
	pygame.display.flip()  # Update the whole window
