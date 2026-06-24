import pandas as pd
from math import radians, sin, cos, sqrt, atan2


# ====================================
# LOAD DATASET
# ====================================

df = pd.read_csv("master_login_data.csv")

df["login_time"] = pd.to_datetime(df["login_time"])

df = df.sort_values(
    by=["user_id", "login_time"]
)


# ====================================
# DISTANCE CALCULATION
# ====================================

def cal_distance(lat1, lon1, lat2, lon2):

    R = 6371

    lat1 = radians(lat1)
    lon1 = radians(lon1)

    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        +
        cos(lat1)
        *
        cos(lat2)
        *
        sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return R * c


# ====================================
# IMPOSSIBLE TRAVEL DETECTION
# ====================================

def detect_impossible_travel(df):

    alerts = []

    for i in range(len(df) - 1):

        if (
            df.iloc[i]["user_id"]
            !=
            df.iloc[i + 1]["user_id"]
        ):

            continue

        lat1 = df.iloc[i]["latitude"]
        lon1 = df.iloc[i]["longitude"]

        lat2 = df.iloc[i + 1]["latitude"]
        lon2 = df.iloc[i + 1]["longitude"]

        distance = cal_distance(
            lat1,
            lon1,
            lat2,
            lon2
        )

        time1 = df.iloc[i]["login_time"]

        time2 = df.iloc[i + 1]["login_time"]

        hours = (
            time2 - time1
        ).total_seconds() / 3600

        if hours <= 0:

            continue

        if distance > 800 and hours < 24:

            alerts.append({

                "user_id":
                df.iloc[i]["user_id"],

                "alert_type":
                "IMPOSSIBLE_TRAVEL",

                "risk_score":
                90,

                "risk_level":
                "HIGH",

                "timestamp":
                df.iloc[i + 1]["login_time"],

                "location":
                df.iloc[i + 1]["city"]

            })

    return pd.DataFrame(alerts)


# ====================================
# DEVICE SPOOFING DETECTION
# ====================================

def detect_device_spoofing(df):

    alerts = []

    for i in range(len(df) - 1):

        if (
            df.iloc[i]["user_id"]
            !=
            df.iloc[i + 1]["user_id"]
        ):

            continue

        time1 = df.iloc[i]["login_time"]

        time2 = df.iloc[i + 1]["login_time"]

        minutes = (
            time2 - time1
        ).total_seconds() / 60

        device1 = df.iloc[i]["device"]

        device2 = df.iloc[i + 1]["device"]

        city1 = df.iloc[i]["city"]

        city2 = df.iloc[i + 1]["city"]

        if (

            device1 != device2

            and

            minutes < 5

            and

            city1 != city2

        ):

            alerts.append({

                "user_id":
                df.iloc[i]["user_id"],

                "alert_type":
                "DEVICE_SPOOFING",

                "risk_score":
                70,

                "risk_level":
                "MEDIUM",

                "timestamp":
                df.iloc[i + 1]["login_time"],

                "location":
                city2

            })

    return pd.DataFrame(alerts)


# ====================================
# ODD HOUR LOGIN DETECTION
# ====================================

def odd_login(df):

    alerts = []

    for user_id, group in df.groupby("user_id"):

        total_logins = len(group)

        night_logins = group[

            (group["login_time"].dt.hour >= 2)

            &

            (group["login_time"].dt.hour < 5)

        ]

        night_count = len(night_logins)

        percentage = (

            night_count / total_logins

        ) * 100

        if percentage < 20:

            for _, row in night_logins.iterrows():

                alerts.append({

                    "user_id":
                    user_id,

                    "alert_type":
                    "ODD_HOURS",

                    "risk_score":
                    30,

                    "risk_level":
                    "LOW",

                    "timestamp":
                    row["login_time"],

                    "location":
                    row["city"],

                    "details":
                    f"Night login percentage: {round(percentage,2)}%"

                })

    return pd.DataFrame(alerts)


# ====================================
# RUN DETECTORS
# ====================================

travel_alerts = detect_impossible_travel(df)

device_alerts = detect_device_spoofing(df)

odd_alerts = odd_login(df)


# ====================================
# MERGE ALERTS
# ====================================

master_alert = pd.concat(

    [

        travel_alerts,

        device_alerts,

        odd_alerts

    ],

    ignore_index=True

)

master_alert = master_alert.sort_values(

    by="risk_score",

    ascending=False

)


# ====================================
# USER RISK SUMMARY
# ====================================

def calculate_user_risk(master_alert):

    summary = []

    for user_id, group in master_alert.groupby("user_id"):

        max_score = group["risk_score"].max()

        if "HIGH" in group["risk_level"].values:

            overall = "HIGH"

        elif "MEDIUM" in group["risk_level"].values:

            overall = "MEDIUM"

        elif "LOW" in group["risk_level"].values:

            overall = "LOW"

        else:

            overall = "NO RISK"

        summary.append({

            "user_id":
            user_id,

            "max_risk_score":
            max_score,

            "overall_risk":
            overall

        })

    return pd.DataFrame(summary)


summary_alert = calculate_user_risk(master_alert)


# ====================================
# SAVE FILES
# ====================================

master_alert.to_csv(

    "risk_alerts.csv",

    index=False

)

summary_alert.to_csv(

    "risk_summary.csv",

    index=False

)


# ====================================
# MARK SUSPICIOUS USERS
# ====================================

df["is_suspicious"] = 0

sus_users = master_alert["user_id"].unique()

df.loc[

    df["user_id"].isin(sus_users),

    "is_suspicious"

] = 1


df.to_csv(

    "master_user_data.csv",

    index=False

)

print("main.py completed successfully")
