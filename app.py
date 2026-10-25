"""FINACOUNT — interface Streamlit réorganisée pour une démonstration pédagogique."""

from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="FINACOUNT | Tableau de bord",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ───────────────────────── Couleurs & styles ─────────────────────────
NAVY = "#142B46"
TEAL = "#087F8C"
GOLD = "#E8AC55"
RED = "#D9534F"
PALETTE = [TEAL, "#3173B1", GOLD, "#7C70B8", "#51AD8E"]

st.markdown(
    """
<style>
  .stApp { background: #F5F8FC; }
    .block-container { padding-top: 4rem !important; padding-bottom: 2.5rem; max-width: 1370px; }
  h1, h2, h3, h4 { color: #142B46; letter-spacing: -.02em; }
  h4 { margin: .2rem 0 .6rem; font-size: 1.02rem; }

  /* Barre latérale */
  section[data-testid="stSidebar"] { background: #142B46; }
  section[data-testid="stSidebar"] * { color: #F1F7FB !important; }
  section[data-testid="stSidebar"] div[role="radiogroup"] label {
    border-radius: 10px; padding: .5rem .6rem; margin-bottom: .15rem; width: 100%;
  }
  section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) { background: #244966; }
  .brand-title { font-size: 1.55rem; font-weight: 850; letter-spacing: .03em; }
  .brand-sub { font-size: .82rem; color: #C4D9E7 !important; margin-top: -.3rem; }
  .side-card { background: rgba(255,255,255,.07); border-radius: 12px; padding: 10px 13px; margin-bottom: 8px; }
  .side-card .lbl { font-size: .72rem; opacity: .75; text-transform: uppercase; letter-spacing: .08em; }
  .side-card .val { font-size: 1.05rem; font-weight: 750; }

  /* Thème clair forcé : étiquettes, champs et cases lisibles même en mode sombre */
  [data-testid="stAppViewContainer"] { color-scheme: light; }
  [data-testid="stMain"] label,
  [data-testid="stMain"] label p,
  [data-testid="stMain"] [data-testid="stWidgetLabel"] p,
  [data-testid="stMain"] [data-testid="stCheckbox"] p,
  [data-testid="stMain"] [data-testid="stCaptionContainer"] { color: #142B46 !important; }
  [data-testid="stMain"] input,
  [data-testid="stMain"] textarea,
  [data-testid="stMain"] [data-baseweb="input"],
  [data-testid="stMain"] [data-baseweb="base-input"],
  [data-testid="stMain"] [data-baseweb="select"] > div {
    background: #FFFFFF !important; color: #142B46 !important;
    -webkit-text-fill-color: #142B46 !important; border-color: #CBD7E4 !important;
  }
  [data-testid="stMain"] input::placeholder { color: #8A9AAC !important; -webkit-text-fill-color: #8A9AAC !important; }
  [data-testid="stMain"] [data-baseweb="select"] svg,
  [data-testid="stMain"] [data-testid="stDateInput"] svg { fill: #142B46 !important; }
  [data-testid="stMain"] [data-testid="stNumberInput"] button { background: #EEF3F8 !important; color: #142B46 !important; }
  [data-testid="stMain"] [data-baseweb="checkbox"] > span:first-child {
    background: #FFFFFF !important; border: 2px solid #8CA0B5 !important;
  }
  [data-testid="stMain"] [data-baseweb="checkbox"]:has(input:checked) > span:first-child {
    background: #087F8C !important; border-color: #087F8C !important;
  }
  [data-testid="stMain"] [data-testid="stForm"] { background: #FFFFFF; border: 1px solid #E2EAF2; border-radius: 16px; }
  [data-testid="stMain"] button[kind="primary"],
  [data-testid="stMain"] button[kind="primaryFormSubmit"] {
    background: #087F8C !important; border-color: #087F8C !important; color: #FFFFFF !important;
  }

  /* Tous les textes de la zone principale en bleu foncé (sans écraser les classes personnalisées) */
  :where([data-testid="stMain"]) :is(p, li, span, strong, em, td, th, [data-testid="stMarkdownContainer"]) { color: #142B46; }
  [data-testid="stMain"] [data-baseweb="select"] * { background-color: #FFFFFF !important; color: #142B46 !important; }
  [data-testid="stMain"] [data-baseweb="select"] svg { fill: #142B46 !important; }
  [data-testid="stMain"] button[kind="primary"] p,
  [data-testid="stMain"] button[kind="primaryFormSubmit"] p { color: #FFFFFF !important; }
  [data-testid="stMain"] [data-baseweb="progress-bar"] > div > div { background-color: #087F8C !important; }
  [data-testid="stMain"] [data-testid="stAlert"] p { color: inherit; }
  [data-testid="stMain"] [data-testid="stExpander"] { background: #FFFFFF; border-radius: 12px; }

  /* Cartes indicateurs */
  div[data-testid="stMetric"] {
    background: #FFFFFF; border: 1px solid #E2EAF2; border-radius: 16px;
    padding: 16px 18px 14px; box-shadow: 0 5px 20px rgba(20,43,70,.035); height: 100%;
  }
  div[data-testid="stMetricLabel"] { color: #627489; font-weight: 600; }
  div[data-testid="stMetricValue"] { color: #142B46; font-weight: 750; font-size: clamp(1.1rem,1.7vw,1.6rem); }
  div[data-testid="stVerticalBlockBorderWrapper"] > div { border-radius: 16px; }

  /* En-tête de page */
  .hero {
    background: linear-gradient(112deg,#142B46 0%,#164E68 59%,#087F8C 100%);
    border-radius: 18px; padding: 22px 30px; margin-bottom: 20px;
    box-shadow: 0 12px 30px rgba(20,43,70,.10);
  }
  .hero, .hero * { color: #FFFFFF !important; }
  .hero .eyebrow { font-size: .72rem; font-weight: 800; letter-spacing: .18em; }
  .hero h1 { font-size: 1.9rem; margin: .25rem 0 .2rem; font-weight: 800 !important; }
  .hero p { margin: 0; max-width: 820px; font-size: .94rem; font-weight: 600; }

  .section-label { text-transform: uppercase; color: #087f8c; font-size: .72rem; font-weight: 800;
    letter-spacing: .12em; margin: 1.3rem 0 .1rem; }
  .subtle { color: #63758a; font-size: .93rem; margin: 0 0 .9rem; }
  .notice { background: #FFF8E8; border: 1px solid #F3DCA7; color: #654D21;
    padding: 12px 16px; border-radius: 12px; line-height: 1.5; margin: 14px 0; }
  .empty { background: #FFFFFF; border: 1.5px dashed #C9D6E3; border-radius: 14px; color: #63758A;
    padding: 34px 20px; text-align: center; line-height: 1.6; }
  .empty b { color: #142B46; display: block; font-size: 1.02rem; margin-bottom: 2px; }
  .pill { display: inline-block; background: #DDF3F1; border: 1px solid #B6E4E0;
    color: #0B6974; font-weight: 700; font-size: .76rem; border-radius: 999px;
    padding: 6px 11px; margin-bottom: 10px; }
  .footer { margin-top: 1.6rem; color: #728499; font-size: .8rem; text-align: center; }
  [data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
  button[data-baseweb="tab"] { font-weight: 600; }
    /* Boutons secondaires et de téléchargement : fond clair, texte lisible */
  [data-testid="stMain"] [data-testid="stDownloadButton"] button,
  [data-testid="stMain"] button[kind="secondary"],
  [data-testid="stMain"] [data-testid="stBaseButton-secondary"] {
    background: #FFFFFF !important; border: 1px solid #087F8C !important; color: #142B46 !important;
  }
  [data-testid="stMain"] [data-testid="stDownloadButton"] button *,
  [data-testid="stMain"] button[kind="secondary"] *,
  [data-testid="stMain"] [data-testid="stBaseButton-secondary"] * { color: #142B46 !important; }
  [data-testid="stMain"] [data-testid="stDownloadButton"] button:hover,
  [data-testid="stMain"] button[kind="secondary"]:hover {
    background: #087F8C !important;
  }
  [data-testid="stMain"] [data-testid="stDownloadButton"] button:hover *,
  [data-testid="stMain"] button[kind="secondary"]:hover * { color: #FFFFFF !important; }

  /* Champ date */
  [data-testid="stMain"] [data-testid="stDateInput"] div,
  [data-testid="stMain"] [data-testid="stDateInput"] input {
    background-color: #FFFFFF !important; color: #142B46 !important;
    -webkit-text-fill-color: #142B46 !important;
  }

  /* Calendrier et listes déroulantes (affichés hors de la zone principale) */
  [data-baseweb="popover"], [data-baseweb="popover"] > div,
  [data-baseweb="calendar"], [data-baseweb="calendar"] *,
  [data-baseweb="menu"], [data-baseweb="menu"] *,
  ul[role="listbox"], ul[role="listbox"] * {
    background-color: #FFFFFF !important; color: #142B46 !important;
  }
  [data-baseweb="calendar"] [aria-selected="true"],
  [data-baseweb="calendar"] [aria-selected="true"] *,
  [data-baseweb="menu"] li:hover, [data-baseweb="menu"] li:hover * {
    background-color: #087F8C !important; color: #FFFFFF !important;
  }
  @media(max-width:650px) {
    .hero { padding: 18px 18px; }
    .hero h1 { font-size: 1.5rem; }
    .block-container { padding-left: 1rem; padding-right: 1rem; }
  }
</style>
""",
    unsafe_allow_html=True,
)

