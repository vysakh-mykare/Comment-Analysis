import streamlit as st
import openai
import pandas as pd
# from openai.api_resources import Engine
import os
from io import BytesIO

openai.api_key =  st.secrets.openai_key


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

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data
# Streamlit app
st.title('Sentiment Analysis with OpenAI')

# Single comment analysis
st.subheader("Single Comment Analysis")
user_input = st.text_area("Enter comment to analyze", "")

if st.button('Analyze'):
    if user_input:
        with st.spinner('Analyzing...'):
            sentiment = classify_comment(user_input)
            st.write(f"Sentiment: {sentiment}")
    else:
        st.write("Please enter some text to analyze.")

# Bulk analysis from file upload
st.subheader("Bulk Comment Analysis")
uploaded_file = st.file_uploader("Choose a file (CSV or Excel)", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # Check the file format and read file
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        # Assuming the column with comments is named 'Comments'
        if 'Comments' in df.columns:
            with st.spinner('Classifying comments in bulk...'):
                df['Sentiment'] = df['Comments'].apply(classify_comment)
            st.success('Classification completed!')
            
            st.write(df)
            
            # Download button
            result = to_excel(df)
            st.download_button(label="📥 Download Result as Excel",
                               data=result,
                               file_name="classified_comments.xlsx",
                               mime="application/vnd.ms-excel")
        else:
            st.error("Please make sure your file contains a 'Comments' column.")
    except Exception as e:
        st.error(f"Error processing file: {e}")
