import pyglet
from pyglet.window import key

class PygletGUI(pyglet.window.Window):

	def __init__(self, init_class):
		super().__init__(width = 1024, height = 768, resizable = False)
		self.init_class = init_class

		# Variables
		self.wait_input = False
		self.board_status = self.init_class.current_game.peek_board()
		self.board_status_old = [[None for _ in range(6)] for _ in range(6)]

		# Graphics
		self.assets = self.load_assets()
		self.sprites = [[None for _ in range(6)] for _ in range(6)]
		self.board = pyglet.sprite.Sprite(self.assets['board'])
		self.game_over_screen = None
		self.score = self.init_class.current_game.score
		self.batch = pyglet.graphics.Batch()
		self.score_text = pyglet.text.Label('Score: {}'.format(self.score),
											x = 490, y = 768 - 144, font_size = 32,
											color = (0, 0, 0, 255))
		
		# Animation Purposes
		self.anim_done = [False for _ in range(5)]
		self.animate_tiles_destroy = []
		self.animate_tiles_create = []
		self.animation_start = True

		# Init run
		
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
			59049: self.load_img('59049', anchor_x = 44, anchor_y = 44),
			'win': self.load_img('youwin'),
			'lose': self.load_img('youlose')
		}
		return assets

	def press_action(self):
		self.board_status_old = self.init_class.current_game.peek_board()
		self.init_class.view_events.move(self.direction)
		self.animation_start = True

	def animate(self, dt):
		if self.animation_start:
			## Part 0: Setup
			if not any(self.anim_done):
				self.board_status = self.init_class.current_game.peek_board()
				self.score = self.init_class.current_game.score
				self.score_text.text = 'Score: {}'.format(self.score)

				for i in range(6):
					for j in range(6):
						if self.board_status[i][j] != self.board_status_old[i][j] and self.board_status_old[i][j] is not None:
							self.animate_tiles_destroy.append((i, j))
						if self.board_status[i][j] != self.board_status_old[i][j] and self.board_status[i][j] is not None:
							self.animate_tiles_create.append((i, j))

				self.anim_done[0] = True

			## Part 1: Destroying Tile Sprites
			elif all(self.anim_done[0:1]) and not any(self.anim_done[1:]):
				for vector in self.animate_tiles_destroy:
					if self.sprites[vector[0]][vector[1]].scale > 0:
						self.sprites[vector[0]][vector[1]].scale -= dt * 100
					else:
						self.sprites[vector[0]][vector[1]] = None
						self.anim_done[1] = True

				if len(self.animate_tiles_destroy) == 0:
					self.anim_done[1] = True

			## Part 2: 0.05 Seconds Delay
			elif all(self.anim_done[0:2]) and not any(self.anim_done[2:]):
				def trig(dt):
					self.anim_done[2] = True
				pyglet.clock.schedule_once(trig, 0.03)

			## Part 3: Creating Tile Sprites
			elif all(self.anim_done[0:3]) and not any(self.anim_done[3:]):
				for vector in self.animate_tiles_create:
					if self.sprites[vector[0]][vector[1]] == None and self.board_status[vector[0]][vector[1]] is not None:
						self.sprites[vector[0]][vector[1]] = pyglet.sprite.Sprite(self.assets[self.board_status[vector[0]][vector[1]]],
																				  x = 253 + (88 * vector[1]) + 44,
																				  y = 768 - (287 + (88 * vector[0])) + 44,
																				  batch = self.batch
																				 )
						self.sprites[vector[0]][vector[1]].scale = 0

				self.anim_done[3] = True

			## Part 4: Animating Created Tile Sprites
			elif all(self.anim_done[0:4]) and not any(self.anim_done[4:]):
				for vector in self.animate_tiles_create:
					if self.sprites[vector[0]][vector[1]].scale < 1:
						self.sprites[vector[0]][vector[1]].scale += dt * 100
					else:
						self.sprites[vector[0]][vector[1]].scale = 1
						self.anim_done[4] = True

				if len(self.animate_tiles_create) == 0:
					self.anim_done[4] = True

			## Part 5: Final Modifications
			elif all(self.anim_done):
				self.animate_tiles_create = []
				self.animate_tiles_destroy = []
				self.wait_input = False
				self.animation_start = False
				self.anim_done = [False for _ in range(5)]

	def on_won(self):
		self.wait_input = True
		self.game_over_screen = pyglet.sprite.Sprite(self.assets['won'])
		self.game_over_screen.opacity = 255 * (85 / 100)

	def on_lost(self):
		self.wait_input = True
		self.game_over_screen = pyglet.sprite.Sprite(self.assets['lost'])
		self.game_over_screen.opacity = 255 * (85 / 100)

	def on_key_press(self, symbol, modifiers):
		directions = {key.UP: 'up', key.DOWN: 'down',
					  key.RIGHT: 'right', key.LEFT: 'left'
		}
		if symbol in directions and not self.wait_input:
			self.direction = directions[symbol]
			self.wait_input = True
			self.press_action()


	def on_draw(self):
		self.clear()
		self.board.draw()
		self.score_text.draw()
		self.batch.draw()

		if self.game_over_screen is not None:
			self.game_over_screen.draw()

	def run(self):
		pyglet.clock.schedule_interval(self.animate, 1 / 60)
		pyglet.app.run()