# ───────────────────────── Données ─────────────────────────
REVENUE_COLUMNS = [
    "Date", "Client", "Type", "Montant (MAD)", "Livraison effectuée",
    "Montant fiable", "Encaissement probable", "Coûts mesurables", "Commentaire",
]
CHECK_COLUMNS = ["Livraison effectuée", "Montant fiable", "Encaissement probable", "Coûts mesurables"]
TYPES = ["Vente de biens", "Prestation de services", "Intérêts / dividendes / redevances"]
EXPENSE_COLUMNS = ["Libellé", "Montant (MAD)"]


def clean_revenues(frame):
    """Normalise le registre : colonnes, types, lignes vides supprimées."""
    frame = frame.copy()
    for col in REVENUE_COLUMNS:
        if col not in frame.columns:
            frame[col] = None
    frame = frame[REVENUE_COLUMNS]
    frame["Date"] = pd.to_datetime(frame["Date"], errors="coerce").dt.date
    frame["Montant (MAD)"] = pd.to_numeric(frame["Montant (MAD)"], errors="coerce").fillna(0.0)
    for col in CHECK_COLUMNS:
        frame[col] = frame[col].fillna(False).astype(bool)
    frame["Client"] = frame["Client"].fillna("").astype(str)
    frame["Commentaire"] = frame["Commentaire"].fillna("").astype(str)
    frame["Type"] = frame["Type"].where(frame["Type"].isin(TYPES), TYPES[0])
    empty_rows = (
        frame["Date"].isna() & (frame["Client"].str.strip() == "")
        & (frame["Montant (MAD)"] == 0) & (frame["Commentaire"].str.strip() == "")
    )
    return frame[~empty_rows].reset_index(drop=True)


