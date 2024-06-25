import streamlit as st
import openai
import os
import pandas as pd

# Set your API key from the environment variable
os.environ["OPENAI_API_KEY"] = "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"

# Load the Excel file and convert it to text
def excel_to_text(file_path):
    df = pd.read_excel(file_path)
    # Convert the dataframe to a text string
    text_data = df.to_string(index=False)
    return text_data

# Initialize the OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")


# Function to initialize the conversation with the document text
def initialize_conversation(document_text):
    return [
        {"role": "system", "content": "You are a helpful assistant. Answer the following question based on the document text provided.Please provide proper details with Units"},
        {"role": "assistant", "content": document_text}


    ]

# Function to ask a question to GPT-4
def ask_gpt4(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",  # Use the correct GPT-4 model identifier
            messages=messages,
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        return f"An error occurred: {e}"

# Function to process each uploaded file
def process_files(uploaded_files):
    for uploaded_file in uploaded_files:
        # Convert the Excel file to text
        document_text = excel_to_text(uploaded_file)

        # Initialize conversation with document text
        conversation = initialize_conversation(document_text)

        # User input
        question = st.text_input(f"Ask your question for {uploaded_file.name}:")

        # Get the answer from GPT-4
        if st.button(f"Get Answer for {uploaded_file.name}"):
            # Add user's question to the conversation
            conversation.append({"role": "user", "content": question})

            # Get the answer from GPT-4 based on the conversation
            answer = ask_gpt4(conversation)

            # Display the answer
            st.text("Answer:")
            st.write(answer)

# Streamlit UI
def main():
    st.title("Q&A App")

    # Allow user to upload multiple Excel files
    uploaded_files = st.file_uploader("Upload Excel files", type=["xlsx"], accept_multiple_files=True)

    # Check if files have been uploaded
    if uploaded_files:
        process_files(uploaded_files)
        print("kaka")

if __name__ == "__main__":
    main()
    print("xxxxx")
    print("cccc")
