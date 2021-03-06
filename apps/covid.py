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
import scipy.stats
import dload
from flask_caching import Cache
import pathlib
import json

cache = Cache(
    app.server,
    config={"CACHE_TYPE": "SimpleCache"},
)
TIMEOUT = 0  # infinity
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../static").resolve()
with open(DATA_PATH.joinpath("USA_COVID.json")) as json_file:
    covid_us_data = json.load(json_file)

covid_ro_data = dload.json("https://www.graphs.ro/json.php")["covid_romania"]


def custom_legend(fig, nameSwap):
    for i, dat in enumerate(fig.data):
        for elem in dat:
            if i >= len(nameSwap):
                return fig
            if elem == "name":
                fig.data[i].name = nameSwap[fig.data[i].name]
    return fig


@cache.memoize(timeout=TIMEOUT)
def covid_fig(covid_ro_data, base, theme):
    global df1
    df1 = pd.DataFrame(
        dict(
            total_cases_fd=np.zeros(base - 1),
            new_cases_fd=np.zeros(base - 1),
            total_cases_us_fd=np.zeros(base - 1),
            new_cases_us_fd=np.zeros(base - 1),
            x_graphic=[
                "Cifra " + str(i) if i < 10 else "Cifra " + chr(ord("a") + i - 10)
                for i in range(1, base)
            ],
            benford=[np.log10(1 + 1 / i) * 100 for i in range(1, base)],
        )
    )
    total_cases_fd = np.zeros(base - 1)
    new_cases_fd = np.zeros(base - 1)
    total_cases_us_fd = np.zeros(base - 1)
    new_cases_us_fd = np.zeros(base - 1)

    for day in covid_ro_data:
        # total cases and new cases in new base
        tot_cases = cb.decimal_to_base(day["total_cases"], base)
        new_cases = cb.decimal_to_base(day["new_cases_today"], base)
        # first digits in my dictionary
        if ord(tot_cases[0]) >= ord("a") and ord(new_cases[0]) >= ord("a"):
            total_cases_fd[int(ord(tot_cases[0]) - ord("a") + 9)] += 1
            new_cases_fd[int(ord(new_cases[0]) - ord("a") + 9)] += 1
        elif ord(tot_cases[0]) >= ord("a"):
            total_cases_fd[int(ord(tot_cases[0]) - ord("a") + 9)] += 1
            new_cases_fd[int(new_cases[0]) - 1] += 1
        elif ord(new_cases[0]) >= ord("a"):
            total_cases_fd[int(tot_cases[0]) - 1] += 1
            new_cases_fd[int(ord(new_cases[0]) - ord("a") + 9)] += 1
        else:
            total_cases_fd[int(tot_cases[0]) - 1] += 1
            new_cases_fd[int(new_cases[0]) - 1] += 1
    # Calculates percentages
    sum_new_cases = np.sum(new_cases_fd)
    sum_total_cases = np.sum(total_cases_fd)
    df1["new_cases_fd"] = (new_cases_fd / sum_new_cases) * 100
    df1["total_cases_fd"] = (total_cases_fd / sum_total_cases) * 100

    for day in covid_us_data:
        # total cases and new cases in new base
        if type(day["positive"]) is not int or type(day["positiveIncrease"]) is not int:
            continue
        tot_us_cases = cb.decimal_to_base(day["positive"], base)
        new_us_cases = cb.decimal_to_base(day["positiveIncrease"], base)
        if len(new_us_cases) < 1:
            continue
        # first digits in my dictionary
        if ord(tot_us_cases[0]) >= ord("a") and ord(new_us_cases[0]) >= ord("a"):
            total_cases_us_fd[int(ord(tot_us_cases[0]) - ord("a") + 9)] += 1
            new_cases_us_fd[int(ord(new_us_cases[0]) - ord("a") + 9)] += 1
        elif ord(tot_us_cases[0]) >= ord("a"):
            total_cases_us_fd[int(ord(tot_us_cases[0]) - ord("a") + 9)] += 1
            new_cases_us_fd[int(new_us_cases[0]) - 1] += 1
        elif ord(new_us_cases[0]) >= ord("a"):
            total_cases_us_fd[int(tot_us_cases[0]) - 1] += 1
            new_cases_us_fd[int(ord(new_us_cases[0]) - ord("a") + 9)] += 1
        else:
            total_cases_us_fd[int(tot_us_cases[0]) - 1] += 1
            new_cases_us_fd[int(new_us_cases[0]) - 1] += 1

    sum_new_us_cases = np.sum(new_cases_us_fd)
    sum_total_us_cases = np.sum(total_cases_us_fd)
    df1["new_cases_us_fd"] = (new_cases_us_fd / sum_new_us_cases) * 100
    df1["total_cases_us_fd"] = (total_cases_us_fd / sum_total_us_cases) * 100

    fig = px.bar(
        df1,
        x="x_graphic",
        y=["new_cases_fd", "total_cases_fd", "new_cases_us_fd", "total_cases_us_fd"],
        barmode="group",
        hover_data={"variable": False, "x_graphic": False},
        color_discrete_sequence=cst.THEMES_LIST[theme],
    )
    fig.add_scatter(
        x=df1["x_graphic"],
        y=df1["benford"],
        line=dict(color="green"),
        name="Benford's law",
    )

    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="Percent%")

    fig = custom_legend(
        fig=fig,
        nameSwap={
            "new_cases_fd": "Cazuri noi Rom??nia",
            "total_cases_fd": "Cazuri totale Rom??nia",
            "new_cases_us_fd": "Cazuri noi SUA",
            "total_cases_us_fd": "Cazuri totale SUA",
        },
    )

    return fig