def clean_expenses(frame):
    frame = frame.copy()
    for col in EXPENSE_COLUMNS:
        if col not in frame.columns:
            frame[col] = None
    frame = frame[EXPENSE_COLUMNS]
    frame["Libellé"] = frame["Libellé"].fillna("").astype(str)
    frame["Montant (MAD)"] = pd.to_numeric(frame["Montant (MAD)"], errors="coerce").fillna(0.0)
    frame = frame[~((frame["Libellé"].str.strip() == "") & (frame["Montant (MAD)"] == 0))]
    return frame.reset_index(drop=True)


if "revenues" not in st.session_state:
    st.session_state.revenues = clean_revenues(pd.DataFrame([{
        "Date": "2026-10-01", "Client": "Client A", "Type": "Vente de biens",
        "Montant (MAD)": 25000.0, "Livraison effectuée": True,
        "Montant fiable": True, "Encaissement probable": True,
        "Coûts mesurables": True, "Commentaire": "Exemple de démonstration",
    }]))
if "expenses" not in st.session_state:
    st.session_state.expenses = clean_expenses(pd.DataFrame([
        {"Libellé": "Achats et charges", "Montant (MAD)": 8000.0},
        {"Libellé": "Charges de personnel", "Montant (MAD)": 5000.0},
    ]))
if "editor_version" not in st.session_state:
    st.session_state.editor_version = 0


# ───────────────────────── Utilitaires ─────────────────────────
def money(value):
    return f"{float(value):,.2f}".replace(",", " ") + " MAD"


def numeric_total(frame):
    if frame.empty or "Montant (MAD)" not in frame.columns:
        return 0.0
    return float(pd.to_numeric(frame["Montant (MAD)"], errors="coerce").fillna(0).sum())


def csv_button(frame, filename, label="Télécharger le CSV", key=None):
    st.download_button(
        label, frame.to_csv(index=False).encode("utf-8-sig"),
        file_name=filename, mime="text/csv", key=key, use_container_width=True,
    )


def section(title, description=None, kicker=None):
    if kicker:
        st.markdown(f'<p class="section-label">{kicker}</p>', unsafe_allow_html=True)
    st.subheader(title)
    if description:
        st.markdown(f'<p class="subtle">{description}</p>', unsafe_allow_html=True)


