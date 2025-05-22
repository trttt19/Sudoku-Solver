
import random
import solver

class Sudoku:
	def __init__(self,mode,board_str=None):
		if mode=="easy":
			self.removed_cells=2
		elif mode=="medium":
			self.removed_cells=25
		elif mode=="hard":
			self.removed_cells=45
		if board_str is None:
			self.board = '0' * 81  # Empty Sudoku board (81 cells, all set to 0)
			self.domain=self.initialize_domains()
		else:
			self.board = board_str
	def set_level(self,level):
		if level=="easy":
			self.removed_cells=10
		elif level =="medium":
			self.removed_cells=25
		elif level =="hard":
			self.removed_cells=45
	def initialize_domains(self):
		domain = []
		for r in range(9):
			row = []
			for c in range(9):
				if self.get_cell(r, c) == 0:
					row.append({1, 2, 3, 4, 5, 6, 7, 8, 9})
				else:
					row.append({self.get_cell(r, c)})
			domain.append(row)
		return domain
	def update_cell(self,row,col,val):
		if val>9 or val<1:
			return False
		if not self.isvalid(row,col,val):
			return False
		index=row*9 + col
		self.board=self.board[:index] + str(val) + self.board[index + 1:]
		return True
	def get_cell(self,row,col):
		index = row * 9 + col
		return self.board[index]
		
	
	def print_board(self):
		for i in range(9):
			print(' '.join(self.board[i * 9:(i + 1) * 9]))
	def generate_random_board(self):
		self.board = '0' * 81
		solve=solver.Solver(self)
		solve.backtracking()
		cells=list(range(81))
		random.shuffle(cells)
		for i in cells[:self.removed_cells]:
			self.board=self.board[:i] + str(0) + self.board[i + 1:]
		
		
	def isvalid(self,row,col,num):
		for c in range(9):
			if self.get_cell(row,c)==str(num):
				return False
		for r in range (9):
			if self.get_cell(r,col)==str(num):
				return False
		start_row, start_col = 3 * (row // 3), 3 * (col // 3)
		for r in range(start_row, start_row + 3):
			for c in range(start_col, start_col + 3):
				if self.get_cell(r, c) == str(num):
					return False
		return True
	
	
# board_str = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
# sudoku = Sudoku("easy")
# sudoku.generate_random_board()
# # cell=sudoku.get_cell(0,1)
# # sudoku.update_cell(0,3,8)
# # print(cell)
# # print(sudoku.board)
# sudoku.print_board()

#sudoku.backtracking()

# if(sudoku.backtracking()):
# 	print("backtracking res")
# else:
# 	print("false res")
#sudoku.print_board()
#sudoku.print_board()

# board_str = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
# # board_str=	"111111111111111111111111111111111111111111111111111111111111111111111111111111111"
# game = Sudoku("easy",board_str)
# game.print_board()
# solverr = solver.Solver(game)
# #domain = solver.ac3( solver.define_arcs())
# #print(solver.domain)
# solverr.solve_ac3()
# #solver.backtracking()
# solverr.sudoko.print_board()
