import os
import base64
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
import PyPDF2
import io
import re
from werkzeug.utils import secure_filename
from resume_parser import extract_resume_data
from chatbot import get_llm_response, generate_fallback_response

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
Bootstrap(app)

# Global variables
RESUME_PATH = 'static/2022UMT1771.pdf'
resume_data = None

# Load resume data on startup
def load_resume_data():
    global resume_data
    resume_data = extract_resume_data(RESUME_PATH)
    
    # Convert raw resume data to a more structured format for the templates
    structured_data = {
        'name': resume_data.get('name', 'Arti'),
        'contact': resume_data.get('contact', '+91 8287963396'),
        'email': resume_data.get('email', 'hello@example.com'),
        'linkedin': resume_data.get('linkedin', 'LinkedIn'),
        'github': resume_data.get('github', 'GitHub'),
        'summary': resume_data.get('summary', 'Aspiring Business Analyst with hands-on experience in data analysis.'),
        'education': [],
        'skills': [],
        'experience': [],
        'projects': []
    }
    
    # Format education data
    education = resume_data.get('education', [])
    structured_data['education'] = [
        {
            'degree': 'Bachelor of Technology',
            'institution': 'MNIT Jaipur',
            'timeline': '2022-2026',
            'details': 'Metallurgical and Materials Engineering'
        },
        {
            'degree': 'Senior Secondary Education',
            'institution': 'CBSE Board',
            'timeline': '2020-2021',    
            'details': ' 94% marks'
        }
    ]
    
    # Format skills data
    skills = resume_data.get('skills', {})
    all_skills = []
    for category, skill_list in skills.items():
        all_skills.extend(skill_list)
    structured_data['skills'] = all_skills
    
    # Create a dictionary for skill categories (used in skills page)
    skill_categories = {
        'Programming': ['Python', 'SQL', 'R (Basic)'],
        'Data Manipulation & Analysis': ['NumPy', 'Pandas', 'Statistical Analysis'],
        'Data Visualization': ['Matplotlib', 'Seaborn', 'Power BI', 'Tableau'],
        'Machine Learning': ['Scikit-learn', 'Regression', 'Classification'],
        'Business Tools': ['Microsoft Excel', 'Google Sheets', 'Jupyter Notebook'],
        'Version Control': ['Git', 'GitHub']
    }
    
    # Format project data
    projects = resume_data.get('projects', [])
    structured_data['projects'] = [
        {
            'name': 'Diwali Sales Analysis',
            'description': 'Performed data cleaning and EDA using Python to improve inventory planning.',
            'technologies': ['Python', 'Pandas', 'Matplotlib', 'Seaborn']
        },
        {
            'name': 'Credit Card Financial Dashboard',
            'description': 'Created interactive Power BI dashboard to analyze transaction patterns.',
            'technologies': ['Power BI', 'DAX', 'Data Modeling']
        }
    ]
    
    # Format experience data
    structured_data['experience'] = [
        {
            'title': 'Database Team Executive',
            'company': 'ALCOM, MNIT Jaipur',
            'timeline': 'Aug 2022 - Present',
            'responsibilities': [
                'Managed alumni database and performed data cleaning operations',
                'Developed automated reports for tracking alumni engagement',
                'Collaborated with team members to organize alumni events'
            ]
        }
    ]
    
    return structured_data

