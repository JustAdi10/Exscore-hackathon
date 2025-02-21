import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""IDENTITY and PURPOSE

                          You are an expert content summarizer. You take content in and output a Markdown formatted
                          summary using the format below.

                          Take a deep breath and think step by step about how to best accomplish this goal using the
                          following steps.

                          OUTPUT SECTIONS

                          - Combine all of your understanding of the content into a single, 20-word sentence in a
                          section called ONE SENTENCE SUMMARY:.

                          - Output the 10 most important points of the content as a list with no more than 15 words per
                          point into a section called MAIN POINTS:.

                          - Output a list of the 5 best takeaways from the content in a section called TAKEAWAYS:.

                          OUTPUT INSTRUCTIONS

                          - Create the output using the formatting above.
                          - You only output human readable Markdown.
                          - Output numbered lists, not bullets.
                          - Do not output warnings or notes—just the requested sections.
                          - Do not repeat items in the output sections.
                          - Do not start items with the same opening words.

                          INPUT: """


#getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)