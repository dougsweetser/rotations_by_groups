import streamlit as st
import plotly.graph_objects as go
import textwrap

from Qs import (
    Q,
    Qs,
    qrandom,
    qrandoms,
    rotation,
    squares,
    norm_squareds,
    permutation,
    all_permutations,
    rotation_only,
    generate_Qs,
    generate_QQs,
    next_rotation,
    next_rotation_randomized,
)


# Sidebar setup.
next_rotation_flag = st.sidebar.checkbox(label="q X q' = q'' ", value=True)
next_rotation_randomized_flag = st.sidebar.checkbox(label="Randomized(q X q' = q'')", value=True)
permutation_flag = st.sidebar.checkbox(label="all permutations", value=True)

dim = st.sidebar.slider(label="Dimensions", min_value=10, max_value=500, value=75)

time = st.sidebar.slider(label="t", min_value=0.1, max_value=100.0, value=2.3)

show_code = st.sidebar.checkbox("Show code", False)

# The calculation - make a DataFrame
point_1 = Q([time, 1, 2, 3])
point_2 = Q([time, 1, 3, 2])

next_rotation_data = generate_QQs(next_rotation, point_1, point_2, dim=dim)
next_rotation_randomized_data = generate_QQs(next_rotation_randomized, point_1, point_2, dim=dim)

all_ps = all_permutations(point_1)

ok_ps = []

for all_p_q in all_ps.qs:
    if all_p_q.t == point_1.t:
        ok_ps.append(all_p_q)
        
permutation_data = Qs(ok_ps)


# collect stats
next_rotation_data_squares = squares(next_rotation_data)
next_rotation_data_norm_squares = norm_squareds(next_rotation_randomized_data)

next_rotation_randomized_data_squares = squares(next_rotation_randomized_data)
next_rotation_randomized_data_norm_squares = norm_squareds(next_rotation_randomized_data)

permutation_data_squares = squares(permutation_data)
permutation_data_norm_squares = norm_squareds(permutation_data)



# Main page.

st.title("Rotations by Groups")

fig = go.Figure()
go.Layout()
POINT_SIZE = 6
OPACITY = 0.8

if next_rotation_flag:
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

if next_rotation_randomized_flag:
    fig.add_trace(
        go.Scatter3d(
            {
                "x": next_rotation_randomized_data.df["x"],
                "y": next_rotation_randomized_data.df["y"],
                "z": next_rotation_randomized_data.df["z"],
            },
            name="Randomized(q X q') = q''",
            mode="markers",
            marker=dict(size=POINT_SIZE, opacity=OPACITY, color="pink"),
        )
    )

if permutation_flag:
    fig.add_trace(
        go.Scatter3d(
            {
                "x": permutation_data.df["x"],
                "y": permutation_data.df["y"],
                "z": permutation_data.df["z"],
            },
            name="txyz -> tzyx",
            mode="markers",
            marker=dict(size=POINT_SIZE, opacity=OPACITY, color="orange"),
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
    
if next_rotation_flag or next_rotation_randomized_flag:
    fig.add_trace(
        go.Scatter3d(
            {"x": [point_2.x], "y": [point_2.y], "z": [point_2.z]},
            name=f"point_2: {point_2.x}, {point_2.y}, {point_2.z}",
            mode="markers",
            marker=dict(size=POINT_SIZE, opacity=1, color="red"),
        )
    )
    
# Make it a fixed cube.
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

st.write(fig)

st.markdown("""## Time Slider Fun

I thought the scalar term would be boring to play with. I think of it as time.
When it is tiny, the q x q' froms a circle. That circle moves over one of the 
red dots and tries to get closer, even if it has to break up. It forms a 6
point start that bends and forms a small spiral. Odd, but true numerically.

A program was written to make this animation, rotations_by_groups_time_lapse.py.
""")

st.image("images/d6k.gif")

def show_file(label: st, file_name: str, code: bool = False):
    """
    Utility to show contents of a file

    Args:
        label: str
        file_name: str
        code:

    Return: None

    """
    st.markdown("&nbsp ")
    st.markdown(f"### {label}")
    st.write(f"{file_name}")
    with open(f"{file_name}", "r") as file:
        file_lines = file.readlines()

    if code:
        st.code(textwrap.dedent("".join(file_lines[1:])))
    else:
        st.markdown(textwrap.dedent("".join(file_lines[1:])))


if show_code:
    show_file("Streamlit Webapp code", __file__, code=True)
    show_file("Qs.py library code", "Qs.py", code=True)
    show_file("rotations_by_groups_time_lapse.py", "rotations_by_groups_time_lapse.py", code=True)
