import arcade
import random


# CONSTANTS

SCREEN_TITLE = "maze-generator"
GRID_WIDTH = 1000
GRID_HEIGHT = 1000
WIDTH = 20
COLUMNS = int(GRID_HEIGHT/WIDTH)
ROWS = int(GRID_WIDTH/WIDTH)

class MyGame(arcade.Window):

	def __init__(self, width, height, title):

 		# Call the parent class initializer
		super().__init__(width, height, title)

		self.grid = []
		self.stack = []
		self.columns = COLUMNS
		self.rows = ROWS
		self.current = Cell(0,0)

		arcade.set_background_color(arcade.color.BLACK)
		



	def setup(self):
		""" Set up the game and initialize the variables. """
		
		for row in range(ROWS):
			row_array = [] 
			for column in range(COLUMNS):
				row_array.append(Cell(row, column))

			self.grid.append(row_array)


		arcade.start_render()

		for row in self.grid:
			for cell in row:
				cell.draw()

		self.current = self.grid[0][0]





	def on_update(self, delta_time):
		
		next_location = self.current.checkNeighbours(self.grid)

		print(f"NEXT LOCK:{next_location}")
		print(f"CURRENT STACK: {len(self.stack)}")

		if next_location is not None:
			print(f"next location: {next_location.row} {next_location.col}")

			self.stack.append(self.current)
			self.current.visited = True
			next_location.visited = True
			
			remove_walls(self.current, next_location)
			
			self.current.draw()
			next_location.draw()
			
			self.current = next_location


		elif self.stack:
			print('stack')
			self.current.draw()
			self.current = self.stack.pop()


		self.current.highlight()


		print(f"new current: {self.current.row, self.current.col}")



class Cell:

	def __init__ (self, row, col):
		
		self.row = row
		self.col = col
		self.walls = { "top": True, "right": True, "bottom": True, "left": True }
		self.visited = False

	def draw(self):

		x = self.row * WIDTH
		y = self.col * WIDTH

		#top line
		if self.walls["top"]:
			arcade.draw_line(x, y + WIDTH, x + WIDTH, y + WIDTH, arcade.color.WHITE, 2)
		#right line
		if self.walls["right"]:
			arcade.draw_line(x + WIDTH, y, x + WIDTH, y + WIDTH, arcade.color.WHITE, 2)
		#bottom lin
		if self.walls["bottom"]:
			arcade.draw_line(x, y, x + WIDTH, y, arcade.color.WHITE, 2)
		#left line
		if self.walls["left"]:
 			arcade.draw_line(x, y, x, y + WIDTH, arcade.color.WHITE, 2)
		
		# Have I been visited?
		if(self.visited):
			arcade.draw_rectangle_filled(x + (WIDTH/2), y + (WIDTH/2), WIDTH, WIDTH, arcade.color.ILLUMINATING_EMERALD)


	def highlight(self):

		x = self.row * WIDTH
		y = self.col * WIDTH
		arcade.draw_rectangle_filled(x+(WIDTH/2), y+(WIDTH/2), WIDTH, WIDTH, arcade.color.EMERALD)


	def checkNeighbours(self, grid):

		row = self.row
		col = self.col
		neighbours = []

		top_neighbour = self.getValidCell(row, col+1, grid)
		right_neighbour = self.getValidCell(row+1, col, grid)
		bottom_neighbour = self.getValidCell(row, col-1, grid)
		left_neighbour = self.getValidCell(row-1, col, grid)


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


	def getValidCell(self, row, col, grid):
		if not row < 0 and not col < 0:
			if not col > COLUMNS-1 and not row > ROWS-1:
				return grid[row][col]



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


def main():
	""" Main method """
	window = MyGame(GRID_WIDTH, GRID_HEIGHT, SCREEN_TITLE)
	window.setup()
	arcade.run()



if __name__ == "__main__":
    main()