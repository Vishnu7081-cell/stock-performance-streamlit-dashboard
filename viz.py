import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(page_title="Stock Performance Dashboard", layout="wide")
st.title("📈 Stock Performance Dashboard")

# -------------------------------
# Company Full Names
# -------------------------------
company_names = {
    "AMZN": "Amazon.com, Inc.",
    "AAPL": "Apple Inc.",
    "GOOGL": "Alphabet Inc. (Google)",
    "GOOG": "Alphabet Inc. (Google)",
    "AAP": "Advance Auto Parts, Inc.",
    "MAA": "Mid-America Apartment Communities, Inc.",
    "GWW": "W. W. Grainger, Inc."
}

# -------------------------------
# Load Data Function
# -------------------------------
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])
    return df

# -------------------------------
# Absolute Windows Paths
# -------------------------------
stocks = {
    "AAP": load_data(r"C:\Users\HP\Desktop\AAP_data.csv"),
    "MAA": load_data(r"C:\Users\HP\Desktop\MAA_data.csv"),
    "GWW": load_data(r"C:\Users\HP\Desktop\GWW_data.csv"),
    "GOOGL": load_data(r"C:\Users\HP\Desktop\GOOGL_data.csv"),
    "AMZN": load_data(r"C:\Users\HP\Desktop\AMZN_data.csv"),
}

# -------------------------------
# Sidebar Navbar (Full Names)
# -------------------------------
st.sidebar.title("📌 Navigation")

menu = ["Dashboard"] + [
    f"{company_names.get(k, k)} ({k})" for k in stocks.keys()
]

selection = st.sidebar.radio("Select Page", menu)

page = "Dashboard" if selection == "Dashboard" else selection.split("(")[-1].replace(")", "")

# -------------------------------
# Dashboard Page
# -------------------------------
if page == "Dashboard":
    st.subheader("📊 All Stock Prices (Single Graph)")

    fig, ax = plt.subplots(figsize=(12, 6))

    for company, df in stocks.items():
        ax.plot(
            df['date'],
            df['close'],
            label=company_names.get(company, company)
        )

    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price")
    ax.set_title("Closing Price Comparison of All Companies")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

# -------------------------------
# Individual Stock Pages
# -------------------------------
else:
    df = stocks[page]

    st.subheader(
        f"📉 {company_names.get(page, page)} ({page}) Stock Performance"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Latest Close Price",
            round(df['close'].iloc[-1], 2),
            round(df['close'].iloc[-1] - df['close'].iloc[-2], 2)
        )

    with col2:
        st.metric(
            "Latest Open Price",
            round(df['open'].iloc[-1], 2)
        )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['date'], df['open'], label="Open Price")
    ax.plot(df['date'], df['close'], label="Close Price")

    ax.set_title(
        f"{company_names.get(page, page)} – Open vs Close Price"
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("📌 Stock Performance Analysis using Streamlit")
