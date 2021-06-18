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

with open(DATA_PATH.joinpath("voting_data_eng.json")) as json_file:
    election_ru_data = json.load(json_file)


def custom_legend(fig, nameSwap):
    for i, dat in enumerate(fig.data):
        for elem in dat:
            if i >= len(nameSwap):
                return fig
            if elem == "name":
                fig.data[i].name = nameSwap[fig.data[i].name]
    return fig


# @cache.memoize(timeout=TIMEOUT)
def election_ru_fig(election_ru_data, base, theme):
    global df3
    if base != 10:
        df3 = pd.DataFrame(
            dict(
                votes_fd_Putin_Vladimir_Vladimirovich=np.zeros(base - 1),
                votes_fd_Baburin_Sergei_Nikolaevich=np.zeros(base - 1),
                votes_fd_Grudinin_Pavel_Nikolaevich=np.zeros(base - 1),
                votes_fd_Zhirinovskiy_Vladimir_Volfovich=np.zeros(base - 1),
                votes_fd_Sobchak_Ksenia_Anatolyevna=np.zeros(base - 1),
                votes_fd_Suraikin_Maksim_Aleksandrovich=np.zeros(base - 1),
                votes_fd_Titov_Boris_Yurievich=np.zeros(base - 1),
                votes_fd_Yavlinskiy_Gregory_Alekseivich=np.zeros(base - 1),
                x_graphic=[
                    "Cifra " + str(i) if i < 10 else "Cifra " + chr(ord("a") + i - 10)
                    for i in range(1, base)
                ],
                benford=[np.log10(1 + 1 / i) * 100 for i in range(1, base)],
            )
        )
        votes_fd_Putin_Vladimir_Vladimirovich = np.zeros(base - 1)
        votes_fd_Baburin_Sergei_Nikolaevich = np.zeros(base - 1)
        votes_fd_Grudinin_Pavel_Nikolaevich = np.zeros(base - 1)
        votes_fd_Zhirinovskiy_Vladimir_Volfovich = np.zeros(base - 1)
        votes_fd_Sobchak_Ksenia_Anatolyevna = np.zeros(base - 1)
        votes_fd_Suraikin_Maksim_Aleksandrovich = np.zeros(base - 1)
        votes_fd_Titov_Boris_Yurievich = np.zeros(base - 1)
        votes_fd_Yavlinskiy_Gregory_Alekseivich = np.zeros(base - 1)
        for location in election_ru_data:
            votes = cb.decimal_to_base(
                int(location["Putin Vladimir Vladimirovich"]), base
            )
            if votes != "":
                if ord(votes[0]) >= ord("a"):
                    votes_fd_Putin_Vladimir_Vladimirovich[
                        int(ord(votes[0]) - ord("a") + 9)
                    ] += 1
                else:
                    votes_fd_Putin_Vladimir_Vladimirovich[int(votes[0]) - 1] += 1

            votes = cb.decimal_to_base(
                int(location["Baburin Sergei Nikolaevich"]), base
            )
            if votes != "":
                if ord(votes[0]) >= ord("a"):
                    votes_fd_Baburin_Sergei_Nikolaevich[
                        int(ord(votes[0]) - ord("a") + 9)
                    ] += 1
                else:
                    votes_fd_Baburin_Sergei_Nikolaevich[int(votes[0]) - 1] += 1

            votes = cb.decimal_to_base(
                int(location["Grudinin Pavel Nikolaevich"]), base
            )
            if votes != "":
                if ord(votes[0]) >= ord("a"):
                    votes_fd_Grudinin_Pavel_Nikolaevich[
                        int(ord(votes[0]) - ord("a") + 9)
                    ] += 1
                else:
                    votes_fd_Grudinin_Pavel_Nikolaevich[int(votes[0]) - 1] += 1

            votes = cb.decimal_to_base(
                int(location["Zhirinovskiy Vladimir Volfovich"]), base
            )
            if votes != "":
                if ord(votes[0]) >= ord("a"):
                    votes_fd_Zhirinovskiy_Vladimir_Volfovich[
                        int(ord(votes[0]) - ord("a") + 9)
                    ] += 1
                else:
                    votes_fd_Zhirinovskiy_Vladimir_Volfovich[int(votes[0]) - 1] += 1

            votes = cb.decimal_to_base(
                int(location["Sobchak Ksenia Anatolyevna"]), base
            )
            if votes != "":
                if ord(votes[0]) >= ord("a"):
                    votes_fd_Sobchak_Ksenia_Anatolyevna[
                        int(ord(votes[0]) - ord("a") + 9)
                    ] += 1
                else:
                    votes_fd_Sobchak_Ksenia_Anatolyevna[int(votes[0]) - 1] += 1

            votes = cb.decimal_to_base(
                int(location["Suraikin Maksim Aleksandrovich"]), base
            )
            if votes != "":
                if ord(votes[0]) >= ord("a"):
                    votes_fd_Suraikin_Maksim_Aleksandrovich[
                        int(ord(votes[0]) - ord("a") + 9)
                    ] += 1
                else:
                    votes_fd_Suraikin_Maksim_Aleksandrovich[int(votes[0]) - 1] += 1

            votes = cb.decimal_to_base(int(location["Titov Boris Yurievich"]), base)
            if votes != "":
                if ord(votes[0]) >= ord("a"):
                    votes_fd_Titov_Boris_Yurievich[
                        int(ord(votes[0]) - ord("a") + 9)
                    ] += 1
                else:
                    votes_fd_Titov_Boris_Yurievich[int(votes[0]) - 1] += 1

            votes = cb.decimal_to_base(
                int(location["Yavlinskiy Gregory Alekseivich"]), base
            )
            if votes != "":
                if ord(votes[0]) >= ord("a"):
                    votes_fd_Yavlinskiy_Gregory_Alekseivich[
                        int(ord(votes[0]) - ord("a") + 9)
                    ] += 1
                else:
                    votes_fd_Yavlinskiy_Gregory_Alekseivich[int(votes[0]) - 1] += 1

        sum_votes = np.sum(votes_fd_Putin_Vladimir_Vladimirovich)
        votes_fd_Putin_Vladimir_Vladimirovich = (
            votes_fd_Putin_Vladimir_Vladimirovich / sum_votes
        ) * 100
        df3[
            "votes_fd_Putin_Vladimir_Vladimirovich"
        ] = votes_fd_Putin_Vladimir_Vladimirovich

        sum_votes = np.sum(votes_fd_Baburin_Sergei_Nikolaevich)
        votes_fd_Baburin_Sergei_Nikolaevich = (
            votes_fd_Baburin_Sergei_Nikolaevich / sum_votes
        ) * 100
        df3["votes_fd_Baburin_Sergei_Nikolaevich"] = votes_fd_Baburin_Sergei_Nikolaevich

        sum_votes = np.sum(votes_fd_Grudinin_Pavel_Nikolaevich)
        votes_fd_Grudinin_Pavel_Nikolaevich = (
            votes_fd_Grudinin_Pavel_Nikolaevich / sum_votes
        ) * 100
        df3["votes_fd_Grudinin_Pavel_Nikolaevich"] = votes_fd_Grudinin_Pavel_Nikolaevich

        sum_votes = np.sum(votes_fd_Zhirinovskiy_Vladimir_Volfovich)
        votes_fd_Zhirinovskiy_Vladimir_Volfovich = (
            votes_fd_Zhirinovskiy_Vladimir_Volfovich / sum_votes
        ) * 100
        df3[
            "votes_fd_Zhirinovskiy_Vladimir_Volfovich"
        ] = votes_fd_Zhirinovskiy_Vladimir_Volfovich

        sum_votes = np.sum(votes_fd_Sobchak_Ksenia_Anatolyevna)
        votes_fd_Sobchak_Ksenia_Anatolyevna = (
            votes_fd_Sobchak_Ksenia_Anatolyevna / sum_votes
        ) * 100
        df3["votes_fd_Sobchak_Ksenia_Anatolyevna"] = votes_fd_Sobchak_Ksenia_Anatolyevna

        sum_votes = np.sum(votes_fd_Suraikin_Maksim_Aleksandrovich)
        votes_fd_Suraikin_Maksim_Aleksandrovich = (
            votes_fd_Suraikin_Maksim_Aleksandrovich / sum_votes
        ) * 100
        df3[
            "votes_fd_Suraikin_Maksim_Aleksandrovich"
        ] = votes_fd_Suraikin_Maksim_Aleksandrovich

        sum_votes = np.sum(votes_fd_Titov_Boris_Yurievich)
        votes_fd_Titov_Boris_Yurievich = (
            votes_fd_Titov_Boris_Yurievich / sum_votes
        ) * 100
        df3["votes_fd_Titov_Boris_Yurievich"] = votes_fd_Titov_Boris_Yurievich

        sum_votes = np.sum(votes_fd_Yavlinskiy_Gregory_Alekseivich)
        votes_fd_Yavlinskiy_Gregory_Alekseivich = (
            votes_fd_Yavlinskiy_Gregory_Alekseivich / sum_votes
        ) * 100
        df3[
            "votes_fd_Yavlinskiy_Gregory_Alekseivich"
        ] = votes_fd_Yavlinskiy_Gregory_Alekseivich
    else:
        df3 = pd.read_fwf(DATA_PATH.joinpath("ru_elections_results.txt"))
        df3["benford"] = [np.log10(1 + 1 / i) * 100 for i in range(1, base)]
        df3["x_graphic"] = [
            "Cifra " + str(i) if i < 10 else "Cifra " + chr(ord("a") + i - 10)
            for i in range(1, base)
        ]
    fig = px.bar(
        df3,
        x="x_graphic",
        y=[
            "votes_fd_Putin_Vladimir_Vladimirovich",
            "votes_fd_Baburin_Sergei_Nikolaevich",
            "votes_fd_Grudinin_Pavel_Nikolaevich",
            "votes_fd_Zhirinovskiy_Vladimir_Volfovich",
            "votes_fd_Sobchak_Ksenia_Anatolyevna",
            "votes_fd_Suraikin_Maksim_Aleksandrovich",
            "votes_fd_Titov_Boris_Yurievich",
            "votes_fd_Yavlinskiy_Gregory_Alekseivich",
        ],
        barmode="group",
        hover_data={"x_graphic": False, "variable": False},
        color_discrete_sequence=cst.THEMES_LIST[theme],
    )
    fig.add_scatter(
        x=df3["x_graphic"],
        y=df3["benford"],
        line=dict(color="green"),
        name="Benford's law",
    )

    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="Percent%")

    fig = custom_legend(
        fig=fig,
        nameSwap={
            "votes_fd_Putin_Vladimir_Vladimirovich": "Putin Vladimir Vladimirovich",
            "votes_fd_Baburin_Sergei_Nikolaevich": "Baburin Sergei Nikolaevich",
            "votes_fd_Grudinin_Pavel_Nikolaevich": "Grudinin Pavel Nikolaevich",
            "votes_fd_Zhirinovskiy_Vladimir_Volfovich": "Zhirinovskiy Vladimir Volfovich",
            "votes_fd_Sobchak_Ksenia_Anatolyevna": "Sobchak Ksenia Anatolyevna",
            "votes_fd_Suraikin_Maksim_Aleksandrovich": "Suraikin Maksim Aleksandrovich",
            "votes_fd_Titov_Boris_Yurievich": "Titov Boris Yurievich",
            "votes_fd_Yavlinskiy_Gregory_Alekseivich": "Yavlinskiy Gregory Alekseivich",
        },
    )

    cs = scipy.stats.chisquare(
        df3["votes_fd_Grudinin_Pavel_Nikolaevich"], df3["benford"]
    )

    return fig


