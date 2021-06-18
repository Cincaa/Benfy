import plotly.express as px

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    "background-color": "#F8F8F8",
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    "margin-left": "25%",
    "margin-right": "5%",
    "top": 0,
    "padding": "20px 10px",
}
HOMEPAGE_CONTENT_STYLE = {
    "margin-left": "5%",
    "margin-right": "5%",
    "top": 0,
    "padding": "20px 10px",
}
HOMEPAGE_SIDEBAR_STYLE = {"display": "none"}
HOMEPAGE_ISTORIC_TEXT1 = """*Legea lui Benford* a avut drept origine o observație a astronomului *Simon Newcomb*. 
                În anul 1881, aflat în Observatorul Naval American, acesta observă că paginile cărților de pe care studia
                 erau întotdeauna mai tocite la începutul scrierii, în timp ce spre final erau aproape neatinse.
                Pornind de la această constatare, formulează ipoteza conform căreia, în seturi mari de date din natură, 
                prima cifră a acestor numere nu respectă o distribuție uniformă, ci una logaritmică, 
                începând de la 1 care ar trebui să apară în cazul a 30% din numere, până la 9 care ar avea un procent de sub 5%.
                 În articolul publicat la acea vreme, concluzionează că [“legea probabilității apariției numerelor
                  este astfel încât toate mantisele logaritmului lor sunt la fel de probabile”](http://www.jstor.org/stable/2369148).
                """
HOMEPAGE_ISTORIC_TEXT2 = """Jumătate de secol mai târziu, în 1938, *Frank Benford* redescoperă legea și publică un articol 
                  în care prezintă rezultatele obținute în urma analizării apariției a peste 20.000 cifre colectate din diverse domenii,
                   precum populația orașelor, numărul deceselor, lungimea râurilor ori numerele tipărite în ediția unui ziar. 
                   Rezultatele urmau, în majoritatea cazurilor, îndeaproape [rezultatele preconizate](https://www.inzichten.nl/contact/images/benford_law.pdf), 
                   nu doar pentru apariția primei cifre, ci și a primelor n cifre. Această lucrare stârnește controverse
                    și face ca descoperirea lui *S. Newcomb* să se popularizeze în lumea științifică, 
                    astfel legea căpătând numele *Benford-Newcomb* sau, pe scurt, *Legea lui Benford*."""
HOMEPAGE_APLICABILITATE_TEXT1 = """Pentru a putea verifica aplicabilitatea Legii lui Benford, este necesar ca acea colecție
                    de numere să cuprindă mai multe magnitudini și minimum 50-100 de date analizate.
                    \nAdmițând faptul că Legea lui Benford este aplicabilă tuturor colecțiilor numerice apărute natural 
                    care respectă condițiile enunțate anterior, apare implicația conform căreia datele falsificate ori 
                    modificate nu o respectă. Pornind de la această premisă, rezultate notabile s-au remarcat în 
                    domeniile:"""
# \n1. **Fiscal-financiar**
HOMEPAGE_APLICABILITATE_TEXT2 = """\nPoate cel mai cunoscut domeniu în care Legea lui Benford este întrebuințată cu succes este cel economic. 
                              Popularizarea acestei descoperiri îi este atribuită lui Mark Nigrini care a observat că 
                              datele verificate de Agenția de Administrare Fiscală a Statelor Unite și declarate ca fiind corecte, 
                              respectau distribuția Benford, în timp ce datele fraudate (date inventate ori falsificate), 
                              cel mai adesea, obțineau rezultate slabe la efectuarea testelor de conformitate. 
                              Astfel, efectuarea unui simplu test chi square poate oferi indicii solide că setul de date a fost manipulat. 
                              Deși testul bazat pe Legea lui Benford nu poate fi folosit ca o dovadă a faptului că a avut loc o ilegalitate,
                               ci mai degrabă ca un instrument de prioritizare și filtrare a verificării propriu-zise, 
                               utilitatea acestuia este evidentă când avem de a face cu numeroase instanțe care urmează a fi controlate.
                                Similar, T. Michalski și G. Stoltz au utilizat Legea lui Benford  pentru a evidenția faptul că, deseori,
                                 statele își declară în mod strategic greșit datele care privesc economia. 
                                 Există, de asemenea, ipoteze conform cărora utilizarea unor mecanisme de verificare bazate
                                  pe distribuția celei mai semnificative cifre, ar fi putut evita criza datoriei publice din Grecia anului 2009."""
