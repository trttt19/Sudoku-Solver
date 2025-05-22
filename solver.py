import queue
import random


class Solver:
	def __init__(self, board):
		self.sudoko = board
		self.domain = self.initialize_domains()
	
	def initialize_domains(self):
		domain = []
		for r in range(9):
			row = []
			for c in range(9):
				if (self.sudoko.get_cell(r, c) == '0'):
					row.append({1, 2, 3, 4, 5, 6, 7, 8, 9})
				else:
					row.append({self.sudoko.get_cell(r, c)})
			domain.append(row)
		return domain
	
	def update_domains(self):
		domain = []
		for r in range(9):
			row = []
			for c in range(9):
				#print(self.board.get_cell(r, c))
				if (self.sudoko.get_cell(r, c) == '0'):
					valid_values = {i for i in range(1, 10) if self.sudoko.isvalid(r, c, i)}
					row.append(valid_values)
				
				else:
					row.append({self.sudoko.get_cell(r, c)})
			domain.append(row)
		self.domain = domain
	
	def define_arcs(self):
		arcs = queue.Queue()
		for row in range(9):
			for col in range(9):
				for j in range(9):
					if j != col:
						arcs.put(((row, col), (row, j)))
				for i in range(9):
					if i != row:
						arcs.put(((row, col), (i, col)))
				box_x = col // 3
				box_y = row // 3
				for i in range(box_y * 3, box_y * 3 + 3):
					for j in range(box_x * 3, box_x * 3 + 3):
						if i != row and j != col:
							arcs.put(((row, col), (i, j)))
		
		return arcs
	
	def revise(self, domaini, domainj):
		revised = False
		to_remove = []
		for i in domaini:
			# print(i)
			# print(domainj)
			if not any(str(i) != str(j) for j in domainj):
				to_remove.append(i)
				revised = True
		dom = domaini.copy()
		for i in to_remove:
			dom.remove(i)
		return revised, dom
	
	def neighbours(self,rowi, coli):
		neighbours = set()
		for j in range(9):
			if j != coli :
				neighbours.add((rowi, j))
		for i in range(9):
			if i != rowi :
				neighbours.add((i, coli))
		box_x = coli // 3
		box_y = rowi // 3
		for i in range(box_y * 3, box_y * 3 + 3):
			for j in range(box_x * 3, box_x * 3 + 3):
				if i != rowi and j != coli :
					neighbours.add((i, j))
		
		return neighbours
	
	def ac3(self, arcs):
		while not arcs.empty():
			((rowi, coli), (rowj, colj)) = arcs.get()
			
			rev, dom = self.revise(self.domain[rowi][coli], self.domain[rowj][colj])
			if rev:
				print(f"Revising arc (X{rowi}{coli}, X{rowj}{colj})")
				print(f"Current domain of X{rowi}{coli}: {self.domain[rowi][coli]}")
				print(f"Domain of X{rowj}{colj}: {self.domain[rowj][colj]}")
				removed = self.domain[rowi][coli] - dom
				for r in removed:
					print(f"Removed value {r} from X{rowi}{coli} because no supporting value exists in X{rowj}{colj}")
				print(f"Updated domain of X{rowi}{coli}: {dom}")
				self.domain[rowi][coli] = dom
				if not self.domain[rowi][coli]:
					return False
				for n in self.neighbours(rowi, coli) - {(rowj, colj)}:
					arcs.put((n, (rowi, coli)))
		
		return True
	
	def mrv(self):
		min_row = 0
		min_col = 0
		min = 10
		empty = False
		for row in range(9):
			for col in range(9):
				if self.sudoko.get_cell(row, col) == '0':
					empty = True
					if (len(self.domain[row][col]) < min):
						min_row = row
						min_col = col
						min = len(self.domain[row][col])
		if not empty:
			return None
		return (min_row, min_col)
	
	def lcv(self, row, col):
		
		loop = {}
		for val in self.domain[row][col]:
			loop[val] = 0
			for c in range(9):
				if self.sudoko.get_cell(row, c) == '0' and val in self.domain[row][c]:
					loop[val] += 1
			for r in range(9):
				if self.sudoko.get_cell(r, col) == '0' and val in self.domain[r][col]:
					loop[val] += 1
			start_row, start_col = 3 * (row // 3), 3 * (col // 3)
			for r in range(start_row, start_row + 3):
				for c in range(start_col, start_col + 3):
					if self.sudoko.get_cell(r, c) == '0' and val in self.domain[r][c]:
						loop[val] += 1
		return sorted(self.domain[row][col], key=lambda x: loop[x])
	def forward_checking(self,row,col,val):
		for n in self.neighbours(row,col):
			(rowj,colj)=n
			if val in self.domain[rowj][colj]:
				self.domain[rowj][colj].remove(val)
				if len(self.domain[rowj][colj])==0:
					return False
		return True
	def backtracking(self):
		self.update_domains()
		var = self.mrv()
		if var is None:
			return True
		(row, col) = var
		lcv_values = self.lcv(row, col)
		for num in lcv_values:
			if self.sudoko.isvalid(row, col, num):
				self.sudoko.update_cell(row, col, num)
				#forward checking
				if self.forward_checking(row,col,num):
					if self.backtracking():
						return True
				self.sudoko.update_cell(row, col, 0)
		return False
	def solve_ac3(self):
		if not self.ac3(self.define_arcs()):
			return False
		return self.backtracking()
	# def ac3_backtracking(self):
	# 	self.update_domains()
	# 	var = self.mrv()
	# 	if var is None:
	# 		return True
	# 	(row, col) = var
	# 	lcv_values = self.lcv(row, col)
	# 	for num in lcv_values:
	# 		if self.sudoko.isvalid(row, col, num):
	# 			self.sudoko.update_cell(row, col, num)
	# 			#ac3
	# 			if self.ac3(self.define_arcs()):
	# 				if self.backtracking():
	# 					return True
	# 			self.sudoko.update_cell(row, col, 0)
	# 	return False
	def generate_valid_puzzle(self):
		self.sudoko = '0' * 81
		self.backtracking()
		self.sudoko.print_board()
		for x in range(40):
			r = random.randint(0, 8)
			c = random.randint(0, 8)
			self.update_cell(r, c, 0)


# board_str = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
# # board_str=	"111111111111111111111111111111111111111111111111111111111111111111111111111111111"
# sudoku = toqua.Sudoku(board_str)
# sudoku.print_board()
# solver = Solver(sudoku)
# #domain = solver.ac3( solver.define_arcs())
# #print(solver.domain)
# solver.ac3_backtracking()
# #solver.backtracking()
# solver.board.print_board()
