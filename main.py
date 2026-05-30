import streamlit as st

# -----------------------------
# Mini Kalkulator ROI Studia
# wersja z kosztami z tabeli użytkownika
# -----------------------------

st.set_page_config(
    page_title="Mini Kalkulator ROI Butikowego Studia",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def pln(value: float) -> str:
    """Format number as PLN."""
    return f"{value:,.0f} zł".replace(",", " ")


def pct(value: float) -> str:
    """Format decimal as percentage."""
    return f"{value * 100:.1f}%".replace(".", ",")


# Link do aplikacji. Podmień URL na właściwy adres formularza/aplikacji.
APPLICATION_URL = "https://tally.so/r/44zL5o"


# Domyślne koszty miesięczne odczytane z przesłanej tabeli.
DEFAULT_COSTS = {
    "Czynsz": 4_000,
    "Media": 1_200,
    "Sprzątanie": 1_000,
    "Oprogramowanie": 300,
    "Serwis sprzętu / amortyzacja": 500,
    "Księgowość / kasa fiskalna": 500,
    "Ubezpieczenie": 100,
    "Internet / telefon": 200,
    "Koszt marketingu": 300,
    "Podatek": 3_458,
}


st.markdown(
    """
    <style>
        :root {
            --bg: #050706;
            --panel: rgba(13, 16, 14, 0.92);
            --panel-soft: rgba(20, 24, 21, 0.88);
            --line: rgba(0, 191, 68, 0.30);
            --line-soft: rgba(255, 255, 255, 0.10);
            --text: #f4f5f4;
            --muted: rgba(244, 245, 244, 0.68);
            --green: #00bf44;
            --green-strong: #00d84d;
            --green-dark: #008f34;
        }

        html, body, [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 78% 12%, rgba(0, 191, 68, 0.18) 0, transparent 34%),
                linear-gradient(90deg, rgba(0, 0, 0, 0.82) 0%, rgba(0, 0, 0, 0.74) 46%, rgba(0, 0, 0, 0.58) 100%),
                #050706 !important;
            color: var(--text) !important;
        }

        [data-testid="stHeader"] {
            background: rgba(5, 7, 6, 0.72) !important;
            backdrop-filter: blur(10px);
        }

        .block-container {
            padding-top: 1.35rem;
            padding-bottom: 1.15rem;
            max-width: 1280px;
        }

        h1 {
            font-size: clamp(2.1rem, 4vw, 4.4rem) !important;
            line-height: 0.95 !important;
            letter-spacing: -0.06em !important;
            margin-bottom: 0.65rem !important;
            color: var(--text) !important;
            font-weight: 900 !important;
            text-shadow: 0 10px 36px rgba(0, 0, 0, 0.60);
        }

        h1::before {
            content: "Brutalna prawda:";
            display: table;
            background: var(--green);
            color: #ffffff;
            font-size: 0.95rem;
            line-height: 1;
            letter-spacing: 0.01em;
            padding: 0.52rem 1rem;
            margin-bottom: 0.85rem;
            font-weight: 900;
            border-radius: 0;
            text-shadow: none;
        }

        h2, h3 {
            margin-top: 0.25rem !important;
            margin-bottom: 0.65rem !important;
            color: var(--text) !important;
            font-weight: 900 !important;
            letter-spacing: -0.035em !important;
        }

        h2::after, h3::after {
            content: "";
            display: block;
            width: 76px;
            height: 2px;
            background: var(--green);
            margin-top: 0.65rem;
        }

        p, span, label, .stMarkdown, [data-testid="stMarkdownContainer"] {
            color: var(--text);
        }

        .small-note {
            font-size: 0.94rem;
            color: var(--muted);
            line-height: 1.46;
            max-width: 760px;
            border-left: 4px solid var(--green);
            padding-left: 1rem;
        }

        hr {
            border-color: rgba(0, 191, 68, 0.38) !important;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            background: linear-gradient(180deg, rgba(18, 22, 19, 0.96), rgba(8, 10, 9, 0.96)) !important;
            border: 1px solid var(--line) !important;
            border-radius: 0 !important;
            box-shadow: 0 20px 56px rgba(0, 0, 0, 0.34);
        }

        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] strong {
            color: var(--green-strong) !important;
            font-weight: 900 !important;
            letter-spacing: -0.02em;
        }

        div[data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(15, 18, 16, 0.96), rgba(7, 9, 8, 0.96));
            border: 1px solid var(--line);
            padding: 0.9rem 1rem;
            border-radius: 0;
            box-shadow: 0 18px 42px rgba(0, 0, 0, 0.28);
            position: relative;
            overflow: hidden;
        }

        div[data-testid="stMetric"]::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            width: 5px;
            height: 100%;
            background: var(--green);
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.7rem;
            font-weight: 900;
            color: var(--text) !important;
            letter-spacing: -0.045em;
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.82rem;
            font-weight: 800;
            color: var(--muted) !important;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        div[data-testid="stMetricLabel"] p,
        div[data-testid="stMetricValue"] div {
            color: inherit !important;
        }

        label, [data-testid="stWidgetLabel"] p {
            color: var(--text) !important;
            font-weight: 800 !important;
        }

        [data-testid="stNumberInput"] input {
            background: rgba(0, 0, 0, 0.38) !important;
            color: var(--text) !important;
            border: 1px solid var(--line-soft) !important;
            border-radius: 0 !important;
            font-weight: 800 !important;
        }

        [data-testid="stNumberInput"] input:focus {
            border-color: var(--green) !important;
            box-shadow: 0 0 0 1px var(--green) !important;
        }

        [data-testid="stNumberInput"] button {
            background: rgba(0, 191, 68, 0.13) !important;
            border-color: rgba(0, 191, 68, 0.22) !important;
            color: var(--green-strong) !important;
            border-radius: 0 !important;
        }

        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p {
            color: var(--muted) !important;
        }

        .cta-box {
            background: linear-gradient(135deg, rgba(0, 191, 68, 0.24) 0%, rgba(5, 7, 6, 0.98) 44%, rgba(0, 0, 0, 0.98) 100%);
            border: 1px solid var(--green);
            border-radius: 0;
            padding: 1.25rem 1.35rem;
            font-size: 1.02rem;
            line-height: 1.45;
            color: #ffffff;
            box-shadow: 0 22px 60px rgba(0, 0, 0, 0.40), 0 0 36px rgba(0, 191, 68, 0.10);
        }

        .cta-box b {
            display: block;
            font-size: 1.35rem;
            line-height: 1.05;
            margin-bottom: 0.45rem;
            color: #ffffff;
            font-weight: 900;
            letter-spacing: -0.04em;
        }

        .cta-box a {
            color: var(--green-strong) !important;
            font-weight: 900;
            text-decoration: none;
            border-bottom: 2px solid var(--green);
        }

        div[data-testid="stLinkButton"] a {
            width: 100%;
            justify-content: center;
            font-weight: 900;
            padding-top: 0.75rem;
            padding-bottom: 0.75rem;
            background: var(--green) !important;
            color: #ffffff !important;
            border-radius: 0 !important;
            border: 1px solid var(--green) !important;
        }

        .result-box {
            padding: 0.9rem 1rem;
            border-radius: 0;
            font-size: 0.98rem;
            line-height: 1.38;
            margin-top: 0.25rem;
            background: rgba(0, 0, 0, 0.42);
            border: 1px solid var(--line);
        }

        .cost-row {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            padding: 0.42rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.09);
            font-size: 0.92rem;
        }

        .cost-row:last-child {
            border-bottom: none;
        }

        .cost-name {
            color: var(--muted);
            font-weight: 700;
        }

        .cost-value {
            font-weight: 900;
            white-space: nowrap;
            color: var(--green-strong);
        }

        .footer-note {
            font-size: 0.8rem;
            color: var(--muted);
            margin-top: 0.75rem;
            line-height: 1.38;
        }

        [data-testid="stToolbar"],
        [data-testid="stDecoration"] {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Header
# -----------------------------

st.title("Mini Kalkulator ROI Butikowego Studia")
st.markdown(
    """
    <div class="small-note">
    Kalkulator uwzględnia miesięczne koszty z podanej tabeli: czynsz, media, sprzątanie,
    oprogramowanie, serwis/amortyzację, księgowość, ubezpieczenie, licencję muzyczną,
    internet/telefon, marketing oraz podatek.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# -----------------------------
# Layout
# -----------------------------

input_col, output_col = st.columns([0.42, 0.58], gap="large")

with input_col:
    st.subheader("Założenia")

    with st.container(border=True):
        st.markdown("**Inwestycja**")
        capital = st.number_input(
            "Kapitał startowy",
            min_value=0,
            value=120_000,
            step=5_000,
            help="Całkowity koszt wejścia: lokal, sprzęt, kaucja, marketing startowy, bufor.",
        )

    with st.container(border=True):
        st.markdown("**Przychód**")
        col_a, col_b = st.columns(2)

        with col_a:
            clients = st.number_input(
                "Klienci / mies.",
                min_value=0,
                value=80,
                step=5,
            )

        with col_b:
            avg_package_price = st.number_input(
                "Średni przychód z klienta",
                min_value=0,
                value=200,
                step=50,
            )

        extra_revenue = st.number_input(
            "Dodatkowy przychód",
            min_value=0,
            value=0,
            step=500,
            help="Opcjonalnie: eventy, konsultacje, dopłaty, produkty.",
        )

    with st.container(border=True):
        st.markdown("**Koszty miesięczne z Twojej tabeli**")
        st.caption("Możesz je edytować — domyślnie wpisane są wartości z przesłanej tabeli.")

        cost_values = {}
        cost_items = list(DEFAULT_COSTS.items())

        for i in range(0, len(cost_items), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                idx = i + j
                if idx < len(cost_items):
                    label, default_value = cost_items[idx]
                    with col:
                        cost_values[label] = st.number_input(
                            label,
                            min_value=0,
                            value=default_value,
                            step=100,
                            key=f"cost_{idx}",
                        )

# -----------------------------
# Calculations
# -----------------------------

monthly_revenue = clients * avg_package_price + extra_revenue
monthly_costs = sum(cost_values.values())
monthly_costs_without_tax = monthly_costs - cost_values.get("Podatek", 0)
monthly_profit = monthly_revenue - monthly_costs
annual_profit = monthly_profit * 12

margin = monthly_profit / monthly_revenue if monthly_revenue > 0 else 0
payback_months = capital / monthly_profit if monthly_profit > 0 else None
annual_roi = annual_profit / capital if capital > 0 else None
break_even_clients = monthly_costs / avg_package_price if avg_package_price > 0 else None
break_even_revenue = monthly_costs

# -----------------------------
# Outputs
# -----------------------------

with output_col:
    st.subheader("Wynik na żywo")

    m1, m2, m3 = st.columns(3)
    m4, m5, m6 = st.columns(3)

    with m1:
        st.metric("Przychód / mies.", pln(monthly_revenue))

    with m2:
        st.metric("Koszty / mies.", pln(monthly_costs))

    with m3:
        st.metric("Zysk / mies.", pln(monthly_profit))

    with m4:
        st.metric(
            "Czas zwrotu",
            f"{payback_months:.1f} mies.".replace(".", ",") if payback_months else "brak zwrotu",
        )

    with m5:
        st.metric(
            "ROI roczne",
            pct(annual_roi) if annual_roi is not None else "brak danych",
        )

    with m6:
        st.metric(
            "Break-even",
            f"{break_even_clients:.0f} klientów" if break_even_clients is not None else "brak danych",
        )

    st.markdown("")

    summary_col, costs_col = st.columns([0.42, 0.58], gap="medium")

    with summary_col:
        st.markdown("**Podsumowanie kosztów**")
        st.metric("Koszty bez podatku", pln(monthly_costs_without_tax))
        st.metric("Próg przychodu", pln(break_even_revenue))
        st.metric("Marża miesięczna", pct(margin) if monthly_revenue > 0 else "brak danych")

    with costs_col:
        st.markdown("**Dane z tabeli**")
        rows_html = "".join(
            f"""
            <div class="cost-row">
                <span class="cost-name">{name}</span>
                <span class="cost-value">{pln(value)}</span>
            </div>
            """
            for name, value in cost_values.items()
        )
        st.markdown(rows_html, unsafe_allow_html=True)

    st.markdown("")

    st.markdown(
        f"""
        <div class="cta-box">
        <b>Chcesz sprawdzić te liczby dokładniej?</b>
        <a href="{APPLICATION_URL}" target="_blank" rel="noopener noreferrer">
        Wypełnij aplikację
        </a>, żeby sprawdzić, czy ten model ma sens w Twojej lokalizacji, budżecie
        i terminie startu.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="footer-note">
        Kalkulator ma charakter edukacyjny i poglądowy. Wyniki zależą od lokalizacji,
        oferty, sprzedaży, kosztów oraz jakości egzekucji.
        </div>
        """,
        unsafe_allow_html=True,
    )
