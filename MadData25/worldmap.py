import dash
import pandas as pd
from dash import html, dcc, Output, Input
from flask import Flask, request
from flask_cors import CORS

# Load country data
df = pd.read_csv("/Users/aashishmankala/Desktop/MadData25/All_Countries.csv")

# Flask server for Dash
server = Flask(__name__)
CORS(server)
app = dash.Dash(__name__, server=server)

# Store selected country globally
selected_country = "None"

# Flask route to receive country click events
@server.route("/select_country", methods=["POST"])
def select_country():
    global selected_country
    selected_country = request.args.get("country", "United States")
    print("Received country:", selected_country)
    return "", 204 

# Dash layout with `dcc.Interval` for periodic updates
app.layout = html.Div([
    html.Iframe(src="/assets/map.html", width="100%", height="600px", id="map-frame"),
    html.Div(id="country-info", style={"margin-top": "20px", "font-size": "20px"}),
    dcc.Interval(id="interval-update", interval=1000, n_intervals=0)
])

# Callback to refresh country info
@app.callback(
    Output("country-info", "children"),
    Input("interval-update", "n_intervals")
)
def display_country_info(_):
    global selected_country
    if selected_country == "None":
        return "Click on a country to see details."

    country_data = df[df["country"] == selected_country]
    
    if country_data.empty:
        return f"No data available for {selected_country}."

    return f"""
    Country: {selected_country}
    Capital: {country_data.iloc[0]['capital_city']}
    Population: {country_data.iloc[0]['population']:,}
    """

if __name__ == "__main__":
    app.run_server(debug=False)