# \n2. **Socio-politic**
HOMEPAGE_APLICABILITATE_TEXT3 = """\nO altă întrebuințare se regăsește în domeniul științelor sociale, unde politologii folosesc 
                            în analize teste de conformitate modificate pentru a valida rezultatele scrutinelor din diverse state.
                             W. Mebane a descoperit că, în cazul numărării voturilor, rezultate concludente se obțin
                              atunci când Legea lui Benford nu este aplicată în forma sa inițială, de bază, ci pentru 
                              cea de a doua cifră semnificativă. Probabil cel mai popular exemplu este reprezentat de 
                              utilizarea legii pentru rezultatele alegerilor prezidențiale din Iran, care au avut loc în anul 2009.
                               W. Mebane a realizat un studiu de caz în acest sens și a arătat că distribuția voturilor 
                               candidaților avea o slabă corelație raportată la Legea lui Benford. Într-o notă ulterioară
                               , acesta concluzionează: “Datele analizate oferă dovezi puternice în favoarea ipotezei 
                               care susține că alegerile au fost afectate de fraude semnificative”. 
                               Un alt articol care vizează același eveniment, realizat de Bernd Beber și Alexandra Scacco,
                                a vizat analizarea ultimei cifre regăsite în numărul voturilor candidaților. 
                                Rezultatele examinate prezentau puternice anomalii, în sensul că cifra 7 apărea în 17% din cazuri,
                                 în timp ce cifra 5 în doar aproximativ 4%."""
HOMEPAGE_APLICABILITATE_TEXT4 = """\nO problemă tot mai întâlnită în ultimii anii este reprezentată de răspândirea accentuată a 
                     informațiilor false, neverificate ori trunchiate, cel mai adesea însoțite de imagini ori videoclipuri 
                     prelucrate. Legea lui Benford poate fi utilizată, complementar cu alte metode, în depistarea 
                     falsurilor și combaterea fenomenului de manipulare la scară largă. 
                     E. Del Acebo și M. Sbert descriu într-o analiză efectuată că “o clasă largă de imagini sintetice și
                      reale tind să respecte legea Benford”, dar masurarea intensitații pixelilor este însă foarte 
                      sensibilă la aplicarea unor filtre ori pentru imagini abstracte, care nu portretizează elemente naturale.
                       D. Fu a dezvoltat un “nou model statistic pe baza Legii lui Benford” pentru imagini în format JPEG,
                        dovedindu-se eficient atât în detectarea compresiei și a dublei compresii. Transformata cosinus 
                        discretă și Legea lui Benford au fost utilizate și de către F. Pérez-González din perspectiva 
                        steganografiei (spre deosebire de cripografie, steganografia are drept scop ascunderea existenței
                         mesajului, nu doar a informației transmise) pentru a determina dacă o imagine în format digital 
                         conține sau nu mesaje ascunse. Nu în ultimul rând, B. Xu a prezentat o tehnică similară, 
                         bazată pe magnitudinea gradientului, de a separa imaginile generate de calculator de cele 
                         obținute prin fotografiere."""
HOMEPAGE_DESPRE_TEXT = """Prin relizarea acestei pagini se dorește punerea la dispoziția utilizatorilor
 posibilitatea analizării datelor din perspectiva corelației cu distribuția Benford, 
 studierea câtorva cazuri actuale, concrete și, totodată, popularizarea Legii lui Benford
 ca instrument de detectare a fraudei.
 \n**Funcționalități**:
 \n1. Schimbarea bazei de numerație
 \n2. Selectarea unui teme cromatice
 \n3. Efectuarea a 3 teste de conformitate (Chi-square, Kolmogorov-Smirnov, d*)
 \n4. Încărcarea propriului set de date, selectarea în aplicație a coloanelor de interes, ștergerea rândurilor
 \n5. Analiza avansată a graficelor:
   * Descărcarea graficului generat sub forma unei imagini
   * Zoom
   * Pan
   * Lasso/Box Select
   * Autoscale
   * Reset axes
   * Compararea datelor
 """

