# import base64
# import streamlit as st
# import requests
# import pandas as pd
# from datetime import datetime
# import io

# API_BASE = "http://localhost:8000/api/v1"

# st.header("Candidate Management")

# # Initialize session state
# if "show_candidate_dialog" not in st.session_state:
#     st.session_state.show_candidate_dialog = False
# if "candidate_files" not in st.session_state:
#     st.session_state.candidate_files = []
# if "analyzed_candidates" not in st.session_state:
#     st.session_state.analyzed_candidates = []
# if "selected_candidate_index" not in st.session_state:
#     st.session_state.selected_candidate_index = None
# if "show_pdf_viewer" not in st.session_state:
#     st.session_state.show_pdf_viewer = False

# def close_dialog():
#     st.session_state.show_candidate_dialog = False
#     st.session_state.candidate_files = []

# def save_candidates():
#     uploaded_files = st.session_state.candidate_files
#     if not uploaded_files:
#         st.warning("Please upload at least one resume.")
#         return

#     for uploaded_file in uploaded_files:
#         # Reset file pointer to beginning
#         uploaded_file.seek(0)
#         file_bytes = uploaded_file.read()
        
#         # Reset file pointer again for the request
#         uploaded_file.seek(0)
        
#         # Create a new BytesIO object to avoid file pointer issues
#         file_like = io.BytesIO(file_bytes)
        
#         files = {"file": (uploaded_file.name, file_like, uploaded_file.type)}

#         # Step 1: Extract text from resume
#         try:
#             print(f"Uploading file: {uploaded_file.name}, type: {uploaded_file.type}, size: {len(file_bytes)} bytes")
            
#             response = requests.post(f"{API_BASE}/resumes/upload", files=files, timeout=15)
            
#             print(f"Response status: {response.status_code}")
#             print(f"Response text: {response.text}")
            
#             response.raise_for_status()
#             result = response.json()
#             extracted_text = result.get("content", "")
            
#         except requests.exceptions.RequestException as e:
#             st.error(f"Network error uploading {uploaded_file.name}: {e}")
#             if hasattr(e, 'response') and e.response is not None:
#                 st.error(f"Server response: {e.response.text}")
#             continue
#         except Exception as e:
#             st.error(f"Failed to extract text from {uploaded_file.name}: {e}")
#             continue

#         # Step 2: Analyze resume
#         try:
#             response = requests.post(
#                 f"{API_BASE}/resumes/analyze",
#                 json={"content": extracted_text},
#                 timeout=15,
#             )
#             response.raise_for_status()
#             analysis = response.json()
#         except Exception as e:
#             st.error(f"Failed to analyze {uploaded_file.name}: {e}")
#             continue

#         # Save result with timestamp, details, and raw file bytes for PDF viewing
#         st.session_state.analyzed_candidates.append({
#             "filename": uploaded_file.name,
#             "candidate_name": analysis.get("candidate_name", "N/A"),
#             "email": analysis.get("email", "N/A"),
#             "phone_number": analysis.get("phone_number", "N/A"),
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "roles": analysis.get("roles", []),
#             "education": analysis.get("education", []),
#             "comment": analysis.get("comment", "N/A"),
#             "responsibilities": analysis.get("responsibilities", []),
#             "technical_skill": analysis.get("technical_skill", []),
#             "soft_skill": analysis.get("soft_skill", []),
#             "certificate": analysis.get("certificate", []),
#             "job_recommended": analysis.get("job_recommended", []),
#             "years_of_experience": analysis.get("years_of_experience", "N/A"),
#             "websites": analysis.get("websites", []),
#             "file_bytes": file_bytes if uploaded_file.type == "application/pdf" else None,
#         })

#     close_dialog()

# st.button("Upload Candidate(s)", on_click=lambda: st.session_state.update(show_candidate_dialog=True))  # type: ignore

# if st.session_state.show_candidate_dialog:
#     with st.container(border=True):
#         st.subheader("Upload Resume Files")
#         st.file_uploader("Upload Resume Files (.pdf, .docx)", type=["pdf", "docx"], accept_multiple_files=True, key="candidate_files")

