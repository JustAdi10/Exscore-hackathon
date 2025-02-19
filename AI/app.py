import streamlit as st
from deoenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt='''You are a youtube summariser. You will be given a transcript of a video and you have to summarise it in 3-4 lines. Make sure they're in the form of typed notes and are well laid out and easy to understand. The transcript is as follows: '''

def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
