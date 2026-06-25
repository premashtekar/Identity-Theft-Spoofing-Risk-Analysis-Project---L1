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

# ===============================
# LOAD DATA
# ===============================

alerts = pd.read_csv("risk_alerts.csv")

risk_summary = pd.read_csv("risk_summary.csv")

master_data = pd.read_csv("master_user_data.csv")

alert_distribution = pd.read_csv("alert_distribution.csv")

city_distribution = pd.read_csv("city_distribution.csv")

top_users = pd.read_csv("top_suspicious_users.csv")

# ===============================
# PROJECT STATISTICS
# ===============================

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


# ===============================
# CREATE PDF
# ===============================

pdf = SimpleDocTemplate(
    "cybersecurity_report.pdf"
)

styles = getSampleStyleSheet()

story = []

title_style = styles["Title"]

title_style.alignment = TA_CENTER

heading = styles["Heading1"]

normal = styles["BodyText"]

story.append(
    Paragraph(
        "Identity Theft & Spoofing Risk Analysis",
        title_style
    )
)

story.append(Spacer(1,25))

story.append(
    Paragraph(
        "Cybersecurity Analytics Report",
        styles["Heading2"]
    )
)

story.append(Spacer(1,40))

story.append(
    Paragraph(
        "<b>Prepared By:</b> Yash",
        normal
    )
)

story.append(Spacer(1,10))

story.append(
    Paragraph(
        "<b>Technology Used:</b>",
        heading
    )
)

story.append(
    Paragraph(
        """
        • Python<br/>
        • Pandas<br/>
        • NumPy<br/>
        • Matplotlib<br/>
        • Streamlit<br/>
        """,
        normal
    )
)

story.append(Spacer(1,30))

story.append(
    Paragraph(
        "Generated Cybersecurity Report",
        styles["Heading2"]
    )
)

story.append(PageBreak())

story.append(
    Paragraph(
        "Project Overview",
        heading
    )
)

overview = """

The Identity Theft & Spoofing Risk Analysis system
detects suspicious login behavior using rule-based
cybersecurity analytics.

The system identifies:

• Impossible Travel

• Device Spoofing

• Odd Hour Login Activity

It assigns LOW, MEDIUM and HIGH risk levels
to every user and automatically generates
alerts for further investigation.

"""

story.append(
    Paragraph(
        overview,
        normal
    )
)

story.append(Spacer(1,20))

story.append(
    Paragraph(
        "Executive Summary",
        heading
    )
)

summary = f"""

The system analyzed
<b>{total_logins}</b> login events belonging to
<b>{total_users}</b> unique users.

A total of
<b>{total_alerts}</b> suspicious activities
were detected.

<b>{high_users}</b> users were classified as HIGH risk,
<b>{medium_users}</b> as MEDIUM risk,
and
<b>{low_users}</b> as LOW risk.

Overall,
<b>{suspicious_users}</b>
users were marked suspicious.

"""

story.append(
    Paragraph(
        summary,
        normal
    )
)

story.append(Spacer(1,20))

# ===============================
# PROJECT STATISTICS
# ===============================

story.append(Paragraph("Project Statistics", heading))
story.append(Spacer(1,10))

stats_data = [

    ["Metric","Value"],

    ["Total Login Records", total_logins],

    ["Unique Users", total_users],

    ["Total Alerts", total_alerts],

    ["Suspicious Users", suspicious_users],

    ["High Risk Users", high_users],

    ["Medium Risk Users", medium_users],

    ["Low Risk Users", low_users]

]

stats_table = Table(stats_data, colWidths=[250,150])

stats_table.setStyle(TableStyle([

    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#003366")),
    ("TEXTCOLOR",(0,0),(-1,0),colors.white),

    ("GRID",(0,0),(-1,-1),1,colors.black),

    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

    ("BACKGROUND",(0,1),(-1,-1),colors.beige),

    ("ALIGN",(0,0),(-1,-1),"CENTER"),

    ("BOTTOMPADDING",(0,0),(-1,0),10)

]))

story.append(stats_table)

story.append(Spacer(1,25))

# ===============================
# RISK DISTRIBUTION
# ===============================

story.append(Paragraph("Risk Distribution", heading))
story.append(Spacer(1,10))

risk_table = [["Risk Level","Number of Users"]]

risk_counts = risk_summary["overall_risk"].value_counts()

for risk,count in risk_counts.items():

    risk_table.append([risk,count])

risk_pdf = Table(risk_table,colWidths=[220,180])

risk_pdf.setStyle(TableStyle([

    ("GRID",(0,0),(-1,-1),1,colors.black),

    ("BACKGROUND",(0,0),(-1,0),colors.darkgreen),

    ("TEXTCOLOR",(0,0),(-1,0),colors.white),

    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

    ("ALIGN",(0,0),(-1,-1),"CENTER"),

    ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke)

]))

story.append(risk_pdf)

story.append(Spacer(1,25))

# ===============================
# ALERT DISTRIBUTION
# ===============================

story.append(Paragraph("Alert Distribution", heading))
story.append(Spacer(1,10))

alert_table = [["Alert Type","Count"]]

for _,row in alert_distribution.iterrows():

    alert_table.append([

        row["alert_type"],

        row["count"]

    ])

alert_pdf = Table(alert_table,colWidths=[250,150])

alert_pdf.setStyle(TableStyle([

    ("GRID",(0,0),(-1,-1),1,colors.black),

    ("BACKGROUND",(0,0),(-1,0),colors.darkred),

    ("TEXTCOLOR",(0,0),(-1,0),colors.white),

    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

    ("ALIGN",(0,0),(-1,-1),"CENTER"),

    ("BACKGROUND",(0,1),(-1,-1),colors.beige)

]))

