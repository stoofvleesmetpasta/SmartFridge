import json
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_daq as daq
import plotly.graph_objs as go

# Dash app setup
app = Dash(__name__)
app.title = "Duvel Cooling Simulation Dashboard"

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("Duvel Cooling Simulation Dashboard", style={
            "textAlign": "center",
            "marginBottom": "30px",
            "color": "#fff",
            "fontFamily": "Arial, sans-serif"
        }),
    ], style={
        "backgroundColor": "#1a1a1a",
        "padding": "20px",
        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.2)"
    }),

    html.Div([
        # Status Card
        html.Div([
            html.H3("Duvel Status", style={
                "textAlign": "center",
                "color": "#333",
                "fontFamily": "Arial, sans-serif"
            }),
            html.Div(id="live-update-text", style={
                "fontSize": "18px",
                "margin": "10px 0",
                "textAlign": "center",
                "color": "#555",
                "fontFamily": "Arial, sans-serif"
            }),
        ], style={
            "padding": "20px",
            "backgroundColor": "#ffffff",
            "borderRadius": "12px",
            "boxShadow": "0px 6px 12px rgba(0, 0, 0, 0.15)",
            "marginBottom": "30px",
            "border": "1px solid #e0e0e0"
        }),

        # Indicator Card
        html.Div([
            daq.Indicator(
                id="bottle-indicator",
                label={"label": "Duvel Alarm", "style": {"fontSize": "18px", "fontFamily": "Arial, sans-serif", "color": "#333"}},
                size=80,
            ),
            html.Div(id="bottle-indicator-status", style={
                "fontSize": "18px",
                "fontWeight": "bold",
                "marginTop": "10px",
                "textAlign": "center",
                "color": "#555",
                "fontFamily": "Arial, sans-serif"
            }),
        ], style={
            "textAlign": "center",
            "padding": "20px",
            "backgroundColor": "#ffffff",
            "borderRadius": "12px",
            "boxShadow": "0px 6px 12px rgba(0, 0, 0, 0.15)",
            "marginBottom": "30px",
            "border": "1px solid #e0e0e0"
        }),

        # Line Chart Card
        html.Div([
            html.H3("Temperatuur", style={
                "textAlign": "center",
                "color": "#333",
                "fontFamily": "Arial, sans-serif"
            }),
            dcc.Graph(id="temperature-line-chart")
        ], style={
            "padding": "20px",
            "backgroundColor": "#ffffff",
            "borderRadius": "12px",
            "boxShadow": "0px 6px 12px rgba(0, 0, 0, 0.15)",
            "marginBottom": "30px",
            "border": "1px solid #e0e0e0"
        }),

    ], style={"width": "60%", "margin": "20px auto", "fontFamily": "Arial, sans-serif"}),

    # Interval component for live updates
    dcc.Interval(
        id="interval-component",
        interval=500,
        n_intervals=0,
    ),
], style={
    "background": "url('/assets/background.jpg') no-repeat center center fixed",
    "backgroundSize": "cover",
    "minHeight": "100vh",
    "padding": "20px 0"
})

@app.callback(
    [Output("live-update-text", "children"),
     Output("bottle-indicator", "value"),
     Output("bottle-indicator-status", "children"),
     Output("bottle-indicator", "color"),
     Output("temperature-line-chart", "figure")],
    [Input("interval-component", "n_intervals")]
)
def update_dashboard(n):
    try:
        # Read data from JSON file
        with open("simulation_data.json", "r") as file:
            simulation_data = json.load(file)

        # Get the most recent entry and temperature history
        if isinstance(simulation_data, list) and simulation_data:
            latest_data = simulation_data[-1]
            temp = latest_data["temperature"]
            bottles = latest_data["bottle_number"]
            cooling = latest_data["cooling_power"]

            # Extract temperatures for line chart
            temperatures = [entry["temperature"] for entry in simulation_data]

            # Text to display
            text = f"Temperatuur: {temp:.2f} °C | Flesjes: {bottles} | Koelvermogen: {cooling}"

            # Red light logic
            low_bottle_alert = bottles <= 2
            status_text = "PANIC" if low_bottle_alert else "chill"
            color = "red" if low_bottle_alert else "green"

            # Create line chart figure
            figure = go.Figure()
            figure.add_trace(go.Scatter(
                x=list(range(1, len(temperatures) + 1)),
                y=temperatures,
                mode='lines+markers',
                name='Temperature',
                line=dict(color='blue', width=2),
                marker=dict(size=8)
            ))
            figure.update_layout(
                title="Laatste 10 Temperatuurmetingen",
                xaxis_title="Reading Index",
                yaxis_title="Temperature (°C)",
                margin=dict(l=20, r=20, t=40, b=20),
                template="plotly_white"
            )

            return text, low_bottle_alert, status_text, color, figure
        else:
            # Default empty figure
            empty_figure = go.Figure()
            empty_figure.update_layout(
                title="No Data Available",
                margin=dict(l=20, r=20, t=40, b=20),
                template="plotly_white"
            )
            return "No simulation data available...", False, "OFF (No Data)", "gray", empty_figure

    except FileNotFoundError:
        empty_figure = go.Figure()
        empty_figure.update_layout(
            title="File Not Found",
            margin=dict(l=20, r=20, t=40, b=20),
            template="plotly_white"
        )
        return "Waiting for simulation data...", False, "OFF (No Data)", "gray", empty_figure
    except json.JSONDecodeError:
        empty_figure = go.Figure()
        empty_figure.update_layout(
            title="Error in Data Format",
            margin=dict(l=20, r=20, t=40, b=20),
            template="plotly_white"
        )
        return "Error reading simulation data...", False, "OFF (Error)", "gray", empty_figure

if __name__ == "__main__":
    app.run_server(debug=True)
