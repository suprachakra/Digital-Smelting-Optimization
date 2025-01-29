"""
app.py
A minimal Plotly Dash app for the MetalX Smelting project.
Shows near real-time sensor data from processed CSV.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os

app = dash.Dash(__name__)
server = app.server  # For deployment if needed

# Path to processed data
DATA_PATH = os.path.join('data','processed','sensor_data_day1_cleaned.csv')

# Layout
app.layout = html.Div([
    html.H1("MetalX Smelting Dashboard"),
    dcc.Interval(id='interval-component', interval=3000, n_intervals=0),
    html.Div(id='live-data-stats'),
    dcc.Graph(id='live-temperature-chart'),
])

@app.callback(
    [Output('live-data-stats', 'children'),
     Output('live-temperature-chart', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    if not os.path.exists(DATA_PATH):
        return ("No data found.", px.scatter(title="No Data Available"))

    # In a real environment, you might read only new rows or pull from a streaming source
    df = pd.read_csv(DATA_PATH, parse_dates=['timestamp'])
    df.sort_values('timestamp', inplace=True)

    # Let's pretend 'n' controls how many rows we display
    max_rows = min(len(df), n+5)
    sub_df = df.iloc[:max_rows]

    avg_temp = sub_df['temperature'].mean()
    stats_text = f"Current average temperature: {avg_temp:.2f} °C (rows up to {max_rows})"

    fig = px.line(sub_df, x='timestamp', y='temperature', title='Temperature Over Time')
    fig.update_layout(uirevision='dataset')  # To prevent re-scaling each interval

    return (stats_text, fig)

if __name__ == '__main__':
    app.run_server(debug=True)

