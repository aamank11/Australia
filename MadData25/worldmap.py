import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Flask, request

# Load country data
data = pd.read_csv("/Users/aashishmankala/Desktop/MadData25/All_Countries.csv")  # Ensure this file exists with 'country' and 'info' columns

# Create Flask server for Dash
server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Store hovered country
hovered_country = "None"

# Flask route to handle hover events
@server.route("/hover_country", methods=["POST"])
def hover_country():
    global hovered_country
    hovered_country = request.args.get("country", "None")
    return "", 204  # No content response

# Layout
app.layout = html.Div([
    html.Embed(src="/Users/aashishmankala/Desktop/MadData25/assets/world.svg", type="image/svg+xml", width="100%", height="600px", id="world-map"),
    html.Div(id="country-info", style={"margin-top": "20px", "font-size": "20px"})
])

# Dash callback to update country info
@app.callback(
    Output("country-info", "children"),
    Input("world-map", "n_clicks")  # Refresh on click to show new data
)
def display_country_info(clickData):
    if clickData:
        country_name = clickData["points"][0]["location"]
        country_data = data[data["country"] == country_name]

        if not country_data.empty:
            details = f"""
            Country: {country_name}
            Capital: {country_data.iloc[0]['capital_city']}
            Population: {country_data.iloc[0]['population']:,}
            GDP: ${country_data.iloc[0]['gdp']:,}
            Life Expectancy: {country_data.iloc[0]['life_expectancy']} years
            Political Leader: {country_data.iloc[0]['political_leader']}
            """
            return html.Pre(details)  # Preformatted text for better readability

    return "Click on a country to see details."

# Run the app
if __name__ == "__main__":
    app.run_server(debug=False)


