from typing import Optional, Tuple

import arcade

""" A simple Camera toy that allows you to controller different components of the
new 3.0 Camera. Here are the controls:

, (comma) - Switch what your controlling left
. (period) - Switch what your controlling right

## Viewport & Projection Controls:

Numpad 4 - Add negative value to viewport/projection left (grows the width)
Numpad 6 - Add positive value to the viewport/projection right (grows the width)
Numpad 8 - Add positive value to viewport/projection top (grows the height)
Numpad 2 - Add negative value to the viewport/projection bottom (grows the height)

Numpad 7 - Decrease viewport width / add/sub to near far for projection
Numpad 9 - Increase viewport height / add/sub to near far for projection

CTRL + any Key - Flip the sign (shrink the value)

## Camera Position Controls:

Numpad 4 - Move the camera left (negative x direction)
Numpad 6 - Move the camera right (positive x direction)
Numpad 8 - Move the camera up (positive y direction)
Numpad 2 - Move the camera down (negative y direction)
Numpad 9 - Move the camera forward (positive z direction)
Numpad 7 - Move the camera backwards (negative z direction)

## Camera Up and Forward

Numpad 4 - Change the direction of the vector in the negative x direction
Numpad 6 - Change the direction of the vector in the positive x direction 
Numpad 8 - Change the direction of the vector in the positive y direction
Numpad 2 - Change the direction of the vector in the negative y direction
Numpad 7 - Change the direction of the vector in the negative z direction
Numpad 9 - Change the direction to the vector in the positive z direction
"""

TITLE = "Camera 2D Toy"
SCREEN_WIDTH = 1000
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

SHIP_SCALING = 0.5

PLAYER_ONE = 0
PLAYER_TWO = 1

CAMERA_ONE = 0
CAMERA_TWO = 1

VIEWPORT = "VIEWPORT SIZE"
CAMERA_POSITION = "CAMERA POSITION"
CAMERA_UP = "CAMERA UP"
CAMERA_FORWARD = "CAMERA FORWARD"
PROJECTION = "PROJECTION"

