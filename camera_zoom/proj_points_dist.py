import os

import numpy as np
import arcade
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

plt.ioff()

class Game(arcade.Window):
    def __init__(self):
        self.screen_width = 10000
        self.screen_height = 10000
        super().__init__(self.screen_width,
                         self.screen_height,
                         "Example",
                         resizable=True)
        self.camera = arcade.camera.Camera2D()
        self.project = None
        self.controlling = 0

    def on_draw(self):
        pass

    def on_update(self, delta_time):
        self.do_map()

    def print_info(self):
        print("Camera:", dir(self.camera))

    def do_map(self, start, end, step):
        arr = np.arange(start, end, step)
        proj = []
        for i in arr:
            proj.append(self.camera.project((0, i)))

        return np.array(proj)


def create_proj_array(window, zoom, start=0, end=1, step=0.1):
    window.zoom = zoom
    proj_arry = window.do_map(start, end, step)
    return proj_arry


def distance_between_points(arry):
    j = 0
    distances = []
    for i in range(arry.shape[0]):
        if i == 0:
            continue
        distances.append((arry[i] - arry[i - 1])[1])

    return distances

def dis(arry):
    distances = []
    for i in range(arry.shape[0]):
        if i == 0:
            continue
        distances.append((arry[i] - arry[i - 1]))

    return distances

def do_thing(window, zoom, start, end, step):
    arry = create_proj_array(window, zoom, start, end, step)
    distances = distance_between_points(arry)

    dist_np = np.array(distances)

    min_dis = 10000000000
    for d in distances:
        if d < min_dis:
            min_dis = d

    print("### New run")
    np.set_printoptions(precision=32, floatmode='fixed')
    print(f"# of Distances: {len(distances)}")
    print(f"Mode: {stats.mode(dist_np)}")
    print(f"Avg: {dist_np.mean()}")
    print(f"min dist: {min_dis}")
    print()

    return dist_np


def normal_distances(start, end, step):
    array = np.arange(start, end, step)
    distances = dis(array)
    return np.array(distances)

window = Game()

zoom = 1
start = 0
stop = 100
step = 1

dist = do_thing(window, zoom, start, stop, step)

norm_dist = normal_distances(start, stop, step)

np.set_printoptions(precision=32, floatmode='fixed')

x = np.arange(0, len(dist), 1)
fig, ax = plt.subplots(2, sharey=True)
fig.suptitle(f'Distance between 0-{len(dist)}, 1 step in between')

plt.yscale('log')

ax[0].set_title('Not Projected (i.e. should be 1)')
ax[1].set_title('Projected - Zoom = 1')

ax[0].bar(x, norm_dist)
ax[1].bar(x, dist)

plt.savefig("projected_0_to_10_1_step.png")