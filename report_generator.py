import os
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch

# ======================================================
# LOAD DATA
# ======================================================

alerts = pd.read_csv("risk_alerts.csv")

risk_summary = pd.read_csv("risk_summary.csv")

master_data = pd.read_csv("master_user_data.csv")

alert_distribution = pd.read_csv("alert_distribution.csv")

city_distribution = pd.read_csv("city_distribution.csv")

top_users = pd.read_csv("top_suspicious_users.csv")


alerts["timestamp"] = pd.to_datetime(
    alerts["timestamp"]
)

# ======================================================
# PROJECT STATISTICS
# ======================================================

total_logins = len(master_data)

total_users = master_data["user_id"].nunique()

total_alerts = len(alerts)

high_users = len(
    risk_summary[
        risk_summary["overall_risk"] == "HIGH"
    ]
)

medium_users = len(
    risk_summary[
        risk_summary["overall_risk"] == "MEDIUM"
    ]
)

low_users = len(
    risk_summary[
        risk_summary["overall_risk"] == "LOW"
    ]
)

suspicious_users = master_data[
    master_data["is_suspicious"] == 1
]["user_id"].nunique()

# ======================================================
# CREATE GRAPH FOLDER
# ======================================================

os.makedirs(
    "graphs",
    exist_ok=True
)

# ======================================================
# GRAPH 1 : RISK DISTRIBUTION
# ======================================================

risk_counts = (
    risk_summary["overall_risk"]
    .value_counts()
)

plt.figure(figsize=(7,4))

plt.bar(
    risk_counts.index,
    risk_counts.values
)

plt.title("Risk Distribution")

plt.xlabel("Risk Level")

plt.ylabel("Users")

plt.tight_layout()

plt.savefig(
    "graphs/risk_distribution.png"
)

plt.close()

# ======================================================
# GRAPH 2 : ALERT DISTRIBUTION
# ======================================================

plt.figure(figsize=(6,6))

plt.pie(

    alert_distribution["count"],

    labels=alert_distribution["alert_type"],

    autopct="%1.1f%%"

)

plt.title("Alert Type Distribution")

plt.tight_layout()

plt.savefig(
    "graphs/alert_distribution.png"
)

plt.close()

# ======================================================
# GRAPH 3 : CITY DISTRIBUTION
# ======================================================

plt.figure(figsize=(8,4))

plt.bar(

    city_distribution["city"],

    city_distribution["count"]

)

plt.title("Suspicious Logins by City")

plt.xlabel("City")

plt.ylabel("Alerts")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "graphs/city_distribution.png"
)

plt.close()

# ======================================================
# GRAPH 4 : LOGIN TREND
# ======================================================

trend = (

    alerts

    .groupby(

        alerts["timestamp"].dt.date

    )

    .size()

)

plt.figure(figsize=(8,4))

plt.plot(

    trend.index,

    trend.values,

    marker="o"

)

plt.title("Suspicious Login Trend")

plt.xlabel("Date")

plt.ylabel("Alerts")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "graphs/login_trend.png"
)

plt.close()

print("All graphs generated successfully.")

# ======================================================
# CREATE PDF
# ======================================================

pdf = SimpleDocTemplate(

    "cybersecurity_report.pdf"

)

styles = getSampleStyleSheet()

story = []

title_style = styles["Title"]

title_style.alignment = TA_CENTER

heading = styles["Heading1"]

normal = styles["BodyText"]
# ======================================================
# COVER PAGE
# ======================================================

story.append(
    Paragraph(
        "Identity Theft & Spoofing Risk Analysis",
        title_style
    )
)

story.append(Spacer(1, 25))

story.append(
    Paragraph(
        "Cybersecurity Analytics Report",
        styles["Heading2"]
    )
)

story.append(Spacer(1, 35))

story.append(
    Paragraph(
        "<b>Prepared Using Python, Pandas, Matplotlib, Streamlit & ReportLab</b>",
        normal
    )
)

story.append(Spacer(1, 15))

story.append(
    Paragraph(
        "<b>Generated Automatically</b>",
        normal
    )
)

story.append(Spacer(1, 20))

story.append(
    Paragraph(
        f"<b>Total Login Records :</b> {total_logins}",
        normal
    )
)

story.append(
    Paragraph(
        f"<b>Total Alerts :</b> {total_alerts}",
        normal
    )
)

story.append(
    Paragraph(
        f"<b>Suspicious Users :</b> {suspicious_users}",
        normal
    )
)

story.append(PageBreak())

# ======================================================
# PROJECT OVERVIEW
# ======================================================

story.append(
    Paragraph(
        "Project Overview",
        heading
    )
)

overview = """
The Identity Theft & Spoofing Risk Analysis system detects suspicious login
activities using rule-based cybersecurity analytics.

The project focuses on identifying users who exhibit suspicious behaviour
through multiple security rules.

The implemented detection modules include:

• Impossible Travel Detection

• Device Spoofing Detection

• Odd Hour Login Detection

Each detected activity is assigned a LOW, MEDIUM or HIGH risk score
which helps security analysts prioritize investigation.
"""

