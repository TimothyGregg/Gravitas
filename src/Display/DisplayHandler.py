from Ants.BoardTypes.AntBoard import *
from GraphTypes.IncrementalGraph import *
import pygame
from pygame import gfxdraw
import time
from typing import Tuple

# Some basic colors that were used early-on in debugging. They are components of the "Solarized" theme.
BASE03 = (0, 43, 54)
BASE01 = (88, 110, 117)
BASE0 = (131, 148, 150)
BASE3 = (253, 246, 227)
ORANGE = (203, 75, 22)
RED = (220, 50, 47)
BLUE = (38, 139, 210)

time_stop = 20


class DisplayHandler:
	"""
	A class for managing the pygame display process.
	"""

	def __init__(self):
		"""
		DisplayHandler constructor.
		"""

		self.window = None
		self.font = None
		self.board = None
		self.fullscreen = None

	def give_window(self, window):
		"""
		Setter for the DisplayHandler window attribute.
		Args:
			window: The window object to be set.
		"""

		self.window = window

	def give_font(self, font):
		"""
		Setter for the DisplayHandler font attribute.
		Args:
			font: The font object to be set.
		"""

		self.font = font


def pygame_wrapper(screen_size: Tuple[int, int], board: Graph, fullscreen: bool = True):
	"""
	The loop-containing method for the pygame display process.

	Args:
		screen_size: The size of the screen to display, given in positive x- and y-dimensions.
		board: The Graph object to be displayed on the screen.
		fullscreen: A boolean describing if the display should be fullscreen (True) or not (False).
	"""

	# Initialize pygame
	pygame.init()

	# Set some stuff up for displaying properly
	# pygame.mouse.set_visible(False)

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
	"""
	Window container class for easily passing a number of elements through functions. This method also creates the
	AntGraph object.

	Args:
		size_x: The maximum size of the AntBoard in the x-direction, positively from 0.
		size_y: The maximum size of the AntBoard in the y-direction, positively from 0.
		vertex_radius: The VISUAL radius of a vertex within the Board. Twice this value is the minimum distance
			between two Vertices
		fullscreen: A boolean describing if the display should be fullscreen (True) or not (False)
		sparcity: A fractional value describing the chance that, after fully generating, any given Edge will be
			deleted (assuming the Edge itself is not a bridge).
	"""

	# Create the first BoardTypes and hand it to the pygame_wrapper
	board = AntBoard(size_x, size_y, vertex_radius, sparcity)
	pygame_wrapper((size_x, size_y), board, fullscreen)


def incremental_graph_window(size_x: int, size_y: int, vertex_radius: int, fullscreen: bool = False, sparcity: float =
1.0):
	"""
	Window container class for easily passing a number of elements through functions. This method also creates the
	IncrementalGraph Object.

	Args:
		size_x: The maximum size of the AntBoard in the x-direction, positively from 0.
		size_y: The maximum size of the AntBoard in the y-direction, positively from 0.
		vertex_radius: The VISUAL radius of a vertex within the Board. Twice this value is the minimum distance
			between two Vertices
		fullscreen: A boolean describing if the display should be fullscreen (True) or not (False)
		sparcity: A fractional value describing the chance that, after fully generating, any given Edge will be
			deleted (assuming the Edge itself is not a bridge).
	"""

	# Create the first BoardTypes and hand it to the pygame_wrapper
	board = IncrementalGraph(size_x, size_y, vertex_radius, sparcity)
	pygame_wrapper((size_x, size_y), board, fullscreen)


def run(display: DisplayHandler):
	"""
	Main pygame display loop.

	Args:
		display: The DisplayHandler object that contains all of the elements for displaying the current board.
	"""

	show_board(display, display.board)
	paused = False
	# Main Loop
	while True:
		# If the mouse is clicked, crete a new board with the seed point at the mouse coordinates
		if pygame.mouse.get_pressed()[0]:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			show_new_board(display, (mouse_x, mouse_y))
		for event in pygame.event.get():
			# This handles the "close" button on the window
			if event.type == pygame.QUIT:
				return
			# If a key is pressed...
			elif event.type == pygame.KEYDOWN:
				# Escape --> quit
				if event.key == pygame.K_ESCAPE:
					return
				# Space --> pause
				if event.key == pygame.K_SPACE:
					paused = not paused
				# Any other key --> ...
				else:
					# update the board if paused
					if paused:
						update(display)
					# generate new if not paused
					else:
						# TODO Throw a "Generating..." splash here
						show_new_board(display)
			# This handles resizing the display to stretch the display to match the pygame window.
			elif event.type == pygame.VIDEORESIZE:
				# This handles resizing the graph to fit the window. Currently it stretches to fill. I think I want
				# to keep it proportional and just fit it inside the window. TODO: <-- That
				if display.fullscreen:
					display.window = pygame.display.set_mode(event.dict['size'], pygame.FULLSCREEN | pygame.RESIZABLE)
				else:
					display.window = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
				show_board(display, display.board)
		# Update the display. This handles timing currently.
		if not paused:
			update(display)


