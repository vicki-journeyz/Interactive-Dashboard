from dash import dash_table, dcc, html, Input, Output

import dash
import pandas as pd
import plotly.express as px

# Load the processed data
df = pd.read_csv("Transformed_Key_Usage_Features_Report.csv")  # Assuming it's saved

# Initialize the Dash app
app = dash.Dash(__name__)
# Layout
app.layout = html.Div(
    [
        html.H1("Usage and Business Value Dashboard"),
        html.Div(
            [
                dcc.Dropdown(
                    id="label-dropdown",
                    options=[{"label": l, "value": l} for l in df["Labels"].unique()],
                    value=df["Labels"].unique()[0],
                    multi=False,
                    placeholder="Select Label",
                    style={"width": "50%", "fontSize": "20px", "padding": "1px"},
                ),
                dcc.Dropdown(
                    id="year-dropdown",
                    options=[{"label": y, "value": y} for y in df["Year"].unique()],
                    value=df["Year"].unique()[0],
                    multi=False,
                    placeholder="Select Year",
                    style={"width": "40%", "fontSize": "20px", "padding": "1px"},
                ),
                dcc.Dropdown(
                    id="category-dropdown",
                    options=[{"label": c, "value": c} for c in df["Category"].unique()],
                    value=df["Category"].unique()[0],
                    multi=False,
                    placeholder="Select Category",
                    style={"width": "40%", "fontSize": "20px", "padding": "1px"},
                ),
            ],
            style={"display": "flex", "gap": "8px"},
        ),
        dcc.Graph(id="bar-chart"),
        dash_table.DataTable(
            id="pivot-table",
            columns=[{"name": i, "id": i} for i in ["Feature", "Usage"]],
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"},
        ),
    ]
)


# Callbacks to update graphs and table
@app.callback(
    [Output("bar-chart", "figure"), Output("pivot-table", "data")],
    [
        Input("label-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("category-dropdown", "value"),
    ],
)
def update_dashboard(selected_label, selected_year, selected_category):
    filtered_df = df[
        (df["Labels"] == selected_label)
        & (df["Year"] == selected_year)
        & (df["Category"] == selected_category)
    ]

    # Bar Chart
    bar_fig = px.bar(
        filtered_df,
        x="Feature",
        y="Usage",
        title=f"Usage for {selected_label} ({selected_year}, {selected_category})",
        labels={"Usage": "Sum of Usage", "Feature": "Feature"},
        text_auto=True,
    )

    # Pivot Table Data
    table_data = filtered_df[["Feature", "Usage"]].to_dict("records")

    return bar_fig, table_data


# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