#         col1, col2 = st.columns(2)
#         col1.button("Save", on_click=save_candidates)
#         col2.button("Close", on_click=close_dialog)

# def delete_candidate(index):
#     if st.session_state.selected_candidate_index == index:
#         st.session_state.selected_candidate_index = None
#     st.session_state.analyzed_candidates.pop(index)

# if st.session_state.analyzed_candidates:
#     st.markdown("### Analyzed Candidates")

#     df = pd.DataFrame(st.session_state.analyzed_candidates)

#     for i, row in df.iterrows():
#         st.markdown("---")
#         cols = st.columns([2, 2, 3, 2, 2, 1, 1])
#         cols[0].write(row["filename"])
#         cols[1].write(row.get("candidate_name", "N/A"))
#         cols[2].write(row.get("email", "N/A"))
#         cols[3].write(row.get("phone_number", "N/A"))
#         cols[4].write(row.get("timestamp", "N/A"))
#         if cols[5].button("Details", key=f"details_{i}"):
#             st.session_state.selected_candidate_index = i
#             st.session_state.show_pdf_viewer = False  # reset pdf viewer
#         if cols[6].button("Delete", key=f"delete_{i}"):
#             delete_candidate(i)
#             st.rerun()
# else:
#     st.info("No candidates analyzed yet.")

# # Sidebar detail panel
# if st.session_state.selected_candidate_index is not None:
#     candidate = st.session_state.analyzed_candidates[st.session_state.selected_candidate_index]  # type: ignore
#     with st.sidebar:
#         st.write("DEBUG - Candidate keys:", list(candidate.keys()))
#         st.write("DEBUG - Candidate data:", candidate)

#         st.markdown(f"# {candidate.get('candidate_name', 'N/A')}")
#         st.markdown(f"**Email:** {candidate.get('email', 'N/A')}")
#         st.markdown(f"**Phone:** {candidate.get('phone_number', 'N/A')}")
        
#         # Display websites if available
#         if candidate.get('websites'):
#             st.markdown("- " + candidate['websites'][0])
        
#         st.markdown(f"## Summary")
#         st.markdown(f"{candidate.get('comment', 'N/A')}")
        
#         st.markdown("## Experience:")
#         st.markdown(f"**Years of Experience:** :grey-badge[{candidate.get('years_of_experience', 'N/A')}]")
        
#         # Fixed: Actually display the roles with proper st.markdown calls
#         if candidate.get("roles"):
#             for role in candidate["roles"]:
#                 st.markdown(f"### {role.get('title', 'N/A')}")
#                 st.markdown(f"**Company:** {role.get('company', 'N/A')}")
#                 st.markdown(f"**Summary:** {role.get('summary', 'N/A')}")
#                 st.markdown("---")  # Add separator between roles
#         else:
#             st.error("No experience found.")
        
#         st.markdown("## Education:")
#         if candidate.get("education"):
#             for edu in candidate["education"]:
#                 st.markdown(f"**{edu.get('level', 'N/A')} in {edu.get('field', 'N/A')}**")
#                 st.markdown(f"Institution: {edu.get('institution', 'N/A')}")
#                 st.markdown(f"Graduation Year: {edu.get('year', 'N/A')}")
#                 if edu.get('gpa'):
#                     st.markdown(f"GPA: {edu.get('gpa')}")
#                 st.markdown("---")
#         else:
#             st.error("No education found.")
        
#         st.markdown("## Responsibilities:")
#         if candidate.get("responsibilities"):
#             for resp in candidate["responsibilities"]:
#                 st.markdown(f"- {resp}")
#         else:
#             st.error("No tasks/responsibilities found.")
        
#         st.markdown("## Technical Skills:")
#         if candidate.get("technical_skill"):
#             # Display skills in a more compact format
#             skills_text = " ".join([f":blue-badge[{skill}]" for skill in candidate["technical_skill"]])
#             st.markdown(skills_text)
#         else:
#             st.error("No technical skills found.")
        
