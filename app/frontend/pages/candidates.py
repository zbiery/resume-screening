import base64
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import io

API_BASE = "http://localhost:8000/api/v1"

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 600;
    }
    
    .main-header p {
        color: white;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .stats-number {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
        margin: 0;
    }
    
    .stats-label {
        color: #666;
        font-size: 0.9rem;
        margin: 0;
    }
    
    .candidate-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
        transition: transform 0.2s;
    }
    
    .candidate-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .candidate-name {
        font-size: 1.2rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .candidate-info {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #f8f9ff;
        margin: 1rem 0;
    }
    
    .action-button {
        background: #667eea;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        margin: 0.2rem;
    }
    
    .delete-button {
        background: #dc3545;
        color: white;
        border: none;
        padding: 0.3rem 0.8rem;
        border-radius: 5px;
        cursor: pointer;
    }
    
    .detail-section {
        margin-bottom: 1.5rem;
    }
    
    .detail-section h3 {
        color: #667eea;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .skill-badge {
        display: inline-block;
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.2rem;
    }
    
    .experience-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 3px solid #667eea;
    }
    
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #666;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>👨‍💼 Candidate Management System</h1>
    <p>Upload, analyze, and manage candidate resumes with ease</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "show_candidate_dialog" not in st.session_state:
    st.session_state.show_candidate_dialog = False
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
    # Don't modify candidate_files here - let it be handled by the widget state

def close_details_dialog():
    st.session_state.show_candidate_details = False
    st.session_state.selected_candidate_index = None
    st.session_state.show_pdf_viewer = False

def show_candidate_details(index):
    st.session_state.selected_candidate_index = index
    st.session_state.show_candidate_details = True
    st.session_state.show_pdf_viewer = False

def save_candidates():
    # Get the uploaded files from the widget directly
    uploaded_files = st.session_state.get("candidate_files", [])
    if not uploaded_files:
        st.error("❌ Please upload at least one resume.")
        return

    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing {uploaded_file.name}...")
        progress_bar.progress((i + 1) / len(uploaded_files))
        
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
            response = requests.post(f"{API_BASE}/resumes/upload", files=files, timeout=15)
            response.raise_for_status()
            result = response.json()
            extracted_text = result.get("content", "")
            
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Network error uploading {uploaded_file.name}: {e}")
            continue
        except Exception as e:
            st.error(f"❌ Failed to extract text from {uploaded_file.name}: {e}")
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
            st.error(f"❌ Failed to analyze {uploaded_file.name}: {e}")
            continue

        # Save result
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

    status_text.text("✅ All files processed successfully!")
    progress_bar.progress(1.0)
    st.success(f"🎉 Successfully processed {len(uploaded_files)} candidate(s)!")
    
    # Use rerun to refresh the page and reset the dialog
    st.session_state.show_candidate_dialog = False
    st.rerun()

