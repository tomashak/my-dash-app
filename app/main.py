import dash
from dash import html
from layouts.index import get_layout
from callbacks.index import register_callbacks

# Create the Dash app
app = dash.Dash(__name__)

# Set the layout of the app
app.layout = html.Div(children=get_layout())

# Register the callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)