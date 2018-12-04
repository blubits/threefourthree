import pyglet
from pyglet.window import key

class PygletGUI(pyglet.window.Window):

	def __init__(self, init_class):
		super().__init__(width = 1024, height = 768)
		self.super_class = init_class
		self.assets = self.load_assets()
		self.batch = pyglet.graphics.Batch()
		self.board = pyglet.sprite.Sprite(self.assets['board'])
		self.direction = None
		self.sprites = []
		for i in range(6):
			self.sprites.append([])
			for j in range(6):
				self.sprites[i].append(None)
		self.score = pyglet.text.Label('Score: {}'.format(self.super_class.current_game.score),
							   x = 490, y = 768 - 144, font_size = 32,
							   color = (0, 0, 0, 255))
		self.board_status = self.super_class.current_game.peek_board()
		self.print_board()

		# Input Wait
		self.animation_complete = True
		self.wait_input = False

		# Animation Purposes
		self.flag = False
		self.flag1 = False
		self.flag2 = False

	def print_board(self):
		self.board_status = self.super_class.current_game.peek_board()
		print()
		print(self.super_class.current_game.board)
		self.output_board(self.board_status)
		self.score.text = 'Score: {}'.format(self.super_class.current_game.score)

	def on_won(self):
		print('ez win')
		self.score.text = 'Score: {}\nYou\'re Winner!'.format(self.super_class.current_game.score)

	def on_lost(self):
		print('lost lol noob')

	def on_exit(self):
		self.view_events.end()

	def output_board(self, board):
		for i in range(len(board)):
			for j in range(len(board[i])):
				if board[i][j] is not None:
					self.sprites[i][j] = pyglet.sprite.Sprite(self.assets[board[i][j]],
														x = 253 + (88 * j) + 44, 
														y = 768 - (287 + (88 * i)) + 44,
														batch = self.batch)
				else:
					self.sprites[i][j] = None

	def load_img(self, file, format = 'png', anchor_x = 0, anchor_y = 0):
		img = pyglet.image.load('assets/{}.{}'.format(file, format))
		img.anchor_x = anchor_x
		img.anchor_y = anchor_y
		return img

	def load_assets(self):
		assets = {
			'board': self.load_img('board', format = 'jpg'),
			3: self.load_img('3', anchor_x = 44, anchor_y = 44),
			9: self.load_img('9', anchor_x = 44, anchor_y = 44),
			27: self.load_img('27', anchor_x = 44, anchor_y = 44),
			81: self.load_img('81', anchor_x = 44, anchor_y = 44),
			243: self.load_img('243', anchor_x = 44, anchor_y = 44),
			729: self.load_img('729', anchor_x = 44, anchor_y = 44),
			2187: self.load_img('2187', anchor_x = 44, anchor_y = 44),
			6561: self.load_img('6561', anchor_x = 44, anchor_y = 44),
			19683: self.load_img('19683', anchor_x = 44, anchor_y = 44),
			59049: self.load_img('59049', anchor_x = 44, anchor_y = 44)
		}
		return assets

	def animate(self):
		if self.wait_input:
			
			
			# Board Update:
			board_status_old = self.super_class.current_game.peek_board()
			self.super_class.view_events.move(self.direction)
			self.board_status = self.super_class.current_game.peek_board()

			# Score Update:
			self.score.text = 'Score: {}'.format(self.super_class.current_game.score)

			self.animate_tiles_move = []
			self.animate_tiles = []
			for i in range(len(self.board_status)):
				for j in range(len(self.board_status)):
					if board_status_old[i][j] != self.board_status[i][j] and board_status_old[i][j] is not None:
						self.animate_tiles_move.append((i, j))
					if board_status_old[i][j] != self.board_status[i][j] and self.board_status[i][j] is not None:
						self.animate_tiles.append((i, j))
			print()
			print(self.super_class.current_game.board)
			print(self.animate_tiles_move)
			print(self.animate_tiles)
			
			self.flag1 = False
			self.flag2 = False
			self.animation_complete = False
			self.direction = None

	def animate_board(self, dt):
		
		
		if not self.animation_complete:
			print('part1')
			if not self.flag1 and not self.flag2:
				# Animate Tiles Fade
				for vector in self.animate_tiles_move:
					if self.sprites[vector[0]][vector[1]].scale > 0:
						self.sprites[vector[0]][vector[1]].scale -= dt * 8
						print(self.sprites[vector[0]][vector[1]].scale)
					else:
						print('part3')
						self.flag1 = True
						self.sprites[vector[0]][vector[1]] = None
					
			elif self.flag1 and not self.flag2:

				# Delay
				def trig(dt):
					self.flag2 = True
					print(self.sprites)
				pyglet.clock.schedule_once(trig, 0.03)

			elif self.flag2 and self.flag1:
			# Animate New Tiles
				for vector in self.animate_tiles:
					if self.sprites[vector[0]][vector[1]] == None and self.board_status[vector[0]][vector[1]] is not None:
						self.sprites[vector[0]][vector[1]] = pyglet.sprite.Sprite(self.assets[self.board_status[vector[0]][vector[1]]],
																x = 253 + (88 * vector[1]) + 44, 
																y = 768 - (287 + (88 * vector[0])) + 44,
																batch = self.batch)
						self.sprites[vector[0]][vector[1]].scale = 0
				for vector in self.animate_tiles:
					if self.sprites[vector[0]][vector[1]].scale < 1:
						self.sprites[vector[0]][vector[1]].scale += dt * 8
					else:
						self.flag = True
						self.sprites[vector[0]][vector[1]].scale = 1
					
			if self.flag:
				self.animate_tiles = []
				self.animate_tiles_move = []
				self.animation_complete = True
				self.flag1 = False
				self.flag2 = False
				self.wait_input = False

	def on_key_press(self, symbol, modifiers):
		directions = {key.LEFT: 'left', key.RIGHT: 'right',
					  key.UP: 'up', key.DOWN: 'down'}
		if symbol in directions and not self.wait_input:
			self.direction = directions[symbol]
			self.wait_input = True
			self.animate()

	def on_draw(self):
		self.clear()
		self.board.draw()
		self.score.draw()
		self.batch.draw()

	def run(self):
		pyglet.clock.schedule_interval(self.animate_board, 1 / 60)
		pyglet.app.run()