import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🚗 Used Cars Data Analysis Dashboard")

# Load data
df = pd.read_excel("vehicles_small.csv")

st.write(df.columns)  # debug once

# Keep only useful columns safely
needed_cols = ["price", "year", "manufacturer", "odometer", "fuel", "transmission"]
available_cols = [c for c in needed_cols if c in df.columns]
df = df[available_cols]

df = df.dropna()


# Remove unrealistic values
df = df[(df["price"] >= 500) & (df["price"] <= 200000)]
df = df[(df["odometer"] >= 0) & (df["odometer"] <= 500000)]

# Convert types
df["price"] = df["price"].astype(float)
df["year"] = df["year"].astype(int)
df["odometer"] = df["odometer"].astype(float)

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
ax1.set_title("Price vs Year")
st.pyplot(fig1)

# Odometer vs Price
st.subheader("Mileage vs Price")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=filtered, x="odometer", y="price", ax=ax2)
ax2.set_title("Mileage vs Price")
st.pyplot(fig2)

# Fuel type distribution
st.subheader("Fuel Type Distribution")
fig3, ax3 = plt.subplots()
sns.countplot(x="fuel", data=filtered, ax=ax3)
ax3.set_title("Fuel Type")
st.pyplot(fig3)

# Transmission distribution
st.subheader("Transmission Distribution")
fig4, ax4 = plt.subplots()
sns.countplot(x="transmission", data=filtered, ax=ax4)
ax4.set_title("Transmission Type")
st.pyplot(fig4)

# Show data
st.subheader("Sample Data")
st.dataframe(filtered.head(20))





