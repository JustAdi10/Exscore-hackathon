# ClipCraft

## Project Description
ClipCraft is a project that takes YouTube video links and summarizes them in the form of text. Whether you're a student, content creator, marketer, or educator, ClipCraft provides an intuitive interface and robust features to help you generate concise summaries of video content for your needs.

## Pre-Requisites
- Python
- Streamlit
- Google Gemini AI (Generative AI API by Google)
- YouTube Transcript API
- dotenv (python-dotenv)
- Google API Key
- YouTube Thumbnail API

## Set-up
```sh
# Clone the repository
git clone https://github.com/JustAdi10/Exscore-hackathon.git

# Navigate to the project directory
cd AI

# Activate the virtual environment
conda activate <path_of_the_virtual_environment>

# Install dependencies
pip install streamlit google-generativeai youtube-transcript-api python-dotenv

# Get a Google API Key and set up environment variables
export GOOGLE_API_KEY=your_google_api_key_here

# Run the Streamlit App
streamlit run your_script.py
```

## Note
Due to the limits of the free API key of Google, we cannot process longer videos.

