from apps import constants as cst
from app import app
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import change_base as cb
import numpy as np
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import json
import pathlib
from flask_caching import Cache
import scipy.stats

cache = Cache(
    app.server,
    config={
        "CACHE_TYPE": "SimpleCache",
    },
)
TIMEOUT = 0  # infinity

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../static").resolve()

with open(DATA_PATH.joinpath("Populatie_Romania.json")) as json_file:
    pop_ro_data = json.load(json_file)


@cache.memoize(timeout=TIMEOUT)
def pop_ro_fig(pop_ro_data, base, theme):
    global df2
    df2 = pd.DataFrame(
        dict(
            pop_fd=np.zeros(base - 1),
            x_graphic=[
                "Cifra " + str(i) if i < 10 else "Cifra " + chr(ord("a") + i - 10)
                for i in range(1, base)
            ],
            benford=[np.log10(1 + 1 / i) * 100 for i in range(1, base)],
        )
    )
    pop_fd = np.zeros(base - 1)
    for town in pop_ro_data:
        population = cb.decimal_to_base(town["populatie"], base)
        if population != "":
            if ord(population[0]) >= ord("a"):
                pop_fd[int(ord(population[0]) - ord("a") + 9)] += 1
            else:
                pop_fd[int(population[0]) - 1] += 1

    sum_pop = np.sum(pop_fd)
    df2["pop_fd"] = (pop_fd / sum_pop) * 100

    fig = px.bar(
        df2,
        x="x_graphic",
        y="pop_fd",
        barmode="group",
        hover_data={"x_graphic": False},
        color_discrete_sequence=cst.THEMES_LIST[theme],
    )
    fig.add_scatter(
        x=df2["x_graphic"],
        y=df2["benford"],
        line=dict(color="green"),
        name="Benford's law",
    )

    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="Percent%")

    cs = scipy.stats.chisquare(df2["pop_fd"], df2["benford"])[0]

    return fig


@app.callback(
    Output("graph_pop-Ro", "figure"),
    Input("input_range", "value"),
    Input("my_dropdown", "value"),
)
@cache.memoize(timeout=TIMEOUT)
def number_render_pop(rangeval, theme):
    if rangeval is None:
        return pop_ro_fig(pop_ro_data, 10, theme)
    else:
        return pop_ro_fig(pop_ro_data, rangeval, theme)


@app.callback(
    Output("text", "style"),
    Output("textTitle", "style"),
    Output("cardText", "color"),
    Output("cardText", "outline"),
    Input("graph_pop-Ro", "figure"),
    prevent_initial_call=True,
)
def text_apear(fig):
    if fig is not None:
        return {}, {}, "primary", True


layout = html.Div(
    [
        html.H1("Legea lui Benford pentru popula??ia Rom??niei", style=cst.TEXT_STYLE),
        html.Hr(),
        dbc.Col(
            dcc.Loading(
                id="loading", children=[dcc.Graph(id="graph_pop-Ro")], type="graph"
            )
        ),
        dbc.Col(dbc.CardGroup(id="cardgrouppop", children=[])),
        dbc.Col(
            dbc.Card(
                id="cardText",
                children=dbc.CardBody(
                    [
                        html.H4(
                            id="textTitle",
                            children="Interpretarea graficului",
                            style={"display": "none"},
                        ),
                        html.P(
                            id="text",
                            children=[
                                "Dup?? cum se poate observa, at??t vizual, c??t ??i ??n urma testelor de conformitate efectuate, "
                                "popula??ia Rom??niei (distribu??ia primei cifre a popula??iei fiecarei unit????i administrativ teritoriale) respect?? Legea lui Benford. Acest fapt se datoreaz?? ??n mare parte dimensiunii"
                                " considerabile a setului de date analizat ??i a distribu??iei pe mai multe ordine de magnitudine "
                                "(de la sate cu c????iva locuitori, pana la cel mai mare ora?? din Rom??nia,"
                                " av??nd ~2.000.000 de locuitori). Popula??ia ????rilor este un exemplu clasic de colec??ie de date pentru "
                                "care Legea lui Benford este aplicabil??."
                            ],
                            style={"display": "none"},
                        ),
                    ]
                ),
            ),
            style={"width": "99%"},
        ),
    ]
)