def note(text):
    st.markdown(f'<div class="notice">{text}</div>', unsafe_allow_html=True)


def empty_state(title, text):
    st.markdown(f'<div class="empty"><b>{title}</b>{text}</div>', unsafe_allow_html=True)


def styled_plot(fig, height=320):
    fig.update_layout(
        height=height, margin=dict(l=12, r=12, t=20, b=12),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        font=dict(family="Arial, sans-serif", color=NAVY, size=12),
        legend_title_text="", hoverlabel=dict(bgcolor="white"),
    )
    return fig


def bool_cols():
    return {c: st.column_config.CheckboxColumn(c) for c in CHECK_COLUMNS}


def amount_col(label="Montant (MAD)"):
    return st.column_config.NumberColumn(label, min_value=0.0, format="%.2f", step=100.0)


# Liste de contrôle pédagogique, volontairement conservée du projet d'origine.
def check_row(row):
    kind = str(row.get("Type", ""))
    if kind == "Vente de biens":
        labels = ["Livraison/transfert des risques et avantages", "Montant du revenu mesurable de façon fiable",
                  "Avantages économiques probablement reçus", "Coûts liés mesurables de façon fiable"]
    elif kind == "Prestation de services":
        labels = ["Degré d'avancement mesurable de façon fiable", "Montant du revenu mesurable de façon fiable",
                  "Avantages économiques probablement reçus", "Coûts liés mesurables de façon fiable"]
    else:
        labels = ["Droit aux intérêts/dividendes/redevances établi", "Montant du revenu mesurable de façon fiable",
                  "Avantages économiques probablement reçus", "Base de mesure/évaluation disponible"]
    checks = [(lab, bool(row.get(col, False))) for lab, col in zip(labels, CHECK_COLUMNS)]
    passed = sum(1 for _, v in checks if v)
    return checks, passed, "À examiner — critères cochés" if passed == 4 else "Vérification nécessaire"


# ───────────────────────── Navigation ─────────────────────────
PAGES = {
    "Vue d’ensemble": ("▦", "SYNTHÈSE", "Vos chiffres essentiels en un coup d’œil : revenus, charges, résultat et activité récente."),
    "Gestion des revenus": ("◈", "SAISIE", "Ajoutez des opérations, corrigez le registre et suivez vos charges."),
    "Contrôle IAS 18": ("✓", "CONTRÔLE PÉDAGOGIQUE", "Grille indicative des critères historiques de comptabilisation des produits."),
    "États financiers · IAS 1": ("▤", "ÉTATS FINANCIERS", "Présentation simplifiée du compte de résultat et contrôle d’équilibre du bilan."),
    "Rapports & exports": ("⇩", "DOCUMENTATION", "Retrouvez les indicateurs principaux et téléchargez vos fichiers."),
    "À propos": ("ⓘ", "LE PROJET", "Objectifs, périmètre et références de cette démonstration."),
}

rev = clean_revenues(st.session_state.revenues)
exp = clean_expenses(st.session_state.expenses)
total_revenue = numeric_total(rev)
total_expenses = numeric_total(exp)
net_result = total_revenue - total_expenses