story.append(
    Paragraph(
        overview,
        normal
    )
)

story.append(Spacer(1, 20))

# ======================================================
# EXECUTIVE SUMMARY
# ======================================================

story.append(
    Paragraph(
        "Executive Summary",
        heading
    )
)

summary = f"""
The system processed <b>{total_logins}</b> login records belonging to
<b>{total_users}</b> unique users.

A total of <b>{total_alerts}</b> suspicious activities were detected.

<b>{high_users}</b> users were classified as HIGH risk.

<b>{medium_users}</b> users were classified as MEDIUM risk.

<b>{low_users}</b> users were classified as LOW risk.

Overall, <b>{suspicious_users}</b> users require further security investigation.
"""

story.append(
    Paragraph(
        summary,
        normal
    )
)

story.append(Spacer(1, 20))

# ======================================================
# PROJECT STATISTICS TABLE
# ======================================================

story.append(
    Paragraph(
        "Project Statistics",
        heading
    )
)

story.append(Spacer(1, 10))

stats = [

    ["Metric", "Value"],

    ["Total Login Records", total_logins],

    ["Unique Users", total_users],

    ["Total Alerts", total_alerts],

    ["Suspicious Users", suspicious_users],

    ["High Risk Users", high_users],

    ["Medium Risk Users", medium_users],

    ["Low Risk Users", low_users]

]

table = Table(
    stats,
    colWidths=[260, 170]
)

table.setStyle(

    TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#003366")),

        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("GRID", (0,0), (-1,-1), 1, colors.black),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

        ("BACKGROUND", (0,1), (-1,-1), colors.beige),

        ("ALIGN", (0,0), (-1,-1), "CENTER"),

        ("BOTTOMPADDING", (0,0), (-1,0), 10)

    ])

)

story.append(table)

story.append(Spacer(1, 25))

# ======================================================
# RISK DISTRIBUTION TABLE
# ======================================================

story.append(
    Paragraph(
        "Risk Distribution",
        heading
    )
)

story.append(Spacer(1, 10))

risk_table = [["Risk Level", "Number of Users"]]

risk_counts = risk_summary["overall_risk"].value_counts()

for risk, count in risk_counts.items():

    risk_table.append([risk, count])

risk_pdf = Table(
    risk_table,
    colWidths=[220, 180]
)

risk_pdf.setStyle(

    TableStyle([

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,0),(-1,0),colors.darkgreen),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke)

    ])

)

story.append(risk_pdf)

story.append(Spacer(1,25))

# ======================================================
# ALERT DISTRIBUTION TABLE
# ======================================================

story.append(
    Paragraph(
        "Alert Distribution",
        heading
    )
)

story.append(Spacer(1,10))

alert_table = [["Alert Type","Count"]]

for _, row in alert_distribution.iterrows():

    alert_table.append([

        row["alert_type"],

        row["count"]

    ])

alert_pdf = Table(
    alert_table,
    colWidths=[250,150]
)

alert_pdf.setStyle(

    TableStyle([

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,0),(-1,0),colors.darkred),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige)

    ])

)

story.append(alert_pdf)

story.append(Spacer(1,25))

# ======================================================
# TOP SUSPICIOUS USERS TABLE
# ======================================================

story.append(
    Paragraph(
        "Top Suspicious Users",
        heading
    )
)

story.append(Spacer(1,10))

top_table = [

    ["User ID","Total Alerts","Highest Score"]

]

for _, row in top_users.iterrows():

    top_table.append([

        row["user_id"],

        row["total_alerts"],

        row["highest_score"]

    ])

top_pdf = Table(
    top_table,
    colWidths=[150,150,150]
)

top_pdf.setStyle(

    TableStyle([

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,0),(-1,0),colors.orange),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke)

    ])

)

story.append(top_pdf)

story.append(Spacer(1,25))

# ======================================================
# CITY DISTRIBUTION TABLE
# ======================================================

story.append(
    Paragraph(
        "City Distribution",
        heading
    )
)

story.append(Spacer(1,10))

city_table = [

    ["City","Suspicious Logins"]

]

for _, row in city_distribution.iterrows():

    city_table.append([

        row["city"],

        row["count"]

    ])

city_pdf = Table(
    city_table,
    colWidths=[220,180]
)

city_pdf.setStyle(

    TableStyle([

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,0),(-1,0),colors.purple),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BACKGROUND",(0,1),(-1,-1),colors.lavender)

    ])

)

story.append(city_pdf)

story.append(PageBreak())
# ======================================================
# VISUAL ANALYSIS
# ======================================================

story.append(
    Paragraph(
        "Visual Analysis",
        heading
    )
)

story.append(Spacer(1, 15))

# ------------------------------------------------------
# Risk Distribution Graph
# ------------------------------------------------------

