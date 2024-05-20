import sys
import os
from pathlib import Path

import arcade

asset_dir = os.path.join(Path(__file__).parent.resolve(), "assets")
arcade.resources.add_resource_handle("assets", asset_dir)

print("__file__:", __file__, Path(__file__).resolve())
print("sys.argv[0]:", sys.argv[0], Path(sys.argv[0]).resolve())

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(400, 400, "Building Example")
        self.sprite_list = arcade.SpriteList()

    def setup(self):
        alien = arcade.Sprite(":assets:png/alienBlue_front.png")
        alien.position = (200, 200)
        self.sprite_list.append(alien)

    def on_draw(self):
        arcade.start_render()
        self.sprite_list.draw()


game = MyGame()
game.setup()
arcade.run()