st.sidebar.markdown('<div class="brand-title">FINACOUNT</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="brand-sub">Finance · Conformité · Reporting</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
page = st.sidebar.radio("ESPACE DE TRAVAIL", list(PAGES.keys()))
st.sidebar.markdown("---")
st.sidebar.markdown(
    f'<div class="side-card"><div class="lbl">Revenus</div><div class="val">{money(total_revenue)}</div></div>'
    f'<div class="side-card"><div class="lbl">Résultat simplifié</div><div class="val">{money(net_result)}</div></div>',
    unsafe_allow_html=True,
)
st.sidebar.caption("PROJET ACADÉMIQUE · Données de démonstration · MAD")
st.sidebar.caption("Les informations sont conservées uniquement pendant la session.")

icon, kicker, tagline = PAGES[page]
st.markdown(
    f'<div class="hero"><div class="eyebrow">{kicker}</div>'
    f'<h1>{page}</h1><p>{tagline}</p></div>',
    unsafe_allow_html=True,
)

# ───────────────────────── Pages ─────────────────────────
if page == "Vue d’ensemble":
    a, b, c, d = st.columns(4, gap="medium")
    a.metric("Revenus enregistrés", money(total_revenue))
    b.metric("Charges de démonstration", money(total_expenses))
    c.metric("Résultat simplifié", money(net_result))
    d.metric("Nombre d’opérations", f"{len(rev)}")

    section("Analyse de l’activité", "Répartition des revenus saisis dans cette session.", "VISUALISATIONS")
    by_type = rev.groupby("Type", as_index=False)["Montant (MAD)"].sum() if not rev.empty else pd.DataFrame()
    left, right = st.columns([1.45, 1], gap="large")
    with left:
        with st.container(border=True):
            st.markdown("**Revenus par catégorie**")
            if by_type.empty or by_type["Montant (MAD)"].sum() <= 0:
                empty_state("Aucune donnée à afficher", "Ajoutez une opération avec un montant pour voir ce graphique.")
            else:
                fig = px.bar(by_type, x="Type", y="Montant (MAD)", color="Type", color_discrete_sequence=PALETTE)
                fig.update_layout(showlegend=False, xaxis_title=None)
                fig.update_traces(marker_line_width=0, hovertemplate="%{x}<br>%{y:,.2f} MAD<extra></extra>")
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(gridcolor="#EAF0F5", zeroline=False)
                st.plotly_chart(styled_plot(fig), use_container_width=True)
    with right:
        with st.container(border=True):
            st.markdown("**Poids des catégories**")
            if by_type.empty or by_type["Montant (MAD)"].sum() <= 0:
                empty_state("Aucune répartition", "Le graphique apparaîtra dès qu’un revenu sera saisi.")
            else:
                fig = px.pie(by_type, names="Type", values="Montant (MAD)", hole=.64, color_discrete_sequence=PALETTE)
                fig.update_traces(textinfo="percent", hovertemplate="%{label}: %{value:,.2f} MAD<extra></extra>")
                fig.update_layout(legend=dict(orientation="h", y=-.14, x=0))
                st.plotly_chart(styled_plot(fig), use_container_width=True)

    section("Opérations récentes", "Les huit dernières écritures enregistrées.", "ACTIVITÉ")
    if rev.empty:
        empty_state("Aucune opération enregistrée", "Rendez-vous dans « Gestion des revenus » pour ajouter la première.")
    else:
        recent = rev.tail(8).iloc[::-1].copy()
        recent["Critères"] = [f"{check_row(r)[1]}/4" for _, r in recent.iterrows()]
        st.dataframe(
            recent[["Date", "Client", "Type", "Montant (MAD)", "Critères", "Commentaire"]],
            use_container_width=True, hide_index=True,
            column_config={
                "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                "Montant (MAD)": st.column_config.NumberColumn("Montant (MAD)", format="%.2f"),
                "Critères": st.column_config.TextColumn("Critères cochés", width="small"),
                "Commentaire": st.column_config.TextColumn("Commentaire", width="medium"),
            },
        )
    note("<b>À retenir :</b> les montants proviennent de données de démonstration ou des saisies de l’utilisateur. Ils ne constituent pas des états financiers certifiés.")

elif page == "Gestion des revenus":
    tab_add, tab_register, tab_exp = st.tabs(["＋ Nouvelle opération", "▤ Registre des opérations", "◧ Charges"])

    with tab_add:
        with st.form("add_revenue", clear_on_submit=True):
            st.markdown("#### Informations générales")
            a, b = st.columns(2, gap="large")
            with a:
                op_date = st.date_input("Date de l’opération", value=date.today())
                client = st.text_input("Client / contrepartie", placeholder="Ex. Client A")
            with b:
                typ = st.selectbox("Nature de l’opération", TYPES)
                amount = st.number_input("Montant (MAD)", min_value=0.0, value=0.0, step=100.0)
            st.markdown("#### Critères de contrôle pédagogique")
            c1, c2 = st.columns(2, gap="large")
            with c1:
                delivered = st.checkbox("Livraison / avancement / droit établi")
                reliable = st.checkbox("Montant mesurable de façon fiable")
            with c2:
                probable = st.checkbox("Avantages économiques probablement reçus")
                costs = st.checkbox("Coûts ou base de mesure évaluables de façon fiable")
            comment = st.text_input("Commentaire", placeholder="Facultatif")
            submitted = st.form_submit_button("Ajouter l’opération", type="primary", use_container_width=True)
        if submitted:
            new = {
                "Date": op_date, "Client": client.strip() or "Non renseigné", "Type": typ,
                "Montant (MAD)": amount, "Livraison effectuée": delivered,
                "Montant fiable": reliable, "Encaissement probable": probable,
                "Coûts mesurables": costs, "Commentaire": comment,
            }
            st.session_state.revenues = clean_revenues(pd.concat([rev, pd.DataFrame([new])], ignore_index=True))
            st.session_state.editor_version += 1
            st.success("Opération enregistrée. Ouvrez l’onglet « Registre » pour la consulter.")

    with tab_register:
        st.caption("Modifiez directement les cellules, ajoutez ou supprimez des lignes, puis enregistrez.")
        if rev.empty:
            empty_state("Le registre est vide", "Ajoutez une opération ci-dessus, ou saisissez une ligne directement dans le tableau.")
        with st.form("edit_registry"):
            edited = st.data_editor(
                rev, use_container_width=True, hide_index=True, num_rows="dynamic",
                key=f"revenue_editor_{st.session_state.editor_version}",
                column_order=REVENUE_COLUMNS,
                column_config={
                    "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY", required=True),
                    "Client": st.column_config.TextColumn("Client", width="medium"),
                    "Type": st.column_config.SelectboxColumn("Type", options=TYPES, required=True, width="medium"),
                    "Montant (MAD)": amount_col(),
                    "Livraison effectuée": st.column_config.CheckboxColumn("Livraison / avancement", width="small"),
                    "Montant fiable": st.column_config.CheckboxColumn("Montant fiable", width="small"),
                    "Encaissement probable": st.column_config.CheckboxColumn("Encaissement probable", width="small"),
                    "Coûts mesurables": st.column_config.CheckboxColumn("Coûts mesurables", width="small"),
                    "Commentaire": st.column_config.TextColumn("Commentaire", width="large"),
                },
            )
            if st.form_submit_button("Enregistrer les modifications", type="primary"):
                st.session_state.revenues = clean_revenues(edited)
                st.session_state.editor_version += 1
                st.success("Registre mis à jour.")
                st.rerun()
        c1, c2 = st.columns([2, 1], gap="medium")
        with c1:
            csv_button(rev, "registre_revenus_finacount.csv", "Exporter le registre (CSV)")
        with c2:
            if st.button("Réinitialiser le registre", use_container_width=True):
                st.session_state.revenues = clean_revenues(pd.DataFrame(columns=REVENUE_COLUMNS))
                st.session_state.editor_version += 1
                st.rerun()

    with tab_exp:
        st.caption("Ces charges alimentent le résultat simplifié et le compte de résultat.")
        left, right = st.columns([1.6, 1], gap="large")
        with left:
            with st.form("edit_expenses"):
                edited_exp = st.data_editor(
                    exp, use_container_width=True, hide_index=True, num_rows="dynamic",
                    key=f"expense_editor_{st.session_state.editor_version}",
                    column_config={
                        "Libellé": st.column_config.TextColumn("Libellé", width="large"),
                        "Montant (MAD)": amount_col(),
                    },
                )
                if st.form_submit_button("Enregistrer les charges", type="primary", use_container_width=True):
                    st.session_state.expenses = clean_expenses(edited_exp)
                    st.session_state.editor_version += 1
                    st.success("Charges mises à jour.")
                    st.rerun()
        with right:
            st.metric("Total des charges", money(total_expenses))
            st.metric("Nombre de lignes", f"{len(exp)}")

