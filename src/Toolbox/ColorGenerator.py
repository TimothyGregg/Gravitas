from typing import Tuple
import random


color_dict = {
	(26, 22, 22): "Background",
	(100, 100, 100): "Graph",
	"Fun": {
		(45, 15, 245): "Dad Purple",
		(255, 69, 0): "Orangered",
		(0, 255, 255): "Cyan",
		(100, 100, 100): "Fake Neutral",
		(26, 22, 22): "Void",
		(124, 252, 0): "Lawn Green",
		(138, 43, 226): "Blue Violet"
	},
	"OG Color Map": {
		(38, 139, 210): "Blue",
		(211, 54, 130): "Pink",
		(59, 178, 63): "Green",
		(203, 75, 22): "Orange",
		(167, 81, 240): "Purple",
		(171, 191, 0): "Yellow"
	},
	"Red": {
		(255, 160, 122): "Light Salmon",
		(250, 128, 114): "Salmon",
		(233, 150, 122): "Dark Salmon",
		(240, 128, 128): "Light Coral",
		(205, 92, 92): "Indian Red",
		(220, 20, 60): "Crimson",
		(178, 34, 34): "Firebrick",
		(255, 0, 0): "Red",
		(139, 0, 0): "Dark Red"
	},
	"Orange": {
		(255, 127, 80): "Coral",
		(255, 99, 71): "Tomato",
		(255, 69, 0): "Orangered",
		(255, 215, 0): "Gold",
		(255, 165, 0): "Orange",
		(255, 140, 0): "Dark Orange"
	},
	"Yellow": {
		(255, 255, 224): "Light Yellow",
		(255, 250, 205): "Lemon Chiffon",
		(250, 250, 210): "Light Goldenrod Yellow",
		(255, 239, 213): "Papaya Whip",
		(255, 228, 181): "Moccasin",
		(255, 218, 185): "Peachpuff",
		(238, 232, 170): "Pale Goldenrod",
		(240, 230, 140): "Khaki",
		(189, 183, 107): "Dark Khaki",
		(255, 255, 0): "Yellow"
	},
	"Green": {
		(124, 252, 0): "Lawn Green",
		(127, 255, 0): "Chartreuse",
		(50, 205, 50): "Lime Green",
		(0, 255, 0): "Lime",
		(34, 139, 34): "Forest Green",
		(0, 128, 0): "Green",
		(0, 100, 0): "Dark Green",
		(173, 255, 47): "Green-yellow",
		(154, 205, 50): "Yellow-green",
		(0, 255, 127): "Spring Green",
		(0, 250, 154): "Medium Spring Green",
		(144, 238, 144): "Light Green",
		(152, 251, 152): "Pale Green",
		(143, 188, 143): "Dark Sea Green",
		(60, 179, 113): "Medium Sea Green",
		(46, 139, 87): "Sea Green",
		(128, 128, 0): "Olive",
		(85, 107, 47): "Dark Olive Green",
		(107, 142, 35): "Olive Drab"
	},
	"Cyan": {
		(224, 255, 255): "Light Cyan",
		(0, 255, 255): "Cyan",
		(0, 255, 255): "Aqua",
		(127, 255, 212): "Aquamarine",
		(102, 205, 170): "Medium Aquamarine",
		(175, 238, 238): "Pale Turquoise",
		(64, 224, 208): "Turquoise",
		(72, 209, 204): "Medium Turquoise",
		(0, 206, 209): "Dark Turquoise",
		(32, 178, 170): "Light Sea Green",
		(95, 158, 160): "Cadet Blue",
		(0, 139, 139): "Dark Cyan",
		(0, 128, 128): "Teal"
	},
	"Blue": {
		(176, 224, 230): "Powder Blue",
		(173, 216, 230): "Light Blue",
		(135, 206, 250): "Light Sky Blue",
		(135, 206, 235): "Sky Blue",
		(0, 191, 255): "Deep Sky Blue",
		(176, 196, 222): "Light Steel Blue",
		(30, 144, 255): "Dodger Blue",
		(100, 149, 237): "Cornflower Blue",
		(70, 130, 180): "Steel Blue",
		(65, 105, 225): "Royal Blue",
		(0, 0, 255): "Blue",
		(0, 0, 205): "Medium Blue",
		(0, 0, 139): "Dark Blue",
		(0, 0, 128): "Navy",
		(25, 25, 112): "Midnight Blue",
		(123, 104, 238): "Medium Slate Blue",
		(106, 90, 205): "Slate Blue",
		(72, 61, 139): "Dark Slate Blue"
	},
	"Purple": {
		(230, 230, 250): "Lavender",
		(216, 191, 216): "Thistle",
		(221, 160, 221): "Plum",
		(238, 130, 238): "Violet",
		(218, 112, 214): "Orchid",
		(255, 0, 255): "Fuchsia",
		(255, 0, 255): "Magenta",
		(186, 85, 211): "Medium Orchid",
		(147, 112, 219): "Medium Purple",
		(138, 43, 226): "Blue Violet",
		(148, 0, 211): "Dark Violet",
		(153, 50, 204): "Dark Orchid",
		(139, 0, 139): "Dark Magenta",
		(128, 0, 128): "Purple",
		(75, 0, 130): "Indigo"
	},
	"Pink": {
		(255, 192, 203): "Pink",
		(255, 182, 193): "Light Pink",
		(255, 105, 180): "Hot Pink",
		(255, 20, 147): "Deep Pink",
		(219, 112, 147): "Pale Violet Red",
		(199, 21, 133): "Medium Violet Red"
	},
	"White": {
		(255, 255, 255): "White",
		(255, 250, 250): "Snow",
		(240, 255, 240): "Honeydew",
		(245, 255, 250): "Mint Cream",
		(240, 255, 255): "Azure",
		(240, 248, 255): "Alice Blue",
		(248, 248, 255): "Ghost White",
		(245, 245, 245): "White Smoke",
		(255, 245, 238): "Seashell",
		(245, 245, 220): "Beige",
		(253, 245, 230): "Old Lace",
		(255, 250, 240): "Floral White",
		(255, 255, 240): "Ivory",
		(250, 235, 215): "Antique White",
		(250, 240, 230): "Linen",
		(255, 240, 245): "Lavender Blush",
		(255, 228, 225): "Misty Rose"
	},
	"Grey": {
		(220, 220, 220): "Gainsboro",
		(211, 211, 211): "Light Gray",
		(192, 192, 192): "Silver",
		(169, 169, 169): "Dark Gray",
		(128, 128, 128): "Gray",
		(105, 105, 105): "Dim Gray",
		(119, 136, 153): "Light slate Gray",
		(112, 128, 144): "Slate Gray",
		(47, 79, 79): "Dark Slate Gray",
		(0, 0, 0): "Black"
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

	# Return a boolean describing if the ColorGenerator has more colors to give
	def has_more(self):
		return len(self.available_colors) > 0

	# Record that a color has been requested and used from the ColorGenerator
	def checkout(self, color_rgb: Tuple[int, int, int]):
		if color_rgb in self.checked_out:
			raise RuntimeError("Color \"" + lookup(color_rgb) + "\" already checked out")
		self.checked_out.add(color_rgb)
		self.available_colors.remove(color_rgb)

	# Ask the ColorGenerator for a new color
	# TODO This assumes that the generator has_more(). Maybe set up validation?
	def request(self):
		# Return the fun colors first
		if len(self.checked_out) < 7:
			selection = random.choice(list(color_dict["Fun"].keys()))
			while selection in self.checked_out:
				selection = random.choice(list(color_dict["Fun"].keys()))
			self.checkout(selection)
			return selection
		# If we've placed all the fun colors already, place the rest
		else:
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
				return color_dict[set_key][color_rgb]
			except KeyError:
				pass
	return "Unknown Color"


def temp_parse(string: str):
	start = 0
	start_brace = string.find("{", start)
	while start_brace != -1:
		end_brace = string.find("}", start_brace)
		start_quote = string.find("\"", start)
		end_quote = string.find("\"", start_quote + 1)
		print("\t\t(" + string[start_brace + 1:end_brace] + "): " + string[start_quote:end_quote + 1] + ",")
		start = end_quote + 1
		start_brace = string.find("{", start)


c = ColorGenerator()
while c.has_more():
	t = c.request()
	print(str(t) + ":" + (int((16 - len(str(t)) + 2) / 4) + 1) * "\t" + lookup(t))
