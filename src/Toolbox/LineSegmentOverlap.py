# Credit to https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
from typing import Tuple


class _Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

# Given three colinear points p, q, r, the function checks if


# point q lies on line segment 'pr'
def _on_segment(p: _Point, q: _Point, r: _Point):
	if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
			(q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
		return True
	return False


def _orientation(p: _Point, q: _Point, r: _Point):
	# to find the _orientation of an ordered triplet (p,q,r)
	# function returns the following values:
	# 0 : Colinear points
	# 1 : Clockwise points
	# 2 : Counterclockwise

	# See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
	# for details of below formula.

	val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))

	# Clockwise orientation
	if val > 0:
		return 1

	# Counterclockwise orientation
	elif val < 0:
		return 2

	# Colinear orientation
	else:
		return 0


# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def do_intersect(p1_tuple: Tuple[int, int], q1_tuple: Tuple[int, int],
				 p2_tuple: Tuple[int, int], q2_tuple: Tuple[int, int]):
	p1 = _Point(p1_tuple[0], p1_tuple[1])
	q1 = _Point(q1_tuple[0], q1_tuple[1])
	p2 = _Point(p2_tuple[0], p2_tuple[1])
	q2 = _Point(q2_tuple[0], q2_tuple[1])
	# Find the 4 orientations required for
	# the general and special cases
	o1 = _orientation(p1, q1, p2)
	o2 = _orientation(p1, q1, q2)
	o3 = _orientation(p2, q2, p1)
	o4 = _orientation(p2, q2, q1)

	# General case
	if (o1 != o2) and (o3 != o4):
		return True

	# Special Cases

	# p1 , q1 and p2 are colinear and p2 lies on segment p1q1
	if (o1 == 0) and _on_segment(p1, p2, q1):
		return True

	# p1 , q1 and q2 are colinear and q2 lies on segment p1q1
	if (o2 == 0) and _on_segment(p1, q2, q1):
		return True

	# p2 , q2 and p1 are colinear and p1 lies on segment p2q2
	if (o3 == 0) and _on_segment(p2, p1, q2):
		return True

	# p2 , q2 and q1 are colinear and q1 lies on segment p2q2
	if (o4 == 0) and _on_segment(p2, q1, q2):
		return True

	# If none of the cases
	return False
