import base64
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import io

API_BASE = "http://localhost:8000/api/v1"

st.header("Candidate Management")

# Initialize session state
if "show_candidate_dialog" not in st.session_state:
    st.session_state.show_candidate_dialog = False
if "candidate_files" not in st.session_state:
    st.session_state.candidate_files = []
if "analyzed_candidates" not in st.session_state:
    st.session_state.analyzed_candidates = []
if "selected_candidate_index" not in st.session_state:
    st.session_state.selected_candidate_index = None
if "show_pdf_viewer" not in st.session_state:
    st.session_state.show_pdf_viewer = False

def close_dialog():
    st.session_state.show_candidate_dialog = False
    st.session_state.candidate_files = []

def save_candidates():
    uploaded_files = st.session_state.candidate_files
    if not uploaded_files:
        st.warning("Please upload at least one resume.")
        return

    for uploaded_file in uploaded_files:
        # Reset file pointer to beginning
        uploaded_file.seek(0)
        file_bytes = uploaded_file.read()
        
        # Reset file pointer again for the request
        uploaded_file.seek(0)
        
        # Create a new BytesIO object to avoid file pointer issues
        file_like = io.BytesIO(file_bytes)
        
        files = {"file": (uploaded_file.name, file_like, uploaded_file.type)}

        # Step 1: Extract text from resume
        try:
            print(f"Uploading file: {uploaded_file.name}, type: {uploaded_file.type}, size: {len(file_bytes)} bytes")
            
            response = requests.post(f"{API_BASE}/resumes/upload", files=files, timeout=15)
            
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            extracted_text = result.get("content", "")
            
        except requests.exceptions.RequestException as e:
            st.error(f"Network error uploading {uploaded_file.name}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                st.error(f"Server response: {e.response.text}")
            continue
        except Exception as e:
            st.error(f"Failed to extract text from {uploaded_file.name}: {e}")
            continue

        # Step 2: Analyze resume
        try:
            response = requests.post(
                f"{API_BASE}/resumes/analyze",
                json={"content": extracted_text},
                timeout=15,
            )
            response.raise_for_status()
            analysis = response.json()
        except Exception as e:
            st.error(f"Failed to analyze {uploaded_file.name}: {e}")
            continue

        # Save result with timestamp, details, and raw file bytes for PDF viewing
        st.session_state.analyzed_candidates.append({
            "filename": uploaded_file.name,
            "name": analysis.get("name", "N/A"),
            "email": analysis.get("email", "N/A"),
            "phone": analysis.get("phone", "N/A"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "roles": analysis.get("roles", []),
            "experiences": analysis.get("experiences", []),
            "synopsis": analysis.get("synopsis", "N/A"),
            "skills": analysis.get("skills", []),
            "file_bytes": file_bytes if uploaded_file.type == "application/pdf" else None,
        })

    close_dialog()

st.button("Upload Candidate(s)", on_click=lambda: st.session_state.update(show_candidate_dialog=True))  # type: ignore

if st.session_state.show_candidate_dialog:
    with st.container(border=True):
        st.subheader("Upload Resume Files")
        st.file_uploader("Upload Resume Files (.pdf, .docx)", type=["pdf", "docx"], accept_multiple_files=True, key="candidate_files")

        col1, col2 = st.columns(2)
        col1.button("Save", on_click=save_candidates)
        col2.button("Close", on_click=close_dialog)

def delete_candidate(index):
    if st.session_state.selected_candidate_index == index:
        st.session_state.selected_candidate_index = None
    st.session_state.analyzed_candidates.pop(index)

if st.session_state.analyzed_candidates:
    st.markdown("### Analyzed Candidates")

    df = pd.DataFrame(st.session_state.analyzed_candidates)

    for i, row in df.iterrows():
        st.markdown("---")
        cols = st.columns([2, 2, 3, 2, 2, 1, 1])
        cols[0].write(row["filename"])
        cols[1].write(row.get("name", "N/A"))
        cols[2].write(row.get("email", "N/A"))
        cols[3].write(row.get("phone", "N/A"))
        cols[4].write(row.get("timestamp", "N/A"))
        if cols[5].button("Details", key=f"details_{i}"):
            st.session_state.selected_candidate_index = i
            st.session_state.show_pdf_viewer = False  # reset pdf viewer
        if cols[6].button("Delete", key=f"delete_{i}"):
            delete_candidate(i)
            st.rerun()
else:
    st.info("No candidates analyzed yet.")

# Sidebar detail panel
if st.session_state.selected_candidate_index is not None:
    candidate = st.session_state.analyzed_candidates[st.session_state.selected_candidate_index]  # type: ignore
    with st.sidebar:
        st.header("Candidate Details")
        st.markdown(f"**Filename:** {candidate['filename']}")
        st.markdown(f"**Name:** {candidate.get('name', 'N/A')}")
        st.markdown(f"**Email:** {candidate.get('email', 'N/A')}")
        st.markdown(f"**Phone:** {candidate.get('phone', 'N/A')}")
        st.markdown(f"**Uploaded At:** {candidate.get('timestamp', 'N/A')}")
        st.markdown(f"**Synopsis:** {candidate.get('synopsis', 'N/A')}")

        st.markdown("**Roles:**")
        if candidate.get("roles"):
            for role in candidate["roles"]:
                st.markdown(f"- {role}")
        else:
            st.write("N/A")

        st.markdown("**Experiences:**")
        if candidate.get("experiences"):
            for exp in candidate["experiences"]:
                st.markdown(f"- {exp}")
        else:
            st.write("N/A")

        st.markdown("**Skills:**")
        if candidate.get("skills"):
            for skill in candidate["skills"]:
                st.markdown(f"- {skill}")
        else:
            st.write("N/A")

        if candidate.get("file_bytes"):
            if st.button("View PDF"):
                st.session_state.show_pdf_viewer = True

        if st.button("Close Details"):
            st.session_state.selected_candidate_index = None
            st.session_state.show_pdf_viewer = False

# PDF viewer below sidebar
if st.session_state.show_pdf_viewer and st.session_state.selected_candidate_index is not None:
    candidate = st.session_state.analyzed_candidates[st.session_state.selected_candidate_index]  # type: ignore
    pdf_bytes = candidate.get("file_bytes")
    if pdf_bytes:
        b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
        st.markdown("### PDF Viewer")
        st.markdown(pdf_display, unsafe_allow_html=True)