# Stats section
if st.session_state.analyzed_candidates:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <p class="stats-number">{len(st.session_state.analyzed_candidates)}</p>
            <p class="stats-label">Total Candidates</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        recent_candidates = sum(1 for c in st.session_state.analyzed_candidates 
                              if (datetime.now() - datetime.strptime(c["timestamp"], "%Y-%m-%d %H:%M:%S")).days < 7)
        st.markdown(f"""
        <div class="stats-card">
            <p class="stats-number">{recent_candidates}</p>
            <p class="stats-label">This Week</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        valid_exp = []
        for c in st.session_state.analyzed_candidates:
            exp = c["years_of_experience"]
            if exp != "N/A":
                try:
                    # Handle both string and numeric values
                    if isinstance(exp, str):
                        # Remove any non-numeric characters except decimal point
                        exp_clean = ''.join(char for char in exp if char.isdigit() or char == '.')
                        if exp_clean and exp_clean != '.':
                            valid_exp.append(float(exp_clean))
                    else:
                        # If it's already a number
                        valid_exp.append(float(exp))
                except (ValueError, TypeError):
                    continue
        
        avg_exp = sum(valid_exp) / len(valid_exp) if valid_exp else 0
        st.markdown(f"""
        <div class="stats-card">
            <p class="stats-number">{avg_exp:.1f}</p>
            <p class="stats-label">Avg Years Experience</p>
        </div>
        """, unsafe_allow_html=True)

# Upload button
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("📁 Upload Candidates", type="primary", use_container_width=True):
        st.session_state.show_candidate_dialog = True

# Upload dialog
if st.session_state.show_candidate_dialog:
    st.markdown("### 📤 Upload Resume Files")
    
    with st.container(border=True):
        st.markdown('<div class="upload-area">', unsafe_allow_html=True)
        st.markdown("**Drag and drop files here or click to browse**")
        st.file_uploader("", type=["pdf", "docx"], accept_multiple_files=True, key="candidate_files", label_visibility="collapsed")
        st.markdown("Supported formats: PDF, DOCX")
        st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Process Files", type="primary", use_container_width=True):
                save_candidates()
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                close_dialog()

def delete_candidate(index):
    if st.session_state.selected_candidate_index == index:
        st.session_state.selected_candidate_index = None
    st.session_state.analyzed_candidates.pop(index)

# Candidates display
if st.session_state.analyzed_candidates:
    st.markdown("### 👥 Candidate Directory")
    
    # Search and filter
    search_col, filter_col = st.columns([3, 1])
    with search_col:
        search_term = st.text_input("🔍 Search candidates...", placeholder="Search by name, email, or skills")
    with filter_col:
        exp_filter = st.selectbox("Experience Level", ["All", "0-2 years", "3-5 years", "5+ years"])
    
    # Filter candidates based on search and filters
    filtered_candidates = []
    for i, candidate in enumerate(st.session_state.analyzed_candidates):
        # Search filter
        if search_term:
            search_fields = [
                candidate.get("candidate_name", ""),
                candidate.get("email", ""),
                " ".join(candidate.get("technical_skill", [])),
                " ".join(candidate.get("soft_skill", []))
            ]
            if not any(search_term.lower() in field.lower() for field in search_fields):
                continue
        
        # Experience filter
        if exp_filter != "All":
            try:
                exp = candidate.get("years_of_experience", 0)
                if exp == "N/A":
                    continue
                
                # Handle both string and numeric values
                if isinstance(exp, str):
                    exp_clean = ''.join(char for char in exp if char.isdigit() or char == '.')
                    if not exp_clean or exp_clean == '.':
                        continue
                    years = float(exp_clean)
                else:
                    years = float(exp)
                
                if exp_filter == "0-2 years" and years > 2:
                    continue
                elif exp_filter == "3-5 years" and (years < 3 or years > 5):
                    continue
                elif exp_filter == "5+ years" and years < 5:
                    continue
            except (ValueError, TypeError):
                continue
        
        filtered_candidates.append((i, candidate))
    
    # Display candidates in a grid
    for i, (original_index, candidate) in enumerate(filtered_candidates):
        st.markdown(f"""
        <div class="candidate-card">
            <div class="candidate-name">👤 {candidate.get('candidate_name', 'N/A')}</div>
            <div class="candidate-info">📧 {candidate.get('email', 'N/A')}</div>
            <div class="candidate-info">📞 {candidate.get('phone_number', 'N/A')}</div>
            <div class="candidate-info">📅 Uploaded: {candidate.get('timestamp', 'N/A')}</div>
            <div class="candidate-info">💼 Experience: {candidate.get('years_of_experience', 'N/A')} years</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("👁️ View Details", key=f"details_{original_index}"):
                show_candidate_details(original_index)
        with col2:
            if st.button("🗑️ Delete", key=f"delete_{original_index}"):
                delete_candidate(original_index)
                st.rerun()

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">📋</div>
        <h3>No candidates yet</h3>
        <p>Upload your first candidate resume to get started!</p>
    </div>
    """, unsafe_allow_html=True)

# Candidate details dialog
if st.session_state.show_candidate_details and st.session_state.selected_candidate_index is not None:
    candidate = st.session_state.analyzed_candidates[st.session_state.selected_candidate_index]
    
    st.markdown("---")
    st.markdown(f"## 👤 {candidate.get('candidate_name', 'N/A')}")
    
    with st.container(border=True):
        # Basic info
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**📧 Email:** {candidate.get('email', 'N/A')}")
            st.markdown(f"**📞 Phone:** {candidate.get('phone_number', 'N/A')}")
        with col2:
            st.markdown(f"**💼 Experience:** {candidate.get('years_of_experience', 'N/A')} years")
            if candidate.get('websites'):
                st.markdown(f"**🌐 Website:** {candidate['websites'][0]}")
        
        # Summary
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown("### 📝 Summary")
        st.markdown(f"{candidate.get('comment', 'N/A')}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Experience
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown("### 💼 Experience")
        if candidate.get("roles"):
            for role in candidate["roles"]:
                st.markdown(f"""
                <div class="experience-card">
                    <h4>{role.get('title', 'N/A')}</h4>
                    <p><strong>Company:</strong> {role.get('company', 'N/A')}</p>
                    <p><strong>Summary:</strong> {role.get('summary', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No experience information available.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Education
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown("### 🎓 Education")
        if candidate.get("education"):
            for edu in candidate["education"]:
                st.markdown(f"""
                <div class="experience-card">
                    <h4>{edu.get('level', 'N/A')} in {edu.get('field', 'N/A')}</h4>
                    <p><strong>Institution:</strong> {edu.get('institution', 'N/A')}</p>
                    <p><strong>Graduation Year:</strong> {edu.get('year', 'N/A')}</p>
                    {f"<p><strong>GPA:</strong> {edu.get('gpa')}</p>" if edu.get('gpa') else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No education information available.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Skills
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="detail-section">', unsafe_allow_html=True)
            st.markdown("### 🔧 Technical Skills")
            if candidate.get("technical_skill"):
                skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in candidate["technical_skill"]])
                st.markdown(skills_html, unsafe_allow_html=True)
            else:
                st.info("No technical skills listed.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="detail-section">', unsafe_allow_html=True)
            st.markdown("### 🤝 Soft Skills")
            if candidate.get("soft_skill"):
                skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in candidate["soft_skill"]])
                st.markdown(skills_html, unsafe_allow_html=True)
            else:
                st.info("No soft skills listed.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Responsibilities
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown("### 📋 Key Responsibilities")
        if candidate.get("responsibilities"):
            for resp in candidate["responsibilities"]:
                st.markdown(f"• {resp}")
        else:
            st.info("No responsibilities listed.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Certificates
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown("### 🏆 Certificates")
        if candidate.get("certificate") and len(candidate["certificate"]) > 0:
            for cert in candidate["certificate"]:
                st.markdown(f"• {cert}")
        else:
            st.info("No certificates listed.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Recommended positions
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown("### 🎯 Recommended Positions")
        if candidate.get('job_recommended'):
            positions_html = "".join([f'<span class="skill-badge">{job}</span>' for job in candidate['job_recommended']])
            st.markdown(positions_html, unsafe_allow_html=True)
        else:
            st.info("No position recommendations available.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if candidate.get("file_bytes"):
                if st.button("📄 View PDF", type="secondary"):
                    st.session_state.show_pdf_viewer = True
        
        with col2:
            if st.button("❌ Close", type="secondary"):
                close_details_dialog()

# PDF viewer
if st.session_state.show_pdf_viewer and st.session_state.selected_candidate_index is not None:
    candidate = st.session_state.analyzed_candidates[st.session_state.selected_candidate_index]
    pdf_bytes = candidate.get("file_bytes")
    if pdf_bytes:
        st.markdown("---")
        st.markdown("### 📄 PDF Viewer")
        b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        if st.button("❌ Close PDF"):
            st.session_state.show_pdf_viewer = False