story.append(
    Paragraph(
        "1. Risk Distribution",
        styles["Heading2"]
    )
)

story.append(
    Image(
        "graphs/risk_distribution.png",
        width=6.5 * inch,
        height=3.8 * inch
    )
)

story.append(Spacer(1, 20))

# ------------------------------------------------------
# Alert Distribution Graph
# ------------------------------------------------------

story.append(
    Paragraph(
        "2. Alert Type Distribution",
        styles["Heading2"]
    )
)

story.append(
    Image(
        "graphs/alert_distribution.png",
        width=6 * inch,
        height=4 * inch
    )
)

story.append(Spacer(1, 20))

# ------------------------------------------------------
# City Distribution Graph
# ------------------------------------------------------

story.append(
    Paragraph(
        "3. City Distribution",
        styles["Heading2"]
    )
)

story.append(
    Image(
        "graphs/city_distribution.png",
        width=6.5 * inch,
        height=3.8 * inch
    )
)

story.append(Spacer(1, 20))

# ------------------------------------------------------
# Login Trend Graph
# ------------------------------------------------------

story.append(
    Paragraph(
        "4. Suspicious Login Trend",
        styles["Heading2"]
    )
)

story.append(
    Image(
        "graphs/login_trend.png",
        width=6.5 * inch,
        height=3.8 * inch
    )
)

story.append(PageBreak())

# ======================================================
# ATTACK ANALYSIS
# ======================================================

story.append(
    Paragraph(
        "Attack Analysis",
        heading
    )
)

most_common_alert = alert_distribution.iloc[0]["alert_type"]
most_common_alert_count = alert_distribution.iloc[0]["count"]

most_affected_city = city_distribution.iloc[0]["city"]
city_alert_count = city_distribution.iloc[0]["count"]

highest_user = top_users.iloc[0]["user_id"]
highest_user_alerts = top_users.iloc[0]["total_alerts"]

analysis = f"""
The cybersecurity analytics engine processed
<b>{total_logins}</b> login events and generated
<b>{total_alerts}</b> security alerts.

The most frequently detected attack was
<b>{most_common_alert}</b>
with <b>{most_common_alert_count}</b> occurrences.

The city with the highest number of suspicious
login activities was
<b>{most_affected_city}</b>
with
<b>{city_alert_count}</b> alerts.

User
<b>{highest_user}</b>
generated the largest number of alerts
(<b>{highest_user_alerts}</b>),
indicating repeated suspicious activity.

The observed attack patterns suggest possible
credential theft,
identity spoofing,
account compromise,
or unauthorized login attempts.

Early detection of these activities enables
security teams to investigate incidents before
they escalate into successful attacks.
"""

story.append(
    Paragraph(
        analysis,
        normal
    )
)

story.append(Spacer(1, 25))

# ======================================================
# SECURITY RECOMMENDATIONS
# ======================================================

story.append(
    Paragraph(
        "Security Recommendations",
        heading
    )
)

recommendations = """
1. Enable Multi-Factor Authentication (MFA)<br/><br/>

2. Block impossible travel login attempts automatically.<br/><br/>

3. Verify newly detected devices before allowing access.<br/><br/>

4. Notify users immediately after suspicious login activity.<br/><br/>

5. Continuously monitor HIGH-risk accounts.<br/><br/>

6. Enable device fingerprint verification.<br/><br/>

7. Apply geo-location validation for login requests.<br/><br/>

8. Increase monitoring during unusual login hours.<br/><br/>

9. Maintain centralized audit logs for forensic investigations.
"""

story.append(
    Paragraph(
        recommendations,
        normal
    )
)

story.append(Spacer(1, 30))

# ======================================================
# CONCLUSION
# ======================================================

story.append(
    Paragraph(
        "Conclusion",
        heading
    )
)

conclusion = f"""
The Identity Theft & Spoofing Risk Analysis system
successfully analyzed
<b>{total_logins}</b>
login records and detected
<b>{total_alerts}</b>
potentially suspicious login activities.

By combining rule-based detection techniques,
risk scoring,
interactive dashboards,
and automated PDF reporting,
the system provides security analysts with a
simple yet effective method for identifying
identity theft and account compromise attempts.

This project demonstrates how Python-based
cybersecurity analytics can improve
organizational security monitoring,
reduce manual investigation effort,
and support faster incident response.
"""

story.append(
    Paragraph(
        conclusion,
        normal
    )
)

story.append(Spacer(1, 30))

# ======================================================
# FOOTER
# ======================================================

story.append(
    Paragraph(
        "<b>End of Cybersecurity Analytics Report</b>",
        styles["Heading2"]
    )
)

story.append(
    Paragraph(
        "Generated automatically using Python, Pandas, Matplotlib and ReportLab.",
        normal
    )
)

# ======================================================
# BUILD PDF
# ======================================================

pdf.build(story)

print("=" * 60)
print("Cybersecurity Report Generated Successfully")
print("Output File : cybersecurity_report.pdf")
print("=" * 60)