@app.callback(
    Output("graph_prez-Ru", "figure"),
    Input("input_range", "value"),
    Input("my_dropdown", "value"),
)
@cache.memoize(timeout=TIMEOUT)
def number_render_pop(rangeval, theme):
    if rangeval is None:
        return election_ru_fig(election_ru_data, 10, theme)
    else:
        return election_ru_fig(election_ru_data, rangeval, theme)


@app.callback(
    Output("textRu", "style"),
    Output("textTitleRu", "style"),
    Output("cardTextRu", "color"),
    Output("cardTextRu", "outline"),
    Input("graph_prez-Ru", "figure"),
    prevent_initial_call=True,
)
def text_apear(fig):
    if fig is not None:
        return {}, {}, "primary", True


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1(
                        "Legea lui Benford pentru numărul voturilor obținute de candidați "
                        "în alegerile prezidențiale din Rusia 2018",
                        style=cst.TEXT_STYLE,
                    ),
                    width=12,
                ),
                html.Hr(),
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(id="graph_prez-Ru"), color="#eb6864", type="graph"
                    ),
                    width=12,
                ),
                dbc.Col(dbc.CardGroup(id="cardgroupru", children=[]), width=12),
            ]
        ),
        html.Br(),
        dbc.Col(
            dbc.Card(
                id="cardTextRu",
                children=dbc.CardBody(
                    [
                        html.H4(
                            id="textTitleRu",
                            children="Interpretarea graficului",
                            style={"display": "none"},
                        ),
                        html.P(
                            id="textRu",
                            children=[
                                html.P(
                                    "Dacă seturile de date reprezentând populații sunt exemplul clasic pentru care Legea lui Benford funcționează,"
                                    " scrutinele electorale sunt adesea luate ca un puternic contraexemplu. Principala problemă o reprezintă faptul că "
                                    " secțiile de votare sunt formate într-o așa manieră, încât să deservească un numar aproximativ egal de"
                                    " locuitori, deci condiția ca datele să fie repartizate pe mai multe ordine de marime nu poate fi respectată."
                                    " În exemplul prezentat mai sus, în majoriatea localităților unde s-a votat, numărul voturilor este de ordinul sutelor,"
                                    " puține fiind cele care au depășit pragul de 1.000. O altă explicație a slabei corelații dintre distribuția"
                                    " celei mai semnificative cifre și cea calculată cu formula enunțată în Legea lui Benford, ar putea fi într-adevar"
                                    " frauda, mulți observatori internaționali susținând această ipoteză[1]."
                                ),
                                html.A(
                                    "[1] Following fraud-tainted vote, Putin claims crushing victory in Russian presidential election",
                                    href="https://www.chicagotribune.com/nation-world/ct-russia-election-putin-20180318-story.html",
                                ),
                            ],
                            style={"display": "none"},
                        ),
                    ]
                ),
            )
        ),
    ]
)


