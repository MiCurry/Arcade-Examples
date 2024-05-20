# Arcade Examples

My personal examples for Python's [Arcade Library](https://api.arcade.academy/en/latest/). 
Please feel to use, these in any way you want!

# Split Screen Example

**WARNING: This example currently uses a development build of arcade 3.0.0.
dev26.
At this time the new camera code is still in development, so this example might
be out of date with later 3.0.0 versions of arcade. I'll try and update it, but
I make no guarantees.**

A simple example that demonstrates using multiple cameras to allow a split 
screen using the new camera in Arcade 3.0.

The left screen follows the player, while the right screen is stationary. The 
code is written in a way that it could easily be extended to two players, or
to more than two players.

# Camera2d_toy.py

**WARNING: This example currently uses a development build of arcade 3.0.0.
dev26.
At this time the new camera code is still in development, so this example might
be out of date with later 3.0.0 versions of arcade. I'll try and update it, but
I make no guarantees.**

A simple Camera toy that allows you to controller different components of the
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

# Building Examples 

Examples showing how to build nuitka or pyinstaller bundlers with custom
resource handlers. Install either nuitkak or pyinstaller and run away!

