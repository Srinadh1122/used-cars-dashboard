import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Used Cars Dashboard", layout="wide")

st.title("🚗 Used Cars Data Analysis Dashboard")

# ---------------------------
# Load data safely
# ---------------------------
df = pd.read_csv("vehicles_small.csv", header=None)

# If everything is in one column → split it
if df.shape[1] == 1:
    df = df[0].str.split(",", expand=True)

df.columns = ["price", "year", "manufacturer", "odometer", "fuel", "transmission"]

# Remove header row if it exists inside data
df = df[df["price"] != "price"]

# Convert numeric columns safely
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["odometer"] = pd.to_numeric(df["odometer"], errors="coerce")

# Drop bad rows
df = df.dropna()

# Filter unrealistic values
df = df[(df["price"] >= 500) & (df["price"] <= 200000)]
df = df[(df["odometer"] >= 0) & (df["odometer"] <= 500000)]

st.write("Dataset Preview:")
st.dataframe(df.head())

# ---------------------------
# Sidebar filter
# ---------------------------
st.sidebar.header("Filter Options")
brand = st.sidebar.selectbox("Select Manufacturer", sorted(df["manufacturer"].unique()))

filtered = df[df["manufacturer"] == brand]

# ---------------------------
# KPI Metrics
# ---------------------------
st.subheader(f"Overview for {brand}")
col1, col2, col3 = st.columns(3)

col1.metric("Average Price", f"${filtered['price'].mean():,.0f}")
col2.metric("Average Mileage", f"{filtered['odometer'].mean():,.0f}")
col3.metric("Total Listings", filtered.shape[0])

# ---------------------------
# Price vs Year
# ---------------------------
st.subheader("📈 Price Trend by Year")
fig1, ax1 = plt.subplots()
sns.lineplot(data=filtered, x="year", y="price", ax=ax1)
ax1.set_xlabel("Year")
ax1.set_ylabel("Price")
st.pyplot(fig1)

# ---------------------------
# Odometer vs Price
# ---------------------------
st.subheader("📉 Mileage vs Price")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=filtered, x="odometer", y="price", ax=ax2)
ax2.set_xlabel("Mileage")
ax2.set_ylabel("Price")
st.pyplot(fig2)

# ---------------------------
# Fuel distribution
# ---------------------------
st.subheader("⛽ Fuel Type Distribution")
fig3, ax3 = plt.subplots()
sns.countplot(x="fuel", data=filtered, ax=ax3)
st.pyplot(fig3)

# ---------------------------
# Transmission distribution
# ---------------------------
st.subheader("⚙ Transmission Distribution")
fig4, ax4 = plt.subplots()
sns.countplot(x="transmission", data=filtered, ax=ax4)
st.pyplot(fig4)

# ---------------------------
# Table
# ---------------------------
st.subheader("Sample Data")
st.dataframe(filtered.head(20))