controllers = [VIEWPORT, CAMERA_POSITION, CAMERA_UP, CAMERA_FORWARD, PROJECTION]


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

    def apply_angle_damping(self):
        self.body.angular_velocity /= 1.05

    def on_update(self, delta_time: float):
        super().update()

        self.dx = self.a_pressed + self.d_pressed
        self.dy = self.w_pressed + self.s_pressed
        self.applied_rotational_vel = self.left_pressed - self.right_pressed

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

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.W:
            self.w_pressed = 0.0
        elif key == arcade.key.S:
            self.s_pressed = 0.0
        elif key == arcade.key.A:
            self.a_pressed = 0.0
        elif key == arcade.key.D:
            self.d_pressed = 0.0


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
        self.camera = None
        self.project = None
        self.camera_viewport = None
        self.physics_engine = None
        self.players: Player = None
        self.controlling = 0

    def switch_controlling(self, direction):
        if direction == "right":
            self.controlling += 1
        elif direction == "left":
            self.controlling -= 1

        if self.controlling == len(controllers):
            self.controlling = 0
        elif self.controlling < 0:
            self.controlling = len(controllers) - 1

        print("You are now controlling: ", controllers[self.controlling])

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.PERIOD:
            self.switch_controlling("right")

        if key == arcade.key.COMMA:
            self.switch_controlling("left")

        for player in self.players:
            player.on_key_press(key, modifiers)

        shrink_or_grow = -(modifiers & arcade.key.MOD_CTRL) or 1
        change_size = 5 * ((arcade.key.MOD_ALT & modifiers) + 1)
        change_size_vec = .05

        if controllers[self.controlling] == VIEWPORT:
            if key == arcade.key.NUM_6:
                self.cameras[0].viewport_right += change_size * shrink_or_grow
            elif key == arcade.key.NUM_4:
                self.cameras[0].viewport_left += -change_size * shrink_or_grow
            elif key == arcade.key.NUM_2:
                self.cameras[0].viewport_bottom += -change_size * shrink_or_grow
            elif key == arcade.key.NUM_8:
                self.cameras[0].viewport_top += change_size * shrink_or_grow
            elif key == arcade.key.NUM_7:
                self.cameras[0].viewport_width += change_size * shrink_or_grow
            elif key == arcade.key.NUM_9:
                self.cameras[0].viewport_height += change_size * shrink_or_grow

            print(f"Viewport (left, right, width, height): {self.cameras[0].viewport}")
        elif controllers[self.controlling] == CAMERA_POSITION:
            cur_pos = self.cameras[0]._data.position
            if key == arcade.key.NUM_6:
                self.cameras[0].position = (cur_pos[0] + change_size, cur_pos[1], cur_pos[2])
            elif key == arcade.key.NUM_4:
                self.cameras[0].position = (cur_pos[0] + -change_size, cur_pos[1], cur_pos[2])
            elif key == arcade.key.NUM_2:
                self.cameras[0].position = (cur_pos[0], cur_pos[1] + -change_size, cur_pos[2])
            elif key == arcade.key.NUM_8:
                self.cameras[0].position = (cur_pos[0], cur_pos[1] + change_size, cur_pos[2])
            elif key == arcade.key.NUM_7:
                self.cameras[0]._data.position = (cur_pos[0], cur_pos[1], cur_pos[2] - change_size)
            elif key == arcade.key.NUM_9:
                self.cameras[0]._data.position = (cur_pos[0], cur_pos[1], cur_pos[2] + change_size)

            print(f"Camera Position (x, y, z): {self.cameras[0]._data.position}")
        elif controllers[self.controlling] == CAMERA_UP:
            cur_up = self.cameras[0]._data.up
            if key == arcade.key.NUM_6:
                self.cameras[0].up = (cur_up[0] + change_size_vec, cur_up[1], cur_up[2])
            elif key == arcade.key.NUM_4:
                self.cameras[0].up = (cur_up[0] + -change_size_vec, cur_up[1], cur_up[2])
            elif key == arcade.key.NUM_2:
                self.cameras[0].up = (cur_up[0], cur_up[1] + change_size_vec, cur_up[2])
            elif key == arcade.key.NUM_8:
                self.cameras[0].up = (cur_up[0], cur_up[1] + -change_size_vec, cur_up[2])
            elif key == arcade.key.NUM_7:
                self.cameras[0]._data.up = (cur_up[0], cur_up[1], cur_up[2] - change_size_vec)
            elif key == arcade.key.NUM_9:
                self.cameras[0]._data.up = (cur_up[0], cur_up[1], cur_up[2] + change_size_vec)

            print(f"Camera Up (x, y, z): {self.cameras[0]._data.up}")

        elif controllers[self.controlling] == CAMERA_FORWARD:
            cur_forward = self.cameras[0]._data.forward
            if key == arcade.key.NUM_6:
                self.cameras[0]._data.forward = (cur_forward[0] + change_size_vec, cur_forward[1], cur_forward[2])
            elif key == arcade.key.NUM_4:
                self.cameras[0]._data.forward = (cur_forward[0] + -change_size_vec, cur_forward[1], cur_forward[2])
            elif key == arcade.key.NUM_2:
                self.cameras[0]._data.forward = (cur_forward[0], cur_forward[1] + change_size_vec, cur_forward[2])
            elif key == arcade.key.NUM_8:
                self.cameras[0]._data.forward = (cur_forward[0], cur_forward[1] + -change_size_vec, cur_forward[2])
            elif key == arcade.key.NUM_7:
                self.cameras[0]._data.forward = (cur_forward[0], cur_forward[1], cur_forward[2] - change_size_vec)
            elif key == arcade.key.NUM_9:
                self.cameras[0]._data.forward = (cur_forward[0], cur_forward[1], cur_forward[2] + change_size_vec)

            print(f"Camera Forward (x, y, z): {self.cameras[0]._data.forward}")
        elif controllers[self.controlling] == PROJECTION:
            if key == arcade.key.NUM_6:
                self.cameras[0]._projection.right += change_size * shrink_or_grow
            elif key == arcade.key.NUM_4:
                self.cameras[0]._projection.left += -change_size * shrink_or_grow
            elif key == arcade.key.NUM_2:
                self.cameras[0]._projection.top += change_size * shrink_or_grow
            elif key == arcade.key.NUM_8:
                self.cameras[0]._projection.bottom += -change_size * shrink_or_grow
            elif key == arcade.key.NUM_7:
                self.cameras[0]._projection.near += -change_size * shrink_or_grow
            elif key == arcade.key.NUM_9:
                self.cameras[0]._projection.far += change_size * shrink_or_grow

            print(f"Projection (left, right, bottom, top): {self.cameras[0].projection}")

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
        # Viewport is defined as: (left, bottom, width, height)
        self.camera_viewport = (0, 0, self.screen_width, self.screen_height)

        player_one_camera = arcade.camera.Camera2D()
        player_one_camera.viewport = self.camera_viewport
        player_one_camera.equalise()

        self.camera = player_one_camera
        self.cameras.append(player_one_camera)

    def center_camera_on_player(self, player_num):
        self.cameras[player_num].position = (self.players_list[player_num].center_x,
                                             self.players_list[player_num].center_y)

    def on_update(self, delta_time: float):
        self.players.on_update(delta_time)
        self.physics_engine.step()
        #self.center_camera_on_player(PLAYER_ONE)

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
