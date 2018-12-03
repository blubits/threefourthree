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

		self.print_board()

	def print_board(self):
		self.board_status = self.super_class.current_game.peek_board()
		self.output_board(self.board_status)
		self.score = pyglet.text.Label('Score: {}'.format(self.super_class.current_game.score),
									   x = 490, y = 768 - 144, font_size = 32,
									   color = (0, 0, 0, 255))

	def output_board(self, board):
		for i in range(len(board)):
			for j in range(len(board[i])):
				if board[i][j] is not None:
					self.sprites[i][j] = pyglet.sprite.Sprite(self.assets[board[i][j]],
														x = 253 + (88 * j), 
														y = 768 - (287 + (88 * i)),
														batch = self.batch)
				else:
					self.sprites[i][j] = None

	def load_img(self, file, format = 'png'):
		return pyglet.image.load('assets/{}.{}'.format(file, format))

	def load_assets(self):
		assets = {
			'board': self.load_img('board', format = 'jpg'),
			3: self.load_img('3'),
			9: self.load_img('9'),
			27: self.load_img('27'),
			81: self.load_img('81'),
			243: self.load_img('243'),
			729: self.load_img('729'),
			2187: self.load_img('2187'),
			6561: self.load_img('6561'),
			19683: self.load_img('19683'),
			59049: self.load_img('59049')
		}
		return assets

	def on_key_press(self, symbol, modifiers):
		directions = {key.LEFT: 'left', key.RIGHT: 'right',
					  key.UP: 'up', key.DOWN: 'down'}
		if symbol in directions:
			self.direction = directions[symbol]
			self.super_class.view_events.move(self.direction)
			self.print_board()
			self.direction = None
	
	def on_draw(self):
		self.clear()
		self.board.draw()
		self.score.draw()
		self.batch.draw()

	def run(self):
		pyglet.app.run()