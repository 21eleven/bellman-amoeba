from __future__ import print_function
import numpy as np
import copy


class amoeba():
	def __init__(self, environment_size=(8,8), foods=1, obstacles=1, poisons=1, demo=False):
		def place_food():
			row = np.random.randint(0,environment_size[0])
			col = np.random.randint(0,environment_size[1])
			if self.environ[row][col] == 1:
				place_food()
			else: self.environ[row][col] = 1

		def place_amoeba():
			row = np.random.randint(0,environment_size[0])
			col = np.random.randint(0,environment_size[1])
			if self.environ[row][col] == 1:
				return place_amoeba()
			else: return [row,col]

		def one_d_project(pt):
			return pt[0]*self.environ.shape[1]+pt[1]

		def build_transition_matrix():
			def render_next_state(r,c,a):
				# 0 = up, 1 = left, 2 = down, 3 = right
				s_prime = np.zeros(self.len) 
				if [r,c] in self.foods + self.obstacles + self.poisons:
					print([r,c])
					return s_prime
				if a == 0:
					try:
						self.environ[r+1][c]
						s_prime[one_d_project((r+1,c))] += 0.8
						try:
							self.environ[r][c+1]
							s_prime[one_d_project((r,c+1))] += 0.1
						except IndexError:
							s_prime[one_d_project((r,c))] += 0.1
						try:
							self.environ[r][c-1]
							s_prime[one_d_project((r,c-1))] += 0.1
						except IndexError:
							s_prime[one_d_project((r,c))] += 0.1
					except IndexError:
						s_prime[one_d_project((r,c))] += 0.8
				elif a == 1:
					try:
						self.environ[r][c-1]
						s_prime[one_d_project((r,c-1))] += 0.8
						try:
							self.environ[r+1][c]
							s_prime[one_d_project((r+1,c))] += 0.1
						except IndexError:
							s_prime[one_d_project((r,c))] += 0.1
						try:
							self.environ[r-1][c]
							s_prime[one_d_project((r-1,c))] += 0.1
						except IndexError:
							s_prime[one_d_project((r,c))] += 0.1
					except IndexError:
						s_prime[one_d_project((r,c))] += 0.8
				elif a == 2:
					try:
						self.environ[r-1][c]
						s_prime[one_d_project((r-1,c))] += 0.8
						try:
							self.environ[r][c+1]
							s_prime[one_d_project((r,c+1))] += 0.1
						except IndexError:
							s_prime[one_d_project((r,c))] += 0.1
						try:
							self.environ[r][c-1]
							s_prime[one_d_project((r,c-1))] += 0.1
						except IndexError:
							s_prime[one_d_project((r,c))] += 0.1
					except IndexError:
						s_prime[one_d_project((r,c))] += 0.8
				elif a == 3:
					if c+1 < self.c:
						s_prime[one_d_project((r,c+1))] += 0.8
					else:
						s_prime[one_d_project((r,c))] += 0.8
					if r+1 < self.r and [r+1,c] not in self.obstacles:
						s_prime[one_d_project((r+1,c))] += 0.1
					else:
						s_prime[one_d_project((r,c))] += 0.1
					if r-1 >= 0:
						s_prime[one_d_project((r-1,c))] += 0.1
					else:
						s_prime[one_d_project((r,c))] += 0.1
				if (r,c,a) == (0,0,3): print(s_prime)
				return s_prime
				
			T = np.zeros((self.len,self.len,4))
			
			one_d_pt = 0
			for row in range(self.r):
				for col in range(self.c):
					for act in range(0,4):
						T[one_d_pt, : , act] = render_next_state(row,col,act)
					one_d_pt += 1
			return T
			

		self.environ = np.zeros(environment_size)
		self.len = environment_size[0]*environment_size[1]
		self.r, self.c = environment_size[0], environment_size[1]
		self.vector = np.zeros((1,self.len))
		if demo == True:
			self.obstacles = [[1,1]]
			self.foods = [[0,3]]
			self.poisons = [[1,3]]
			self.location = [2,0]
		else:	
			self.location = place_amoeba()
		self.t = build_transition_matrix()
		print(self.t[:,:,3])
	def print_environ(self):
		border = ''.join(["-" for i in range((4*self.environ.shape[1])+1)])
		print(border)
		env = copy.deepcopy(self.environ)
		env[self.location[0]][self.location[1]] = 1
		for obj in self.foods:
			env[obj[0],obj[1]] = 3
		for obj in self.obstacles:
			env[obj[0],obj[1]] = 5
		for obj in self.poisons:
			env[obj[0],obj[1]] = -1
		for row in env:
			row_string = ['|']
			for col in row:
				if col == 1:
					row_string += [' @ |']
				elif col == 3:
					row_string += [' $ |']
				elif col == -1:
					row_string += [' X |']
				elif col == 5:
					row_string += ['||||']
				else:
					row_string += ['   |']
			print(''.join(row_string))
			print(border)
	def move_south(self):
		limits = self.environ.shape
		if self.location[0] + 1 != limits[0]:
			self.location[0] += 1

	def move_north(self):
		limits = self.environ.shape
		if self.location[0] - 1 >= 0:
			self.location[0] -= 1

	def move_east(self):
		limits = self.environ.shape
		if self.location[1] + 1 != limits[1]:
			self.location[1] += 1

	def move_west(self):
		limits = self.environ.shape
		if self.location[1] - 1 >= 0:
			self.location[1] -= 1

if __name__ == "__main__":
	np.random.seed(2111)
	#amoeba = amoeba()
	#amoeba(environment_size=(3,4), foods=1, obstacles=1, poisons=1).print_environ()
	amoeba(environment_size=(3,4), demo=True).print_environ()

			
