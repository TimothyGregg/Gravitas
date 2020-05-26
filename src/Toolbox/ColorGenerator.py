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
		print("(" + string[start_brace + 1:end_brace] + "): " + string[start_quote:end_quote + 1])
		start = end_quote + 1
		start_brace = string.find("{", start)


c = ColorGenerator()
print(lookup(c.request()))

temp_parse("""tempMap.put(new int[]{45, 15, 245},   "Dad Purple");
    tempMap.put(new int[]{255, 69, 0},    "Orangered");
    tempMap.put(new int[]{0, 255, 255},   "Cyan");
    // tempMap.put(GRAPHCOLOR, "Fake Neutral");
    // tempMap.put(BGCOLOR,    "Void");
    tempMap.put(new int[]{124, 252, 0},   "Lawn Green");
    tempMap.put(new int[]{138, 43, 226},  "Blue Violet");
    funColorMap = tempMap;

    tempMap = new HashMap<>();
    tempMap.put(new int[]{38, 139, 210},  "Blue");
    tempMap.put(new int[]{211, 54, 130},  "Pink");
    tempMap.put(new int[]{59, 178, 63},   "Green");
    tempMap.put(new int[]{203, 75, 22},   "Orange");
    tempMap.put(new int[]{167, 81, 240},  "Purple");
    tempMap.put(new int[]{171, 191, 0},   "Yellow");
    OGColorMap = tempMap;

    //Red
    tempMap = new HashMap<>();
    tempMap.put(new int[]{255, 160, 122}, "Light Salmon");
    tempMap.put(new int[]{250, 128, 114}, "Salmon");
    tempMap.put(new int[]{233, 150, 122}, "Dark Salmon");
    tempMap.put(new int[]{240, 128, 128}, "Light Coral");
    tempMap.put(new int[]{205, 92, 92},   "Indian Red");
    tempMap.put(new int[]{220, 20, 60},   "Crimson");
    tempMap.put(new int[]{178, 34, 34},   "Firebrick");
    tempMap.put(new int[]{255, 0, 0},     "Red");
    tempMap.put(new int[]{139, 0, 0},     "Dark Red");
    colorMaps.add(tempMap);
    numColors += tempMap.size();

    //Orange
    tempMap = new HashMap<>();
    tempMap.put(new int[]{255, 127, 80},  "Coral");
    tempMap.put(new int[]{255, 99, 71},   "Tomato");
    tempMap.put(new int[]{255, 69, 0},    "Orangered");
    tempMap.put(new int[]{255, 215, 0},   "Gold");
    tempMap.put(new int[]{255, 165, 0},   "Orange");
    tempMap.put(new int[]{255, 140, 0},   "Dark Orange");
    colorMaps.add(tempMap);
    numColors += tempMap.size();

    //Yellow
    tempMap = new HashMap<>();
    tempMap.put(new int[]{255, 255, 224}, "Light Yellow");
    tempMap.put(new int[]{255, 250, 205}, "Lemon Chiffon");
    tempMap.put(new int[]{250, 250, 210}, "Light Goldenrod Yellow");
    tempMap.put(new int[]{255, 239, 213}, "Papaya Whip");
    tempMap.put(new int[]{255, 228, 181}, "Moccasin");
    tempMap.put(new int[]{255, 218, 185}, "Peachpuff");
    tempMap.put(new int[]{238, 232, 170}, "Pale Goldenrod");
    tempMap.put(new int[]{240, 230, 140}, "Khaki");
    tempMap.put(new int[]{189, 183, 107}, "Dark Khaki");
    tempMap.put(new int[]{255, 255, 0},   "Yellow");
    colorMaps.add(tempMap);
    numColors += tempMap.size();

    //Green
    tempMap = new HashMap<>();
    tempMap.put(new int[]{124, 252, 0},   "Lawn Green");
    tempMap.put(new int[]{127, 255, 0},   "Chartreuse");
    tempMap.put(new int[]{50, 205, 50},   "Lime Green");
    tempMap.put(new int[]{0, 255, 0},     "Lime");
    tempMap.put(new int[]{34, 139, 34},   "Forest Green");
    tempMap.put(new int[]{0, 128, 0},     "Green");
    tempMap.put(new int[]{0, 100, 0},     "Dark Green");
    tempMap.put(new int[]{173, 255, 47},  "Green-yellow");
    tempMap.put(new int[]{154, 205, 50},  "Yellow-green");
    tempMap.put(new int[]{0, 255, 127},   "Spring Green");
    tempMap.put(new int[]{0, 250, 154},   "Medium Spring Green");
    tempMap.put(new int[]{144, 238, 144}, "Light Green");
    tempMap.put(new int[]{152, 251, 152}, "Pale Green");
    tempMap.put(new int[]{143, 188, 143}, "Dark Sea Green");
    tempMap.put(new int[]{60, 179, 113},  "Medium Sea Green");
    tempMap.put(new int[]{46, 139, 87},   "Sea Green");
    tempMap.put(new int[]{128, 128, 0},   "Olive");
    tempMap.put(new int[]{85, 107, 47},   "Dark Olive Green");
    tempMap.put(new int[]{107, 142, 35},  "Olive Drab");
    colorMaps.add(tempMap);
    numColors += tempMap.size();

    //Cyan
    tempMap = new HashMap<>();
    tempMap.put(new int[]{224, 255, 255}, "Light Cyan");
    tempMap.put(new int[]{0, 255, 255},   "Cyan");
    tempMap.put(new int[]{0, 255, 255},   "Aqua");
    tempMap.put(new int[]{127, 255, 212}, "Aquamarine");
    tempMap.put(new int[]{102, 205, 170}, "Medium Aquamarine");
    tempMap.put(new int[]{175, 238, 238}, "Pale Turquoise");
    tempMap.put(new int[]{64, 224, 208},  "Turquoise");
    tempMap.put(new int[]{72, 209, 204},  "Medium Turquoise");
    tempMap.put(new int[]{0, 206, 209},   "Dark Turquoise");
    tempMap.put(new int[]{32, 178, 170},  "Light Sea Green");
    tempMap.put(new int[]{95, 158, 160},  "Cadet Blue");
    tempMap.put(new int[]{0, 139, 139},   "Dark Cyan");
    tempMap.put(new int[]{0, 128, 128},   "Teal");
    colorMaps.add(tempMap);
    numColors += tempMap.size();

    //Blue
    tempMap = new HashMap<>();
    tempMap.put(new int[]{176, 224, 230}, "Powder Blue");
    tempMap.put(new int[]{173, 216, 230}, "Light Blue");
    tempMap.put(new int[]{135, 206, 250}, "Light Sky Blue");
    tempMap.put(new int[]{135, 206, 235}, "Sky Blue");
    tempMap.put(new int[]{0, 191, 255},   "Deep Sky Blue");
    tempMap.put(new int[]{176, 196, 222}, "Light Steel Blue");
    tempMap.put(new int[]{30, 144, 255},  "Dodger Blue");
    tempMap.put(new int[]{100, 149, 237}, "Cornflower Blue");
    tempMap.put(new int[]{70, 130, 180},  "Steel Blue");
    tempMap.put(new int[]{65, 105, 225},  "Royal Blue");
    tempMap.put(new int[]{0, 0, 255},     "Blue");
    tempMap.put(new int[]{0, 0, 205},     "Medium Blue");
    tempMap.put(new int[]{0, 0, 139},     "Dark Blue");
    tempMap.put(new int[]{0, 0, 128},     "Navy");
    tempMap.put(new int[]{25, 25, 112},   "Midnight Blue");
    tempMap.put(new int[]{123, 104, 238}, "Medium Slate Blue");
    tempMap.put(new int[]{106, 90, 205},  "Slate Blue");
    tempMap.put(new int[]{72, 61, 139},   "Dark Slate Blue");
    colorMaps.add(tempMap);
    numColors += tempMap.size();

    //Purple
    tempMap = new HashMap<>();
    tempMap.put(new int[]{230, 230, 250}, "Lavender");
    tempMap.put(new int[]{216, 191, 216}, "Thistle");
    tempMap.put(new int[]{221, 160, 221}, "Plum");
    tempMap.put(new int[]{238, 130, 238}, "Violet");
    tempMap.put(new int[]{218, 112, 214}, "Orchid");
    tempMap.put(new int[]{255, 0, 255},   "Fuchsia");
    tempMap.put(new int[]{255, 0, 255},   "Magenta");
    tempMap.put(new int[]{186, 85, 211},  "Medium Orchid");
    tempMap.put(new int[]{147, 112, 219}, "Medium Purple");
    tempMap.put(new int[]{138, 43, 226},  "Blue Violet");
    tempMap.put(new int[]{148, 0, 211},   "Dark Violet");
    tempMap.put(new int[]{153, 50, 204},  "Dark Orchid");
    tempMap.put(new int[]{139, 0, 139},   "Dark Magenta");
    tempMap.put(new int[]{128, 0, 128},   "Purple");
    tempMap.put(new int[]{75, 0, 130},    "Indigo");
    colorMaps.add(tempMap);
    numColors += tempMap.size();

    //Pink
    tempMap = new HashMap<>();
    tempMap.put(new int[]{255, 192, 203}, "Pink");
    tempMap.put(new int[]{255, 182, 193}, "Light Pink");
    tempMap.put(new int[]{255, 105, 180}, "Hot Pink");
    tempMap.put(new int[]{255, 20, 147},  "Deep Pink");
    tempMap.put(new int[]{219, 112, 147}, "Pale Violet Red");
    tempMap.put(new int[]{199, 21, 133},  "Medium Violet Red");
    colorMaps.add(tempMap);
    numColors += tempMap.size();

    //White
    tempMap = new HashMap<>();
    tempMap.put(new int[]{255, 255, 255}, "White");
    tempMap.put(new int[]{255, 250, 250}, "Snow");
    tempMap.put(new int[]{240, 255, 240}, "Honeydew");
    tempMap.put(new int[]{245, 255, 250}, "Mint Cream");
    tempMap.put(new int[]{240, 255, 255}, "Azure");
    tempMap.put(new int[]{240, 248, 255}, "Alice Blue");
    tempMap.put(new int[]{248, 248, 255}, "Ghost White");
    tempMap.put(new int[]{245, 245, 245}, "White Smoke");
    tempMap.put(new int[]{255, 245, 238}, "Seashell");
    tempMap.put(new int[]{245, 245, 220}, "Beige");
    tempMap.put(new int[]{253, 245, 230}, "Old Lace");
    tempMap.put(new int[]{255, 250, 240}, "Floral White");
    tempMap.put(new int[]{255, 255, 240}, "Ivory");
    tempMap.put(new int[]{250, 235, 215}, "Antique White");
    tempMap.put(new int[]{250, 240, 230}, "Linen");
    tempMap.put(new int[]{255, 240, 245}, "Lavender Blush");
    tempMap.put(new int[]{255, 228, 225}, "Misty Rose");
    colorMaps.add(tempMap);
    numColors += tempMap.size();

    //Grey
    tempMap = new HashMap<>();
    tempMap.put(new int[]{220, 220, 220}, "Gainsboro");
    tempMap.put(new int[]{211, 211, 211}, "Light Gray");
    tempMap.put(new int[]{192, 192, 192}, "Silver");
    tempMap.put(new int[]{169, 169, 169}, "Dark Gray");
    tempMap.put(new int[]{128, 128, 128}, "Gray");
    tempMap.put(new int[]{105, 105, 105}, "Dim Gray");
    tempMap.put(new int[]{119, 136, 153}, "Light slate Gray");
    tempMap.put(new int[]{112, 128, 144}, "Slate Gray");
    tempMap.put(new int[]{47, 79, 79},    "Dark Slate Gray");
    tempMap.put(new int[]{0, 0, 0},       "Black");""")
