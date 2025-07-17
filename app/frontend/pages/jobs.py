import streamlit as st
import requests
import pandas as pd
from datetime import datetime

API_BASE = "http://localhost:8000/api/v1"

# Custom CSS for better styling (consistent with candidate page)
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
    
    .job-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
        transition: transform 0.2s;
    }
    
    .job-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .job-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .job-info {
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
    
    .requirement-card {
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
    
    .level-badge {
        display: inline-block;
        background: #fff3cd;
        color: #856404;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>💼 Job Management System</h1>
    <p>Create, analyze, and manage job postings with detailed requirements</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "show_job_dialog" not in st.session_state:
    st.session_state.show_job_dialog = False
if "registered_jobs" not in st.session_state:
    st.session_state.registered_jobs = []
if "selected_job_index" not in st.session_state:
    st.session_state.selected_job_index = None
if "show_job_details" not in st.session_state:
    st.session_state.show_job_details = False

def close_dialog():
    st.session_state.show_job_dialog = False

def close_details_dialog():
    st.session_state.show_job_details = False
    st.session_state.selected_job_index = None

def show_job_details(index):
    st.session_state.selected_job_index = index
    st.session_state.show_job_details = True

def save_job(title, description):
    if not description.strip():
        st.error("❌ Please enter a job description.")
        return False
    
    if not title.strip():
        st.error("❌ Please enter a job title.")
        return False

    with st.spinner("🔄 Analyzing job description..."):
        try:
            response = requests.post(
                f"{API_BASE}/jobs/analyze",
                json={"content": description},
                timeout=15,
            )
            response.raise_for_status()
            result = response.json()
            
            # Save job with analysis results
            st.session_state.registered_jobs.append({
                "title": title,
                "description": description,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "job_title": result.get("job_title", title),
                "job_level": result.get("job_level", "N/A"),
                "employment_type": result.get("employment_type", "N/A"),
                "location_requirement": result.get("location_requirement", "N/A"),
                "years_of_experience": result.get("years_of_experience", 0),
                "educational_requirements": result.get("educational_requirements", []),
                "experience": result.get("experience", []),
                "technical_skill": result.get("technical_skill", []),
                "responsibilities": result.get("responsibilities", []),
                "certificate": result.get("certificate", []),
                "soft_skill": result.get("soft_skill", []),
                "domain": result.get("domain", "N/A"),
                "ideal_candidate_summary": result.get("ideal_candidate_summary", "N/A")
            })
            
            st.success("🎉 Job successfully analyzed and saved!")
            close_dialog()
            st.rerun()
            return True
            
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Network error: {e}")
            return False
        except Exception as e:
            st.error(f"❌ Failed to analyze job: {e}")
            return False

def delete_job(index):
    if st.session_state.selected_job_index == index:
        st.session_state.selected_job_index = None
    st.session_state.registered_jobs.pop(index)

# Stats section
if st.session_state.registered_jobs:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <p class="stats-number">{len(st.session_state.registered_jobs)}</p>
            <p class="stats-label">Total Jobs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        recent_jobs = sum(1 for j in st.session_state.registered_jobs 
                         if (datetime.now() - datetime.strptime(j["timestamp"], "%Y-%m-%d %H:%M:%S")).days < 7)
        st.markdown(f"""
        <div class="stats-card">
            <p class="stats-number">{recent_jobs}</p>
            <p class="stats-label">This Week</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        valid_exp = []
        for j in st.session_state.registered_jobs:
            exp = j.get("years_of_experience", 0)
            if exp and exp != "N/A":
                try:
                    valid_exp.append(float(exp))
                except (ValueError, TypeError):
                    continue
        
        avg_exp = sum(valid_exp) / len(valid_exp) if valid_exp else 0
        st.markdown(f"""
        <div class="stats-card">
            <p class="stats-number">{avg_exp:.1f}</p>
            <p class="stats-label">Avg Years Required</p>
        </div>
        """, unsafe_allow_html=True)

# Upload button
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("📝 Create Job", type="primary", use_container_width=True):
        st.session_state.show_job_dialog = True

# Job creation dialog
if st.session_state.show_job_dialog:
    st.markdown("### 📝 Create New Job Posting")
    
    with st.container(border=True):
        st.markdown('<div class="upload-area">', unsafe_allow_html=True)
        job_title = st.text_input("Job Title", placeholder="e.g., Senior Software Engineer")
        job_description = st.text_area("Job Description", height=250, 
                                     placeholder="Paste the complete job description here...")
        st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Analyze & Save", type="primary", use_container_width=True):
                if save_job(job_title, job_description):
                    st.rerun()
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                close_dialog()
                st.rerun()

# Jobs display
if st.session_state.registered_jobs:
    st.markdown("### 💼 Job Postings")
    
    # Search and filter
    search_col, filter_col = st.columns([3, 1])
    with search_col:
        search_term = st.text_input("🔍 Search jobs...", placeholder="Search by title, skills, or domain")
    with filter_col:
        level_filter = st.selectbox("Job Level", ["All", "Entry-level", "Mid", "Senior", "Lead", "Director"])
    
    # Filter jobs based on search and filters
    filtered_jobs = []
    for i, job in enumerate(st.session_state.registered_jobs):
        # Search filter
        if search_term:
            search_fields = [
                job.get("title", ""),
                job.get("job_title", ""),
                job.get("domain", ""),
                " ".join(job.get("technical_skill", [])),
                " ".join(job.get("soft_skill", []))
            ]
            if not any(search_term.lower() in field.lower() for field in search_fields):
                continue
        
        # Level filter
        if level_filter != "All":
            job_level = job.get("job_level", "")
            if level_filter.lower() not in job_level.lower():
                continue
        
        filtered_jobs.append((i, job))
    
    # Display jobs in cards
    for i, (original_index, job) in enumerate(filtered_jobs):
        st.markdown(f"""
        <div class="job-card">
            <div class="job-title">💼 {job.get('title', 'N/A')}</div>
            <div class="job-info">📊 Level: {job.get('job_level', 'N/A')}</div>
            <div class="job-info">🏢 Type: {job.get('employment_type', 'N/A')}</div>
            <div class="job-info">📍 Location: {job.get('location_requirement', 'N/A')}</div>
            <div class="job-info">⏱️ Experience: {job.get('years_of_experience', 0)} years</div>
            <div class="job-info">📅 Created: {job.get('timestamp', 'N/A')}</div>
            <div class="job-info">🏭 Domain: {job.get('domain', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("👁️ View Details", key=f"details_{original_index}"):
                show_job_details(original_index)
        with col2:
            if st.button("🗑️ Delete", key=f"delete_{original_index}"):
                delete_job(original_index)
                st.rerun()

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">💼</div>
        <h3>No jobs posted yet</h3>
        <p>Create your first job posting to get started!</p>
    </div>
    """, unsafe_allow_html=True)

# Job details dialog
if st.session_state.show_job_details and st.session_state.selected_job_index is not None:
    job = st.session_state.registered_jobs[st.session_state.selected_job_index]
    
    st.markdown("---")
    st.markdown(f"## 💼 {job.get('title', 'N/A')}")
    
    with st.container(border=True):
        # Basic info
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**📊 Level:** {job.get('job_level', 'N/A')}")
            st.markdown(f"**🏢 Type:** {job.get('employment_type', 'N/A')}")
            st.markdown(f"**📍 Location:** {job.get('location_requirement', 'N/A')}")
        with col2:
            st.markdown(f"**⏱️ Experience:** {job.get('years_of_experience', 0)} years")
            st.markdown(f"**🏭 Domain:** {job.get('domain', 'N/A')}")
            st.markdown(f"**📅 Created:** {job.get('timestamp', 'N/A')}")
        
        # Ideal candidate summary
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown("### 🎯 Ideal Candidate Profile")
        st.markdown(f"{job.get('ideal_candidate_summary', 'N/A')}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Educational requirements
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown("### 🎓 Educational Requirements")
        if job.get("educational_requirements"):
            for edu in job["educational_requirements"]:
                fields_str = ", ".join(edu.get("fields", []))
                st.markdown(f"""
                <div class="requirement-card">
                    <h4>{edu.get('level', 'N/A')}</h4>
                    <p><strong>Acceptable Fields:</strong> {fields_str if fields_str else 'N/A'}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No specific educational requirements listed.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Experience requirements
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown("### 💼 Experience Requirements")
        if job.get("experience"):
            for exp in job["experience"]:
                st.markdown(f"• {exp}")
        else:
            st.info("No specific experience requirements listed.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Responsibilities
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown("### 📋 Key Responsibilities")
        if job.get("responsibilities"):
            for resp in job["responsibilities"]:
                st.markdown(f"• {resp}")
        else:
            st.info("No responsibilities listed.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Skills
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="detail-section">', unsafe_allow_html=True)
            st.markdown("### 🔧 Technical Skills")
            if job.get("technical_skill"):
                skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in job["technical_skill"]])
                st.markdown(skills_html, unsafe_allow_html=True)
            else:
                st.info("No technical skills listed.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="detail-section">', unsafe_allow_html=True)
            st.markdown("### 🤝 Soft Skills")
            if job.get("soft_skill"):
                skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in job["soft_skill"]])
                st.markdown(skills_html, unsafe_allow_html=True)
            else:
                st.info("No soft skills listed.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Certificates
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown("### 🏆 Required/Preferred Certificates")
        if job.get("certificate") and len(job["certificate"]) > 0:
            for cert in job["certificate"]:
                st.markdown(f"• {cert}")
        else:
            st.info("No certificates required.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Original job description
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown("### 📄 Original Job Description")
        with st.expander("View Full Description"):
            st.text(job.get("description", "N/A"))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Close button
        st.markdown("---")
        if st.button("❌ Close", type="secondary"):
            close_details_dialog()
            st.rerun()