elif page == "Contrôle IAS 18":
    note("<b>Important :</b> IAS 18 a été remplacée par IFRS 15 pour les exercices ouverts à compter du 1er janvier 2018. Cette grille pédagogique est conservée pour le sujet académique.")
    if rev.empty:
        empty_state("Aucune opération à contrôler", "Commencez par en ajouter dans « Gestion des revenus ».")
    else:
        outputs = []
        for i, row in rev.iterrows():
            checks, passed, _ = check_row(row)
            outputs.append({
                "Opération": i + 1, "Client": row["Client"], "Type": row["Type"],
                "Montant (MAD)": row["Montant (MAD)"], "Critères cochés": passed,
                "Conclusion": "À examiner par le comptable" if passed == 4 else "Vérification nécessaire",
                "Points de contrôle": "; ".join(("✓ " if v else "✗ ") + lab for lab, v in checks),
            })
        result = pd.DataFrame(outputs)
        checked = int((result["Critères cochés"] == 4).sum())
        a, b, c = st.columns(3, gap="medium")
        a.metric("Opérations contrôlées", len(rev))
        b.metric("4 critères cochés", checked)
        c.metric("Points à revoir", len(rev) - checked)

        section("Tableau de contrôle", "La validation comptable doit être faite par une personne compétente.", "RÉSULTATS")
        st.dataframe(
            result.drop(columns=["Points de contrôle"]), use_container_width=True, hide_index=True,
            column_config={
                "Opération": st.column_config.NumberColumn("N°", width="small"),
                "Montant (MAD)": st.column_config.NumberColumn("Montant (MAD)", format="%.2f"),
                "Critères cochés": st.column_config.ProgressColumn("Critères cochés", min_value=0, max_value=4, format="%d/4"),
                "Conclusion": st.column_config.TextColumn("Conclusion", width="medium"),
            },
        )
        csv_button(result, "controle_ias18_finacount.csv", "Exporter les contrôles (CSV)")

        section("Détail d’une opération", None, "ANALYSE")
        selected = st.selectbox(
            "Choisir une opération", range(len(rev)),
            format_func=lambda i: f"{i+1} · {rev.iloc[i]['Client'] or 'Sans nom'} · {money(rev.iloc[i]['Montant (MAD)'])}",
        )
        checks, passed, verdict = check_row(rev.iloc[selected])
        left, right = st.columns([1, 1.4], gap="large")
        with left:
            with st.container(border=True):
                st.metric("Critères cochés", f"{passed} / 4")
                st.progress(passed / 4)
                st.caption(verdict)
        with right:
            with st.container(border=True):
                for label, ok in checks:
                    st.write(("Validé" if ok else "À vérifier") + label)
        st.info("La présence de quatre coches n’atteste pas de la conformité de l’opération : une revue professionnelle reste indispensable.")

