# Arti's Portfolio Website

A professional portfolio website built with Flask, featuring a resume showcase and AI-powered chatbot integration.

## Features

- **Modern UI**: Dark theme with elegant animations and responsive design
- **Interactive Sections**:
  - Home page with professional introduction
  - Skills visualization with animated bars and proficiency indicators
  - Project showcase with detailed descriptions
  - Resume view with PDF preview and download option
  - Contact form for professional inquiries
- **AI Chatbot**: Powered by Groq API to answer questions about the resume
- **Achievement Badges**: Visual showcase of certifications and accomplishments

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **AI Integration**: Groq API (Llama3 model)
- **PDF Processing**: PyPDF2

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd portfolio-website
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r dependencies.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your Groq API key (required for chatbot functionality):
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```
   - You can get a Groq API key by signing up at https://console.groq.com/

### Running the Website

1. Start the Flask server:
   ```
   python flask_app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Project Structure

- `flask_app.py`: Main Flask application file
- `chatbot.py`: AI chatbot implementation using Groq API
- `resume_parser.py`: Tools for extracting data from resume PDF
- `/templates`: HTML templates for all pages
- `/static`: CSS, JavaScript, and image assets and pdf


## Chatbot API

The chatbot API endpoint is accessible at:
```
POST /ask
```

Request format:
```json
{
  "query": "Your question about the resume"
}
```

Response format:
```json
{
  "response": "AI-generated answer about the resume"
}
```

## Local Development

For local development, make sure to:
1. Set the GROQ_API_KEY in your .env file
2. Replace the resume file path in flask_app.py if needed
3. Update personal information in the templates as required

## License

This project is open source and available under the [MIT License](LICENSE).