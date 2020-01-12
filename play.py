import arcade
import random

grid = []
stack = []
grid_width = 500
grid_height = 500
width = 20;
columns = int(grid_width / width)
rows = int(grid_height / width)
current = None


class Cell:

	visited = False

	def __init__ (self, row, col):
		
		self.row = row
		self.col = col
		self.walls = { "top": True, "right": True, "bottom": True, "left": True }


	def draw(self):

		x = self.row * width
		y = self.col * width

		#top line
		if self.walls["top"]:
			arcade.draw_line(x, y+width, x+width, y+width, arcade.color.WHITE, 2)
		#right line
		if self.walls["right"]:
			arcade.draw_line(x+width, y, x+width, y+width, arcade.color.WHITE, 2)
		#bottom lin
		if self.walls["bottom"]:
			arcade.draw_line(x, y, x+width, y, arcade.color.WHITE, 2)
		#left line
		if self.walls["left"]:
 			arcade.draw_line(x, y, x, y+width, arcade.color.WHITE, 2)
		
		# Have I been visited?
		if(self.visited):
			arcade.draw_rectangle_filled(x+(width/2), y+(width/2), width, width, arcade.color.ILLUMINATING_EMERALD)


	def highlight(self):

		x = self.row * width
		y = self.col * width
		arcade.draw_rectangle_filled(x+(width/2), y+(width/2), width, width, arcade.color.EMERALD)


	def checkNeighbours(self):

		row = self.row
		col = self.col
		neighbours = []

		top_neighbour = getValidCell(row, col+1)
		right_neighbour = getValidCell(row+1, col)
		bottom_neighbour = getValidCell(row, col-1)
		left_neighbour = getValidCell(row-1, col)


		if top_neighbour is not None and not top_neighbour.visited:
			neighbours.append(top_neighbour)

		if right_neighbour is not None and not right_neighbour.visited:
			neighbours.append(right_neighbour)

		if bottom_neighbour is not None and not bottom_neighbour.visited:
			neighbours.append(bottom_neighbour)

		if left_neighbour is not None and not left_neighbour.visited:
			neighbours.append(left_neighbour)

		print("possible neighbours:")
		for neigh in neighbours:
			print(neigh.row, neigh.col)

		if neighbours:
			return random.choice(neighbours)
		else:
			return None



def getValidCell(row, col):
	if not row < 0 and not col < 0:
		if not col > columns-1 and not row > rows-1:
			return grid[row][col]



def draw_grid(grid):
	for row in grid:
		for cell in row:
			cell.draw()



def remove_walls(current, next_location):

	x = current.row - next_location.row
	y = current.col - next_location.col

	if x == 1: 
		current.walls["left"] = False
		next_location.walls["right"] = False
	elif x == -1:
		current.walls["right"] = False
		next_location.walls["left"] = False

	if y == 1: 
		current.walls["bottom"] = False
		next_location.walls["top"] = False
	elif y == -1:
		current.walls["top"] = False
		next_location.walls["bottom"] = False


def on_draw():

	global current

	arcade.start_render()

	draw_grid(grid)


def on_update(delta_time):
	
	global current

	next_location = current.checkNeighbours()


	if next_location is not None:

		stack.append(current)
		
		next_location.visited = True
		
		remove_walls(current, next_location)
		
		current.draw()
		next_location.draw()
		
		current = next_location

	elif stack:

		current.draw()
		current = stack.pop()


	current.highlight()


	print(f"new current: {current.row, current.col}")


def main():

	global current
	
	for row in range(rows):

		row_array = [] 

		for column in range(columns):
			row_array.append(Cell(row, column))

		grid.append(row_array)


	current = grid[0][0]
	current.visited = True

	arcade.open_window(grid_width, grid_height, "Grid")
	arcade.set_background_color(arcade.color.BLACK)

	on_draw()

	arcade.schedule(on_update, 1/500)
	arcade.run()


if __name__ == "__main__":
    main()