@app.callback(Output("cardgroupru", "children"), Input("checklist", "value"))
def goodness_of_fit(values):
    CardArray = []
    if values is None:
        return None
    else:
        names = [
            "Putin Vladimir Vladimirovich",
            "Baburin Sergei Nikolaevich",
            "Grudinin Pavel Nikolaevich",
            "Zhirinovskiy Vladimir Volfovich",
            "Sobchak Ksenia Anatolyevna",
            "Suraikin Maksim Aleksandrovich",
            "Titov Boris Yurievich",
            "Yavlinskiy Gregory Alekseivich",
        ]
        for option in values:
            if option == "CS":
                cs = [
                    scipy.stats.chisquare(df3[key], df3["benford"])
                    for key in df3.keys()[:-2]
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
                    scipy.stats.kstest(df3[key], df3["benford"])
                    for key in df3.keys()[:-2]
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
                                (df3[key][i] / 100 - df3["benford"][i] / 100) ** 2
                                for i in range(len(df3["benford"]))
                            ]
                        )
                    )
                    / 1.03606
                    for key in df3.keys()[:-2]
                ]
                body = [
                    html.P(
                        "Deviația d* (Distanța euclidiană)[1] pentru "
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
                                        "Deviația (d*) reprezintă distanța Euclidiană dintre reprezentarea setului de date "
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