#         st.markdown("## Soft Skills:")
#         if candidate.get("soft_skill"):
#             skills_text = " ".join([f":green-badge[{skill}]" for skill in candidate["soft_skill"]])
#             st.markdown(skills_text)
#         else:
#             st.error("No soft skills found.")
        
#         st.markdown("## Certificates:")
#         if candidate.get("certificate") and len(candidate["certificate"]) > 0:
#             for cert in candidate["certificate"]:
#                 st.markdown(f"- {cert}")
#         else:
#             st.info("No certificates found.")
        
#         st.markdown("## Recommended Positions:")
#         if candidate.get('job_recommended'):
#             positions_text = " ".join([f":grey-badge[{job}]" for job in candidate['job_recommended']])
#             st.markdown(positions_text)
#         else:
#             st.error("No recommended positions found.")
        
#         # PDF viewer button
#         if candidate.get("file_bytes"):
#             if st.button("View PDF"):
#                 st.session_state.show_pdf_viewer = True
        
#         if st.button("Close Details"):
#             st.session_state.selected_candidate_index = None
#             st.session_state.show_pdf_viewer = False

# # PDF viewer below sidebar
# if st.session_state.show_pdf_viewer and st.session_state.selected_candidate_index is not None:
#     candidate = st.session_state.analyzed_candidates[st.session_state.selected_candidate_index]  # type: ignore
#     pdf_bytes = candidate.get("file_bytes")
#     if pdf_bytes:
#         b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
#         pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
#         st.markdown("### PDF Viewer")
#         st.markdown(pdf_display, unsafe_allow_html=True)

# import base64
# import streamlit as st
# import requests
# import pandas as pd
# from datetime import datetime
# import io

# API_BASE = "http://localhost:8000/api/v1"

# st.header("Candidate Management")

# # Initialize session state
# if "show_candidate_dialog" not in st.session_state:
#     st.session_state.show_candidate_dialog = False
# if "candidate_files" not in st.session_state:
#     st.session_state.candidate_files = []
# if "analyzed_candidates" not in st.session_state:
#     st.session_state.analyzed_candidates = []
# if "selected_candidate_index" not in st.session_state:
#     st.session_state.selected_candidate_index = None
# if "show_candidate_details" not in st.session_state:
#     st.session_state.show_candidate_details = False
# if "show_pdf_viewer" not in st.session_state:
#     st.session_state.show_pdf_viewer = False

# def close_dialog():
#     st.session_state.show_candidate_dialog = False
#     st.session_state.candidate_files = []

# def close_details_dialog():
#     st.session_state.show_candidate_details = False
#     st.session_state.selected_candidate_index = None
#     st.session_state.show_pdf_viewer = False

# def show_candidate_details(index):
#     st.session_state.selected_candidate_index = index
#     st.session_state.show_candidate_details = True
#     st.session_state.show_pdf_viewer = False

# def save_candidates():
#     uploaded_files = st.session_state.candidate_files
#     if not uploaded_files:
#         st.warning("Please upload at least one resume.")
#         return

#     for uploaded_file in uploaded_files:
#         # Reset file pointer to beginning
#         uploaded_file.seek(0)
#         file_bytes = uploaded_file.read()
        
#         # Reset file pointer again for the request
#         uploaded_file.seek(0)
        
#         # Create a new BytesIO object to avoid file pointer issues
#         file_like = io.BytesIO(file_bytes)
        
#         files = {"file": (uploaded_file.name, file_like, uploaded_file.type)}

#         # Step 1: Extract text from resume
#         try:
#             print(f"Uploading file: {uploaded_file.name}, type: {uploaded_file.type}, size: {len(file_bytes)} bytes")
            
#             response = requests.post(f"{API_BASE}/resumes/upload", files=files, timeout=15)
            
#             print(f"Response status: {response.status_code}")
#             print(f"Response text: {response.text}")
            
#             response.raise_for_status()
#             result = response.json()
#             extracted_text = result.get("content", "")
            
#         except requests.exceptions.RequestException as e:
#             st.error(f"Network error uploading {uploaded_file.name}: {e}")
#             if hasattr(e, 'response') and e.response is not None:
#                 st.error(f"Server response: {e.response.text}")
#             continue
#         except Exception as e:
#             st.error(f"Failed to extract text from {uploaded_file.name}: {e}")
#             continue

