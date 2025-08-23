# Multi-Agent Blog Content Writer

## Overview

This project is a Streamlit web application that automates the blog post creation process using a multi-agent system powered by Google's Gemini Pro model. The application orchestrates a team of specialized AI agents that collaborate through a sequential workflow to draft, review, and finalize a blog post based on a user-provided topic.

This system is designed to simulate a real-world content creation pipeline, ensuring that the final output is well-written, reviewed from multiple perspectives, and ready for publication.

---

## Features

- **Multi-Agent Workflow**: Utilizes a team of specialized AI agents, each with a distinct role:
    - **Draft Writer**: Creates the initial blog post.
    - **SEO Reviewer**: Provides feedback to optimize for search engines.
    - **Legal Reviewer**: Checks for potential legal compliance issues.
    - **Ethics Reviewer**: Assesses the content for ethical considerations.
    - **Plagiarism Checker**: Simulates an originality check.
    - **Final Editor**: Polishes the revised draft into a final, publishable article.
- **Interactive Web UI**: Built with Streamlit to provide a simple and intuitive interface for users to input topics and view results.
- **Conversation Logging**: An optional feature to display the entire backend conversation between the AI agents, providing transparency into the workflow.
- **Powered by Google Gemini**: Leverages the `gemini-1.5-flash` model for fast and high-quality content generation and review.

---

## Technology Stack

- **Backend**: Python
- **AI Model**: Google Gemini Pro (`gemini-1.5-flash`)
- **Web Framework**: Streamlit
- **API Library**: `google-generativeai`
- **Environment Management**: `python-dotenv`

---

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/kathiravanthilagar31/Blog-Writer.git
cd Blog-Writer
```

### 2. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**For macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

You need a Google Generative AI API key to run this application.

- Get your free API key from Google AI Studio https://aistudio.google.com/app/apikey.
- Create a file named `.env` in the root directory of the project.
- Add your API key to the `.env` file as shown below:

```
GOOGLE_API_KEY="your_google_api_key_here"
```

---

## Usage

Once the setup is complete, you can run the Streamlit application with a single command:

```bash
streamlit run app.py
```

This will start a local web server and open the application in your default web browser.

1.  Enter a topic for the blog post.
2.  Set the desired word limit.
3.  Check the "Show agent conversation log" box if you want to see the backend communication.
4.  Click the "Generate Blog Post" button to start the workflow.

---

## Project Structure

The project is organized into the following files and directories:

```
.
├── .env                  # Stores the API key (not committed to version control)
├── app.py                # The main Streamlit application file
├── requirements.txt      # Lists all project dependencies
├── setup.py              # Project setup script
├── src/
│   ├── __init__.py       # Marks 'src' as a Python package
│   └── helper.py         # Contains the core logic for the multi-agent workflow
└── README.md             # This file
