import streamlit as st
import requests
import pandas as pd

API_BASE = "http://localhost:8000/api/v1"

st.set_page_config(page_title="Job Management", layout="wide")

st.header("Job Management")

if "show_job_dialog" not in st.session_state:
    st.session_state.show_job_dialog = False
if "job_title" not in st.session_state:
    st.session_state.job_title = ""
if "job_description" not in st.session_state:
    st.session_state.job_description = ""
if "registered_jobs" not in st.session_state:
    st.session_state.registered_jobs = []

def close_dialog():
    st.session_state.show_job_dialog = False
    st.session_state.job_title = ""
    st.session_state.job_description = ""

def save_job():
    if not st.session_state.job_description.strip():
        st.warning("Please enter a job description.")
        return

    try:
        response = requests.post(
            f"{API_BASE}/jobs/analyze",
            json={"content": st.session_state.job_description},
            timeout=10,
        )
        response.raise_for_status()
        result = response.json()
        synopsis = result.get("synopsis", "N/A")
    except Exception as e:
        st.error(f"Failed to analyze job: {e}")
        return

    st.session_state.registered_jobs.append({
        "title": st.session_state.job_title,
        "synopsis": synopsis,
        "description": st.session_state.job_description,
    })
    close_dialog()

st.button("Upload Job", on_click=lambda: st.session_state.update(show_job_dialog=True))  # type: ignore

if st.session_state.show_job_dialog:
    with st.container(border=True):
        st.subheader("Upload New Job")
        st.text_input("Job Title", key="job_title")
        st.text_area("Job Description", height=250, key="job_description")

        col1, col2 = st.columns(2)
        col1.button("Save", on_click=save_job)
        col2.button("Close", on_click=close_dialog)

if st.session_state.registered_jobs:
    st.markdown("### Registered Jobs")
    df = pd.DataFrame(st.session_state.registered_jobs)
    st.dataframe(df[["title", "synopsis"]], use_container_width=True)
else:
    st.info("No jobs registered yet.")