#         # Step 2: Analyze resume
#         try:
#             response = requests.post(
#                 f"{API_BASE}/resumes/analyze",
#                 json={"content": extracted_text},
#                 timeout=15,
#             )
#             response.raise_for_status()
#             analysis = response.json()
#         except Exception as e:
#             st.error(f"Failed to analyze {uploaded_file.name}: {e}")
#             continue

#         # Save result with timestamp, details, and raw file bytes for PDF viewing
#         st.session_state.analyzed_candidates.append({
#             "filename": uploaded_file.name,
#             "candidate_name": analysis.get("candidate_name", "N/A"),
#             "email": analysis.get("email", "N/A"),
#             "phone_number": analysis.get("phone_number", "N/A"),
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "roles": analysis.get("roles", []),
#             "education": analysis.get("education", []),
#             "comment": analysis.get("comment", "N/A"),
#             "responsibilities": analysis.get("responsibilities", []),
#             "technical_skill": analysis.get("technical_skill", []),
#             "soft_skill": analysis.get("soft_skill", []),
#             "certificate": analysis.get("certificate", []),
#             "job_recommended": analysis.get("job_recommended", []),
#             "years_of_experience": analysis.get("years_of_experience", "N/A"),
#             "websites": analysis.get("websites", []),
#             "file_bytes": file_bytes if uploaded_file.type == "application/pdf" else None,
#         })

#     close_dialog()

# st.button("Upload Candidate(s)", on_click=lambda: st.session_state.update(show_candidate_dialog=True))

# # Upload dialog
# if st.session_state.show_candidate_dialog:
#     with st.container(border=True):
#         st.subheader("Upload Resume Files")
#         st.file_uploader("Upload Resume Files (.pdf, .docx)", type=["pdf", "docx"], accept_multiple_files=True, key="candidate_files")

#         col1, col2 = st.columns(2)
#         col1.button("Save", on_click=save_candidates)
#         col2.button("Close", on_click=close_dialog)

# def delete_candidate(index):
#     if st.session_state.selected_candidate_index == index:
#         st.session_state.selected_candidate_index = None
#     st.session_state.analyzed_candidates.pop(index)

# # Candidates table
# if st.session_state.analyzed_candidates:
#     st.markdown("### Analyzed Candidates")
    
#     # Create table with proper formatting
#     df = pd.DataFrame(st.session_state.analyzed_candidates)
    
#     # Create table header
#     cols = st.columns([3, 3, 4, 3, 3, 1.5, 1.5])
#     cols[0].markdown("**Filename**")
#     cols[1].markdown("**Name**")
#     cols[2].markdown("**Email**")
#     cols[3].markdown("**Phone**")
#     cols[4].markdown("**Uploaded**")
#     cols[5].markdown("**Actions**")
#     cols[6].markdown("**Delete**")
    
#     st.markdown("---")
    
#     # Table rows
#     for i, row in df.iterrows():
#         cols = st.columns([6, 5, 5, 3, 3, 1.5, 1.5])
#         cols[0].write(row["filename"])
#         cols[1].write(row.get("candidate_name", "N/A"))
#         cols[2].write(row.get("email", "N/A"))
#         cols[3].write(row.get("phone_number", "N/A"))
#         cols[4].write(row.get("timestamp", "N/A"))
        
#         if cols[5].button(":information_source:", key=f"details_{i}", help="View candidate details."):
#             show_candidate_details(i)
        
#         if cols[6].button(":wastebasket:", key=f"delete_{i}", help= "Delete candidate."):
#             delete_candidate(i)
#             st.rerun()

# else:
#     st.info("No candidates analyzed yet.")

# # Candidate details dialog
# if st.session_state.show_candidate_details and st.session_state.selected_candidate_index is not None:
#     candidate = st.session_state.analyzed_candidates[st.session_state.selected_candidate_index]
    
