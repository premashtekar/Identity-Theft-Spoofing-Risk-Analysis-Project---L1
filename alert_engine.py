import pandas as pd


# ====================================
# LOAD FILES
# ====================================

alerts = pd.read_csv("risk_alerts.csv")

risk_summary = pd.read_csv("risk_summary.csv")

users = pd.read_csv("master_user_data.csv")


# ====================================
# OVERALL STATISTICS
# ====================================

total_alerts = len(alerts)

high_risk = len(

    alerts[

        alerts["risk_level"]

        ==

        "HIGH"

    ]

)

medium_risk = len(

    alerts[

        alerts["risk_level"]

        ==

        "MEDIUM"

    ]

)

low_risk = len(

    alerts[

        alerts["risk_level"]

        ==

        "LOW"

    ]

)

total_suspicious_users = users[

    users["is_suspicious"] == 1

]["user_id"].nunique()


# ====================================
# ALERT DISTRIBUTION
# ====================================

alert_distribution = (

    alerts["alert_type"]

    .value_counts()

    .reset_index()

)

alert_distribution.columns = [

    "alert_type",

    "count"

]


# ====================================
# TOP USERS
# ====================================

top_users = (

    alerts.groupby("user_id")

    .agg(

        total_alerts=(

            "user_id",

            "count"

        ),

        highest_score=(

            "risk_score",

            "max"

        )

    )

    .reset_index()

)

top_users = top_users.sort_values(

    by=[

        "highest_score",

        "total_alerts"

    ],

    ascending=False

)

top_users = top_users.head(10)


# ====================================
# CITY DISTRIBUTION
# ====================================

city_distribution = (

    alerts["location"]

    .value_counts()

    .reset_index()

)

city_distribution.columns = [

    "city",

    "count"

]


# ====================================
# PRINT REPORT
# ====================================

print("\n=========================")

print("ALERT SUMMARY REPORT")

print("=========================")

print(f"Total Alerts : {total_alerts}")

print(f"HIGH Risk : {high_risk}")

print(f"MEDIUM Risk : {medium_risk}")

print(f"LOW Risk : {low_risk}")

print(

    f"Suspicious Users : {total_suspicious_users}"

)


print("\nTOP SUSPICIOUS USERS")

print(top_users)


# ====================================
# SAVE FILES
# ====================================

alert_distribution.to_csv(

    "alert_distribution.csv",

    index=False

)

top_users.to_csv(

    "top_suspicious_users.csv",

    index=False

)

city_distribution.to_csv(

    "city_distribution.csv",

    index=False

)

print("\nPhase 3 completed successfully.")