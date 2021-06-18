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
            "new_cases_fd": "Cazuri noi România",
            "total_cases_fd": "Cazuri totale România",
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
            "Legea lui Benford pentru cazurile COVID din România și SUA",
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
                                "Atât pentru numărul cazurilor noi raportate de coronavirus în România, cât și pentru numărul cazurilor totale"
                                " se observă o ușoară neconcordanță"
                                " între distribuția celei mai semnficative cifre și procentele așteptate, conform legii lui Benford."
                                " Cauzele sunt multiple, iar în lipsa altor date, nu pot fi decât speculații."
                                " Când vine vorba de cazurile noi zilnice, unul din motivele principale ar putea fi "
                                " ordinul de magnitudine redus, datele pornind de la momentul 0 pana la un maxim de ~10.000 cazuri/zi."
                                " De asemenea, alte motive ar putea fi reprezentate de erorile umane apărute în procesul de raportare [1] ori numărul redus de teste"
                                " zilnice efectuate la debutul pandemiei."
                                "Totuși, rezultatele obținute în cele două țări se plasează sub pragul critic și,"
                                " conform Legii lui Benford, nu prezintă risc de fraudă."
                            ],
                            style={"display": "none"},
                        ),
                        html.A(
                            id="covLink",
                            children="[1] Declarația ministrului sănătății cu referire la erorile de raportare",
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
            "cazuri noi România",
            "cazuri totale România",
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
                                        " În timp ce o statistică de testare este o modalitate de a măsura cât"
                                        " de extremă este o statistică pentru un anumit eșantion, "
                                        "valorile p sunt un alt mod de a măsura acest lucru."
                                        " În general, cu cât valoarea p este mai mică, cu atât avem "
                                        "mai multe dovezi împotriva ipotezei noastre nule (adica cele 2 seturi de date NU sunt la fel)."
                                    ),
                                    html.H6("Cât de mic este suficient de mic?"),
                                    html.P(
                                        "Cât de mică este o valoare p pentru a respinge ipoteza nulă ? "
                                        "Răspunsul la acest lucru este: „Depinde”. O regulă obișnuită este că "
                                        "valoarea p trebuie să fie mai mică sau egală cu 0.05, dar nu există nimic "
                                        "universal în această valoare. Sunt folosite de asemenea si valoarile 0.10 sau 0.01."
                                    ),
                                    html.H6("Concluzie"),
                                    html.P(
                                        "Simplificând, o valoare p mică indică faptul că cele 2 seturi de date comparate"
                                        " nu sunt asemănătoare, în timp ce o valoare apropiată de 1 indică un grad mare de asemănare."
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
                                        " În timp ce o statistică de testare este o modalitate de a măsura cât"
                                        " de extremă este o statistică pentru un anumit eșantion, "
                                        "valorile p sunt un alt mod de a măsura acest lucru."
                                        " În general, cu cât valoarea p este mai mică, cu atât avem "
                                        "mai multe dovezi împotriva ipotezei noastre nule (adica cele 2 seturi de date NU sunt la fel)."
                                    ),
                                    html.H6("Cât de mic este suficient de mic?"),
                                    html.P(
                                        "Cât de mică este o valoare p pentru a respinge ipoteza nulă ? "
                                        "Răspunsul la acest lucru este: „Depinde”. O regulă obișnuită este că "
                                        "valoarea p trebuie să fie mai mică sau egală cu 0.05, dar nu există nimic "
                                        "universal în această valoare. Sunt folosite de asemenea si valorile 0.10 sau 0.01."
                                    ),
                                    html.H6("Concluzie"),
                                    html.P(
                                        "Simplificând, o valoare p mică indică faptul că cele 2 seturi de date comparate"
                                        " nu sunt asemănătoare, în timp ce o valoare apropiată de 1 indică un grad mare de asemănare."
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
                        "Deviația d* (Distanța euclidiană) [1] pentru "
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
                                    "Deviația d* (Distanța euclidiană) [1]",
                                    className="card-title",
                                )
                            ),
                            dbc.CardBody(body),
                            dbc.CardFooter(
                                [
                                    html.P(
                                        "Deviația (d*) reprezintă distanța Euclidiană dintre seria de date "
                                        "(cazuri noi, cazuri totale) "
                                        "și distribuția Benford. Aceasta poate să ia valori între 0 și 1. Dacă distribuția"
                                        " primei cifre în cadrul unui set de date este exact ca distribuția Benford, d* va fi 0."
                                        " Cu cât datele se abat mai mult de la această distribuție, d* se va apropia de 1."
                                        " Se sugerează că un posibil indicator al faptului că seria de date este coruptă"
                                        " e un d* > 0.25 [1]."
                                    ),
                                    dbc.CardLink(
                                        "[1] Formula de calcul utilizată",
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
