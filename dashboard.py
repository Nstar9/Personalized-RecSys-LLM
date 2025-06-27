import streamlit as st
import pandas as pd
import os
from collections import Counter

st.set_page_config(page_title="RecSys Analytics", layout="wide")
st.title("Personalized Recommendation System – Analytics Dashboard")

# --- 1. LOAD LOG DATA ---
log_file = "ab_log.csv"
if not os.path.exists(log_file):
    st.warning("No log file found. Make some /recommend API calls first!")
    st.stop()

df = pd.read_csv(log_file)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# --- 1.1 INTERACTIVE FILTERS ---
st.sidebar.header("Filter Data")

model_versions = df['model_version'].unique().tolist()
selected_model = st.sidebar.multiselect("Model Version", model_versions, default=model_versions)

user_ids = df['user_id'].unique().tolist()
selected_user = st.sidebar.multiselect("User ID", user_ids, default=user_ids)

filtered_df = df[
    df['model_version'].isin(selected_model) &
    df['user_id'].isin(selected_user)
]

# --- 2. BASIC STATS ---
st.subheader("A/B Test Results")
ab_counts = filtered_df['model_version'].value_counts()
st.write(ab_counts)
st.bar_chart(ab_counts)

# --- 3. SHOW SAMPLE RECOMMENDATIONS ---
st.subheader("Sample Recommendations")
for i, row in filtered_df.head(10).iterrows():
    st.write(f"User {row['user_id']} | Model: {row['model_version']} | Recommendations: {row['recommendations']}")

# --- 4. TOP RECOMMENDED MOVIES ---
st.subheader("Top Recommended Movies")
all_recs = []
for recs in filtered_df['recommendations']:
    all_recs.extend(str(recs).split(';'))
top_recs = Counter(all_recs).most_common(10)
top_df = pd.DataFrame(top_recs, columns=["movie_id", "count"])
top_df['movie_id'] = top_df['movie_id'].astype(int)

# Load movie titles only ONCE
movies = pd.read_csv(
    "data/u.item",
    sep="|",
    encoding="latin-1",
    names=["movie_id", "title"] + [f"junk{i}" for i in range(22)],
    usecols=[0, 1]
)
movies['movie_id'] = movies['movie_id'].astype(int)

# Merge ONCE and fill NaN titles
top_df = top_df.merge(movies, on="movie_id", how="left")
top_df['title'] = top_df['title'].fillna("Unknown Title")

# Show the top recommended movies table
st.table(top_df[['movie_id', 'title', 'count']])

# --- 5. OPTIONAL: SAMPLE LLM EXPLANATIONS (if you log them separately) ---
st.subheader("Sample LLM Explanations")
expl_file = "explanation_log.csv"
if os.path.exists(expl_file):
    expl_df = pd.read_csv(expl_file)
    st.write(expl_df.tail(10))  # Show last 10 explanations
else:
    st.info("No explanations logged yet. Call the /explain endpoint to generate some!")

# --- 6. API CALLS OVER TIME ---
st.subheader("API Calls Over Time")
df_hour = filtered_df.copy()
df_hour['hour'] = df_hour['timestamp'].dt.hour
calls_by_hour = df_hour.groupby('hour').size()
st.line_chart(calls_by_hour)

# --- 7. RAW DATA EXPANDER ---
with st.expander("Show raw A/B log data"):
    st.dataframe(filtered_df)
