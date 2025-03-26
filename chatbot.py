import os
import requests
import json
import time

def get_llm_response(prompt, model="llama3-8b-8192"):
    """
    Get a response from an LLM API (Groq in this case)
    
    Args:
        prompt: The prompt to send to the API
        model: The model to use
        
    Returns:
        str: The response from the API
    """
    # Get API key from environment variables
    api_key = os.getenv("GROQ_API_KEY")
    
    # For demo purposes, if no API key is available, return a simple response
    if not api_key:
        print("No API key found. Using fallback responses.")
        time.sleep(1)  # Simulate API call delay
        return generate_fallback_response(prompt)
    
    # API endpoint
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # Headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Enhanced system prompt with more details from the resume
    system_prompt = """
    You are Arti's AI assistant that answers questions about her resume and professional profile.
    
    Key facts about Arti:
    - She's a Business Analyst & Data Professional
    - Currently pursuing Bachelor of Technology at MNIT Jaipur (Expected June 2026)
    - Skilled in Python, SQL, Data Analysis, PowerBI, and Excel
    - Has worked on several data analytics projects including Diwali Sales Analysis and Credit Card Financial Dashboard
    - Has certifications in data analytics from Microsoft and LinkedIn
    
    Be friendly, professional, and concise in your answers. Focus on showcasing Arti's skills and experience.
    If asked about contact information, mention email, phone, LinkedIn, or GitHub without giving specific details.
    If you're not sure about something, acknowledge it and provide the most relevant information you have.
    """
    
    # Data
    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,  # Lower temperature for more factual responses
        "max_tokens": 800,   # Increased for more detailed responses
        "top_p": 0.95
    }
    
    try:
        # Make API call with timeout
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=15)
        
        # Log the response status for debugging
        if response.status_code != 200:
            print(f"API responded with status code: {response.status_code}")
            print(f"Response content: {response.text[:200]}...")
            return generate_fallback_response(prompt)
        
        # Parse response
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    except requests.exceptions.Timeout:
        print("API request timed out. Using fallback response.")
        return generate_fallback_response(prompt)
    
    except requests.exceptions.RequestException as e:
        print(f"API connection error: {e}")
        return generate_fallback_response(prompt)
    
    except Exception as e:
        print(f"Error calling LLM API: {e}")
        return generate_fallback_response(prompt)

def generate_fallback_response(prompt):
    """
    Generate a fallback response based on the resume data when API is not available
    
    Args:
        prompt: The user's question
        
    Returns:
        str: A response based on the prompt
    """
    prompt_lower = prompt.lower()
    
    if "education" in prompt_lower or "study" in prompt_lower or "university" in prompt_lower or "college" in prompt_lower:
        return "Arti is pursuing a Bachelor of Technology at Malaviya National Institute of Technology Jaipur (MNIT Jaipur), expected to graduate in June 2026. She's currently in her 3rd year, studying Metallurgical and Materials Engineering. She completed high school with CBSE board and scored 94% in 12th grade."
    
    elif "skill" in prompt_lower or "expertise" in prompt_lower or "proficient" in prompt_lower:
        return "Arti's key skills include:\n\n- Programming: Python, SQL\n- Data Manipulation & Analysis: NumPy, Pandas\n- Data Visualization: Matplotlib, Tableau, PowerBI\n- Machine Learning: scikit-learn\n- Statistical Analysis: Hypothesis testing, Regression analysis\n- Spreadsheet tools: Microsoft Excel, Google sheets\n- Version Control: Git, GitHub"
    
    elif "project" in prompt_lower or "work" in prompt_lower or "experience" in prompt_lower:
        return "Arti has worked on several data analysis projects including:\n\n1. Diwali Sales Analysis - Using Python for EDA to improve inventory planning\n2. Coffee Shop Sales Analysis - Identifying business challenges and solutions\n3. Credit Card Financial Dashboard - Using Power BI to analyze transaction data\n4. Rapido Ride Analysis - Analyzing user behavior patterns and peak hours"
    
    elif "certificate" in prompt_lower or "certification" in prompt_lower:
        return "Arti has earned several certificates including:\n\n1. Certificate of completion of data analytics and Visualization job Simulation at Forage\n2. Certificate of completion of the Career Essentials in Data Analysis learning path by Microsoft and LinkedIn\n3. Certificate of Executive in Alumni Committee"
    
    elif "hobby" in prompt_lower or "interest" in prompt_lower or "activities" in prompt_lower:
        return "Arti enjoys playing chess and learning new languages. She's currently learning Spanish! Additionally, she's involved in extracurricular activities as a Team coordinator & Executive in the Database team of ALCOM in MNIT and is a Member of the Entrepreneurship club of MNIT."
    
    elif "contact" in prompt_lower or "reach" in prompt_lower or "email" in prompt_lower or "phone" in prompt_lower:
        return "You can contact Arti at +91 8287963396 or via email. She's also available on LinkedIn and GitHub."
    
    elif "summary" in prompt_lower or "about" in prompt_lower or "introduction" in prompt_lower or "who" in prompt_lower:
        return "Arti is an aspiring Business Analyst with hands-on experience in data analysis, Power BI, and Python. She's skilled in Excel, SQL, and machine learning concepts to derive actionable insights. She's passionate about leveraging data-driven strategies to improve business performance and has a strong understanding of key business metrics like CAC, CLV, and ROI."
    
    else:
        return "I'm here to answer questions about Arti's resume! You can ask about her education, skills, projects, certificates, hobbies, or contact information. What would you like to know?"

def get_chatbot_response(prompt, resume_data):
    """
    Get a response from the chatbot based on the resume data
    
    Args:
        prompt: The user's question
        resume_data: The parsed resume data
        
    Returns:
        str: The chatbot's response
    """
    # Try to get a response from the LLM API
    return get_llm_response(prompt)