#     with st.container(border=True):
#         # Dialog header with close button
#         col1, col2 = st.columns([4, 1])
#         col1.markdown(f"# {candidate.get('candidate_name', 'N/A')}")
#         if col2.button("✕", key="close_details", help="Close details"):
#             close_details_dialog()
        
#         st.markdown(f"**Email:** {candidate.get('email', 'N/A')}")
#         st.markdown(f"**Phone:** {candidate.get('phone_number', 'N/A')}")
        
#         # Display websites if available
#         if candidate.get('websites'):
#             st.markdown("- " + candidate['websites'][0])
        
#         st.markdown(f"## Summary")
#         st.markdown(f"{candidate.get('comment', 'N/A')}")
        
#         st.markdown("## Experience:")
#         st.markdown(f"**Years of Experience:** :grey-badge[{candidate.get('years_of_experience', 'N/A')}]")
        
#         # Display the roles with proper st.markdown calls
#         if candidate.get("roles"):
#             for role in candidate["roles"]:
#                 st.markdown(f"### {role.get('title', 'N/A')}")
#                 st.markdown(f"**Company:** {role.get('company', 'N/A')}")
#                 st.markdown(f"**Summary:** {role.get('summary', 'N/A')}")
#                 st.markdown("---")  # Add separator between roles
#         else:
#             st.error("No experience found.")
        
#         st.markdown("## Education:")
#         if candidate.get("education"):
#             for edu in candidate["education"]:
#                 st.markdown(f"**{edu.get('level', 'N/A')} in {edu.get('field', 'N/A')}**")
#                 st.markdown(f"Institution: {edu.get('institution', 'N/A')}")
#                 st.markdown(f"Graduation Year: {edu.get('year', 'N/A')}")
#                 if edu.get('gpa'):
#                     st.markdown(f"GPA: {edu.get('gpa')}")
#                 st.markdown("---")
#         else:
#             st.error("No education found.")
        
#         st.markdown("## Responsibilities:")
#         if candidate.get("responsibilities"):
#             for resp in candidate["responsibilities"]:
#                 st.markdown(f"- {resp}")
#         else:
#             st.error("No tasks/responsibilities found.")
        
#         st.markdown("## Technical Skills:")
#         if candidate.get("technical_skill"):
#             # Display skills in a more compact format
#             skills_text = " ".join([f":blue-badge[{skill}]" for skill in candidate["technical_skill"]])
#             st.markdown(skills_text)
#         else:
#             st.error("No technical skills found.")
        
#         st.markdown("## Soft Skills:")
#         if candidate.get("soft_skill"):
#             skills_text = " ".join([f":green-badge[{skill}]" for skill in candidate["soft_skill"]])
#             st.markdown(skills_text)
#         else:
#             st.error("No soft skills found.")
        
#         st.markdown("## Certificates:")
#         if candidate.get("certificate") and len(candidate["certificate"]) > 0:
#             for cert in candidate["certificate"]:
#                 st.markdown(f"- {cert}")
#         else:
#             st.info("No certificates found.")
        
#         st.markdown("## Recommended Positions:")
#         if candidate.get('job_recommended'):
#             positions_text = " ".join([f":grey-badge[{job}]" for job in candidate['job_recommended']])
#             st.markdown(positions_text)
#         else:
#             st.error("No recommended positions found.")
        
#         # Action buttons
#         st.markdown("---")
#         button_cols = st.columns([1, 1, 4])
        
#         # PDF viewer button
#         if candidate.get("file_bytes"):
#             if button_cols[0].button("View PDF"):
#                 st.session_state.show_pdf_viewer = True
        
#         if button_cols[1].button("Close Details"):
#             close_details_dialog()

# # PDF viewer (shown below the details dialog)
# if st.session_state.show_pdf_viewer and st.session_state.selected_candidate_index is not None:
#     candidate = st.session_state.analyzed_candidates[st.session_state.selected_candidate_index]
#     pdf_bytes = candidate.get("file_bytes")
#     if pdf_bytes:
#         st.markdown("### PDF Viewer")
#         b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
#         pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
#         st.markdown(pdf_display, unsafe_allow_html=True)
        
