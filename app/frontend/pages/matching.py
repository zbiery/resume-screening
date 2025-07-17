import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import asyncio
import time

API_BASE = "http://localhost:8000/api/v1"

# Custom CSS for better styling (consistent with other pages)
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
    
    .selection-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    .job-selection {
        background: #f8f9ff;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .candidate-selection {
        background: #f8fff8;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #28a745;
    }
    
    .match-result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
        transition: transform 0.2s;
    }
    
    .match-result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .match-score {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
        text-align: center;
    }
    
    .score-excellent {
        color: #28a745;
    }
    
    .score-good {
        color: #ffc107;
    }
    
    .score-fair {
        color: #fd7e14;
    }
    
    .score-poor {
        color: #dc3545;
    }
    
    .candidate-name {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .match-details {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    
    .detail-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        padding: 0.3rem 0;
        border-bottom: 1px solid #eee;
    }
    
    .detail-label {
        font-weight: 500;
        color: #666;
    }
    
    .detail-value {
        font-weight: 600;
        color: #333;
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
    
    .progress-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
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
    
    .skill-badge-missing {
        background: #ffebee;
        color: #c62828;
    }
    
    .match-summary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .verdict-badge {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .verdict-strong {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .verdict-moderate {
        background: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    .verdict-weak {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .verdict-not {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .score-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .score-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        text-align: center;
    }
    
    .score-card h4 {
        margin: 0 0 0.5rem 0;
        color: #333;
        font-size: 0.9rem;
    }
    
    .score-card .score {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .score-card .comment {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    .strengths-gaps {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .strengths-card, .gaps-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    
    .strengths-card {
        border-left: 4px solid #28a745;
    }
    
    .gaps-card {
        border-left: 4px solid #dc3545;
    }
    
    .strengths-card h4, .gaps-card h4 {
        margin: 0 0 0.5rem 0;
        color: #333;
    }
    
    .strengths-card ul, .gaps-card ul {
        margin: 0;
        padding-left: 1.2rem;
    }
    
    .strengths-card li {
        color: #155724;
        margin-bottom: 0.3rem;
    }
    
    .gaps-card li {
        color: #721c24;
        margin-bottom: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 Job-Candidate Matching</h1>
    <p>Analyze candidate fit for job positions using AI-powered matching</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "matching_results" not in st.session_state:
    st.session_state.matching_results = []
if "selected_job" not in st.session_state:
    st.session_state.selected_job = None
if "selected_candidates" not in st.session_state:
    st.session_state.selected_candidates = []
if "matching_in_progress" not in st.session_state:
    st.session_state.matching_in_progress = False

# Load jobs and candidates from session state
registered_jobs = st.session_state.get("registered_jobs", [])
analyzed_candidates = st.session_state.get("analyzed_candidates", [])

def get_score_class(score):
    """Return CSS class based on score value (0-100)"""
    if score >= 80:
        return "score-excellent"
    elif score >= 60:
        return "score-good"
    elif score >= 40:
        return "score-fair"
    else:
        return "score-poor"

def get_score_label(score):
    """Return label based on score value (0-100)"""
    if score >= 80:
        return "Excellent Match"
    elif score >= 60:
        return "Good Match"
    elif score >= 40:
        return "Fair Match"
    else:
        return "Poor Match"

def get_verdict_class(verdict):
    """Return CSS class based on verdict"""
    verdict_lower = verdict.lower()
    if "strong" in verdict_lower:
        return "verdict-strong"
    elif "moderate" in verdict_lower:
        return "verdict-moderate"
    elif "weak" in verdict_lower:
        return "verdict-weak"
    else:
        return "verdict-not"

def calculate_overall_score(match_result):
    weights = {
        "education": 0.20,
        "experience": 0.25,
        "technical_skill": 0.25,
        "responsibility": 0.20,
        "soft_skill": 0.05,
        "domain": 0.05,
        "certificate": 0,
    }

    total_score = 0
    for key, weight in weights.items():
        score = match_result.get(key, {}).get("score", 0)
        total_score += score * weight

    return round(total_score, 2)

def run_matching_analysis():
    """Run matching analysis for selected job and candidates"""
    
    if st.session_state.selected_job is None or not st.session_state.selected_candidates:
        st.error("❌ Please select a job and at least one candidate.")
        return
    
    st.session_state.matching_in_progress = True
    st.session_state.matching_results = []
    
    job = registered_jobs[st.session_state.selected_job]
    selected_candidate_indices = st.session_state.selected_candidates
    
    # Create progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Prepare job data
    job_data = {
        "title": job.get("title", ""),
        "description": job.get("description", ""),
        "job_level": job.get("job_level", ""),
        "years_of_experience": job.get("years_of_experience", 0),
        "technical_skill": job.get("technical_skill", []),
        "soft_skill": job.get("soft_skill", []),
        "educational_requirements": job.get("educational_requirements", []),
        "experience": job.get("experience", []),
        "responsibilities": job.get("responsibilities", []),
        "certificate": job.get("certificate", []),
        "domain": job.get("domain", ""),
        "employment_type": job.get("employment_type", ""),
        "location_requirement": job.get("location_requirement", "")
    }
    
    # Prepare candidates data
    candidates_data = []
    for candidate_index in selected_candidate_indices:
        candidate = analyzed_candidates[candidate_index]
        candidate_data = {
            "candidate_name": candidate.get("candidate_name", ""),
            "email": candidate.get("email", ""),
            "phone_number": candidate.get("phone_number", ""),
            "years_of_experience": candidate.get("years_of_experience", 0),
            "technical_skill": candidate.get("technical_skill", []),
            "soft_skill": candidate.get("soft_skill", []),
            "education": candidate.get("education", []),
            "roles": candidate.get("roles", []),
            "responsibilities": candidate.get("responsibilities", []),
            "certificate": candidate.get("certificate", []),
            "job_recommended": candidate.get("job_recommended", []),
            "comment": candidate.get("comment", "")
        }
        candidates_data.append(candidate_data)
    
    # Prepare the request payload according to API specification
    payload = {
        "job": job_data,
        "candidates": candidates_data  # Note: plural "candidates" as a list
    }
    
    status_text.text("Analyzing matches...")
    progress_bar.progress(0.5)
    
    try:
        # Make API call to match/analyze endpoint
        response = requests.post(
            f"{API_BASE}/match/analyze",
            json=payload,
            timeout=60  # Increased timeout for multiple candidates
        )
        
        # Debug: Print response details
        st.write(f"Response Status: {response.status_code}")
        if response.status_code != 200:
            st.error(f"API Error: {response.status_code}")
            st.error(f"Response: {response.text}")
            return
        
        response.raise_for_status()
        match_results = response.json()
        
        # Process results
        results = []
        for i, match_result in enumerate(match_results):
            candidate = analyzed_candidates[selected_candidate_indices[i]]
            
            # Add candidate info to the result
            match_result["candidate_info"] = {
                "name": candidate.get("candidate_name", "Unknown"),
                "email": candidate.get("email", ""),
                "phone": candidate.get("phone_number", ""),
                "experience": candidate.get("years_of_experience", 0),
                "filename": candidate.get("filename", "")
            }
            
            # Calculate overall score for sorting
            match_result["overall_match_score"] = calculate_overall_score(match_result)
            
            results.append(match_result)
        
        # Sort results by overall match score (descending)
        results.sort(key=lambda x: x.get("overall_match_score", 0), reverse=True)
        
        st.session_state.matching_results = results
        st.session_state.matching_in_progress = False
        
        status_text.text("✅ Matching analysis complete!")
        progress_bar.progress(1.0)
        
        # Clear the progress indicators after a short delay
        time.sleep(1)
        status_text.empty()
        progress_bar.empty()
        
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Network error: {e}")
        st.session_state.matching_in_progress = False
    except Exception as e:
        st.error(f"❌ Failed to analyze matches: {e}")
        st.session_state.matching_in_progress = False

# Check if we have jobs and candidates
if not registered_jobs and not analyzed_candidates:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">📊</div>
        <h3>No jobs or candidates available</h3>
        <p>Please add jobs and candidates first before running matching analysis.</p>
    </div>
    """, unsafe_allow_html=True)
elif not registered_jobs:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">💼</div>
        <h3>No jobs available</h3>
        <p>Please create job postings first in the Jobs page.</p>
    </div>
    """, unsafe_allow_html=True)
elif not analyzed_candidates:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">👥</div>
        <h3>No candidates available</h3>
        <p>Please upload candidate resumes first in the Candidates page.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Job selection
    st.markdown("### 💼 Select Job Position")
    with st.container(border=True):
        job_options = [f"{job.get('title', 'Untitled')} - {job.get('domain', 'Unknown Domain')}" 
                      for job in registered_jobs]
        
        selected_job_index = st.selectbox(
            "Choose a job to match candidates against:",
            range(len(registered_jobs)),
            format_func=lambda x: job_options[x],
            key="job_selectbox"
        )
        
        # Always update session state when selection changes
        st.session_state.selected_job = selected_job_index
        
        if selected_job_index is not None:
            job = registered_jobs[selected_job_index]
            
            st.markdown(f"""
            <div class="job-selection">
                <h4>📋 Selected Job: {job.get('title', 'N/A')}</h4>
                <p><strong>Level:</strong> {job.get('job_level', 'N/A')}</p>
                <p><strong>Experience Required:</strong> {job.get('years_of_experience', 0)} years</p>
                <p><strong>Domain:</strong> {job.get('domain', 'N/A')}</p>
                <p><strong>Employment Type:</strong> {job.get('employment_type', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)

    # Candidate selection
    st.markdown("### 👥 Select Candidates")
    with st.container(border=True):
        candidate_options = [f"{candidate.get('candidate_name', 'Unknown')} - {candidate.get('email', 'No email')} ({candidate.get('years_of_experience', 0)} years exp)" 
                           for candidate in analyzed_candidates]
        
        selected_candidate_indices = st.multiselect(
            "Choose candidates to analyze:",
            range(len(analyzed_candidates)),
            format_func=lambda x: candidate_options[x],
            key="candidate_multiselect"
        )
        
        # Always update session state when selection changes
        st.session_state.selected_candidates = selected_candidate_indices
        
        if selected_candidate_indices:
            st.markdown(f"""
            <div class="candidate-selection">
                <h4>✅ Selected {len(selected_candidate_indices)} candidate(s)</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Show selected candidates
            for idx in selected_candidate_indices:
                candidate = analyzed_candidates[idx]
                st.markdown(f"• **{candidate.get('candidate_name', 'Unknown')}** - {candidate.get('email', 'No email')}")

    # Run matching button
    st.markdown("### 🚀 Run Analysis")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🎯 Run Matching Analysis", type="primary", use_container_width=True, disabled=st.session_state.matching_in_progress):
            run_matching_analysis()
    
    with col2:
        if st.session_state.matching_in_progress:
            st.info("🔄 Analysis in progress...")

# Display results
if st.session_state.matching_results:
    st.markdown("### 📊 Matching Results")
    
    # Summary statistics
    results = st.session_state.matching_results
    avg_score = sum(r.get("overall_match_score", 0) for r in results) / len(results)
    top_score = max(r.get("overall_match_score", 0) for r in results)
    
    st.markdown(f"""
    <div class="match-summary">
        <h3>📈 Analysis Summary</h3>
        <p><strong>Candidates Analyzed:</strong> {len(results)}</p>
        <p><strong>Average Match Score:</strong> {avg_score:.1f}%</p>
        <p><strong>Top Match Score:</strong> {top_score:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Results cards
    for i, result in enumerate(results):
        candidate_info = result.get("candidate_info", {})
        overall_score = result.get("overall_match_score", 0)
        verdict = result.get("verdict", "Not evaluated")
        score_class = get_score_class(overall_score)
        score_label = get_score_label(overall_score)
        verdict_class = get_verdict_class(verdict)
        
        st.markdown(f"""
        <div class="match-result-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div class="candidate-name">#{i+1} {candidate_info.get('name', 'Unknown')}</div>
                    <p style="margin: 0; color: #666;">📧 {candidate_info.get('email', 'No email')}</p>
                    <p style="margin: 0; color: #666;">💼 {candidate_info.get('experience', 0)} years experience</p>
                    <div class="verdict-badge {verdict_class}">{verdict}</div>
                </div>
                <div>
                    <div class="match-score {score_class}">{overall_score:.1f}%</div>
                    <p style="margin: 0; text-align: center; color: #666; font-size: 0.9rem;">{score_label}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed breakdown (expandable)
        with st.expander(f"📋 Detailed Analysis for {candidate_info.get('name', 'Unknown')}"):
            
            # Category scores grid
            st.markdown("#### 📊 Category Scores")
            score_html = '<div class="score-grid">'
            
            categories = [
                ('education', '🎓 Education'),
                ('experience', '💼 Experience'),
                ('technical_skill', '⚙️ Technical Skills'),
                ('responsibility', '📋 Responsibilities'),
                ('certificate', '📜 Certificates'),
                ('soft_skill', '🤝 Soft Skills'),
                ('domain', '🏢 Domain Knowledge')
            ]
            
            for category_key, category_name in categories:
                if category_key in result:
                    category_data = result[category_key]
                    score = category_data.get('score', 0)
                    comment = category_data.get('comment', 'No comment')
                    score_class = get_score_class(score)
                    
                    score_html += f'''
                    <div class="score-card">
                        <h4>{category_name}</h4>
                        <div class="score {score_class}">{score}%</div>
                        <div class="comment">{comment}</div>
                    </div>
                    '''
            
            score_html += '</div>'
            st.markdown(score_html, unsafe_allow_html=True)
            
            # Strengths and Gaps
            st.markdown("#### 💪 Strengths & Gaps")
            strengths = result.get('strengths', [])
            gaps = result.get('gaps', [])
            
            strengths_gaps_html = f'''
            <div class="strengths-gaps">
                <div class="strengths-card">
                    <h4>✅ Strengths</h4>
                    <ul>
                        {"".join([f"<li>{strength}</li>" for strength in strengths]) if strengths else "<li>No strengths identified</li>"}
                    </ul>
                </div>
                <div class="gaps-card">
                    <h4>❌ Gaps</h4>
                    <ul>
                        {"".join([f"<li>{gap}</li>" for gap in gaps]) if gaps else "<li>No gaps identified</li>"}
                    </ul>
                </div>
            </div>
            '''
            st.markdown(strengths_gaps_html, unsafe_allow_html=True)
            
            # Overall Summary
            st.markdown("#### 📝 Overall Summary")
            overall_summary = result.get('overall_summary', 'No summary available')
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea;">
                {overall_summary}
            </div>
            """, unsafe_allow_html=True)
            
            # Raw data (for debugging)
            with st.expander("🔍 Raw Match Data (Debug)"):
                st.json(result)

# Clear results button
if st.session_state.matching_results:
    st.markdown("---")
    if st.button("🗑️ Clear Results", type="secondary"):
        st.session_state.matching_results = []
        st.rerun()