# Update base and theme in covid graph
@app.callback(
    Output("graph_covid-Ro", "figure"),
    Input("input_range", "value"),
    Input("my_dropdown", "value"),
)
@cache.memoize(timeout=TIMEOUT)
def number_render_cov(rangeval, theme):
    if rangeval is None:
        return covid_fig(covid_ro_data, 10, theme)
    else:
        return covid_fig(covid_ro_data, rangeval, theme)


@app.callback(
    Output("textCov", "style"),
    Output("textTitleCov", "style"),
    Output("cardTextCov", "color"),
    Output("cardTextCov", "outline"),
    Output("covLink", "style"),
    Input("graph_covid-Ro", "figure"),
    prevent_initial_call=True,
)
def text_apear(fig):
    if fig is not None:
        return {}, {}, "primary", True, {}


layout = html.Div(
    [
        html.H1(
            "Legea lui Benford pentru cazurile COVID din Rom??nia ??i SUA",
            style=cst.TEXT_STYLE,
        ),
        html.Hr(),
        dbc.Col(dcc.Loading(children=[dcc.Graph(id="graph_covid-Ro")], type="graph")),
        dbc.CardGroup(id="cardgroupcovid", children=[]),
        html.Br(),
        dbc.Col(
            dbc.Card(
                id="cardTextCov",
                children=dbc.CardBody(
                    children=[
                        html.H4(
                            id="textTitleCov",
                            children="Interpretarea graficului",
                            style={"display": "none"},
                        ),
                        html.P(
                            id="textCov",
                            children=[
                                "At??t pentru num??rul cazurilor noi raportate de coronavirus ??n Rom??nia, c??t ??i pentru num??rul cazurilor totale"
                                " se observ?? o u??oar?? neconcordan????"
                                " ??ntre distribu??ia celei mai semnficative cifre ??i procentele a??teptate, conform legii lui Benford."
                                " Cauzele sunt multiple, iar ??n lipsa altor date, nu pot fi dec??t specula??ii."
                                " C??nd vine vorba de cazurile noi zilnice, unul din motivele principale ar putea fi "
                                " ordinul de magnitudine redus, datele pornind de la momentul 0 pana la un maxim de ~10.000 cazuri/zi."
                                " De asemenea, alte motive ar putea fi reprezentate de erorile umane ap??rute ??n procesul de raportare [1] ori num??rul redus de teste"
                                " zilnice efectuate la debutul pandemiei."
                                "Totu??i, rezultatele ob??inute ??n cele dou?? ????ri se plaseaz?? sub pragul critic ??i,"
                                " conform Legii lui Benford, nu prezint?? risc de fraud??."
                            ],
                            style={"display": "none"},
                        ),
                        html.A(
                            id="covLink",
                            children="[1] Declara??ia ministrului s??n??t????ii cu referire la erorile de raportare",
                            href="https://www.g4media.ro/video-mihaila-exista-diferente-de-pana-la-500-de-decese-covid-pe-spital-intre-raportarile-in-cele-doua-platforme-utilizate-in-anul-2020-spitalele-au-raportat-26-106-decese-cu-diagnostic-principal-s.html",
                            style={"display": "none"},
                        ),
                    ]
                ),
            )
        ),
    ]
)


