import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dental No-Show Reduction", layout="wide")

# Load data
patients_df = pd.read_csv("data/patients.csv")
appointments_df = pd.read_csv("data/appointments.csv")

# Risk scoring logic
def risk_level(no_shows):
    if no_shows >= 2:
        return "High"
    elif no_shows == 1:
        return "Medium"
    else:
        return "Low"

patients_df["risk_level"] = patients_df["total_no_shows"].apply(risk_level)

# Merge patient and appointment data
merged_df = appointments_df.merge(patients_df, on="patient_id", how="left")

# Metrics
total_appointments = len(appointments_df)
no_show_count = len(appointments_df[appointments_df["status"] == "No Show"])
completed_count = len(appointments_df[appointments_df["status"] == "Completed"])
scheduled_count = len(appointments_df[appointments_df["status"] == "Scheduled"])
lost_revenue = appointments_df[appointments_df["status"] == "No Show"]["estimated_value"].sum()

# At-risk counts
high_risk_count = len(patients_df[patients_df["risk_level"] == "High"])
medium_risk_count = len(patients_df[patients_df["risk_level"] == "Medium"])

# Title
st.title("Dental No-Show Reduction Dashboard")
st.subheader("AI-Driven Patient Retention & Revenue Recovery System")

# Top metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Appointments", total_appointments)
col2.metric("No-Shows", no_show_count)
col3.metric("Completed", completed_count)
col4.metric("Estimated Lost Revenue", f"${lost_revenue:,}")

st.divider()

# At-risk patients
st.subheader("At-Risk Patients")
at_risk_df = patients_df[patients_df["risk_level"].isin(["High", "Medium"])][
    ["patient_id", "patient_name", "phone", "last_visit_date", "total_no_shows", "risk_level"]
]
st.dataframe(at_risk_df, use_container_width=True)

st.divider()

# Missed appointments
st.subheader("Missed Appointments")
missed_df = merged_df[merged_df["status"] == "No Show"][
    [
        "appointment_id",
        "patient_name",
        "appointment_date",
        "procedure_type",
        "estimated_value",
        "risk_level",
        "phone"
    ]
]
st.dataframe(missed_df, use_container_width=True)

st.divider()

# Full appointment list
st.subheader("All Appointments")
st.dataframe(merged_df, use_container_width=True)

st.divider()

# Business insight
st.subheader("Business Insight")
st.info(
    f"Current analysis shows {no_show_count} missed appointments, representing ${lost_revenue:,} in unrealized revenue. "
    f"High-risk patients account for the majority of repeat no-shows, indicating a need for targeted intervention such as automated reminders and proactive scheduling recovery."
)

st.divider()

# Revenue recovery simulator
st.subheader("Revenue Recovery Simulator")
recovery_rate = st.slider("Expected No-Show Reduction (%)", 0, 100, 30)
potential_recovery = lost_revenue * (recovery_rate / 100)

st.success(
    f"If no-shows are reduced by {recovery_rate}%, this practice could recover approximately ${potential_recovery:,.0f} per period."
)

st.divider()

# Executive summary
st.subheader("Executive Summary")

summary_text = f"""
This dental practice currently has {no_show_count} no-show appointment(s), resulting in approximately ${lost_revenue:,} in unrealized revenue.

There are {high_risk_count} high-risk patient(s) and {medium_risk_count} medium-risk patient(s) requiring targeted follow-up.

The highest-value opportunity is to automate reminders and schedule recovery outreach for repeat no-show patients.

If intervention reduces no-shows by {recovery_rate}%, the practice could recover about ${potential_recovery:,.0f} in revenue per period.
"""

st.write(summary_text)


