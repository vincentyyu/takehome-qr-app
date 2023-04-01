from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output

# Read in corresponding dataframes
fea_dir = Path("data/04_feature")
corr_df = pd.read_feather(fea_dir / "master_df.feather")
agg_df = pd.read_feather(fea_dir / "agg_by_freq.feather")

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Design dashboard components
app.layout = html.Div(
    [
        dcc.Tabs(
            id="dashboard-tabs",
            value="tab-1",
            children=[
                # Correlation dashboard
                dcc.Tab(
                    label="Correlation Analysis",
                    children=[
                        dbc.Container(
                            html.Div(
                                [
                                    html.H2("Dashboard 1: Correlations"),
                                    html.Label("Company Name:"),
                                    dcc.Dropdown(
                                        id="company-dropdown",
                                        options=[
                                            {"label": c, "value": c}
                                            for c in corr_df["company_name"].unique()
                                        ],
                                        value=corr_df["company_name"].unique()[0],
                                    ),
                                    html.Label("Start Date:"),
                                    dcc.DatePickerSingle(
                                        id="start-date", date=corr_df["date"].min()
                                    ),
                                    html.Label("End Date:"),
                                    dcc.DatePickerSingle(
                                        id="end-date", date=corr_df["date"].max()
                                    ),
                                    dcc.Graph(id="corr-heatmap"),
                                    dash_table.DataTable(id="correlation-data-table"),
                                ]
                            ),
                        )
                    ],
                ),
                # Historical Trend Dashboard
                dcc.Tab(
                    label="Historical Trend",
                    children=[
                        dbc.Container(
                            html.Div(
                                [
                                    html.H2("Dashboard 2: Historical Trend"),
                                    html.Label("Companies:"),
                                    dcc.Dropdown(
                                        id="company-dropdown2",
                                        options=[
                                            {
                                                "label": company_name,
                                                "value": company_name,
                                            }
                                            for company_name in agg_df[
                                                "company_name"
                                            ].unique()
                                        ],
                                        multi=True,
                                        value=[agg_df["company_name"].unique()[0]],
                                    ),
                                    html.Label("Analysis Metric:"),
                                    dcc.Dropdown(
                                        id="metric-dropdown",
                                        options=[
                                            {"label": col, "value": col}
                                            for col in agg_df.columns
                                            if col
                                            # TODO: this should be
                                            # dynamically controlled
                                            not in [
                                                "date",
                                                "company_name",
                                                "symbol",
                                                "year",
                                                "quarter",
                                                "month",
                                                "week",
                                                "dt_label",
                                            ]
                                        ],
                                        value="price_mean",
                                    ),
                                    html.Label("Analysis Frequency:"),
                                    dcc.Dropdown(
                                        id="frequency-dropdown",
                                        options=[
                                            {"label": "Yearly", "value": "Y"},
                                            {"label": "Quarterly", "value": "Q"},
                                            {"label": "Monthly", "value": "M"},
                                            {"label": "Weekly", "value": "W"},
                                            {"label": "Daily", "value": "D"},
                                        ],
                                        value="Q",
                                    ),
                                    html.Label("Start Date:"),
                                    dcc.DatePickerSingle(
                                        id="start-date2", date=corr_df["date"].min()
                                    ),
                                    html.Label("End Date:"),
                                    dcc.DatePickerSingle(
                                        id="end-date2", date=corr_df["date"].max()
                                    ),
                                    dcc.Graph(id="historical-trend"),
                                ]
                            ),
                        )
                    ],
                ),
                # Point-to-point comparison dashboard
                dcc.Tab(
                    label="Point Comparison",
                    children=[
                        dbc.Container(
                            html.Div(
                                [
                                    html.H2("Dashboard 3: Point-to-Point Comparison"),
                                    html.Label("Companies:"),
                                    dcc.Dropdown(
                                        id="company-dropdown3",
                                        options=[
                                            {
                                                "label": company_name,
                                                "value": company_name,
                                            }
                                            for company_name in agg_df[
                                                "company_name"
                                            ].unique()
                                        ],
                                        value=agg_df["company_name"].unique()[0],
                                    ),
                                    html.Label("Analysis Metric:"),
                                    dcc.Dropdown(
                                        id="metric-dropdown2",
                                        options=[
                                            {"label": col, "value": col}
                                            for col in agg_df.columns
                                            if col
                                            not in [
                                                "date",
                                                "company_name",
                                                "symbol",
                                                "year",
                                                "quater",
                                                "month",
                                                "week",
                                            ]
                                        ],
                                        value="price_mean",
                                    ),
                                    html.Label("Analysis Frequency:"),
                                    dcc.Dropdown(
                                        id="frequency-dropdown2",
                                        options=[
                                            {"label": "Yearly", "value": "Y"},
                                            {"label": "Quarterly", "value": "Q"},
                                            {"label": "Monthly", "value": "M"},
                                            {"label": "Weekly", "value": "W"},
                                            {"label": "Daily", "value": "D"},
                                        ],
                                        value="Q",
                                    ),
                                    html.Label("Point 1:"),
                                    dcc.Dropdown(
                                        id="datapoint-dropdown", options=[], value=None
                                    ),
                                    html.Label("Point 2:"),
                                    dcc.Dropdown(
                                        id="datapoint-dropdown2", options=[], value=None
                                    ),
                                    dcc.Graph(id="cmp-bar-chart"),
                                    dash_table.DataTable(id="cmp-data-table"),
                                ]
                            ),
                        )
                    ],
                ),
            ],
        )
    ]
)


