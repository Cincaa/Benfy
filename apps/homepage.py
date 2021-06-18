from apps import constants as cst
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from app import app
from dash.dependencies import Input, Output, State

url = "https://assets2.lottiefiles.com/packages/lf20_eTaPAG.json"
options = dict(
    loop=True,
    autoplay=True,
    rendererSettings=dict(preserveAspectRatio="xMidYMid slice"),
)


layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.Img(
                    src="https://i.ibb.co/stCNz8K/isaac-smith-6-En-TPv-PPL6-I-unsplash-jpg.png",
                    height="700vh",
                    width="100%",
                    style={
                        "display": "block",
                        "margin-left": "auto",
                        "margin-right": "auto",
                    },
                ),
                style={"z-index": "-1", "position": "relative"},
            )
        ),
        dbc.Row(dbc.Col(html.H3("Despre"), style={"text-align": "center"})),
        dbc.Row(
            dbc.Col(
                dbc.CardBody(
                    [
                        html.Blockquote(
                            [
                                dcc.Markdown(cst.HOMEPAGE_DESPRE_TEXT, dedent=False),
                            ],
                            className="blockquote",
                        )
                    ]
                ),
                width={"size": 10, "offset": 1},
            )
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Img(
                        src="https://i.ibb.co/BC8dt2Y/picography-notepad-pen-desk-small-1-768x512.jpg",
                        width="100%",
                        height="750vh",
                        style={
                            "display": "block",
                            "margin-left": "auto",
                            "opacity": "100%",
                            "margin-right": "auto",
                            "z-index": "1",
                        },
                    ),
                    dbc.Col(
                        html.Blockquote(
                            [
                                html.Br(),
                                dcc.Markdown(
                                    cst.HOMEPAGE_ISTORIC_TEXT1,
                                    dedent=False,
                                    style={
                                        "font-size": "16px",
                                        "background-color": "rgb(0,0,0,0.3)",
                                    },
                                ),
                            ],
                            style={
                                "overflow": "hidden",
                                "position": "absolute",
                                "padding-left": "15px",
                                "bottom": -5,
                                "color": "#f1f1f1",
                                "height": "750px",
                                "text-align": "justify",
                            },
                        ),
                        width=8,
                    ),
                    dbc.Col(
                        html.Blockquote(
                            [
                                html.Br(),
                                dcc.Markdown(
                                    cst.HOMEPAGE_ISTORIC_TEXT2,
                                    dedent=False,
                                    style={
                                        "font-size": "16px",
                                        "background-color": "rgb(0,0,0,0.3)",
                                    },
                                ),
                            ],
                            style={
                                "overflow": "hidden",
                                "position": "absolute",
                                "bottom": -549,
                                "padding-right": "15px",
                                "color": "#f1f1f1",
                                "height": "750px",
                                "text-align": "justify",
                            },
                        ),
                        width={"size": 8, "offset": 4},
                    ),
                ],
                style={},
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Aplicabilitate", style={"text-align": "center"}),
                        dcc.Markdown(
                            cst.HOMEPAGE_APLICABILITATE_TEXT1,
                            dedent=False,
                            style={"padding": "15px"},
                        ),
                    ],
                    width=12,
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            children=html.Img(
                                src="https://i.ibb.co/DWSyq5g/Pngtree-money-bag-icon-moneybag-cartoon-4992604.png",
                                style={"height": "120px"},
                            ),
                            id="buttonFinanciar",
                            style={
                                "background-color": "white",
                                "position": "absolute",
                                "left": "30%",
                            },
                        ),
                        dbc.Collapse(
                            children=dbc.Card(
                                dbc.CardBody(cst.HOMEPAGE_APLICABILITATE_TEXT2)
                            ),
                            id="textFinanciar",
                            style={"position": "absolute", "top": "135px"},
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            children=html.Img(
                                src="https://i.ibb.co/p0ydZdJ/Pngtree-mbe-icon-camera-4683487.png",
                                style={"height": "120px", "width": "120px"},
                            ),
                            id="buttonSocio",
                            style={
                                "background-color": "white",
                                "position": "absolute",
                                "left": "30%",
                            },
                        ),
                        dbc.Collapse(
                            children=dbc.Card(
                                dbc.CardBody(cst.HOMEPAGE_APLICABILITATE_TEXT4)
                            ),
                            id="textSocio",
                            style={"position": "absolute", "top": "135px"},
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            children=html.Img(
                                src="https://i.ibb.co/GCQKYQm/Pngtree-campaign-political-politics-vote-abstract-4781302.png",
                                style={"height": "120px", "width": "120px"},
                            ),
                            id="buttonImg",
                            style={
                                "background-color": "white",
                                "position": "absolute",
                                "left": "30%",
                            },
                        ),
                        dbc.Collapse(
                            children=dbc.Card(
                                dbc.CardBody(cst.HOMEPAGE_APLICABILITATE_TEXT3)
                            ),
                            id="textImg",
                            style={"position": "absolute", "top": "135px"},
                        ),
                    ],
                    width=4,
                ),
            ]
        ),
    ]
)


@app.callback(
    Output("textFinanciar", "is_open"),
    Input("buttonFinanciar", "n_clicks"),
)
def collapse_text(n):
    if n:
        if n % 2:
            return True
        return False


@app.callback(
    Output("textSocio", "is_open"),
    Input("buttonSocio", "n_clicks"),
)
def collapse_text(n):
    if n:
        if n % 2:
            return True
        return False


@app.callback(
    Output("textImg", "is_open"),
    Input("buttonImg", "n_clicks"),
)
def collapse_text(n):
    if n:
        if n % 2:
            return True
        return False
