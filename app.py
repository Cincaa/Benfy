import dash
import dash_bootstrap_components as dbc
from whitenoise import WhiteNoise

external_css = [
    dbc.themes.JOURNAL,
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_css,
    suppress_callback_exceptions=True,
)

server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root="static/")
