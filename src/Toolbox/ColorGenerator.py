from typing import Tuple
import random


color_dict = {
	(26, 22, 22): "Background",
	(100, 100, 100): "Graph",
	"Fun": {
		(45, 15, 245): "Dad Purple",
		(255, 69, 0): "Orangered",
		(0, 255, 255): "Cyan",
		(124, 252, 0): "Lawn Green",
		(138, 43, 226): "Blue Violet"
	}
}


class ColorGenerator:
	def __init__(self):
		# Set of checked-out colors for easy checked-out-ness checking
		self.checked_out = set()

		# Set of all available colors
		self.available_colors = set()
		# Build the available_colors set
		# Iterate through the different color sets
		for set_key in color_dict:
			# If the color set contains a dict (i.e. it isn't just a single color
			if type(set_key) == str:
				# Iterate through each of the color tuples found in the color set and add them all to available_colors
				for color_tuple in color_dict[set_key]:
					self.available_colors.add(color_tuple)

	def checkout(self, color_rgb: Tuple[int, int, int]):
		if color_rgb in self.checked_out:
			raise RuntimeError("Color \"" + lookup(color_rgb) + "\" already checked out")
		self.checked_out.add(color_rgb)
		self.available_colors.remove(color_rgb)
		return color_rgb

	def request(self):
		selection = random.sample(self.available_colors, 1)[0]
		self.checkout(selection)
		return selection


def lookup(color_rgb: Tuple[int, int, int]):
	# Iterate through the different color sets
	for set_key in color_dict:
		# If the color set contains a dict (i.e. it isn't just a single color)
		if type(set_key) == str:
			# Iterate through the different colors in the set to find the color name associated with the rgb values
			try:
				return color_dict[set_key[color_rgb]]
			except KeyError:
				pass
	return "Unknown Color"


c = ColorGenerator()
print(c.request())
