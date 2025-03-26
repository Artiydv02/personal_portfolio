import re
import PyPDF2
import os
from pathlib import Path

def extract_resume_data(pdf_path):
    """
    Extract data from a resume PDF file
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        dict: Dictionary containing the resume data
    """
    # Check if file exists
    if not os.path.exists(pdf_path):
        # Copy from the uploaded assets if possible
        src_path = "attached_assets/2022UMT1771.pdf"
        if os.path.exists(src_path):
            # Ensure assets directory exists
            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
            # Copy file
            import shutil
            shutil.copy(src_path, pdf_path)
        else:
            print(f"Resume file not found at {pdf_path}")
            return {}
    
    # Extract text from PDF
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return {}
    
    # Parse the resume text
    resume_data = {
        'name': '',
        'contact': '',
        'email': '',
        'linkedin': '',
        'github': '',
        'summary': '',
        'education': [],
        'skills': {},
        'projects': [],
        'certificates': [],
        'activities': [],
        'hobbies': []
    }
    
    # Extract name (first line typically)
    lines = text.split('\n')
    if lines:
        resume_data['name'] = lines[0].strip()
    
    # Extract contact info
    contact_match = re.search(r'\(?\+?[0-9]{1,3}?\)?\s*[0-9]{3,}[-\s]?[0-9]{3,}', text)
    if contact_match:
        resume_data['contact'] = contact_match.group(0)
    
    # Extract email
    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    if email_match:
        resume_data['email'] = email_match.group(0)
    else:
        resume_data['email'] = "Gmail"  # From the resume
    
    # Extract LinkedIn and GitHub
    if "LinkedIn" in text:
        resume_data['linkedin'] = "LinkedIn"
    if "GitHub" in text:
        resume_data['github'] = "GitHub"
    
    # Extract summary
    summary_match = re.search(r'SUMMARY\s*(.*?)(?:EDUCATION|SKILLS)', text, re.DOTALL)
    if summary_match:
        resume_data['summary'] = summary_match.group(1).strip()
    
    # Extract education
    education_match = re.search(r'EDUCATION\s*(.*?)(?:SKILLS|PROJECTS)', text, re.DOTALL)
    if education_match:
        education_text = education_match.group(1).strip()
        education_entries = re.split(r'\n\s*\n', education_text)
        for entry in education_entries:
            if entry.strip():
                resume_data['education'].append(entry.strip())
    
    # Extract skills
    skills_match = re.search(r'SKILLS\s*(.*?)(?:PROJECTS|CERTIFICATES)', text, re.DOTALL)
    if skills_match:
        skills_text = skills_match.group(1).strip()
        skill_categories = re.findall(r'([^:]+):(.*?)(?=\n[^:]+:|$)', skills_text, re.DOTALL)
        
        for category, skills in skill_categories:
            category = category.strip()
            skills_list = [s.strip() for s in skills.strip().split(',')]
            resume_data['skills'][category] = skills_list
    
    # Extract projects
    projects_match = re.search(r'PROJECTS\s*(.*?)(?:CERTIFICATES|EXTRA)', text, re.DOTALL)
    if projects_match:
        projects_text = projects_match.group(1).strip()
        project_entries = re.findall(r'➢\s*(.*?)(?=➢|\Z)', projects_text, re.DOTALL)
        
        for entry in project_entries:
            if entry.strip():
                resume_data['projects'].append(entry.strip())
    
    # Extract certificates
    certs_match = re.search(r'CERTIFICATES\s*(.*?)(?:EXTRA|HOBBIES)', text, re.DOTALL)
    if certs_match:
        certs_text = certs_match.group(1).strip()
        cert_entries = re.findall(r'➢\s*(.*?)(?=➢|\Z)', certs_text, re.DOTALL)
        
        for entry in cert_entries:
            if entry.strip():
                resume_data['certificates'].append(entry.strip())
    
    # Extract extra activities
    activities_match = re.search(r'EXTRA CURRICULUM ACTIVITIES\s*(.*?)(?:HOBBIES|\Z)', text, re.DOTALL)
    if activities_match:
        activities_text = activities_match.group(1).strip()
        activity_entries = re.findall(r'➢\s*(.*?)(?=➢|\Z)', activities_text, re.DOTALL)
        
        for entry in activity_entries:
            if entry.strip():
                resume_data['activities'].append(entry.strip())
    
    # Extract hobbies
    hobbies_match = re.search(r'HOBBIES\s*(.*?)(?:\Z)', text, re.DOTALL)
    if hobbies_match:
        hobbies_text = hobbies_match.group(1).strip()
        resume_data['hobbies'] = [h.strip() for h in hobbies_text.split(',')]
    
    return resume_data
