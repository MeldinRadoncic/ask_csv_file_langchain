import os


import replicate
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from elevenlabs import generate
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import create_csv_agent


from langchain.llms import OpenAI
import openai

load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")



def generate_response(files, prompt):
    for file in files:
        agent = create_csv_agent(OpenAI(temperature=0.5), file.name , verbose=True)
        response = agent(prompt)
        
        
    return response['output']



def save_csv(files):
    for file in files:
        with open(file.name, 'wb') as csv_file:
            csv_file.write(file.read())
            st.success(f"Saved file {file.name}")    

def get_text():
    input_text = st.text_input("Ask me", key="input")
    return input_text

# Store and track user input and generated text in session state
if 'past' not in st.session_state:
    st.session_state['past'] = [] # User input text

# Store and track AI generated text in session state
if 'generated' not in st.session_state:
    st.session_state['generated'] = [] # AI generated text


def main():
    st.title("Ask your CSV File")


    with st.form(key='my_form'):
        csv_files = st.file_uploader("Upload your csv file...", type=["csv"], accept_multiple_files=True)
        

        user_input = get_text() if csv_files else None ## user input text
        submit_button = st.form_submit_button(label='Submit') 

        if submit_button:
            if csv_files and user_input:
                response = generate_response(csv_files,user_input)
                st.session_state.past.append(user_input)
                st.session_state.generated.append(response)
                
                
            elif csv_files:
                save_csv(csv_files)


    # Display all generated text and user input
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True)
            message(st.session_state['generated'][i])
            
    

if __name__ == "__main__":
    main()