# Convert PDF to base64 for embedding in HTML
def get_pdf_base64(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_data = file.read()
            return base64.b64encode(pdf_data).decode('utf-8')
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""
        
# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/skills')
def skills():
    # Create a dictionary for skill categories
    skill_categories = {
        'Programming': ['Python', 'SQL'],
        'Data Manipulation & Analysis': ['NumPy', 'Pandas', 'Statistical Analysis'],
        'Data Visualization': ['Matplotlib', 'Seaborn', 'Power BI', 'Tableau'],
        'Machine Learning': ['Scikit-learn', 'Regression', 'Classification'],
        'Business Tools': ['Microsoft Excel', 'Google Sheets', 'Jupyter Notebook'],
        'Version Control': ['Git', 'GitHub']
    }
    
    # Create skill proficiency data for visualizations
    skill_proficiency = {
        'Programming': [
            {'name': 'Python', 'level': 85},
            {'name': 'SQL', 'level': 80}
        ],
        'Data Analysis': [
            {'name': 'Excel', 'level': 95},
            {'name': 'Power BI', 'level': 95},
            {'name': 'Pandas', 'level': 80},
            {'name': 'NumPy', 'level': 75},
            {'name': 'Statistical Analysis', 'level': 80}
        ],
        'Visualization': [
            {'name': 'Matplotlib', 'level': 85},
            {'name': 'Seaborn', 'level': 80},
            {'name': 'Tableau', 'level': 90}
        ],
        'Soft Skills': [
            {'name': 'Problem Solving', 'level': 90},
            {'name': 'Communication', 'level': 85},
            {'name': 'Team Collaboration', 'level': 85},
            {'name': 'Time Management', 'level': 80},
            {'name': 'Adaptability', 'level': 90}
        ]
    }
    
    # Create education data
    education = [
        {
            'degree': 'Bachelor of Technology',
            'institution': 'MNIT Jaipur',
            'timeline': '2022-2026',
            'details': 'Metallurgical and Materials Engineering'
        },
        {
            'degree': 'Senior Secondary Education',
            'institution': 'CBSE Board',
            'timeline': '2020-2021',
            'details': '94% marks'
        }
    ]
    
    # Add certificates and achievements
    certificates = [
        {
            'name': 'Data Analytics and Visualization with Python',
            'issuer': 'Accenture',
            'date': 'August 2024',
            'badge_icon': 'fa-chart-bar'
        },
        {
            'name': ' Career Essentials in Data Analysis',
            'issuer': 'Microsoft',
            'date': 'January 2025',
            'badge_icon': 'fa-brain'
        },
        {
            'name': 'Executive Leadership ',
            'issuer': 'ALCOM, MNIT Jaipur',
            'date': 'December 2023', 
            'badge_icon': 'fa-database'
        }
    ]
    
    return render_template('skills.html', 
                           skill_categories=skill_categories, 
                           education=education, 
                           skill_proficiency=skill_proficiency,
                           certificates=certificates)

@app.route('/resume')
def resume():
    # Get PDF as base64 for embedding and downloading
    pdf_base64 = get_pdf_base64(RESUME_PATH)
    
    # For displaying PDF preview as an image in the resume page
    # In a real implementation, you'd convert the first page to an image
    # Here we'll use the same base64 data
    pdf_image = pdf_base64
    
    # Simplified approach: if we don't have global resume_data yet, load it
    global resume_data
    if resume_data is None:
        resume_data = load_resume_data()
    
    return render_template('resume.html', pdf_base64=pdf_base64, pdf_image=pdf_image, resume_data=resume_data)

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact', methods=['GET'])
def contact():
    message = request.args.get('message')
    return render_template('contact.html', message=message)

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # In a real application, you would save this to a database
        # and/or send an email notification
        
        # For now, just redirect with a success message
        return redirect(url_for('contact', message="Thank you for your message! I'll get back to you soon."))

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    if request.method == 'POST':
        try:
            # Get question from JSON data
            data = request.get_json()
            query = data.get('query', '')
            
            if not query:
                return jsonify({'response': 'Please ask a question!'})
            
            # Get response from chatbot
            global resume_data
            if resume_data is None:
                resume_data = load_resume_data()
                
            # In a real app, we would pass resume_data to get more personalized responses
            response = get_llm_response(query)
            
            return jsonify({'response': response})
            
        except Exception as e:
            print(f"Error processing question: {e}")
            return jsonify({'response': 'Sorry, I encountered an error. Please try again.'})

if __name__ == '__main__':
    # Load resume data on startup
    resume_data = load_resume_data()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)