elif page == "États financiers · IAS 1":
    tab_result, tab_balance = st.tabs(["Compte de résultat simplifié", "Contrôle du bilan"])
    with tab_result:
        with st.container(border=True):
            st.markdown("#### Hypothèses de calcul")
            col1, col2, col3, col4 = st.columns(4, gap="medium")
            other_income = col1.number_input("Autres produits (MAD)", min_value=0.0, value=0.0, step=100.0)
            cost_of_sales = col2.number_input("Coût des ventes (MAD)", min_value=0.0, value=0.0, step=100.0)
            operating_expenses = col3.number_input(
                "Autres charges d’exploitation (MAD)", min_value=0.0, value=float(total_expenses), step=100.0)
            finance_costs = col4.number_input("Charges financières (MAD)", min_value=0.0, value=0.0, step=100.0)

        income = total_revenue + other_income
        charges = cost_of_sales + operating_expenses + finance_costs
        result_net = income - charges
        a, b, c = st.columns(3, gap="medium")
        a.metric("Total des produits", money(income))
        b.metric("Total des charges", money(charges))
        c.metric("Résultat", money(result_net))

        statement = pd.DataFrame([
            {"Poste": "Produits des activités ordinaires saisis", "Montant (MAD)": total_revenue},
            {"Poste": "Autres produits", "Montant (MAD)": other_income},
            {"Poste": "Total des produits", "Montant (MAD)": income},
            {"Poste": "Coût des ventes", "Montant (MAD)": -cost_of_sales},
            {"Poste": "Autres charges d’exploitation", "Montant (MAD)": -operating_expenses},
            {"Poste": "Charges financières", "Montant (MAD)": -finance_costs},
            {"Poste": "Total des charges", "Montant (MAD)": -charges},
            {"Poste": "Résultat simplifié de la période", "Montant (MAD)": result_net},
        ])
        left, right = st.columns([1.2, 1], gap="large")
        with left:
            st.markdown("#### Synthèse des postes")
            st.dataframe(
                statement, use_container_width=True, hide_index=True,
                column_config={
                    "Poste": st.column_config.TextColumn("Poste", width="large"),
                    "Montant (MAD)": st.column_config.NumberColumn("Montant (MAD)", format="%.2f"),
                },
            )
            csv_button(statement, "compte_resultat_simplifie_finacount.csv", "Exporter le compte de résultat (CSV)")
        with right:
            with st.container(border=True):
                st.markdown("**Produits, charges et résultat**")
                if income == 0 and charges == 0:
                    empty_state("Rien à représenter", "Saisissez des produits ou des charges pour voir le graphique.")
                else:
                    fig = go.Figure(go.Bar(
                        x=["Produits", "Charges", "Résultat"], y=[income, charges, result_net],
                        marker_color=[TEAL, GOLD, TEAL if result_net >= 0 else RED],
                        hovertemplate="%{x} : %{y:,.2f} MAD<extra></extra>",
                    ))
                    fig.update_yaxes(gridcolor="#EAF0F5", zeroline=True)
                    st.plotly_chart(styled_plot(fig, 300), use_container_width=True)

    with tab_balance:
        with st.container(border=True):
            st.markdown("#### Test d’équilibre arithmétique")
            st.caption("Ces montants sont saisis séparément et ne sont pas déduits automatiquement des revenus.")
            a, b, c = st.columns(3, gap="medium")
            assets = a.number_input("Total des actifs (MAD)", min_value=0.0, value=0.0, step=1000.0)
            liabilities = b.number_input("Total des passifs (MAD)", min_value=0.0, value=0.0, step=1000.0)
            equity = c.number_input("Capitaux propres (MAD)", min_value=0.0, value=0.0, step=1000.0)
        difference = assets - liabilities - equity
        if abs(difference) < .01:
            st.success("Équilibre arithmétique : actifs = passifs + capitaux propres.")
        else:
            st.warning(f"Écart de contrôle : {money(difference)}. Vérifiez les montants saisis.")
    note("<b>Limite :</b> cette page est une maquette pédagogique. Elle ne produit pas un jeu complet d’états financiers conforme à toutes les exigences de l’IAS 1.")

