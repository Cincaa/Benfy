from app import app
from app import server
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_extensions as de

from apps import constants as cst
from apps import homepage
from apps import pop_ro
from apps import covid
from apps import ru_elections
from apps import upload

controls = dbc.Col(
    [
        html.P("Baza", style={"textAlign": "center"}),
        dcc.Input(
            id="input_range",
            type="number",
            placeholder="input with range",
            min=2,
            max=20,
            step=1,
            inputMode="numeric",
            value=10,
            style=cst.INPUT_BASE_STYLE,
        ),
        html.Br(),
        html.P("Schema de culori", style={"textAlign": "center"}),
        html.Div(
            dcc.Dropdown(
                id="my_dropdown",
                options=[
                    {"label": "Plotly", "value": 0},
                    {"label": "D3", "value": 1},
                    {"label": "G10", "value": 2},
                    {"label": "T10", "value": 3},
                    {"label": "Alphabet", "value": 4},
                    {"label": "Dark24", "value": 5},
                    {"label": "Dark2", "value": 6},
                    {"label": "Light24", "value": 7},
                    {"label": "Set1", "value": 8},
                    {"label": "Set2", "value": 9},
                    {"label": "Set3", "value": 10},
                    {"label": "Pastel", "value": 11},
                    {"label": "Pastel1", "value": 12},
                    {"label": "Pastel2", "value": 13},
                    {"label": "Antique", "value": 14},
                    {"label": "Bold", "value": 15},
                    {"label": "Prism", "value": 16},
                    {"label": "Safe", "value": 17},
                    {"label": "Vivid", "value": 18},
                ],
                optionHeight=35,  # height/space between dropdown options
                value=12,  # dropdown value selected automatically when page loads
                disabled=False,  # disable dropdown value selection
                multi=False,  # allow multiple dropdown values to be selected
                searchable=True,  # allow user-searching of dropdown values
                search_value="",  # remembers the value searched in dropdown
                placeholder="Please select...",  # gray, default text shown when no option is selected
                clearable=False,  # allow user to removes the selected value
                style=cst.DROPDOWN_STYLE,  # use dictionary to define CSS styles of your dropdown
                persistence=True,  # remembers dropdown value. Used with persistence_type
                persistence_type="session",  # remembers dropdown value selected until...
            ),
            style=cst.DROPDOWNDIV_STYLE,
        ),
        html.Br(),
        html.P("Teste de conformitate", style={"textAlign": "center"}),
        dcc.Checklist(
            id="checklist",
            options=[
                {"label": " Chi Square", "value": "CS"},
                {"label": " Kolmogorov-Smirnov", "value": "KS"},
                {"label": " Deviația d* (Distanța euclidiană)", "value": "DE"},
            ],
            value=[],
            persistence=False,
            style={"display": "flex", "flex-direction": "column", "margin-left": "11%"},
        ),
    ]
)

sidebar = dbc.Col(
    id="side-content",
    children=[html.Hr(), controls],
)

content = html.Div(id="page-content", children=[])

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=cst.LOGO, height="48px")),
                    dbc.Col(dbc.NavbarBrand("Benfy", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="/",
        ),
        dbc.Nav(
            [
                dbc.NavLink(
                    children=["Populația României"], href="/pop-ro", active="exact"
                ),
                dbc.NavLink("Prezidențiale Rusia", href="/prez-ru", active="exact"),
                dbc.NavLink("Cazuri Covid", href="/covid", active="exact"),
                dbc.NavLink("Încarcă un fișier", href="/upload", active="exact"),
            ],
            horizontal=True,
            pills=True,
        ),
    ],
    color="dark",
    dark=True,
    className="icon-bar",
)


@app.callback(
    Output("collapse", "is_open"),
    Output("sidebarGif", "url"),
    Output("divLottie", "style"),
    Output("sidebarGif", "height"),
    Output("sidebarGif", "width"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        if n % 2:
            return True, url2, {"top": "505px", "position": "sticky"}, "75%", "75%"
    return False, url, {"top": "105px", "position": "sticky"}, "30%", "30%"


url = "https://assets4.lottiefiles.com/packages/lf20_edprXU.json"
url2 = "https://assets1.lottiefiles.com/packages/lf20_r6ahcm9f.json"
options = dict(
    loop=True,
    autoplay=True,
    rendererSettings=dict(preserveAspectRatio="xMidYMid slice"),
)

app.layout = html.Div(
    children=[
        dcc.Location(id="url"),
        dbc.Row(dbc.Col(navbar, width=12)),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button(
                            "Instrumente",
                            id="collapse-button",
                            className="btn-primary",
                            color="primary",
                            style={
                                "top": "67px",
                                "left": "8%",
                                "position": "sticky",
                            },
                        ),
                        dbc.Collapse(
                            sidebar,
                            id="collapse",
                            style={
                                "top": "125px",
                                # "left": "8%",
                                "position": "sticky",
                            },
                        ),
                        html.Div(
                            de.Lottie(
                                options=options,
                                width="30%",
                                height="30%",
                                url=url,
                                id="sidebarGif",
                                isClickToPauseDisabled=True,
                            ),
                            style={
                                "top": "125px",
                                "position": "sticky",
                            },
                            id="divLottie",
                        ),
                    ],
                    width=3,
                    id="sidebar",
                ),
                dbc.Col(children=content, id="contentCol", width=9),
            ]
        ),
    ]
)

app.title = "Benfy"


@app.callback(
    Output("page-content", "children"),
    Output("sidebar", "style"),
    Output("contentCol", "width"),
    Output("checklist", "value"),
    [Input("url", "pathname")],
)
def render_page_content(pathname):
    if pathname == "/":
        return homepage.layout, {"display": "none"}, 12, []
    elif pathname == "/pop-ro":
        return pop_ro.layout, {}, 9, []
    elif pathname == "/covid":
        return covid.layout, {}, 9, []
    elif pathname == "/prez-ru":
        return ru_elections.layout, {}, 9, []
    elif pathname == "/upload":
        return upload.layout, {}, 9, []
        # If the user tries to reach a different page, return a 404 message
    return (
        (
            dbc.Jumbotron(
                [
                    html.H1("404: Not found", className="text-danger"),
                    html.Hr(),
                    html.P(f"The pathname {pathname} was not recognised..."),
                ]
            )
        ),
        {"display": "none"},
        12,
        None,
    )


if __name__ == "__main__":
    app.run_server(debug=False)
