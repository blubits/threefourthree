import pyglet

class TFTTile(pyglet.sprite.Sprite):

    def __init__(self, number, *args, **kwargs):

        # initialize helper variables
        tile_image = pyglet.image.load("resources/img/tiles.png")
        self.tile_assets = pyglet.image.ImageGrid(
            tile_image, 2, 5)
        self.indices = {
            0: 0,
            None: 0,
            3: 1,
            9: 2,
            27: 3,
            81: 4,
            243: 5,
            729: 6,
            2187: 7,
            6561: 8,
            19683: 9
        }
        super().__init__(
            img=self.tile_assets[self.indices[number]], *args, **kwargs)

class TFTBoard:

    def __init__(self, board, window_width, window_height):
        self.batch = pyglet.graphics.Batch()
        board_bg_img = pyglet.image.load("resources/img/grid.png")
        board_bg_img.anchor_x = board_bg_img.width // 2
        board_bg_img.anchor_y = board_bg_img.height // 2
        self.board_bg = pyglet.sprite.Sprite(
            img=board_bg_img,
            x=window_width / 2, y=window_height / 2)
        self.tiles = []
        di = len(board) - 1
        dj = 0
        for row in board:
            dj = 0
            self.tiles.append(list())
            for value in row:
                print(di, dj)
                tile = TFTTile(value, batch=self.batch)
                ti = ((window_height - board_bg_img.height) // 2) + 25 + \
                    ((100) * di) + 2
                tj = ((window_width - board_bg_img.width) // 2) + 25 + \
                    ((100) * dj) + 1
                tile.set_position(tj, ti)
                self.tiles[-1].append(tile)
                dj += 1
            di -= 1

    def draw(self):
        self.board_bg.draw()
        self.batch.draw()


class TFTWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)

        self.bg = pyglet.image.SolidColorImagePattern(
            (255, 255, 255, 100)).create_image(self.width, self.height)
        self.board = TFTBoard([[None, 3, None, None]
                               for i in range(4)], self.width, self.height)

    def on_draw(self):
        self.bg.blit(0, 0)
        self.board.draw()

def main():
    window = TFTWindow(height=700, width=600)

    pyglet.app.run()

if __name__ == "__main__":
    main()