elif page == "Rapports & exports":
    summary = pd.DataFrame([
        {"Indicateur": "Nombre d’opérations enregistrées", "Valeur": float(len(rev))},
        {"Indicateur": "Total des revenus saisis (MAD)", "Valeur": total_revenue},
        {"Indicateur": "Total des charges de démonstration (MAD)", "Valeur": total_expenses},
        {"Indicateur": "Résultat simplifié (MAD)", "Valeur": net_result},
    ])
    left, right = st.columns([1.3, 1], gap="large")
    with left:
        section("Synthèse", "Principaux indicateurs de la session.", "INDICATEURS")
        st.dataframe(
            summary, use_container_width=True, hide_index=True,
            column_config={
                "Indicateur": st.column_config.TextColumn("Indicateur", width="large"),
                "Valeur": st.column_config.NumberColumn("Valeur", format="%.2f"),
            },
        )
    with right:
        section("Téléchargements", "Les fichiers CSV sont compatibles avec Excel.", "EXPORTS")
        with st.container(border=True):
            csv_button(rev, "registre_revenus_finacount.csv", "Registre des revenus · CSV", key="dl_rev")
            csv_button(exp, "charges_finacount.csv", "Charges · CSV", key="dl_exp")
            csv_button(summary, "synthese_finacount.csv", "Synthèse générale · CSV", key="dl_sum")
            report = f"""FINACOUNT — Rapport pédagogique
Date de génération : {date.today().isoformat()}

Nombre d'opérations : {len(rev)}
Total des revenus saisis : {total_revenue:.2f} MAD
Total des charges de démonstration : {total_expenses:.2f} MAD
Résultat simplifié : {net_result:.2f} MAD

Limites :
- Prototype pédagogique, non certifié.
- Le contrôle IAS 18 est une grille simplifiée nécessitant une revue professionnelle.
- IAS 18 a été remplacée par IFRS 15 à compter de 2018.
- Les chiffres dépendent des données de la session.
"""
            st.download_button("Rapport pédagogique · TXT", report.encode("utf-8"),
                               file_name="rapport_finacount.txt", mime="text/plain", use_container_width=True)

else:
    left, right = st.columns([1.6, 1], gap="large")
    with left:
        st.markdown('<span class="pill">Prototype académique</span>', unsafe_allow_html=True)
        st.markdown("""
**FINACOUNT** est une plateforme pédagogique de présentation financière créée avec
**Python, Streamlit, Pandas et Plotly**.

#### Objectifs
- Enregistrer et centraliser les opérations de revenus.
- Appliquer une grille de contrôle simplifiée inspirée des critères historiques d’IAS 18.
- Illustrer un compte de résultat simplifié et un contrôle arithmétique du bilan.
- Exporter les tableaux pour documenter les vérifications.
""")
    with right:
        with st.container(border=True):
            st.markdown("#### Limites")
            st.markdown(
                "Cette application ne constitue ni un logiciel comptable certifié, ni une mission d’audit, "
                "ni une garantie de conformité aux normes IFRS. Les conclusions nécessitent un jugement professionnel."
            )
    with st.expander("Consulter les références officielles"):
        st.markdown("""
- [IAS 1 — Présentation des états financiers](https://www.ifrs.org/issued-standards/list-of-standards/ias-1-presentation-of-financial-statements/)
- [IAS 18 — Produits des activités ordinaires (ancienne norme)](https://www.ifrs.org/issued-standards/list-of-standards/ias-18-revenue/)
- [IFRS 15 — Produits des activités ordinaires](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-15-revenue-from-contracts-with-customers/)
""")

st.markdown('<div class="footer">FINACOUNT · Prototype pédagogique · Les données restent dans la session de l’application. Vérifier les textes applicables avec l’enseignant.</div>', unsafe_allow_html=True)