# Callbacks for updating the plots
# Correlation plot
@app.callback(
    Output("corr-heatmap", "figure"),
    Output("correlation-data-table", "data"),
    Input("company-dropdown", "value"),
    Input("start-date", "date"),
    Input("end-date", "date"),
)
def update_corr_heatmap(company_name, start_date, end_date):
    # Filter data to specific company and time range
    filtered_df = corr_df[
        (corr_df["company_name"] == company_name)
        & (corr_df["date"] >= start_date)
        & (corr_df["date"] <= end_date)
    ]

    # Calculate correlation, removing self-correlation
    corr = filtered_df.corr(numeric_only=True)
    np.fill_diagonal(corr.values, None)

    fig = px.imshow(corr, x=corr.columns, y=corr.columns)
    return fig, corr.to_dict("records")


# Historical trend plot
@app.callback(
    Output("historical-trend", "figure"),
    Input("company-dropdown2", "value"),
    Input("frequency-dropdown", "value"),
    Input("metric-dropdown", "value"),
    Input("start-date2", "date"),
    Input("end-date2", "date"),
)
def update_historical_trend(
    selected_companies, selected_freq, selected_metric, start_date, end_date
):
    # Filter data to selected subset only
    filtered_df = agg_df[
        (agg_df["company_name"].isin(selected_companies))
        & (agg_df["agg_freq"] == selected_freq)
        & (agg_df["date"] >= start_date)
        & (agg_df["date"] <= end_date)
    ][["company_name", "dt_label", selected_metric]]

    # Add lineplot for each company
    traces = []
    for company in selected_companies:
        traces.append(
            go.Scatter(
                x=filtered_df[filtered_df["company_name"] == company]["dt_label"],
                y=filtered_df[filtered_df["company_name"] == company][selected_metric],
                mode="lines",
                name=company,
            )
        )

    return {
        "data": traces,
        "layout": go.Layout(
            xaxis={"title": "Time Period"},
            yaxis={"title": selected_metric},
            title="Historical Trend",
        ),
    }


# Point-to-point comparison
# Make point selection dropdown conditional on frequency selection
@app.callback(
    Output("datapoint-dropdown", "options"),
    Output("datapoint-dropdown2", "options"),
    Input("frequency-dropdown2", "value"),
)
def update_datapoint_dropdown_options(selected_freq):
    options = []
    if selected_freq:
        options = [
            {"label": label, "value": label}
            for label in agg_df[agg_df["agg_freq"] == selected_freq][
                "dt_label"
            ].unique()
        ]
    return options, options


@app.callback(
    Output("cmp-bar-chart", "figure"),
    Output("cmp-data-table", "data"),
    Input("company-dropdown3", "value"),
    Input("frequency-dropdown2", "value"),
    Input("metric-dropdown2", "value"),
    Input("datapoint-dropdown", "value"),
    Input("datapoint-dropdown2", "value"),
)
def update_comparison_chart(
    selected_company, selected_freq, selected_metric, data_point_1, data_point_2
):
    if data_point_1 is None or data_point_2 is None:
        return go.Figure(), []

    # Filter data to selected datapoints
    selected_data = agg_df[
        (agg_df["company_name"] == selected_company)
        & (agg_df["agg_freq"] == selected_freq)
        & (agg_df["dt_label"].isin([data_point_1, data_point_2]))
    ]

    # Create bar plot
    bar_chart = px.bar(
        selected_data,
        x="dt_label",
        y=selected_metric,
        text=selected_metric,
        color="company_name",
        barmode="group",
    )
    bar_chart.update_xaxes(title_text="Time Period")

    # Find difference statistics
    point_diff = _find_point_diff(selected_data, selected_metric)

    return bar_chart, point_diff.to_dict("records")


def _find_point_diff(df: pd.DataFrame, selected_metric: str) -> pd.DataFrame:
    # Transpose the datapoints for readability
    df = df[["dt_label", selected_metric]].set_index("dt_label").T

    points = df.columns.to_list()

    # Only calculate the difference with two points
    if len(points) == 2:
        data_pt_1, data_pt_2 = points
        df["pct_diff"] = ((df.pct_change(axis=1)[data_pt_2]) * 100).round(2).astype(
            str
        ) + "%"
        df["diff"] = (df[data_pt_2] - df[data_pt_1]).round(2)

    return df


if __name__ == "__main__":
    app.run_server(debug=True)