def update(display: DisplayHandler):
	"""
	Update the current display. This currently handles the timing (e.g. time between frame updates.) TODO Threading o bb

	Args:
		display: The DisplayHandler object
	"""

	updated_successfully = display.board.update()
	if updated_successfully:
		show_board(display, display.board)
		time.sleep(time_stop / 1000)  # Time stop in ms
	else:
		# display.board.get_voronoi_regions()
		time.sleep(2)
		show_new_board(display)
	pygame.display.flip()  # Update the whole window


def show_new_board(display, seed_point: Tuple[int, int] = None):
	"""
	Generate a new board within the display, with an optional seed point for the first point.
	Args:
		display: The DisplayHandler object
		seed_point: The optional argument to specify the seed point of the Poisson generator to be used for the new
		board.
	"""

	if type(display.board) == AntBoard:
		display.board = AntBoard(display.window.get_width(), display.window.get_height(),
								 display.board.vertex_radius, display.board.sparcity, seed_point)
	elif type(display.board) == IncrementalGraph:
		display.board = IncrementalGraph(display.window.get_width(), display.window.get_height(),
										 display.board.vertex_radius, display.board.sparcity, seed_point)
	show_board(display, display.board)


def show_board(display: DisplayHandler, board: Board):
	"""
	This pushes all the updates to the pygame window that allow for the display of a Graph object.

	Args:
		display: The DisplayHandler object
		board: The Board object that is being displayed.
	"""
	board_surface = pygame.Surface((board.size_x, board.size_y))  # Make a new surface to draw
	# everything on (to aid in resizing)
	board_surface.fill(BASE03)

	# Vertices
	for vertex_uid in board.vertices:
		vertex = board.vertices[vertex_uid]
		# Circles
		# This is 2 * vertex_radius as seen by the Poisson Generator. This is the maximum spawn radius.
		# pygame.gfxdraw.circle(board_surface, vertex.x, vertex.y, 4 * board.vertex_radius, BLUE)  # 4x radius
		# This is vertex_radius as seen by the Poisson Generator. This is the exclusion radius.
		# pygame.gfxdraw.circle(board_surface, vertex.x, vertex.y, 2 * board.vertex_radius, RED)  # 2x radius
		# pygame.gfxdraw.circle(board_surface, vertex.x, vertex.y, board.vertex_radius, BASE01)  # True radius
		pygame.gfxdraw.circle(board_surface, vertex.x, vertex.y, 5, (100, 100, 100))  # Center circle

		# Fun color-changing nodes based on connections (best in Incremental Graph)
		num_connected = len(board.adjacency_list[vertex_uid])
		# 8 is the max because if there are 8 connections, the Vertex is connected to all the vertices in its
		# adjacent cells in the backing grid for the generator. I think.
		# pygame.gfxdraw.filled_circle(board_surface, vertex.x, vertex.y, 5, tuple([(255 * num_connected / 8)] * 3))

		# Display the colors of the vertices if they are owned by a team
		if type(board) == AntBoard:
			for team_uid in board.teams:
				if vertex_uid in board.teams[team_uid].controlled_vertices:
					pygame.gfxdraw.filled_circle(board_surface, vertex.x, vertex.y, 20, board.teams[team_uid].color)

		# Text
		# if len(board.vertices) < 500:
		# 	# arguments are: string, antialias, then color
		# 	text_surface = display.font.render("(" + str(vertex.x) + ", " + str(vertex.y) + ")", True, ORANGE)
		# 	board_surface.blit(text_surface, dest=(vertex.x, vertex.y))  # Vertex number

	# Edges
	for edge_uid in board.edges:
		edge = board.edges[edge_uid]
		pygame.gfxdraw.line(board_surface, edge.v1.x, edge.v1.y, edge.v2.x, edge.v2.y, BASE3)

	# Center of the Graph
	pygame.gfxdraw.circle(board_surface, round(board.center.x), round(board.center.y), 7, RED)
	pygame.gfxdraw.circle(board_surface, round(board.center.x), round(board.center.y), 2, RED)

	display.window.blit(pygame.transform.scale(board_surface,
											   (display.window.get_width(), display.window.get_height())), (0, 0))  # Add the new surface to the main window

