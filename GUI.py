from tkinter import *
from sudoku import *
from tkinter import ttk, messagebox
from solver import *
class sudoku_gui:
	def __init__(self):
		self.root = Tk()
		self.root.title("Sudoku Game")
		self.board_frame = Frame(self.root)
		self.game_level = "easy"
		self.mode = "AI-AC3"
		self.board_mode = "Generate Random Board"
		self.sudoku_game = Sudoku(self.game_level)
		self.sudoku_game.generate_random_board()
		self.solver= Solver(self.sudoku_game)
		self.entered_board = [[ None for _ in range(9)] for _ in range(9)]
		self.draw_board()
		self.add_buttons()
		print(self.sudoku_game.get_cell(1, 2))
		self.root.mainloop()
	
	def draw_board(self):
		
		self.board_frame.pack(pady=10)
		for r in range(9):
			for c in range(9):
				left = 2 if c % 3 == 0 else 0
				top = 2 if r % 3 == 0 else 0
				right = 2 if c == 8 else 0
				bottom = 2 if r == 8 else 0
				value = self.sudoku_game.get_cell(r, c)
				if value == '0':
					entry = Entry(self.board_frame, background="#DDEEF0", width=2, justify="center", font=("Arial", 18))
				else:
					entry = Entry(self.board_frame, width=2, justify="center", font=("Arial", 18))
					entry.config(disabledbackground="#DDEEF0", disabledforeground="black")
					entry.insert(0, value)
					entry.config(state="disabled")
				entry.grid(row=r, column=c, padx=(left, right), pady=(top, bottom))
				self.entered_board[r][c] = entry
	
	def add_buttons(self):
		#buttons frame
		button_frame = Frame(self.root)
		button_frame.pack(pady=8)
		#modes dropdown
		modes = ["AI-Backtracking", "AI-AC3", "Interactive"]
		cb = ttk.Combobox(button_frame, values=modes, state="readonly")
		cb.set("Mode")
		cb.pack(side="left")
		cb.bind("<<ComboboxSelected>>", lambda e: self.update_combobox("mode", cb))
		#Input board dropdown
		boards = ["Input Board", "Generate Random Board"]
		board_cb = ttk.Combobox(button_frame, values=boards, state="readonly")
		board_cb.set("New Board")
		board_cb.pack(side="left")
		board_cb.bind("<<ComboboxSelected>>", lambda e: self.update_combobox("board_mode", board_cb))
		#generate board button
		generate_board_button = Button(button_frame, text="Generate Board", background="#CDF0F8", command=self.generate_board)
		generate_board_button.pack(side="left")
		#solve board button
		solve_button = Button(button_frame, text="Solve",background="#CDF0F8", command=self.solve_puzzle)
		solve_button.pack(side="left")
		
	def generate_board(self):
		if self.board_mode=="Input Board":
			self.read_board_entries()
		else:
			self.sudoku_game.generate_random_board()
		self.redraw_board()
	def read_board_entries(self):
		for i in range(9):
			for j in range(9):
				value = self.entered_board[i][j].get().strip()
				if value !="":
					value = int(self.entered_board[i][j].get().strip())
					if not self.sudoku_game.update_cell(i, j, value):
						messagebox.showerror("Invalid Input", f"Invalid number {value} at ({i},{j})")
						self.reset_board()
						return False
		messagebox.showinfo("Board Generation","Board Generated Successfully")
		
				
	def reset_board(self):
		self.sudoku_game.board = '0' * 81
		self.redraw_board()
	
	def solve_puzzle(self):
		solved=True
		if(self.mode == "AI-Backtracking"):
			solved=self.solver.backtracking()
			self.sudoku_game.board=self.solver.sudoko.board
			self.redraw_board()
			messagebox.showinfo(title="Success", message="Board solved using backtracking")
		elif(self.mode == "AI-AC3"):
			solved=self.solver.solve_ac3()
			self.sudoku_game.board = self.solver.sudoko.board
			self.redraw_board()
			messagebox.showinfo(title="Success", message="Board solved using arc consistency backtracking")
		else:
			self.validate()
		if not solved:
			messagebox.showerror("Unsolvable","This sudoku is Unsolvable!")
		
			
	def validate(self):
		full = True
		
		self.solver.backtracking()
		
		for i in range(9):
			for j in range(9):
				try:
					value = self.entered_board[i][j].get().strip()
					if value:
						if not value == self.solver.sudoko.get_cell(i, j):
							raise ValueError(f"Invalid number {value} at ({i},{j})")
					else:
						full = False
				except ValueError:
					if self.entered_board[i][j].get() != "":
						messagebox.showerror("Invalid Input",
											 f"Invalid value at cell ({i},{j}).")
					return None
		if full:
			messagebox.showinfo(title="Success", message="You have solved the sudoku ;)")
		
	def redraw_board(self):
		self.draw_board()
	
	def update_combobox(self, target, combobox):
		combobox_value = combobox.get()
		setattr(self, target, combobox_value)
		print (target)
		if(target=="board_mode" and combobox_value=="Input Board"):
			self.reset_board()
		



start_game=sudoku_gui()