@app.callback(Output("cardgroupcovid", "children"), Input("checklist", "value"))
def goodness_of_fit(values):
    CardArray = []
    if values is None:
        return None
    else:
        names = [
            "cazuri noi Rom??nia",
            "cazuri totale Rom??nia",
            "cazuri noi SUA",
            "cazuri tota;e SUA",
        ]
        for option in values:
            if option == "CS":
                cs = [
                    scipy.stats.chisquare(df1[key], df1["benford"])
                    for key in df1.keys()[:-2]
                ]
                body = [
                    html.P(
                        "Rezultatul testului Chi Square pentru "
                        + names[i]
                        + ": "
                        + str(cs[i][0])[:4]
                        + "; p-value: "
                        + str(cs[i][1])[:4]
                    )
                    for i in range(len(cs))
                ]
                CardArray.append(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H4("Chi Square test", className="card-title")
                            ),
                            dbc.CardBody(body),
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
                ks = [
                    scipy.stats.kstest(df1[key], df1["benford"])
                    for key in df1.keys()[:-2]
                ]
                body = [
                    html.P(
                        "Rezultatul testului Kolmogorov-Smirnov pentru "
                        + names[i]
                        + ": "
                        + str(ks[i][0])[:4]
                        + "; p-value: "
                        + str(ks[i][1])[:4]
                    )
                    for i in range(len(ks))
                ]
                CardArray.append(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H4("Kolmogorov-Smirnov", className="card-title"),
                            ),
                            dbc.CardBody(body),
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
                                        " nu sunt asem??n??toare, ??n timp ce o valoare apropiat?? de 1 indic?? un grad mare de asem??nare."
                                    ),
                                ]
                            ),
                        ],
                        color="primary",
                        outline=True,
                    )
                )
            elif option == "DE":
                de = [
                    np.sqrt(
                        np.sum(
                            [
                                (df1[key][i] / 100 - df1["benford"][i] / 100) ** 2
                                for i in range(len(df1["benford"]))
                            ]
                        )
                    )
                    / 1.03606
                    for key in df1.keys()[:-2]
                ]
                body = [
                    html.P(
                        "Devia??ia d* (Distan??a euclidian??) [1] pentru "
                        + names[i]
                        + ": "
                        + str(de[i])[:4]
                    )
                    for i in range(len(de))
                ]
                CardArray.append(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H4(
                                    "Devia??ia d* (Distan??a euclidian??) [1]",
                                    className="card-title",
                                )
                            ),
                            dbc.CardBody(body),
                            dbc.CardFooter(
                                [
                                    html.P(
                                        "Devia??ia (d*) reprezint?? distan??a Euclidian?? dintre seria de date "
                                        "(cazuri noi, cazuri totale) "
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
