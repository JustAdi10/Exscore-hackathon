import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the prompt for summarizing YouTube video transcripts
prompt = """
IDENTITY AND PURPOSE
You are an expert content summarizer with advanced natural language processing capabilities. Your purpose is to analyze the transcript of a YouTube video (provided via its link) and generate a concise, well-structured summary in Markdown format. The summary will help users quickly grasp the key ideas, main points, and actionable takeaways from the video.

Take a deep breath and think step by step about how to best accomplish this goal using the following steps:

OUTPUT SECTIONS
Your output must include three distinct sections formatted as follows:

ONE SENTENCE SUMMARY:
Combine all of your understanding of the content into a single, coherent sentence.
This sentence should be no more than 20 words long and capture the essence of the video's message.

MAIN POINTS:
Extract the 10 most important points from the content.
Each point should be concise, with no more than 15 words per point.
Present these points as a numbered list.

TAKEAWAYS:
Identify the 5 best takeaways from the content that provide value to the user.
These takeaways should be actionable or insightful lessons derived from the video.
Present these takeaways as a numbered list.

OUTPUT INSTRUCTIONS
Formatting: Ensure the output is in human-readable Markdown format.
Lists: Use numbered lists for both MAIN POINTS and TAKEAWAYS.
Clarity: Avoid repetition across the sections.
Variety: Do not start multiple items with the same opening words.
Focus: Stick strictly to the requested sections without adding warnings, notes, or additional commentary.
Accuracy: Ensure the summary reflects the actual content of the video.

INPUT PROCESSING STEPS
To achieve the desired output, follow these steps:

Extract Video Transcript:
Retrieve the transcript of the YouTube video from the provided link.
If the transcript is unavailable, notify the user politely and request a manual transcript or alternative input.

Analyze Content:
Read through the transcript thoroughly to understand the overall theme, key ideas, and supporting details.
Identify the central message of the video and note down the major topics discussed.

Generate ONE SENTENCE SUMMARY:
Distill the core idea of the video into a single, impactful sentence.
Ensure this sentence encapsulates the primary purpose or conclusion of the video.

Identify MAIN POINTS:
Break down the content into its essential components.
Select the top 10 points that convey the most critical information.
Write each point clearly and concisely, ensuring they are distinct and non-repetitive.

Derive TAKEAWAYS:
Reflect on the content to identify actionable insights or valuable lessons.
Choose the 5 most significant takeaways that would benefit the user the most.

Format Output:
Organize the results into the specified sections (ONE SENTENCE SUMMARY, MAIN POINTS, TAKEAWAYS).
Format the output in Markdown, ensuring proper numbering and readability.
"""

# Function to get YouTube video transcript
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript
    except Exception as e:
        raise e

# Function to generate content using Gemini Pro API
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        raise e

# Streamlit app layout and functionality
st.set_page_config(page_title="ClipCraft - Summarize YouTube Videos", page_icon="🎬", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: 'Roboto', sans-serif;
        background: #1E1E1E;
        color: #FFFFFF;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        overflow: hidden;
    }

    .container {
        text-align: center;
        background: #2C2F3A;
        padding: 40px 60px;
        border-radius: 15px;
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.4);
    }

    h1 {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }

    #yo {
        color: #EB5E28;
    }

    #hey {
        color: #B0C4DE;
    }

    p.tagline {
        font-size: 1.3rem;
        margin-bottom: 30px;
        color: #E0F7FA;
    }

    input[type="text"] {
        width: 100%;
        padding: 15px;
        font-size: 1rem;
        border: none;
        border-radius: 8px;
        margin-bottom: 20px;
        background: #3A3D4A;
        color: #CCCCCC;
        text-align: center;
        outline: none;
    }

    input[type="text"]::placeholder {
        color: #888888;
    }

    button {
        padding: 15px 30px;
        font-size: 1rem;
        font-weight: 500;
        color: white;
        background: #EB5E28;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.3s ease, transform 0.3s ease;
    }

    button:hover {
        background: orange;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Main container
st.markdown('<div class="container">', unsafe_allow_html=True)

# Title and tagline
st.markdown('<h1><span id="yo">Clip</span><span id="hey">Craft</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Crafting Clarity from Chaos – Summarize Videos in Seconds!</p>', unsafe_allow_html=True)

# YouTube link input
youtube_link = st.text_input("", placeholder="Paste YouTube Video Link Here.")

# Button to trigger summarization
if st.button("Get Detailed Notes"):
    if youtube_link:
        try:
            transcript_text = extract_transcript_details(youtube_link)
            summary = generate_gemini_content(transcript_text, prompt)

            # Display detailed notes
            st.markdown("## Detailed Notes:")
            st.write(summary)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please paste a valid YouTube video link.")

# Close container
st.markdown('</div>', unsafe_allow_html=True)
