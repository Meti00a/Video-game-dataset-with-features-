import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine
import joblib


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Video Game Dashboard",
    page_icon="🎮",
    layout="wide"
)


# ============================================================
# BACKEND - DATABASE
# ============================================================

engine = create_engine("sqlite:///games.db")


@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM games", engine)


df = load_data()

# Convert release date once
df["release_date"] = pd.to_datetime(
    df["release_date"],
    errors="coerce"
)


# ============================================================
# HEADER
# ============================================================

st.title("🎮 Video Game Dashboard")
st.caption("Explore video game sales, ratings and statistics")
st.image("gaming.jpg", use_container_width=True)

# ============================================================
# OVERVIEW METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Number of Games",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "Total Sales",
        f"{df['total_sales'].sum():,.1f} M"
    )

with col3:
    st.metric(
        "Average Critic Score",
        f"{df['critic_score'].mean():.1f}"
    )

with col4:
    st.metric(
        "Consoles",
        f"{df['console'].nunique():,}"
    )


st.divider()


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🤖 AI Predictor",
    "🔎 Search & Filter",
    "📈 Statistics"
])


# ============================================================
# TAB 1 - OVERVIEW
# ============================================================

with tab1:

    st.header("Top Selling Games")
    st.write("The 10 games with the highest total sales.")

    top_games = (
        df.sort_values(
            "total_sales",
            ascending=False
        )
        .head(10)
    )

    col1, col2 = st.columns([1.4, 1])

    # -----------------------------
    # Chart
    # -----------------------------

    with col1:

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            top_games["title"],
            top_games["total_sales"]
        )

        ax.set_xlabel("Game")
        ax.set_ylabel("Total Sales (Millions)")
        ax.set_title("Top 10 Best Selling Games")

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.tight_layout()

        st.pyplot(fig)

    # -----------------------------
    # Table
    # -----------------------------

    with col2:

        st.dataframe(
            top_games[
                [
                    "title",
                    "console",
                    "genre",
                    "total_sales"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# TAB 2 - AI PREDICTOR
# ============================================================

with tab2:

    st.header("🤖 AI Sales Predictor")

    st.write(
        "Use the trained machine learning model to "
        "predict total game sales based on the Critic Score."
    )

    try:

        model = joblib.load("sales_model.pkl")

        col1, col2 = st.columns([1, 2])

        with col1:

            input_score = st.number_input(
                "Critic Score",
                min_value=0.0,
                max_value=10.0,
                value=8.0,
                step=0.1
            )

            predict_button = st.button(
                "🔮 Predict Sales",
                use_container_width=True
            )

        with col2:

            if predict_button:

                predicted_sales = model.predict(
                    [[input_score]]
                )[0]

                predicted_sales = max(
                    0,
                    predicted_sales
                )

                st.success(
                    f"### {predicted_sales:.2f} million units"
                )

                st.caption(
                    "Predicted total sales based on the entered Critic Score."
                )

            else:

                st.info(
                    "Enter a Critic Score and press "
                    "**Predict Sales**."
                )

    except Exception:

        st.warning(
            "No saved AI model was found. "
            "Run `train_model.py` first to generate it."
        )


# ============================================================
# TAB 3 - SEARCH & FILTER
# ============================================================

with tab3:

    st.header("🔎 Search & Filter Games")

    col1, col2 = st.columns(2)

    # -----------------------------
    # Search
    # -----------------------------

    with col1:

        search = st.text_input(
            "Search for a game",
            placeholder="Enter game title..."
        )

    # -----------------------------
    # Score filter
    # -----------------------------

    with col2:

        score = st.slider(
            "Minimum Critic Score",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.1
        )

    # -----------------------------
    # Apply filters
    # -----------------------------

    filtered_games = df[
        df["critic_score"] >= score
    ]

    if search:

        filtered_games = filtered_games[
            filtered_games["title"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.divider()

    st.subheader(
        f"Results: {len(filtered_games):,} games"
    )

display_columns = [
    "title",
    "console",
    "genre",
    "critic_score",
    "total_sales"
]

st.dataframe(
    filtered_games[display_columns],
    use_container_width=True,
    hide_index=True
)


# ============================================================
# TAB 4 - STATISTICS
# ============================================================

with tab4:

    st.header("📈 Game Statistics")

    col1, col2 = st.columns(2)
    # ========================================================
    # SALES BY GENRE
    # ========================================================
    with col1:
        st.subheader("Sales by Genre")
    col1, col2 =st.columns(2)

    genre_sales = (
        df.groupby("genre")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        genre_sales.index,
        genre_sales.values
    )

    ax.set_xlabel("Genre")
    ax.set_ylabel("Total Sales (Millions)")
    ax.set_title("Total Sales by Genre")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    st.pyplot(fig)


    # ========================================================
    # SALES BY CONSOLE
    # ========================================================
    with col2:
        st.subheader("Sales by Console")

    console_sales = (
        df.groupby("console")["total_sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        console_sales.index,
        console_sales.values
    )

    ax.set_xlabel("Console")
    ax.set_ylabel("Total Sales (Millions)")
    ax.set_title("Top 10 Consoles by Sales")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    st.pyplot(fig)


    # ========================================================
    # SALES BY REGION
    # ========================================================
    with col3:
        st.subheader("Sales by Region")

    region_sales = {
        "North America": df["na_sales"].sum(),
        "Japan": df["jp_sales"].sum(),
        "Europe": df["pal_sales"].sum(),
        "Other": df["other_sales"].sum()
    }

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        region_sales.keys(),
        region_sales.values()
    )

    ax.set_xlabel("Region")
    ax.set_ylabel("Total Sales (Millions)")
    ax.set_title("Total Sales by Region")

    plt.tight_layout()

    st.pyplot(fig)


    # ========================================================
    # RELEASE YEAR
    # ========================================================
    with col4:
        st.subheader("Games Released by Year")

    release_year = (
        df["release_date"]
        .dt.year
        .value_counts()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        release_year.index,
        release_year.values
    )

    ax.set_xlabel("Release Year")
    ax.set_ylabel("Number of Games")
    ax.set_title("Games Released by Year")

    plt.tight_layout()

    st.pyplot(fig)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Video Game Dashboard • Built with Streamlit, Pandas, "
    "SQLAlchemy and Scikit-learn"
)
