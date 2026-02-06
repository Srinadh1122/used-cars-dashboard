import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🚗 Used Cars Data Analysis Dashboard")

# Load CSV properly (your header is stored as data)
df = pd.read_csv("vehicles_small.csv", header=None)

# Assign correct column names
df.columns = ["price", "year", "manufacturer", "odometer", "fuel", "transmission"]

# Drop first row (it contains header text)
df = df.iloc[1:]

# Convert types
df["price"] = df["price"].astype(float)
df["year"] = df["year"].astype(int)
df["odometer"] = df["odometer"].astype(float)

st.write("Columns:", df.columns)
st.dataframe(df.head())

# Remove unrealistic values
df = df[(df["price"] >= 500) & (df["price"] <= 200000)]
df = df[(df["odometer"] >= 0) & (df["odometer"] <= 500000)]

# Sidebar filter
st.sidebar.header("Filter Options")
brand = st.sidebar.selectbox("Select Manufacturer", sorted(df["manufacturer"].unique()))

filtered = df[df["manufacturer"] == brand]

# KPI metrics
st.subheader(f"Overview for {brand}")
col1, col2, col3 = st.columns(3)
col1.metric("Average Price", f"${filtered['price'].mean():,.0f}")
col2.metric("Average Mileage", f"{filtered['odometer'].mean():,.0f}")
col3.metric("Total Listings", filtered.shape[0])

# Price vs Year
st.subheader("Price Trend by Year")
fig1, ax1 = plt.subplots()
sns.lineplot(data=filtered, x="year", y="price", ax=ax1)
st.pyplot(fig1)

# Odometer vs Price
st.subheader("Mileage vs Price")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=filtered, x="odometer", y="price", ax=ax2)
st.pyplot(fig2)

# Fuel type distribution
st.subheader("Fuel Type Distribution")
fig3, ax3 = plt.subplots()
sns.countplot(x="fuel", data=filtered, ax=ax3)
st.pyplot(fig3)

# Transmission distribution
st.subheader("Transmission Distribution")
fig4, ax4 = plt.subplots()
sns.countplot(x="transmission", data=filtered, ax=ax4)
st.pyplot(fig4)

# Show data
st.subheader("Sample Data")
st.dataframe(filtered.head(20))
