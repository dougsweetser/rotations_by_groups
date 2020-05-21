#!/usr/bin/env python
"""
Can make animations of rotation group operations.

usage: rotations_by_groups_time_lapse.py [-d DIM] [-t TMIN] [-m TMAX] [-n NFRAMES] [--v1 XYZ1] [--v2 XYZ2] [-o OUTPUT]

optional arguments:
    -d DIM --dim DIM                Number of dimensions [default: 100]
    -t TMIN --tmin TMIN             Minimum time value [default: 0.1]
    -m TMAX --tmax TMAX             Maximumm time value [default: 5.0]
    -n NFRAMES --n_frames NFRAMES   Number of frames total [default: 100 ]
    --v1 XYZ1                       point_1 3-vector in quotes [default: 1 2 3]
    --v2 XYZ2                       point_2 3-vector in quotes [default: 3 2 1]
    -o OUTPUT --output OUTPUT       output file_name [default: images/out3]
"""

import plotly.graph_objects as go
from PIL import Image
from docopt import docopt
from Qs import *
import os

if __name__ == "__main__":
    ARGS = docopt(__doc__)

dim = int(ARGS["--dim"])

tmin = float(ARGS["--tmin"])
tmax = float(ARGS["--tmax"])
n_frames = int(ARGS["--n_frames"])
dt = (tmax - tmin) / n_frames

v1 = [float(d) for d in ARGS["--v1"].split()]
v2 = [float(d) for d in ARGS["--v2"].split()]

output = ARGS["--output"]

time = tmin

for i in range(100, 100 + n_frames):

    point_1 = Q([time, v1[0], v1[1], v1[2]])
    point_2 = Q([time, v2[0], v2[1], v2[2]])

    next_rotation_data = generate_QQs(next_rotation, point_1, point_2, dim=dim)

    fig = go.Figure()
    go.Layout()
    POINT_SIZE = 6
    OPACITY = 0.8
    
    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=1.25, y=1.25, z=1.25)
    )

    fig.update_layout(scene_camera=camera)

    fig.update_layout(
        scene={
            'xaxis': {'range': [-4, 4], 'rangemode': 'tozero', 'tickmode': "linear", 'tick0': -4, 'dtick': 1},
            'yaxis': {'range': [-4, 4], 'rangemode': 'tozero', 'tickmode': "linear", 'tick0': -4, 'dtick': 1},
            'zaxis': {'range': [-4, 4], 'rangemode': 'tozero', 'tickmode': "linear", 'tick0': -4, 'dtick': 1},
            'aspectmode': 'cube'},
        margin={'autoexpand': False},
        autosize=False,
        width=600,
        height=600)

    fig.add_trace(
        go.Scatter3d(
            {
                "x": next_rotation_data.df["x"],
                "y": next_rotation_data.df["y"],
                "z": next_rotation_data.df["z"],
            },
            name="q X q' = q''",
            mode="markers",
            marker=dict(size=POINT_SIZE, opacity=OPACITY, color="blue"),
        )
    )

    fig.add_trace(
        go.Scatter3d(
            {"x": [point_1.x], "y": [point_1.y], "z": [point_1.z]},
            name=f"point_1: {point_1.x}, {point_1.y}, {point_1.z}",
            mode="markers",
            marker=dict(size=POINT_SIZE, opacity=1, color="red"),
        )
    )
        
    fig.add_trace(
        go.Scatter3d(
            {"x": [point_2.x], "y": [point_2.y], "z": [point_2.z]},
            name=f"point_2: {point_2.x}, {point_2.y}, {point_2.z}",
            mode="markers",
            marker=dict(size=POINT_SIZE, opacity=1, color="red"),
        )
    )
    
    image_file = f"{output}.{i}.png"
    fig.write_image(image_file)
    print(f"created: {image_file}")
    time += dt

command = f"convert {output}.*png {output}.gif;"
print(f"running: {command}", flush=True)
os.system(command)
