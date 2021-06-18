from apps import constants as cst
from app import app
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import change_base as cb
import numpy as np
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
import dash_extensions as de
import io
import base64
import dash_table
import scipy.stats


def parse_contents(contents, filename):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    return html.Div(
        [
            dbc.Alert(
                'Fișierul "' + filename + '" încărcat cu succes!',
                color="success",
                dismissable=True,
                fade=True,
                duration=5000,
            ),
            html.Br(),
            dash_table.DataTable(
                id="datatable-interactivity",
                data=df.to_dict("records"),
                columns=[
                    {
                        "name": i,
                        "id": i,
                        "deletable": True,
                        "selectable": True,
                        "hideable": True,
                    }
                    for i in df.columns
                ],
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="single",
                column_selectable="multi",
                row_selectable=None,
                row_deletable=True,
                selected_rows=[],
                selected_columns=[df.columns[0]],
                hidden_columns=[],
                page_action="native",
                page_size=10,
                style_cell=cst.CELL_STYLE,
                style_data=cst.STYLE_DATA,
                style_header=cst.HEADER_STYLE,
                style_as_list_view=False,
                tooltip_data=[
                    {
                        column: {"value": str(value), "type": "markdown"}
                        for column, value in row.items()
                    }
                    for row in df.to_dict("records")
                ],
                tooltip_header={i: i for i in df.columns},
                tooltip_duration=None,
                tooltip_delay=500,
            ),
            html.Br(),
            html.Br(),
        ]
    )


@app.callback(
    Output("output-data-upload", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
)
# data for uploaded table
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        return children


# Create bar chart
@app.callback(
    Output(component_id="bar-container", component_property="children"),
    Input(
        component_id="datatable-interactivity",
        component_property="derived_virtual_data",
    ),
    Input(
        component_id="datatable-interactivity", component_property="selected_columns"
    ),
    Input(component_id="input_range", component_property="value"),
    Input(component_id="my_dropdown", component_property="value"),
    prevent_initial_call=True,
)
def update_bar(all_rows_data, slctd_cols, base, theme):
    global df4
    global dff
    dff = pd.DataFrame(all_rows_data)
    dictionary = {"FD distibution for " + i: np.zeros(base - 1) for i in slctd_cols}
    dictionary["x_graphic"] = [
        "Cifra " + str(i) if i < 10 else "Cifra " + chr(ord("a") + i - 10)
        for i in range(1, base)
    ]
    dictionary["benford"] = [np.log10(1 + 1 / i) * 100 for i in range(1, base)]
    df4 = pd.DataFrame(dictionary)
    try:
        if len(slctd_cols) > 0:
            for column in slctd_cols:
                if column in dff:
                    FD_distribution_for = np.zeros(base - 1)
                    for row in dff[column]:
                        try:
                            if type(row) is int or float:
                                votes = cb.decimal_to_base(int(row), base)
                                if votes != "":
                                    if ord(votes[0]) >= ord("a"):
                                        FD_distribution_for[
                                            int(ord(votes[0]) - ord("a") + 9)
                                        ] += 1
                                    else:
                                        FD_distribution_for[int(votes[0]) - 1] += 1

                                    sum_votes = np.sum(FD_distribution_for)
                                    df4["FD distibution for " + column] = (
                                        FD_distribution_for / sum_votes
                                    ) * 100
                            else:
                                raise Exception
                        except Exception as e:
                            print(e)
                            return html.Div(
                                dbc.Alert(
                                    "Coloanele selectate trebuie să conțină doar numere.",
                                    color="danger",
                                    dismissable=True,
                                    fade=True,
                                )
                            )
        else:
            raise Exception
    except:
        return html.Div(
            dbc.Alert(
                "Nicio coloană selectată!",
                color="danger",
                dismissable=True,
                fade=True,
            )
        )

    fig = px.bar(
        data_frame=df4,
        x="x_graphic",
        y=["FD distibution for " + i for i in slctd_cols],
        barmode="group",
        hover_data={"x_graphic": False},
        # color=rand_color.generate(count=len(slctd_cols),
        color_discrete_sequence=cst.THEMES_LIST[theme],
    )
    fig.add_scatter(
        x=df4["x_graphic"],
        y=df4["benford"],
        line=dict(color="green"),
        name="Benford's law",
    )

    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="Percent%")

    return [dcc.Graph(id="bar-chart", figure=fig)]


layout = html.Div(
    dbc.Row(
        [
            dbc.Col(
                html.H1(
                    "Încarcă propriul fișier .csv sau .xls și verifică în ce măsură datele respectă "
                    "Legea lui Benford",
                    style=cst.TEXT_STYLE,
                ),
                width=12,
            ),
            # html.Hr(),
            dbc.Col(
                dcc.Upload(
                    id="upload-data",
                    children=html.Div(
                        [
                            "Drag & Drop sau ",
                            html.A(id="A_select_files", children="Click"),
                        ],
                    ),
                    style=cst.UPLOAD_STYLE,
                    # Allow multiple files to be uploaded
                    multiple=True,
                ),
                width=12,
            ),
            # html.Hr(),
            dbc.Col(
                dcc.Loading(
                    id="loading-table",
                    children=html.Div(id="output-data-upload"),
                    color="#eb6864",
                    type="cube",
                    style={"height": "0px"},
                ),
                width=12,
            ),
            # html.Br(),
            dbc.Col(
                dcc.Loading(
                    html.Div(id="bar-container"),
                    color="#eb6864",
                    type="graph",
                    style={"height": "0px"},
                ),
                width=12,
            ),
            # html.Br(),
            dbc.Col(dbc.CardGroup(id="cardgroupup", children=[]), width=12),
        ]
    )
)


@app.callback(
    Output("cardgroupup", "children"),
    Input("checklist", "value"),
    Input("datatable-interactivity", "selected_columns"),
    Input(component_id="bar-container", component_property="children"),
    prevent_initial_call=True,
)
def goodness_of_fit(values, columns, nmc):
    CardArray = []
    # Appear when all columns are eligible
    for column in columns:
        for row in dff[column]:
            if type(row) is str:
                return None
    # If there is any value then...
    if values is None:
        return None
    else:
        names = columns
        for option in values:
            if option == "CS":
                cs = [
                    scipy.stats.chisquare(df4[key], df4["benford"])
                    for key in df4.keys()[:-2]
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
                                        "universal în această valoare. Sunt folosite de asemenea si valorile 0.10 sau 0.01."
                                    ),
                                    html.H6("Concluzie"),
                                    html.P(
                                        "Simplificând, o valoare p mică indică faptul că cele 2 seturi de date comparate"
                                        " nu sunt asemănătoare, în timp ce, o valoare apropiată de 1 indică un grad mare de asemănare."
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
                    scipy.stats.kstest(df4[key], df4["benford"])
                    for key in df4.keys()[:-2]
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
                                        "universal în această valoare. Sunt folosite de asemenea si valoarile 0.10 sau 0.01."
                                    ),
                                    html.H6("Concluzie"),
                                    html.P(
                                        "Simplificând, o valoare p mică indică faptul că cele 2 seturi de date comparate"
                                        " nu sunt asemănătoare, în timp ce, o valoare apropiată de 1 indică un grad mare de asemănare."
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
                                (df4[key][i] / 100 - df4["benford"][i] / 100) ** 2
                                for i in range(len(df4["benford"]))
                            ]
                        )
                    )
                    / 1.03606
                    for key in df4.keys()[:-2]
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
                                        "Deviația (d*) reprezintă distanța Euclidiană dintre seria de date "
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
