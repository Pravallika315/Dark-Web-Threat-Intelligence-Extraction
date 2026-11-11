
import streamlit as st
import pandas as pd
import sqlite3
import json
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Dark Web Threat Intelligence",
    page_icon="🛡️",
    layout="wide"
)

# Load database
@st.cache_data
def load_data():

    conn = sqlite3.connect("threat_intelligence.db")

    threats = pd.read_sql(
        "SELECT * FROM threat_analysis", conn
    )

    topics = pd.read_sql(
        "SELECT * FROM topic_analysis", conn
    )

    predictions = pd.read_sql(
        "SELECT * FROM category_predictions", conn
    )

    conn.close()

    return threats, topics, predictions


try:
    threats, topics, predictions = load_data()

except Exception as e:
    st.error(f"Database loading failed: {e}")
    st.stop()


# Convert JSON threat lists into categories
def parse_threats(value):

    try:
        result = json.loads(value)

        if isinstance(result, list):
            return result

    except (ValueError, TypeError):
        pass

    return ["Unclassified"]


threats["threat_list"] = threats["threats"].apply(
    parse_threats
)

# Sidebar
st.sidebar.title("🛡️ Threat Intelligence")
st.sidebar.markdown("Dark Web Analysis System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Threat Analysis",
        "IOC Extraction",
        "Topic Analysis",
        "ML Results"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "NLP-based analysis of forum text data."
)


# Dashboard page
if page == "Dashboard":

    st.title("🛡️ Dark Web Threat Intelligence Dashboard")

    st.caption(
        "NLP-based extraction and analysis of unstructured text"
    )

    total = len(threats)

    detected = sum(
        1 for items in threats["threat_list"]
        if "Unclassified" not in items
    )

    high = (threats["risk"] == "High").sum()
    medium = (threats["risk"] == "Medium").sum()
    low = (threats["risk"] == "Low").sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Records", total)
    col2.metric("Threat Flagged Records", detected)
    col3.metric("High Risk", int(high))
    col4.metric("Medium Risk", int(medium))

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        st.subheader("Threat Category Distribution")

        category_counts = {}

        for items in threats["threat_list"]:

            for item in items:

                if item != "Unclassified":

                    category_counts[item] = (
                        category_counts.get(item, 0) + 1
                    )

        if category_counts:

            chart_data = pd.DataFrame({
                "Threat": list(category_counts.keys()),
                "Count": list(category_counts.values())
            })

            fig = px.bar(
                chart_data,
                x="Threat",
                y="Count",
                title="Detected Threat Categories"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No threat categories detected.")

    with right:

        st.subheader("Risk Distribution")

        risk_data = pd.DataFrame({
            "Risk": ["High", "Medium", "Low"],
            "Count": [int(high), int(medium), int(low)]
        })

        fig = px.pie(
            risk_data,
            names="Risk",
            values="Count",
            hole=0.4
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("Recent Analyzed Records")

    display_cols = [
        col for col in
        ["title", "category", "threats", "risk"]
        if col in threats.columns
    ]

    st.dataframe(
        threats[display_cols].head(10),
        use_container_width=True
    )


# Threat analysis page
elif page == "Threat Analysis":

    st.title("Threat Analysis")

    selected = st.selectbox(
        "Select Threat Category",
        [
            "All",
            "Malware",
            "Ransomware",
            "Phishing",
            "Credential Theft",
            "Data Breach",
            "DDoS",
            "Vulnerability",
            "Unclassified"
        ]
    )

    if selected == "All":

        filtered = threats.copy()

    else:

        filtered = threats[
            threats["threat_list"].apply(
                lambda x: selected in x
            )
        ]

    st.write("Matching Records:", len(filtered))

    st.dataframe(
        filtered[
            [
                col for col in
                ["id", "title", "threats", "risk", "full_text"]
                if col in filtered.columns
            ]
        ],
        use_container_width=True
    )


# IOC extraction page
elif page == "IOC Extraction":

    st.title("Indicator of Compromise Extraction")

    ioc_type = st.selectbox(
        "Select IOC Type",
        [
            "All",
            "IP Address",
            "Email",
            "Domain",
            "Hash",
            "CVE"
        ]
    )

    extracted = []

    for _, row in threats.iterrows():

        try:
            iocs = json.loads(row["iocs"])

            for kind, values in iocs.items():

                if ioc_type == "All" or kind == ioc_type:

                    for value in values:

                        extracted.append({
                            "Record ID": row["id"],
                            "IOC Type": kind,
                            "IOC Value": value
                        })

        except (ValueError, TypeError):
            continue

    ioc_df = pd.DataFrame(extracted)

    st.metric("Total Extracted IOCs", len(ioc_df))

    if not ioc_df.empty:

        st.dataframe(
            ioc_df,
            use_container_width=True
        )

        st.download_button(
            "Download IOC Report",
            ioc_df.to_csv(index=False),
            "ioc_report.csv",
            "text/csv"
        )

    else:

        st.info("No matching IOCs found.")


# Topic analysis page
elif page == "Topic Analysis":

    st.title("LDA Topic Modelling Analysis")

    if "topic_id" in topics.columns:

        topic_counts = (
            topics["topic_id"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        topic_counts.columns = ["Topic", "Records"]

        fig = px.bar(
            topic_counts,
            x="Topic",
            y="Records",
            title="Document Distribution Across Topics"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Topic Records")

        selected_topic = st.selectbox(
            "Select Topic",
            sorted(topics["topic_id"].unique())
        )

        topic_data = topics[
            topics["topic_id"] == selected_topic
        ]

        st.dataframe(
            topic_data[
                [
                    col for col in
                    ["title", "category", "topic_probability"]
                    if col in topic_data.columns
                ]
            ],
            use_container_width=True
        )

    else:

        st.warning("Topic information unavailable.")


# Machine learning results page
elif page == "ML Results":

    st.title("Machine Learning Classification Results")

    st.info(
        "These results represent forum-category prediction, "
        "not verified cybersecurity threat classification."
    )

    if not predictions.empty:

        accuracy = (
            predictions["actual_category"]
            == predictions["predicted_category"]
        ).mean() * 100

        st.metric(
            "Test Accuracy",
            f"{accuracy:.2f}%"
        )

        st.subheader("Actual vs Predicted Categories")

        st.dataframe(
            predictions,
            use_container_width=True
        )

        comparison = pd.DataFrame({
            "Result": ["Correct", "Incorrect"],
            "Count": [
                int((
                    predictions["actual_category"]
                    == predictions["predicted_category"]
                ).sum()),
                int((
                    predictions["actual_category"]
                    != predictions["predicted_category"]
                ).sum())
            ]
        })

        fig = px.pie(
            comparison,
            names="Result",
            values="Count",
            title="Prediction Performance"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("No ML predictions available.")


# Footer
st.sidebar.markdown("---")
st.sidebar.caption(
    "Dark Web Threat Intelligence Extraction | NLP Project"
)