TEXT_STYLE = {"textAlign": "center", "color": "black"}

CARD_TEXT_STYLE = {"textAlign": "center", "color": "#0074D9"}

NAVBAR_STYLE = {"margin-left": "20%"}

INPUT_BASE_STYLE = {
    "width": "75%",
    "display": "block",
    "margin-left": "auto",
    "margin-right": "auto",
    "border": "none",
    "border-radius": "4px",
    "background-color": "#FDEFEF",
    "text-align": "center",
}
DROPDOWN_STYLE = {
    "border": "none",
    "border-radius": "4px",
    "background-color": "#FDEFEF",
}
DROPDOWNDIV_STYLE = {
    "width": "75%",
    "margin-left": "auto",
    "margin-right": "auto",
    "text-align": "center",
    "padding": "0px",
}
THEMES_LIST = [
    px.colors.qualitative.Plotly,
    px.colors.qualitative.D3,
    px.colors.qualitative.G10,
    px.colors.qualitative.T10,
    px.colors.qualitative.Alphabet,
    px.colors.qualitative.Dark24,
    px.colors.qualitative.Dark2,
    px.colors.qualitative.Light24,
    px.colors.qualitative.Set1,
    px.colors.qualitative.Set2,
    px.colors.qualitative.Set3,
    px.colors.qualitative.Pastel,
    px.colors.qualitative.Pastel1,
    px.colors.qualitative.Pastel2,
    px.colors.qualitative.Antique,
    px.colors.qualitative.Bold,
    px.colors.qualitative.Prism,
    px.colors.qualitative.Safe,
    px.colors.qualitative.Vivid,
]
LOGO = "https://i.ibb.co/4f9c0d6/logo-transparent.png"
BENFORDIMG = "https://i.ibb.co/SnLy6Y7/MV5-BYjcx-Zj-Ax-Mzct-NDBk-Yi00-Nj-Bi-LTli-Mj-It-Zj-Yw-Y2-I3-Yj-Bi-YThh-Xk-Ey-Xk-Fqc-Gde-QXVy-Nj-Ux-M.jpg"
BENFORDIMG_STYLE = {
    "display": "block",
    "margin-left": "auto",
    "margin-right": "auto",
    "width": "10%",
    # "height":"50%",
    "borderRadius": "100px",
}
BENFORDFIGCAPTION_STYLE = {
    "display": "block",
    "margin-left": "auto",
    "margin-right": "auto",
    # "width": "10%",
    "textAlign": "center",
}
UPLOAD_STYLE = {
    "width": "97%",
    "height": "80px",
    "lineHeight": "80px",
    "borderWidth": "1px",
    "borderStyle": "dashed",
    "borderRadius": "10px",
    "textAlign": "center",
    "margin": "10px",
}
CELL_STYLE = {
    "overflow": "hidden",
    "textOverflow": "ellipsis",
    "maxWidth": 0,
    "textAlign": "center",
    "padding": "5px",
}
STYLE_DATA = {"whiteSpace": "normal", "height": "auto"}
HEADER_STYLE = {
    "padding": "2px",
    "overflow": "hidden",
    "textOverflow": "ellipsis",
    "whiteSpace": "normal",
    "height": "auto",
    # 'fontWeight': 'bold',
    # 'background-color': '#eb6864',
    # 'color': '#eb6864',
    # 'border': '1px solid black',
}
CONTAINER_STYLE = {
    "padding-right": "0",
    "padding-left": "0",
    "margin-right": "auto",
    "margin-left": "auto",
}