story.append(alert_pdf)

story.append(Spacer(1,25))

# ===============================
# TOP SUSPICIOUS USERS
# ===============================

story.append(Paragraph("Top Suspicious Users", heading))
story.append(Spacer(1,10))

top_table = [

    ["User ID","Total Alerts","Highest Score"]

]

for _,row in top_users.iterrows():

    top_table.append([

        row["user_id"],

        row["total_alerts"],

        row["highest_score"]

    ])

top_pdf = Table(top_table,colWidths=[140,150,150])

top_pdf.setStyle(TableStyle([

    ("GRID",(0,0),(-1,-1),1,colors.black),

    ("BACKGROUND",(0,0),(-1,0),colors.orange),

    ("TEXTCOLOR",(0,0),(-1,0),colors.white),

    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

    ("ALIGN",(0,0),(-1,-1),"CENTER"),

    ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke)

]))

story.append(top_pdf)

story.append(Spacer(1,25))
# ===============================
# CITY DISTRIBUTION
# ===============================

story.append(Paragraph("City Distribution", heading))
story.append(Spacer(1,10))

city_table = [

    ["City","Suspicious Logins"]

]

for _,row in city_distribution.iterrows():

    city_table.append([

        row["city"],

        row["count"]

    ])

city_pdf = Table(city_table,colWidths=[220,180])

city_pdf.setStyle(TableStyle([

    ("GRID",(0,0),(-1,-1),1,colors.black),

    ("BACKGROUND",(0,0),(-1,0),colors.purple),

    ("TEXTCOLOR",(0,0),(-1,0),colors.white),

    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

    ("ALIGN",(0,0),(-1,-1),"CENTER"),

    ("BACKGROUND",(0,1),(-1,-1),colors.lavender)

]))

story.append(city_pdf)

story.append(PageBreak())

# ===============================
# VISUAL ANALYSIS
# ===============================

story.append(Paragraph("Visual Analysis", heading))
story.append(Spacer(1,10))

story.append(Paragraph("Risk Distribution", styles["Heading2"]))

story.append(
    Image(
        "graphs/risk_distribution.png",
        width=6*inch,
        height=3.5*inch
    )
)

story.append(Spacer(1,20))

story.append(Paragraph("Alert Type Distribution", styles["Heading2"]))

story.append(
    Image(
        "graphs/alert_distribution.png",
        width=6*inch,
        height=4*inch
    )
)

story.append(Spacer(1,20))

story.append(Paragraph("City Distribution", styles["Heading2"]))

story.append(
    Image(
        "graphs/city_distribution.png",
        width=6*inch,
        height=3.5*inch
    )
)

story.append(Spacer(1,20))

story.append(Paragraph("Suspicious Login Trend", styles["Heading2"]))

story.append(
    Image(
        "graphs/login_trend.png",
        width=6*inch,
        height=3.5*inch
    )
)

story.append(PageBreak())

# ===============================
# ATTACK ANALYSIS
# ===============================

story.append(
    Paragraph(
        "Attack Analysis",
        heading
    )
)

analysis = f"""

The cybersecurity monitoring system analyzed
<b>{total_logins}</b> login events and detected
<b>{total_alerts}</b> suspicious activities.

The analysis identified
<b>{high_users}</b> HIGH risk users requiring immediate investigation.

The majority of alerts originated from
<b>{alert_distribution.iloc[0]['alert_type']}</b>,
making it the most common security incident.

The city with the highest suspicious activity was
<b>{city_distribution.iloc[0]['city']}</b>.

Repeated alerts for the same users indicate
possible credential compromise,
identity spoofing,
or unauthorized access attempts.

"""

story.append(
    Paragraph(
        analysis,
        normal
    )
)

story.append(Spacer(1,20))

# ===============================
# SECURITY RECOMMENDATIONS
# ===============================

story.append(
    Paragraph(
        "Security Recommendations",
        heading
    )
)

recommendations = """

• Enable Multi-Factor Authentication (MFA)

<br/><br/>

• Verify all new login devices before granting access.

<br/><br/>

• Block impossible travel login attempts.

<br/><br/>

• Notify users immediately when a new device logs in.

<br/><br/>

• Continuously monitor high-risk users.

<br/><br/>

• Implement geo-location verification.

<br/><br/>

• Increase monitoring during unusual login hours.

<br/><br/>

• Maintain detailed login audit logs.

"""

story.append(
    Paragraph(
        recommendations,
        normal
    )
)

story.append(Spacer(1,25))

# ===============================
# CONCLUSION
# ===============================

story.append(
    Paragraph(
        "Conclusion",
        heading
    )
)

conclusion = """

The Identity Theft & Spoofing Risk Analysis System
successfully detects suspicious login activities
using rule-based cybersecurity analytics.

The generated dashboard,
automated reports,
risk scoring,
and visual analytics
provide security analysts with
actionable insights for identifying
potential identity theft attempts.

The system demonstrates how
Python-based data analytics
can assist organizations
in strengthening account security
and improving threat detection.

"""

story.append(
    Paragraph(
        conclusion,
        normal
    )
)



story.append(Spacer(1,30))
# ===============================
# GENERATE PDF
# ===============================

pdf.build(story)

print("="*50)
print("Cybersecurity Report Generated Successfully")
print("Output File : cybersecurity_report.pdf")
print("="*50)