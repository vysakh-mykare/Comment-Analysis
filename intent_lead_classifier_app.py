import streamlit as st
import openai
# from openai.api_resources import Engine
import os

openai.api_key = "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"


def classify_comment(comment):
    completion = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Classify the following lead comment as 'intent lead' or 'not intent lead':\n\n'{comment}'",
        temperature=0.7,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    # Corrected the way to access the sentiment analysis result
    sentiment = completion.choices[0].text.strip()
    return sentiment

# Streamlit app
st.title('Welcome to Intent Detective: Lead Classification Tool')

user_input = st.text_area("Enter comment to analyze", "")

if st.button('Analyze'):
    if user_input:
        with st.spinner('Analyzing...'):
            sentiment = classify_comment(user_input)
            st.write(f"Classification: {sentiment}")
    else:
        st.write("Please enter some text to analyze.")
