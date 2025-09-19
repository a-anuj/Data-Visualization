import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# ----------------------
# Load dataset
# ----------------------
df = pd.read_csv("retail_sales_dataset.csv")

# Ensure Date column is datetime & extract Month
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.strftime("%b")

# ----------------------
# Dash App
# ----------------------
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Retail Sales Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Label("Filter by Product Category:"),
        dcc.Dropdown(
            options=[{"label": c, "value": c} for c in df["Product Category"].unique()],
            value=None,
            id="category-filter",
            placeholder="Beauty, Clothing..."
        ),
        html.Label("Filter by Gender:"),
        dcc.Dropdown(
            options=[{"label": g, "value": g} for g in df["Gender"].unique()],
            value=None,
            id="gender-filter",
            placeholder="Select gender"
        )
    ], style={"width": "40%", "margin": "auto"}),

    html.Div(id="summary-cards", style={
        "display": "flex",
        "justifyContent": "space-around",
        "margin": "20px 0"
    }),




    # Charts
    html.Div([
        dcc.Graph(id="line-chart", style={"width": "48%", "display": "inline-block"}),
        dcc.Graph(id="bar-chart", style={"width": "48%", "display": "inline-block"}),
    ]),
    html.Div([
        dcc.Graph(id="pie-chart", style={"width": "60%", "margin": "auto"})
    ])
])


# ----------------------
# Callbacks
# ----------------------
@app.callback(
    [Output("line-chart", "figure"),
     Output("bar-chart", "figure"),
     Output("pie-chart", "figure"),
     Output("summary-cards", "children")],
    [Input("category-filter", "value"),
     Input("gender-filter", "value")]
)
def update_charts(category, gender):
    dff = df.copy()

    if category:
        dff = dff[dff["Product Category"] == category]
    if gender:
        dff = dff[dff["Gender"] == gender]

    # Line Chart: Monthly Sales Trend
    line_data = dff.groupby("Month", as_index=False)["Total Amount"].sum()
    line_fig = px.line(line_data, x="Month", y="Total Amount", title="Monthly Sales Trend")

    # Bar Chart: Sales by Product Category
    bar_data = dff.groupby("Product Category", as_index=False)["Total Amount"].sum()
    bar_fig = px.bar(bar_data, x="Product Category", y="Total Amount",
                     title="Sales by Product Category")

    # Pie Chart: Distribution by Gender
    pie_data = dff.groupby("Gender", as_index=False)["Total Amount"].sum()
    pie_fig = px.pie(pie_data, names="Gender", values="Total Amount",
                     title="Sales Distribution by Gender")

    # Summary Cards
    total_sales = dff["Total Amount"].sum()
    avg_order_value = round(dff["Total Amount"].sum() / len(dff["Transaction ID"].unique()), 2)
    top_product = dff.groupby("Product Category")["Total Amount"].sum().idxmax()

    cards = [
        html.Div([
            html.H3("Total Sales"),
            html.P(f"${total_sales:,.0f}")
        ], style={"padding": "20px", "border": "1px solid #ddd", "borderRadius": "5px", "width": "25%"}),

        html.Div([
            html.H3("Avg Order Value"),
            html.P(f"${avg_order_value:,.2f}")
        ], style={"padding": "20px", "border": "1px solid #ddd", "borderRadius": "5px", "width": "25%"}),

        html.Div([
            html.H3("Top Product"),
            html.P(top_product)
        ], style={"padding": "20px", "border": "1px solid #ddd", "borderRadius": "5px", "width": "25%"})
    ]

    return line_fig, bar_fig, pie_fig, cards


if __name__ == "__main__":
    app.run(debug=True)
