from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd


app = Dash(__name__)

iris = px.data.iris()
num_columns = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
]
species_values = sorted(iris["species"].unique())


app.layout = html.Div([
    html.H2("Iris Dashboard"),
    html.Div([
        html.Div([
            html.Label("X-axis"),
            dcc.Dropdown(
                id="x-col",
                options=[{"label": c, "value": c} for c in num_columns],
                value="sepal_length",
                clearable=False,
            ),
        ], style={"flex": 1, "minWidth": 220, "marginRight": 8}),
        html.Div([
            html.Label("Y-axis"),
            dcc.Dropdown(
                id="y-col",
                options=[{"label": c, "value": c} for c in num_columns],
                value="sepal_width",
                clearable=False,
            ),
        ], style={"flex": 1, "minWidth": 220, "marginRight": 8}),
        html.Div([
            html.Label("Species"),
            dcc.Dropdown(
                id="species",
                options=[{"label": s, "value": s} for s in species_values],
                value=species_values,
                multi=True,
            ),
        ], style={"flex": 1, "minWidth": 240}),
    ], style={"display": "flex", "flexWrap": "wrap", "marginBottom": 12}),

    html.Div([
        html.Div([dcc.Graph(id="scatter")], style={"flex": 1, "minWidth": 360, "marginRight": 8}),
        html.Div([dcc.Graph(id="hist")], style={"flex": 1, "minWidth": 360}),
    ], style={"display": "flex", "flexWrap": "wrap", "marginBottom": 8}),

    html.Div([
        html.Div([dcc.Graph(id="box")], style={"flex": 1, "minWidth": 360, "marginRight": 8}),
        html.Div([dcc.Graph(id="pair")], style={"flex": 1, "minWidth": 360}),
    ], style={"display": "flex", "flexWrap": "wrap"}),
])


@app.callback(
    Output("scatter", "figure"),
    Output("hist", "figure"),
    Output("box", "figure"),
    Output("pair", "figure"),
    Input("x-col", "value"),
    Input("y-col", "value"),
    Input("species", "value"),
)
def update_figures(x_col: str, y_col: str, species_selected: list[str]):
    df = iris.copy()
    if species_selected:
        df = df[df["species"].isin(species_selected)]

    scatter_fig = px.scatter(
        df, x=x_col, y=y_col, color="species", height=420,
        title=f"Scatter: {x_col} vs {y_col}", template="plotly",
    )

    hist_fig = px.histogram(
        df, x=x_col, color="species", barmode="overlay", nbins=25,
        opacity=0.65, height=420, title=f"Histogram: {x_col}", template="plotly",
    )

    box_fig = px.box(
        df, x="species", y=y_col, points="all", height=420,
        title=f"Box: {y_col} by species", template="plotly",
    )

    pair_fig = px.scatter_matrix(
        df, dimensions=num_columns, color="species", height=420,
        title="Scatter Matrix", template="plotly",
    )

    return scatter_fig, hist_fig, box_fig, pair_fig


if __name__ == "__main__":
    app.run(debug=True)