@app.callback(Output("cardgrouppop", "children"), Input("checklist", "value"))
def goodness_of_fit(values):
    CardArray = []
    if values is None:
        return None
    else:
        for option in values:
            if option == "CS":
                cs = scipy.stats.chisquare(df2["pop_fd"], df2["benford"])
                CardArray.append(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H4("Chi Square test", className="card-title")
                            ),
                            dbc.CardBody(
                                [
                                    html.P(
                                        "Rezultatul testului Chi Square este: "
                                        + str(cs[0])[:4]
                                    ),
                                    html.P("p-value este: " + str(cs[1])[:4]),
                                ]
                            ),
                            dbc.CardFooter(
                                [
                                    html.H6("Interpretarea valorii P"),
                                    html.P(
                                        "Valoarea p este o probabilitate."
                                        " ??n timp ce o statistic?? de testare este o modalitate de a m??sura c??t"
                                        " de extrem?? este o statistic?? pentru un anumit e??antion, "
                                        "valorile p sunt un alt mod de a m??sura acest lucru."
                                        " ??n general, cu c??t valoarea p este mai mic??, cu at??t avem "
                                        "mai multe dovezi ??mpotriva ipotezei noastre nule (adica cele 2 seturi de date NU sunt la fel)."
                                    ),
                                    html.H6("C??t de mic este suficient de mic?"),
                                    html.P(
                                        "C??t de mic?? este o valoare p pentru a respinge ipoteza nul?? ? "
                                        "R??spunsul la acest lucru este: ???Depinde???. O regul?? obi??nuit?? este c?? "
                                        "valoarea p trebuie s?? fie mai mic?? sau egal?? cu 0.05, dar nu exist?? nimic "
                                        "universal ??n aceast?? valoare. Sunt folosite de asemenea si valoarile 0.10 sau 0.01."
                                    ),
                                    html.H6("Concluzie"),
                                    html.P(
                                        "Simplific??nd, o valoare p mic?? indic?? faptul c?? cele 2 seturi de date comparate"
                                        " nu sunt asem??n??toare, ??n timp ce o valoare apropiat?? de 1 indic?? un grad mare de asem??nare."
                                    ),
                                ]
                            ),
                        ],
                        color="primary",
                        outline=True,
                    )
                )
            elif option == "KS":
                ks = scipy.stats.kstest(df2["pop_fd"], df2["benford"])
                CardArray.append(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H4("Kolmogorov-Smirnov", className="card-title"),
                            ),
                            dbc.CardBody(
                                [
                                    html.P(
                                        "Rezultatul testului Kolmogorov-Smirnov este: "
                                        + str(ks[0])[:4]
                                    ),
                                    html.P("p-value este: " + str(ks[1])[:4]),
                                ]
                            ),
                            dbc.CardFooter(
                                [
                                    html.H6("Interpretarea valorii P"),
                                    html.P(
                                        "Valoarea p este o probabilitate."
                                        " ??n timp ce o statistic?? de testare este o modalitate de a m??sura c??t"
                                        " de extrem?? este o statistic?? pentru un anumit e??antion, "
                                        "valorile p sunt un alt mod de a m??sura acest lucru."
                                        " ??n general, cu c??t valoarea p este mai mic??, cu at??t avem "
                                        "mai multe dovezi ??mpotriva ipotezei noastre nule (adica cele 2 seturi de date NU sunt la fel)."
                                    ),
                                    html.H6("C??t de mic este suficient de mic?"),
                                    html.P(
                                        "C??t de mic?? este o valoare p pentru a respinge ipoteza nul?? ? "
                                        "R??spunsul la acest lucru este: ???Depinde???. O regul?? obi??nuit?? este c?? "
                                        "valoarea p trebuie s?? fie mai mic?? sau egal?? cu 0.05, dar nu exist?? nimic "
                                        "universal ??n aceast?? valoare. Sunt folosite de asemenea si valorile 0.10 sau 0.01."
                                    ),
                                    html.H6("Concluzie"),
                                    html.P(
                                        "Simplific??nd, o valoare p mic?? indic?? faptul c?? cele 2 seturi de date comparate"
                                        " nu sunt asem??n??toare ??n timp ce, o valoare apropiat?? de 1 indic?? un grad mare de asem??nare."
                                    ),
                                ]
                            ),
                        ],
                        color="primary",
                        outline=True,
                    )
                )
            elif option == "DE":
                de = (
                    np.sqrt(
                        np.sum(
                            [
                                (df2["pop_fd"][i] / 100 - df2["benford"][i] / 100) ** 2
                                for i in range(len(df2["benford"]))
                            ]
                        )
                    )
                    / 1.03606
                )
                CardArray.append(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H4(
                                    "Devia??ia d* (Distan??a euclidian??) [1]",
                                    className="card-title",
                                )
                            ),
                            dbc.CardBody(
                                [
                                    html.P(
                                        "Distan??a euclidian?? dup?? normalizare este: "
                                        + str(de)[:4]
                                    )
                                ]
                            ),
                            dbc.CardFooter(
                                [
                                    html.P(
                                        "Devia??ia (d*) reprezint?? distan??a Euclidian?? dintre reprezentarea setului de date "
                                        "??i distribu??ia Benford. Aceasta poate s?? ia valori ??ntre 0 ??i 1. Dac?? distribu??ia"
                                        " primei cifre ??n cadrul unui set de date este exact ca distribu??ia Benford, d* va fi 0."
                                        " Cu c??t datele se abat mai mult de la aceast?? distribu??ie, d* se va apropia de 1."
                                        " Se sugereaz?? c?? un posibil indicator al faptului c?? seria de date este corupt??"
                                        " e un d* > 0.25 [1]."
                                    ),
                                    dbc.CardLink(
                                        "[1] Formula de calcul utilizat??",
                                        href="https://www.researchgate.net/publication/344164702_Is_COVID-19_data_reliable_A_statistical_analysis_with_Benford%27s_Law",
                                    ),
                                ]
                            ),
                        ],
                        color="primary",
                        outline=True,
                    )
                )
    return CardArray
