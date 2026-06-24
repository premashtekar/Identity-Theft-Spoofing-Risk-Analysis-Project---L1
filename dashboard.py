import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(

    page_title="Identity Theft Dashboard",

    page_icon="🛡️",

    layout="wide"

)


# ===================================
# LOAD DATA
# ===================================

alerts = pd.read_csv("risk_alerts.csv")

users = pd.read_csv("master_user_data.csv")

risk_summary = pd.read_csv("risk_summary.csv")

top_users = pd.read_csv("top_suspicious_users.csv")

city_distribution = pd.read_csv("city_distribution.csv")

alert_distribution = pd.read_csv("alert_distribution.csv")


alerts["timestamp"] = pd.to_datetime(

    alerts["timestamp"]

)


# ===================================
# HEADER
# ===================================

st.title(

    "🛡️ Identity Theft & Spoofing Risk Analysis"

)

st.markdown(

    "Cybersecurity Analytics Dashboard"

)

st.divider()


# ===================================
# SIDEBAR FILTERS
# ===================================

st.sidebar.header("Filters")


selected_risk = st.sidebar.multiselect(

    "Risk Level",

    alerts["risk_level"].unique(),

    default=alerts["risk_level"].unique()

)


selected_alert = st.sidebar.multiselect(

    "Alert Type",

    alerts["alert_type"].unique(),

    default=alerts["alert_type"].unique()

)


selected_city = st.sidebar.multiselect(

    "City",

    alerts["location"].unique(),

    default=alerts["location"].unique()

)


filtered = alerts[

    alerts["risk_level"].isin(selected_risk)

]

filtered = filtered[

    filtered["alert_type"].isin(selected_alert)

]

filtered = filtered[

    filtered["location"].isin(selected_city)

]


# ===================================
# KPI CARDS
# ===================================

col1, col2, col3, col4 = st.columns(4)


total_alerts = len(filtered)

suspicious_users = filtered["user_id"].nunique()

high_risk_users = len(

    risk_summary[

        risk_summary["overall_risk"]

        ==

        "HIGH"

    ]

)


highest_user = (

    risk_summary

    .sort_values(

        by="max_risk_score",

        ascending=False

    )

    .iloc[0]["user_id"]

)


col1.metric(

    "Total Alerts",

    total_alerts

)

col2.metric(

    "Suspicious Users",

    suspicious_users

)

col3.metric(

    "High Risk Users",

    high_risk_users

)

col4.metric(

    "Highest Risk User",

    highest_user

)

st.divider()


# ===================================
# RISK DISTRIBUTION
# ===================================

st.subheader("Risk Distribution")


risk_counts = (

    filtered["risk_level"]

    .value_counts()

)

fig = plt.figure(

    figsize=(6,4)

)

plt.bar(

    risk_counts.index,

    risk_counts.values

)

plt.xlabel("Risk Level")

plt.ylabel("Count")

plt.title("Risk Distribution")

st.pyplot(fig)


# ===================================
# ALERT TYPE DISTRIBUTION
# ===================================

st.subheader("Alert Type Distribution")


alert_counts = (

    filtered["alert_type"]

    .value_counts()

)

fig = plt.figure(

    figsize=(6,6)

)

plt.pie(

    alert_counts.values,

    labels=alert_counts.index,

    autopct="%1.1f%%"

)

plt.title("Alert Types")

st.pyplot(fig)


# ===================================
# TOP SUSPICIOUS USERS
# ===================================

st.subheader(

    "Top Suspicious Users"

)

fig = plt.figure(

    figsize=(10,5)

)

plt.bar(

    top_users["user_id"],

    top_users["total_alerts"]

)

plt.xlabel("User")

plt.ylabel("Alerts")

plt.title("Top 10 Suspicious Users")

plt.xticks(rotation=45)

st.pyplot(fig)


# ===================================
# CITY DISTRIBUTION
# ===================================

st.subheader(

    "Suspicious Logins by City"

)

fig = plt.figure(

    figsize=(8,5)

)

plt.bar(

    city_distribution["city"],

    city_distribution["count"]

)

plt.xlabel("City")

plt.ylabel("Count")

plt.title("City Distribution")

plt.xticks(rotation=45)

st.pyplot(fig)


# ===================================
# LOGIN TREND
# ===================================

st.subheader(

    "Suspicious Login Trend"

)


trend = (

    filtered

    .groupby(

        filtered["timestamp"].dt.date

    )

    .size()

)

fig = plt.figure(

    figsize=(10,5)

)

plt.plot(

    trend.index,

    trend.values

)

plt.xlabel("Date")

plt.ylabel("Suspicious Logins")

plt.title("Login Trend")

plt.xticks(rotation=45)

st.pyplot(fig)


# ===================================
# DATA TABLE
# ===================================

st.subheader(

    "Alert Table"

)

st.dataframe(

    filtered,

    use_container_width=True

)


# ===================================
# FOOTER
# ===================================

st.success(

    "Dashboard Loaded Successfully"

)