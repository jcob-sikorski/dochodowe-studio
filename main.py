import streamlit as st

# -----------------------------
# Mini Kalkulator ROI Studia
# single-screen version
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

# Compact CSS so the whole calculator fits on one screen more easily.
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 1rem;
            max-width: 1280px;
        }

        h1 {
            font-size: 2rem !important;
            margin-bottom: 0.25rem !important;
        }

        h2, h3 {
            margin-top: 0.25rem !important;
            margin-bottom: 0.25rem !important;
        }

        div[data-testid="stMetric"] {
            background: #f7f7f9;
            border: 1px solid #ececf1;
            padding: 0.75rem 0.9rem;
            border-radius: 14px;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.45rem;
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.85rem;
        }

        .small-note {
            font-size: 0.86rem;
            color: #666;
            line-height: 1.35;
        }

        .cta-box {
            background: #f7f7f9;
            border: 1px solid #ececf1;
            padding: 0.85rem 1rem;
            border-radius: 14px;
            font-size: 0.94rem;
            line-height: 1.35;
        }

        .result-box {
            padding: 0.9rem 1rem;
            border-radius: 14px;
            font-size: 0.98rem;
            line-height: 1.38;
            margin-top: 0.25rem;
        }

        .footer-note {
            font-size: 0.78rem;
            color: #777;
            margin-top: 0.5rem;
        }

        hr {
            margin-top: 0.75rem;
            margin-bottom: 0.75rem;
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
    Zmień założenia po lewej i od razu zobacz wynik po prawej: przychód, koszty, zysk,
    czas zwrotu, ROI oraz próg rentowności.
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
                "Klienci",
                min_value=0,
                value=80,
                step=5,
            )

        with col_b:
            avg_package_price = st.number_input(
                "Cena pakietu",
                min_value=0,
                value=700,
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
        st.markdown("**Koszty miesięczne**")
        col_c, col_d = st.columns(2)

        with col_c:
            rent = st.number_input(
                "Najem",
                min_value=0,
                value=8_000,
                step=500,
            )

            marketing = st.number_input(
                "Marketing",
                min_value=0,
                value=5_000,
                step=500,
            )

        with col_d:
            team_cost = st.number_input(
                "Zespół",
                min_value=0,
                value=18_000,
                step=1_000,
            )

            other_costs = st.number_input(
                "Pozostałe",
                min_value=0,
                value=8_000,
                step=500,
                help="Media, księgowość, systemy, recepcja, administracja, drobne koszty.",
            )

# -----------------------------
# Calculations
# -----------------------------

monthly_revenue = clients * avg_package_price + extra_revenue
monthly_costs = rent + team_cost + marketing + other_costs
monthly_profit = monthly_revenue - monthly_costs
annual_profit = monthly_profit * 12

margin = monthly_profit / monthly_revenue if monthly_revenue > 0 else 0
payback_months = capital / monthly_profit if monthly_profit > 0 else None
annual_roi = annual_profit / capital if capital > 0 else None
break_even_clients = monthly_costs / avg_package_price if avg_package_price > 0 else None

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

    if monthly_profit <= 0:
        st.markdown(
            """
            <div class="result-box" style="background:#fff2f2;border:1px solid #ffd6d6;">
            <b>Model się nie spina na tych liczbach.</b><br>
            Studio nie generuje zysku, więc przed decyzją trzeba poprawić cenę,
            liczbę klientów albo koszty.
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif payback_months <= 12:
        st.markdown(
            """
            <div class="result-box" style="background:#eefaf2;border:1px solid #cfeedd;">
            <b>Bardzo ciekawy scenariusz.</b><br>
            Zwrot poniżej 12 miesięcy wygląda atrakcyjnie, ale warto sprawdzić realność
            lokalizacji, sprzedaży i kosztów zespołu.
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif payback_months <= 24:
        st.markdown(
            """
            <div class="result-box" style="background:#f2f7ff;border:1px solid #d6e6ff;">
            <b>Sensowny scenariusz do dalszej analizy.</b><br>
            Zwrot w 12-24 miesiące może być dobrym wynikiem, jeśli założenia są realistyczne.
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif payback_months <= 36:
        st.markdown(
            """
            <div class="result-box" style="background:#fff8e8;border:1px solid #ffe5a8;">
            <b>Scenariusz wymaga ostrożności.</b><br>
            Zwrot w 24-36 miesięcy oznacza, że warto poprawić cenę, sprzedaż lub koszty.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="result-box" style="background:#fff2f2;border:1px solid #ffd6d6;">
            <b>Zwrot powyżej 36 miesięcy.</b><br>
            Bez korekty modelu ta inwestycja może być zbyt słaba względem ryzyka i zaangażowania.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    st.markdown(
        """
        <div class="cta-box">
        <b>Chcesz sprawdzić te liczby dokładniej?</b><br>
        Napisz <b>„ROI”</b> albo wypełnij aplikację, żeby sprawdzić,
        czy ten model ma sens w Twojej lokalizacji, budżecie i terminie startu.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="footer-note">
        Kalkulator ma charakter edukacyjny i poglądowy. Wyniki zależą od lokalizacji,
        oferty, sprzedaży, zespołu, kosztów oraz jakości egzekucji.
        </div>
        """,
        unsafe_allow_html=True,
    )