#         if st.button("Close PDF"):
#             st.session_state.show_pdf_viewer = False

import base64
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import io

API_BASE = "http://localhost:8000/api/v1"

st.header("Candidate Management")

# Custom CSS to style the sidebar
st.markdown("""
<style>
    .candidate-sidebar {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        height: 100vh;
        overflow-y: auto;
    }
    
    /* Match Streamlit's default sidebar styling */
    .candidate-sidebar .stMarkdown {
        color: #262730;
    }
    
    .candidate-sidebar h1 {
        color: #262730;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .candidate-sidebar h2 {
        color: #262730;
        font-size: 1.2rem;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .candidate-sidebar h3 {
        color: #262730;
        font-size: 1rem;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "show_candidate_dialog" not in st.session_state:
    st.session_state.show_candidate_dialog = False
if "candidate_files" not in st.session_state:
    st.session_state.candidate_files = []
if "analyzed_candidates" not in st.session_state:
    st.session_state.analyzed_candidates = []
if "selected_candidate_index" not in st.session_state:
    st.session_state.selected_candidate_index = None
if "show_candidate_details" not in st.session_state:
    st.session_state.show_candidate_details = False
if "show_pdf_viewer" not in st.session_state:
    st.session_state.show_pdf_viewer = False

def close_dialog():
    st.session_state.show_candidate_dialog = False
    st.session_state.candidate_files = []

def close_details_dialog():
    st.session_state.show_candidate_details = False
    st.session_state.selected_candidate_index = None
    st.session_state.show_pdf_viewer = False

def show_candidate_details(index):
    st.session_state.selected_candidate_index = index
    st.session_state.show_candidate_details = True
    st.session_state.show_pdf_viewer = False

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
            "candidate_name": analysis.get("candidate_name", "N/A"),
            "email": analysis.get("email", "N/A"),
            "phone_number": analysis.get("phone_number", "N/A"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "roles": analysis.get("roles", []),
            "education": analysis.get("education", []),
            "comment": analysis.get("comment", "N/A"),
            "responsibilities": analysis.get("responsibilities", []),
            "technical_skill": analysis.get("technical_skill", []),
            "soft_skill": analysis.get("soft_skill", []),
            "certificate": analysis.get("certificate", []),
            "job_recommended": analysis.get("job_recommended", []),
            "years_of_experience": analysis.get("years_of_experience", "N/A"),
            "websites": analysis.get("websites", []),
            "file_bytes": file_bytes if uploaded_file.type == "application/pdf" else None,
        })

    close_dialog()

st.button("Upload Candidate(s)", on_click=lambda: st.session_state.update(show_candidate_dialog=True))

# Upload dialog
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

# Candidates table
if st.session_state.analyzed_candidates:
    st.markdown("### Analyzed Candidates")
    
    # Create table with proper formatting
    df = pd.DataFrame(st.session_state.analyzed_candidates)
    
    # Create table header
    cols = st.columns([3, 3, 4, 3, 3, 1.5, 1.5])
    cols[0].markdown("**Filename**")
    cols[1].markdown("**Name**")
    cols[2].markdown("**Email**")
    cols[3].markdown("**Phone**")
    cols[4].markdown("**Uploaded**")
    cols[5].markdown("**Actions**")
    cols[6].markdown("**Delete**")
    
    st.markdown("---")
    
    # Table rows
    for i, row in df.iterrows():
        cols = st.columns([3, 3, 4, 3, 3, 1.5, 1.5])
        cols[0].write(row["filename"])
        cols[1].write(row.get("candidate_name", "N/A"))
        cols[2].write(row.get("email", "N/A"))
        cols[3].write(row.get("phone_number", "N/A"))
        cols[4].write(row.get("timestamp", "N/A"))
        
        if cols[5].button("Details", key=f"details_{i}"):
            show_candidate_details(i)
        
        if cols[6].button("Delete", key=f"delete_{i}"):
            delete_candidate(i)
            st.rerun()

else:
    st.info("No candidates analyzed yet.")

# Candidate details sidebar
if st.session_state.show_candidate_details and st.session_state.selected_candidate_index is not None:
    candidate = st.session_state.analyzed_candidates[st.session_state.selected_candidate_index]
    
    # Create two columns - main content and sidebar
    main_col, sidebar_col = st.columns([2, 1])
    
    with sidebar_col:
        with st.container(border=True):
            # Dialog header with close button
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"# {candidate.get('candidate_name', 'N/A')}")
            if col2.button("✕", key="close_details", help="Close details"):
                close_details_dialog()
            
            st.markdown(f"**Email:** {candidate.get('email', 'N/A')}")
            st.markdown(f"**Phone:** {candidate.get('phone_number', 'N/A')}")
            
            # Display websites if available
            if candidate.get('websites'):
                st.markdown("- " + candidate['websites'][0])
            
            st.markdown(f"## Summary")
            st.markdown(f"{candidate.get('comment', 'N/A')}")
            
            st.markdown("## Experience:")
            st.markdown(f"**Years of Experience:** :grey-badge[{candidate.get('years_of_experience', 'N/A')}]")
            
            # Display the roles with proper st.markdown calls
            if candidate.get("roles"):
                for role in candidate["roles"]:
                    st.markdown(f"### {role.get('title', 'N/A')}")
                    st.markdown(f"**Company:** {role.get('company', 'N/A')}")
                    st.markdown(f"**Summary:** {role.get('summary', 'N/A')}")
                    st.markdown("---")  # Add separator between roles
            else:
                st.error("No experience found.")
            
            st.markdown("## Education:")
            if candidate.get("education"):
                for edu in candidate["education"]:
                    st.markdown(f"**{edu.get('level', 'N/A')} in {edu.get('field', 'N/A')}**")
                    st.markdown(f"Institution: {edu.get('institution', 'N/A')}")
                    st.markdown(f"Graduation Year: {edu.get('year', 'N/A')}")
                    if edu.get('gpa'):
                        st.markdown(f"GPA: {edu.get('gpa')}")
                    st.markdown("---")
            else:
                st.error("No education found.")
            
            st.markdown("## Responsibilities:")
            if candidate.get("responsibilities"):
                for resp in candidate["responsibilities"]:
                    st.markdown(f"- {resp}")
            else:
                st.error("No tasks/responsibilities found.")
            
            st.markdown("## Technical Skills:")
            if candidate.get("technical_skill"):
                # Display skills in a more compact format
                skills_text = " ".join([f":blue-badge[{skill}]" for skill in candidate["technical_skill"]])
                st.markdown(skills_text)
            else:
                st.error("No technical skills found.")
            
            st.markdown("## Soft Skills:")
            if candidate.get("soft_skill"):
                skills_text = " ".join([f":green-badge[{skill}]" for skill in candidate["soft_skill"]])
                st.markdown(skills_text)
            else:
                st.error("No soft skills found.")
            
            st.markdown("## Certificates:")
            if candidate.get("certificate") and len(candidate["certificate"]) > 0:
                for cert in candidate["certificate"]:
                    st.markdown(f"- {cert}")
            else:
                st.info("No certificates found.")
            
            st.markdown("## Recommended Positions:")
            if candidate.get('job_recommended'):
                positions_text = " ".join([f":grey-badge[{job}]" for job in candidate['job_recommended']])
                st.markdown(positions_text)
            else:
                st.error("No recommended positions found.")
            
            # Action buttons
            st.markdown("---")
            button_cols = st.columns([1, 1, 4])
            
            # PDF viewer button
            if candidate.get("file_bytes"):
                if button_cols[0].button("View PDF"):
                    st.session_state.show_pdf_viewer = True
            
            if button_cols[1].button("Close Details"):
                close_details_dialog()

# PDF viewer (shown below the details dialog)
if st.session_state.show_pdf_viewer and st.session_state.selected_candidate_index is not None:
    candidate = st.session_state.analyzed_candidates[st.session_state.selected_candidate_index]
    pdf_bytes = candidate.get("file_bytes")
    if pdf_bytes:
        st.markdown("### PDF Viewer")
        b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        if st.button("Close PDF"):
            st.session_state.show_pdf_viewer = False