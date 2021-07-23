# *****************************************************************************
#
# Copyright (c) 2021, the iexexamples authors.
#
# This file is part of the iexexamples library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
import plotly.graph_objects as go


def yieldCurveSurface(df):
    fig = go.Figure(
        data=[
            go.Surface(
                x=df.columns,
                y=df.index.values,
                z=df.values,
                colorscale=[
                    [0, "rgb(230,245,254)"],
                    [0.3, "rgb(123,171,203)"],
                    [0.6, "rgb(40,119,174)"],
                    [1, "rgb(37,61,81)"],
                ],
                lighting={
                    "ambient": 0.95,
                    "diffuse": 0.99,
                    "fresnel": 0.01,
                    "roughness": 0.01,
                    "specular": 0.01,
                },
                connectgaps=True,
                opacity=1,
            )
        ],
        layout=go.Layout(height=1000),
    )

    fig.update_layout(
        margin=dict(t=50, b=0, l=0, r=0),
        scene_camera=dict(
            # up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=1, z=-1),
            eye=dict(x=-5, y=6, z=3),
        ),
        scene=dict(
            aspectmode="manual",
            aspectratio=dict(x=5, y=7, z=2),
            xaxis=dict(
                tickmode="linear",
                tick0=df.columns[0],
                dtick=1.0,
                title="Curve",
                type="category",
                showspikes=False,
            ),
            zaxis=dict(
                type="log",
                title="Value",
            ),
            yaxis=dict(
                title="Date",
            ),
        ),
    )
    return fig


def lineOverlay(figure, df, name):
    figure.add_trace(
        go.Scatter3d(
            x=[name] * len(df),
            y=df.index.values,
            z=df["value"].values,
            marker=dict(
                size=4,
                color="darkblue",
            ),
            line=dict(color="darkblue", width=5),
            name=name,
        )
    )
