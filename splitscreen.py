from typing import Optional, Tuple

import arcade

""" A simple example that demonstrates using multiple cameras to allow a split 
screen using Arcade's 3.0 camera.

The left screen follows the player, while the right screen is stationary. The 
code is written in a way that it could easily be extended to two players, or
to more than two players.

WARNING: This example currently uses a development build of arcade 3.0.0.dev26.
At this time the new camera code is still in development, so this example might
be out of date with later 3.0.0 versions of arcade. I'll try and update it, but
I make no guarantees.
"""

TITLE = "Split Screen Test"
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000
BACKGROUND_COLOR = arcade.color.SPACE_CADET
BACKGROUND_IMAGE = ":resources:images/backgrounds/stars.png"

DEFAULT_DAMPING = 1.0

GRAVITY = 0.0
SHIP_MASS = 1.0
SHIP_FRICTION = 0.0
SHIP_ELASTICITY = 0.1

SHIP_FRICTION = 0.0
ROTATION_SPEED = 0.05
KEYBOARD_THRUSTER_FORCE = 200.0
KEYBOARD_ROTATION_FORCE = 0.05

SHIP_SCALING = 0.5

PLAYER_ONE = 0
PLAYER_TWO = 1

CAMERA_ONE = 0
CAMERA_TWO = 1


class Player(arcade.Sprite):
    def __init__(self, main,
                 start_position: Tuple):
        self.shape = None
        self.sprite_filename = ":resources:images/space_shooter/playerShip1_orange.png"
        self.main = main
        self.dx = 0.0
        self.dy = 0.0
        self.force = 0.0
        self.applied_rotational_vel = 0
        self.body = None
        self.start_position = start_position
        self.friction = SHIP_FRICTION

        self.w_pressed = 0.0
        self.s_pressed = 0.0
        self.a_pressed = 0.0
        self.d_pressed = 0.0
        self.left_pressed = 0.0
        self.right_pressed = 0.0

        super().__init__(self.sprite_filename)
        self.position = start_position
        self.mass = SHIP_MASS
        self.friction = SHIP_FRICTION
        self.elasticity = SHIP_ELASTICITY
        self.texture = arcade.load_texture(self.sprite_filename,
                                           hit_box_algorithm=arcade.hitbox.PymunkHitBoxAlgorithm())
        self.main = main
        self.scale = SHIP_SCALING

    def setup(self):
        self.body = self.main.physics_engine.get_physics_object(self).body
        self.shape = self.main.physics_engine.get_physics_object(self).shape
        self.controller = arcade.get_controllers()[0]
        self.controller.open()

    def apply_angle_damping(self):
        self.body.angular_velocity /= 1.05

    def on_update(self, delta_time: float):
        super().update()

        self.dx = self.a_pressed + self.d_pressed
        self.dy = self.w_pressed + self.s_pressed
        self.applied_rotational_vel = self.left_pressed - self.right_pressed
        
        print(self.controller.lefty)

        if self.applied_rotational_vel == 0.0:
            self.apply_angle_damping()

        self.body.angular_velocity += self.applied_rotational_vel
        self.body.apply_force_at_world_point((self.dx, -self.dy), (self.center_x, self.center_y))

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.W:
            self.w_pressed = -KEYBOARD_THRUSTER_FORCE
        elif key == arcade.key.S:
            self.s_pressed = KEYBOARD_THRUSTER_FORCE
        elif key == arcade.key.A:
            self.a_pressed = -KEYBOARD_THRUSTER_FORCE
        elif key == arcade.key.D:
            self.d_pressed = KEYBOARD_THRUSTER_FORCE
        elif key == arcade.key.LEFT:
            self.left_pressed = KEYBOARD_ROTATION_FORCE
        elif key == arcade.key.RIGHT:
            self.right_pressed = KEYBOARD_ROTATION_FORCE

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.W:
            self.w_pressed = 0.0
        elif key == arcade.key.S:
            self.s_pressed = 0.0
        elif key == arcade.key.A:
            self.a_pressed = 0.0
        elif key == arcade.key.D:
            self.d_pressed = 0.0
        elif key == arcade.key.LEFT:
            self.left_pressed = 0.0
        elif key == arcade.key.RIGHT:
            self.right_pressed = 0.0


class Game(arcade.Window):
    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        super().__init__(self.screen_width,
                         self.screen_height,
                         TITLE,
                         resizable=True)
        arcade.set_background_color(BACKGROUND_COLOR)
        self.background_image = BACKGROUND_IMAGE
        self.cameras = []
        self.player_two_projection_data = None
        self.player_two_viewport = None
        self.player_one_projection_data = None
        self.player_one_viewport = None
        self.players_list = None
        self.physics_engine = None
        self.players: Optional[Player] = None

    def on_key_press(self, key: int, modifiers: int):
        for player in self.players:
            player.on_key_press(key, modifiers)

    def on_key_release(self, key: int, modifers: int):
        for player in self.players:
            player.on_key_release(key, modifers)

    def setup(self):
        self.setup_spritelists()
        self.setup_physics_engine()
        self.setup_players()
        self.setup_players_cameras()
        self.background = arcade.load_texture(self.background_image)

    def setup_spritelists(self):
        self.players = arcade.SpriteList()

    def setup_physics_engine(self):
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DEFAULT_DAMPING,
                                                         gravity=(0, 0))

    def setup_players(self):
        self.players.append(Player(self, (self.screen_width / 2.0, self.screen_height / 2.0)))

        self.players_list = [self.players[PLAYER_ONE]]

        self.physics_engine.add_sprite(self.players[PLAYER_ONE],
                                       friction=self.players[PLAYER_ONE].friction,
                                       elasticity=self.players[PLAYER_ONE].elasticity,
                                       mass=self.players[PLAYER_ONE].mass,
                                       moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="SHIP")

        for player in self.players:
            player.setup()

    def setup_players_cameras(self):
        half_width = self.screen_width // 2

        # Viewport is defined as: (left, bottom, width, height)
        self.player_one_viewport = (0, 0, half_width, self.screen_height)
        self.player_two_viewport = (half_width, 0, half_width, self.screen_height)

        player_one_camera = arcade.camera.Camera2D()
        player_one_camera.viewport = self.player_one_viewport
        player_one_camera.equalise()

        player_two_camera = arcade.camera.Camera2D()
        player_two_camera.viewport = self.player_two_viewport
        player_two_camera.equalise()

        self.cameras.append(player_one_camera)
        self.cameras.append(player_two_camera)

        self.center_camera_on_player(PLAYER_ONE)

    def center_camera_on_player(self, player_num):
        self.cameras[player_num].position = (self.players_list[player_num].center_x,
                                             self.players_list[player_num].center_y)

    def on_update(self, delta_time: float):
        self.players.on_update(delta_time)
        self.physics_engine.step()
        self.center_camera_on_player(PLAYER_ONE)

    def on_draw(self):
        for camera in range(len(self.cameras)):
            self.cameras[camera].use()
            self.clear()
            arcade.draw_lrwh_rectangle_textured(0, 0,
                                                self.screen_width, self.screen_height,
                                                self.background)
            self.players.draw()



if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
